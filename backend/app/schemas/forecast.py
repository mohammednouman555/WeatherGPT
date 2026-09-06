from datetime import datetime

from pydantic import BaseModel


class HourlyForecastItem(BaseModel):
    forecast_time: datetime

    temperature: float | None = None
    feels_like: float | None = None
    humidity: float | None = None
    pressure: float | None = None

    wind_speed: float | None = None
    wind_direction: float | None = None

    rainfall: float | None = None
    precipitation_probability: float | None = None

    visibility: float | None = None
    cloud_cover: float | None = None

    weather_condition: str | None = None


class HourlyForecastResponse(BaseModel):
    location: str

    latitude: float
    longitude: float

    forecasts: list[HourlyForecastItem]

    source: str