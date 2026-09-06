from __future__ import annotations

from datetime import datetime, timedelta

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

    @staticmethod
    def _value(values: list, index: int):
        return values[index] if index < len(values) else None

    def _cached_forecasts(
        self,
        location: Location,
        db: Session,
    ) -> list[Forecast]:
        now = datetime.utcnow()
        cutoff = now - timedelta(hours=settings.fallback_max_age_hours)

        return (
            db.query(Forecast)
            .filter(
                Forecast.location_id == location.id,
                Forecast.source == self.SOURCE,
                Forecast.generated_at >= cutoff,
            )
            .order_by(Forecast.forecast_time.asc())
            .all()
        )

    def get_hourly_forecast(
        self,
        location: Location,
        db: Session,
    ) -> list[Forecast]:
        try:
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
            forecasts: list[Forecast] = []

            for index, time_value in enumerate(times):
                forecast_time = datetime.fromisoformat(time_value)

                forecast = (
                    db.query(Forecast)
                    .filter(
                        Forecast.location_id == location.id,
                        Forecast.forecast_time == forecast_time,
                        Forecast.source == self.SOURCE,
                    )
                    .first()
                )

                if forecast is None:
                    forecast = Forecast(
                        location_id=location.id,
                        source=self.SOURCE,
                        forecast_time=forecast_time,
                        generated_at=generated_at,
                    )
                    db.add(forecast)
                else:
                    forecast.generated_at = generated_at

                forecast.temperature = self._value(
                    hourly.get("temperature_2m", []), index
                )
                forecast.feels_like = self._value(
                    hourly.get("apparent_temperature", []), index
                )
                forecast.humidity = self._value(
                    hourly.get("relative_humidity_2m", []), index
                )
                forecast.pressure = self._value(
                    hourly.get("pressure_msl", []), index
                )
                forecast.wind_speed = self._value(
                    hourly.get("wind_speed_10m", []), index
                )
                forecast.wind_direction = self._value(
                    hourly.get("wind_direction_10m", []), index
                )
                forecast.rainfall = self._value(
                    hourly.get("precipitation", []), index
                )
                forecast.precipitation_probability = self._value(
                    hourly.get("precipitation_probability", []), index
                )
                forecast.visibility = self._value(
                    hourly.get("visibility", []), index
                )
                forecast.cloud_cover = self._value(
                    hourly.get("cloud_cover", []), index
                )
                weather_code = self._value(
                    hourly.get("weather_code", []), index
                )
                forecast.weather_condition = (
                    str(weather_code) if weather_code is not None else None
                )

                forecasts.append(forecast)

            db.commit()
            for forecast in forecasts:
                db.refresh(forecast)

            return forecasts

        except (ExternalServiceError, OSError, TimeoutError):
            cached = self._cached_forecasts(location, db)
            if cached:
                return cached
            raise DataUnavailableError(
                "Hourly forecast is temporarily unavailable and no cached "
                "forecast exists."
            )
