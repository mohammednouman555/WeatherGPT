from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.weather import CurrentWeatherResponse
from app.services.location_service import LocationService
from app.services.weather_service import WeatherService

from app.schemas.forecast import (
    HourlyForecastItem,
    HourlyForecastResponse,
)
from app.services.forecast_service import ForecastService

from app.schemas.daily_forecast import (
    DailyForecastItem,
    DailyForecastResponse,
)

from app.services.daily_forecast_service import (
    DailyForecastService,
)


router = APIRouter(
    prefix="/api/weather",
    tags=["Weather"],
)


location_service = LocationService()
weather_service = WeatherService()

forecast_service = ForecastService()

daily_forecast_service = DailyForecastService()


@router.get(
    "/current",
    response_model=CurrentWeatherResponse,
)
def get_current_weather(
    city: str,
    db: Session = Depends(get_db),
):
    try:
        location = location_service.get_or_create_location(
            city=city,
            db=db,
        )

        observation = weather_service.get_current_weather(
            location=location,
            db=db,
        )

        return CurrentWeatherResponse(
            location=location.name,

            latitude=location.latitude,
            longitude=location.longitude,

            observed_at=observation.observed_at,

            temperature=observation.temperature,
            feels_like=observation.feels_like,
            humidity=observation.humidity,
            pressure=observation.pressure,

            wind_speed=observation.wind_speed,
            wind_direction=observation.wind_direction,

            rainfall=observation.rainfall,
            visibility=observation.visibility,
            cloud_cover=observation.cloud_cover,

            weather_condition=observation.weather_condition,

            source=observation.source,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve weather data.",
        )


@router.get(
    "/hourly",
    response_model=HourlyForecastResponse,
)
def get_hourly_forecast(
    city: str,
    db: Session = Depends(get_db),
):
    try:
        location = location_service.get_or_create_location(
            city=city,
            db=db,
        )

        forecasts = forecast_service.get_hourly_forecast(
            location=location,
            db=db,
        )

        return HourlyForecastResponse(
            location=location.name,

            latitude=location.latitude,
            longitude=location.longitude,

            forecasts=[
                HourlyForecastItem(
                    forecast_time=forecast.forecast_time,

                    temperature=forecast.temperature,
                    feels_like=forecast.feels_like,
                    humidity=forecast.humidity,
                    pressure=forecast.pressure,

                    wind_speed=forecast.wind_speed,
                    wind_direction=forecast.wind_direction,

                    rainfall=forecast.rainfall,
                    precipitation_probability=(
                        forecast.precipitation_probability
                    ),

                    visibility=forecast.visibility,
                    cloud_cover=forecast.cloud_cover,

                    weather_condition=(
                        forecast.weather_condition
                    ),
                )

                for forecast in forecasts
            ],

            source="Open-Meteo",
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve hourly forecast.",
        )


@router.get(
    "/daily",
    response_model=DailyForecastResponse,
)
def get_daily_forecast(
    city: str,
    db: Session = Depends(get_db),
):
    try:
        location = location_service.get_or_create_location(
            city=city,
            db=db,
        )

        forecasts = (
            daily_forecast_service.get_daily_forecast(
                location=location,
                db=db,
            )
        )

        return DailyForecastResponse(
            location=location.name,

            latitude=location.latitude,
            longitude=location.longitude,

            forecasts=[
                DailyForecastItem(
                    forecast_date=forecast.forecast_date,

                    temperature_max=(
                        forecast.temperature_max
                    ),

                    temperature_min=(
                        forecast.temperature_min
                    ),

                    feels_like_max=(
                        forecast.feels_like_max
                    ),

                    feels_like_min=(
                        forecast.feels_like_min
                    ),

                    precipitation_sum=(
                        forecast.precipitation_sum
                    ),

                    rain_sum=forecast.rain_sum,

                    precipitation_probability_max=(
                        forecast
                        .precipitation_probability_max
                    ),

                    precipitation_hours=(
                        forecast.precipitation_hours
                    ),

                    wind_speed_max=(
                        forecast.wind_speed_max
                    ),

                    wind_gusts_max=(
                        forecast.wind_gusts_max
                    ),

                    wind_direction_dominant=(
                        forecast
                        .wind_direction_dominant
                    ),

                    sunrise=forecast.sunrise,
                    sunset=forecast.sunset,

                    weather_condition=(
                        forecast.weather_condition
                    ),
                )

                for forecast in forecasts
            ],

            source="Open-Meteo",
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve daily forecast.",
        )