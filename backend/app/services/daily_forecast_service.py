from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import DataUnavailableError, ExternalServiceError
from app.data.collectors.open_meteo import OpenMeteoClient
from app.models.daily_forecast import DailyForecast
from app.models.location import Location


class DailyForecastService:
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
    ) -> list[DailyForecast]:
        cutoff = datetime.utcnow() - timedelta(
            hours=settings.fallback_max_age_hours
        )

        return (
            db.query(DailyForecast)
            .filter(
                DailyForecast.location_id == location.id,
                DailyForecast.source == self.SOURCE,
                DailyForecast.generated_at >= cutoff,
            )
            .order_by(DailyForecast.forecast_date.asc())
            .all()
        )

    def get_daily_forecast(
        self,
        location: Location,
        db: Session,
    ) -> list[DailyForecast]:
        try:
            data = self.client.get_daily_forecast(
                latitude=location.latitude,
                longitude=location.longitude,
            )
            daily = data.get("daily") or {}
            dates = daily.get("time") or []

            if not dates:
                raise ExternalServiceError(
                    "Open-Meteo returned no daily forecast."
                )

            generated_at = datetime.utcnow()
            forecasts: list[DailyForecast] = []

            for index, date_value in enumerate(dates):
                forecast_date = datetime.fromisoformat(date_value).date()

                forecast = (
                    db.query(DailyForecast)
                    .filter(
                        DailyForecast.location_id == location.id,
                        DailyForecast.forecast_date == forecast_date,
                        DailyForecast.source == self.SOURCE,
                    )
                    .first()
                )

                if forecast is None:
                    forecast = DailyForecast(
                        location_id=location.id,
                        source=self.SOURCE,
                        forecast_date=forecast_date,
                        generated_at=generated_at,
                    )
                    db.add(forecast)
                else:
                    forecast.generated_at = generated_at

                forecast.temperature_max = self._value(
                    daily.get("temperature_2m_max", []), index
                )
                forecast.temperature_min = self._value(
                    daily.get("temperature_2m_min", []), index
                )
                forecast.feels_like_max = self._value(
                    daily.get("apparent_temperature_max", []), index
                )
                forecast.feels_like_min = self._value(
                    daily.get("apparent_temperature_min", []), index
                )
                forecast.precipitation_sum = self._value(
                    daily.get("precipitation_sum", []), index
                )
                forecast.rain_sum = self._value(
                    daily.get("rain_sum", []), index
                )
                forecast.precipitation_probability_max = self._value(
                    daily.get("precipitation_probability_max", []), index
                )
                forecast.precipitation_hours = self._value(
                    daily.get("precipitation_hours", []), index
                )
                forecast.wind_speed_max = self._value(
                    daily.get("wind_speed_10m_max", []), index
                )
                forecast.wind_gusts_max = self._value(
                    daily.get("wind_gusts_10m_max", []), index
                )
                forecast.wind_direction_dominant = self._value(
                    daily.get("wind_direction_10m_dominant", []), index
                )

                sunrise = self._value(daily.get("sunrise", []), index)
                sunset = self._value(daily.get("sunset", []), index)
                forecast.sunrise = (
                    datetime.fromisoformat(sunrise) if sunrise else None
                )
                forecast.sunset = (
                    datetime.fromisoformat(sunset) if sunset else None
                )

                weather_code = self._value(
                    daily.get("weather_code", []), index
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
                "Daily forecast is temporarily unavailable and no cached "
                "forecast exists."
            )
