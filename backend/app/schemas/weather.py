from datetime import datetime

from pydantic import BaseModel


class CurrentWeatherResponse(BaseModel):
    location: str

    latitude: float
    longitude: float

    observed_at: datetime

    temperature: float | None = None
    feels_like: float | None = None
    humidity: float | None = None
    pressure: float | None = None

    wind_speed: float | None = None
    wind_direction: float | None = None

    rainfall: float | None = None
    visibility: float | None = None
    cloud_cover: float | None = None

    weather_condition: str | None = None

    source: str