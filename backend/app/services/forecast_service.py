from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import DataUnavailableError, ExternalServiceError
from app.data.collectors.open_meteo import OpenMeteoClient
from app.models.forecast import Forecast
from app.models.location import Location


class ForecastService:
    SOURCE = "Open-Meteo"

    def __init__(self):
        self.client = OpenMeteoClient()

    # =========================================================
    # SAFE VALUE HELPER
    # =========================================================

    @staticmethod
    def _value(values: list, index: int):
        if index < len(values):
            return values[index]

        return None

    # =========================================================
    # CACHED FORECASTS
    # =========================================================

    def _cached_forecasts(
        self,
        location: Location,
        db: Session,
    ) -> list[Forecast]:
        now = datetime.utcnow()

        cutoff = now - timedelta(
            hours=settings.fallback_max_age_hours
        )

        return (
            db.query(Forecast)
            .filter(
                Forecast.location_id == location.id,
                Forecast.source == self.SOURCE,
                Forecast.generated_at >= cutoff,
            )
            .order_by(
                Forecast.forecast_time.asc()
            )
            .all()
        )

    # =========================================================
    # GET HOURLY FORECAST
    # =========================================================

    def get_hourly_forecast(
        self,
        location: Location,
        db: Session,
    ) -> list[Forecast]:

        try:
            # -------------------------------------------------
            # 1. FETCH FRESH FORECAST FROM OPEN-METEO
            # -------------------------------------------------

            data = self.client.get_hourly_forecast(
                latitude=location.latitude,
                longitude=location.longitude,
            )

            hourly = data.get("hourly") or {}

            times = hourly.get("time") or []

            if not times:
                raise ExternalServiceError(
                    "Open-Meteo returned no hourly forecast."
                )

            generated_at = datetime.utcnow()

            # -------------------------------------------------
            # 2. PREPARE DATABASE ROWS
            # -------------------------------------------------

            rows = []

            for index, time_value in enumerate(times):

                forecast_time = datetime.fromisoformat(
                    time_value
                )

                weather_code = self._value(
                    hourly.get("weather_code", []),
                    index,
                )

                rows.append(
                    {
                        "location_id": location.id,
                        "source": self.SOURCE,
                        "forecast_time": forecast_time,
                        "generated_at": generated_at,

                        "temperature": self._value(
                            hourly.get("temperature_2m", []),
                            index,
                        ),

                        "feels_like": self._value(
                            hourly.get("apparent_temperature", []),
                            index,
                        ),

                        "humidity": self._value(
                            hourly.get("relative_humidity_2m", []),
                            index,
                        ),

                        "pressure": self._value(
                            hourly.get("pressure_msl", []),
                            index,
                        ),

                        "wind_speed": self._value(
                            hourly.get("wind_speed_10m", []),
                            index,
                        ),

                        "wind_direction": self._value(
                            hourly.get("wind_direction_10m", []),
                            index,
                        ),

                        "rainfall": self._value(
                            hourly.get("precipitation", []),
                            index,
                        ),

                        "precipitation_probability": self._value(
                            hourly.get(
                                "precipitation_probability",
                                [],
                            ),
                            index,
                        ),

                        "visibility": self._value(
                            hourly.get("visibility", []),
                            index,
                        ),

                        "cloud_cover": self._value(
                            hourly.get("cloud_cover", []),
                            index,
                        ),

                        "weather_condition": (
                            str(weather_code)
                            if weather_code is not None
                            else None
                        ),
                    }
                )

            if not rows:
                raise ExternalServiceError(
                    "No hourly forecast data was prepared."
                )

            # -------------------------------------------------
            # 3. POSTGRESQL UPSERT
            # -------------------------------------------------
            #
            # IMPORTANT:
            #
            # We DO NOT use:
            #
            # constraint="uq_forecast_location_time_source"
            #
            # because your Forecast model defines this as a
            # UNIQUE INDEX rather than a named constraint.
            #
            # Instead we specify the conflict columns directly.
            # -------------------------------------------------

            stmt = insert(Forecast).values(rows)

            stmt = stmt.on_conflict_do_update(
                index_elements=[
                    Forecast.location_id,
                    Forecast.forecast_time,
                    Forecast.source,
                ],
                set_={
                    "generated_at": stmt.excluded.generated_at,

                    "temperature": (
                        stmt.excluded.temperature
                    ),

                    "feels_like": (
                        stmt.excluded.feels_like
                    ),

                    "humidity": (
                        stmt.excluded.humidity
                    ),

                    "pressure": (
                        stmt.excluded.pressure
                    ),

                    "wind_speed": (
                        stmt.excluded.wind_speed
                    ),

                    "wind_direction": (
                        stmt.excluded.wind_direction
                    ),

                    "rainfall": (
                        stmt.excluded.rainfall
                    ),

                    "precipitation_probability": (
                        stmt.excluded.precipitation_probability
                    ),

                    "visibility": (
                        stmt.excluded.visibility
                    ),

                    "cloud_cover": (
                        stmt.excluded.cloud_cover
                    ),

                    "weather_condition": (
                        stmt.excluded.weather_condition
                    ),
                },
            )

            # -------------------------------------------------
            # 4. EXECUTE UPSERT
            # -------------------------------------------------

            db.execute(stmt)

            db.commit()

            # -------------------------------------------------
            # 5. FETCH FINAL FORECASTS
            # -------------------------------------------------

            forecast_times = [
                row["forecast_time"]
                for row in rows
            ]

            forecasts = (
                db.query(Forecast)
                .filter(
                    Forecast.location_id == location.id,

                    Forecast.source == self.SOURCE,

                    Forecast.forecast_time.in_(
                        forecast_times
                    ),
                )
                .order_by(
                    Forecast.forecast_time.asc()
                )
                .all()
            )

            return forecasts

        # =====================================================
        # EXTERNAL WEATHER SERVICE ERRORS
        # =====================================================

        except (
            ExternalServiceError,
            OSError,
            TimeoutError,
        ):

            db.rollback()

            cached = self._cached_forecasts(
                location,
                db,
            )

            if cached:
                return cached

            raise DataUnavailableError(
                "Hourly forecast is temporarily unavailable "
                "and no cached forecast exists."
            )

        # =====================================================
        # DATABASE ERRORS
        # =====================================================

        except SQLAlchemyError as exc:

            db.rollback()

            print(
                f"DATABASE ERROR while storing hourly forecast "
                f"for '{location.name}': {exc}"
            )

            cached = self._cached_forecasts(
                location,
                db,
            )

            if cached:
                print(
                    f"Using cached forecast for "
                    f"'{location.name}'."
                )

                return cached

            raise DataUnavailableError(
                "Hourly forecast could not be stored or "
                "retrieved from the database, and no cached "
                "forecast exists."
            )