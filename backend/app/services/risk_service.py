from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.risk.forecast_window import ForecastWindowEngine
from app.services.forecast_service import ForecastService
from app.services.location_service import LocationService


class RiskService:
    def __init__(self):
        self.location_service = LocationService()
        self.forecast_service = ForecastService()
        self.risk_engine = ForecastWindowEngine()

    @staticmethod
    def build_forecast_records_from_models(forecasts) -> list[dict]:
        records = []

        for forecast in forecasts:
            records.append(
                {
                    "forecast_time": forecast.forecast_time,
                    "temperature": forecast.temperature,
                    "feels_like": forecast.feels_like,
                    "humidity": forecast.humidity,
                    "pressure": forecast.pressure,
                    "wind_speed": forecast.wind_speed,
                    "wind_direction": forecast.wind_direction,
                    "rainfall": forecast.rainfall,
                    "precipitation_probability": (
                        forecast.precipitation_probability
                    ),
                    "visibility": forecast.visibility,
                    "cloud_cover": forecast.cloud_cover,
                    "weather_code": (
                        int(forecast.weather_condition)
                        if forecast.weather_condition is not None
                        and str(forecast.weather_condition).lstrip("-").isdigit()
                        else None
                    ),
                }
            )

        return records

    # Kept for backwards compatibility with existing tests/callers.
    @staticmethod
    def build_forecast_records(weather_data: dict) -> list[dict]:
        hourly = weather_data.get("hourly")
        if not hourly:
            raise ValueError("Hourly forecast data is unavailable.")

        times = hourly.get("time", [])
        records = []

        def value(name: str, index: int):
            values = hourly.get(name, [])
            return values[index] if index < len(values) else None

        for index, forecast_time in enumerate(times):
            weather_code = value("weather_code", index)
            records.append(
                {
                    "forecast_time": datetime.fromisoformat(forecast_time),
                    "temperature": value("temperature_2m", index),
                    "feels_like": value("apparent_temperature", index),
                    "humidity": value("relative_humidity_2m", index),
                    "pressure": value("pressure_msl", index),
                    "wind_speed": value("wind_speed_10m", index),
                    "wind_direction": value("wind_direction_10m", index),
                    "rainfall": value("precipitation", index),
                    "precipitation_probability": value(
                        "precipitation_probability", index
                    ),
                    "visibility": value("visibility", index),
                    "cloud_cover": value("cloud_cover", index),
                    "weather_code": weather_code,
                }
            )

        return records

    def calculate_city_risk(
        self,
        city: str,
        start_time: datetime,
        end_time: datetime,
        db: Session,
        activity: str | None = None,
        warning_color: str | None = None,
    ) -> dict:
        if end_time < start_time:
            raise ValueError(
                "end_time must be greater than or equal to start_time."
            )

        location = self.location_service.get_or_create_location(
            city=city,
            db=db,
        )

        # ForecastService owns live fetch + database fallback.
        forecasts = self.forecast_service.get_hourly_forecast(
            location=location,
            db=db,
        )

        records = self.build_forecast_records_from_models(forecasts)

        result = self.risk_engine.calculate_risk_window(
            forecasts=records,
            start_time=start_time,
            end_time=end_time,
            activity=activity,
            warning_color=warning_color,
        )

        return {
            "location": {
                "name": location.name,
                "district": location.district,
                "state": location.state,
                "country": location.country,
                "latitude": location.latitude,
                "longitude": location.longitude,
            },
            "risk": result,
            "activity": activity,
        }
