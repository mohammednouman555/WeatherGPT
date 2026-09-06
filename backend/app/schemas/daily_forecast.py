from datetime import date, datetime

from pydantic import BaseModel


class DailyForecastItem(BaseModel):
    forecast_date: date

    temperature_max: float | None = None
    temperature_min: float | None = None

    feels_like_max: float | None = None
    feels_like_min: float | None = None

    precipitation_sum: float | None = None
    rain_sum: float | None = None

    precipitation_probability_max: float | None = None
    precipitation_hours: float | None = None

    wind_speed_max: float | None = None
    wind_gusts_max: float | None = None
    wind_direction_dominant: float | None = None

    sunrise: datetime | None = None
    sunset: datetime | None = None

    weather_condition: str | None = None


class DailyForecastResponse(BaseModel):
    location: str

    latitude: float
    longitude: float

    forecasts: list[DailyForecastItem]

    source: str