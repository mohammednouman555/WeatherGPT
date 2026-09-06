import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
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


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Router
# ---------------------------------------------------------

router = APIRouter(
    prefix="/api/weather",
    tags=["Weather"],
)


# ---------------------------------------------------------
# Services
# ---------------------------------------------------------

location_service = LocationService()
weather_service = WeatherService()
forecast_service = ForecastService()
daily_forecast_service = DailyForecastService()


# =========================================================
# CURRENT WEATHER
# =========================================================

@router.get(
    "/current",
    response_model=CurrentWeatherResponse,
)
def get_current_weather(
    city: str,
    db: Session = Depends(get_db),
):
    try:
        logger.info(
            "Fetching current weather for city: %s",
            city,
        )

        # -------------------------------------------------
        # Get/create location
        # -------------------------------------------------

        location = location_service.get_or_create_location(
            city=city,
            db=db,
        )

        logger.info(
            "Resolved location: %s (%s, %s)",
            location.name,
            location.latitude,
            location.longitude,
        )

        # -------------------------------------------------
        # Get current weather
        # -------------------------------------------------

        observation = weather_service.get_current_weather(
            location=location,
            db=db,
        )

        # -------------------------------------------------
        # Response
        # -------------------------------------------------

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

    except ValueError as exc:
        db.rollback()

        logger.warning(
            "Invalid location/weather request for '%s': %s",
            city,
            exc,
        )

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except SQLAlchemyError as exc:
        db.rollback()

        logger.exception(
            "DATABASE ERROR while fetching current weather for '%s'",
            city,
        )

        raise HTTPException(
            status_code=500,
            detail="Database error while retrieving weather data.",
        )

    except Exception as exc:
        db.rollback()

        logger.exception(
            "ERROR while fetching current weather for '%s': %s",
            city,
            exc,
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve weather data.",
        )


# =========================================================
# HOURLY FORECAST
# =========================================================

@router.get(
    "/hourly",
    response_model=HourlyForecastResponse,
)
def get_hourly_forecast(
    city: str,
    db: Session = Depends(get_db),
):
    try:
        logger.info(
            "Fetching hourly forecast for city: %s",
            city,
        )

        # -------------------------------------------------
        # Get/create location
        # -------------------------------------------------

        location = location_service.get_or_create_location(
            city=city,
            db=db,
        )

        logger.info(
            "Resolved location: %s (%s, %s)",
            location.name,
            location.latitude,
            location.longitude,
        )

        # -------------------------------------------------
        # Get hourly forecast
        # -------------------------------------------------

        forecasts = forecast_service.get_hourly_forecast(
            location=location,
            db=db,
        )

        logger.info(
            "Retrieved %d hourly forecast records for '%s'",
            len(forecasts),
            city,
        )

        # -------------------------------------------------
        # Response
        # -------------------------------------------------

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

    except ValueError as exc:
        db.rollback()

        logger.warning(
            "Invalid hourly forecast request for '%s': %s",
            city,
            exc,
        )

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except SQLAlchemyError as exc:
        db.rollback()

        logger.exception(
            "DATABASE ERROR while fetching hourly forecast for '%s'",
            city,
        )

        raise HTTPException(
            status_code=500,
            detail="Database error while retrieving hourly forecast.",
        )

    except Exception as exc:
        db.rollback()

        logger.exception(
            "ERROR while fetching hourly forecast for '%s': %s",
            city,
            exc,
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve hourly forecast.",
        )


# =========================================================
# DAILY FORECAST
# =========================================================

@router.get(
    "/daily",
    response_model=DailyForecastResponse,
)
def get_daily_forecast(
    city: str,
    db: Session = Depends(get_db),
):
    try:
        logger.info(
            "Fetching daily forecast for city: %s",
            city,
        )

        # -------------------------------------------------
        # Get/create location
        # -------------------------------------------------

        location = location_service.get_or_create_location(
            city=city,
            db=db,
        )

        logger.info(
            "Resolved location: %s (%s, %s)",
            location.name,
            location.latitude,
            location.longitude,
        )

        # -------------------------------------------------
        # Get daily forecast
        # -------------------------------------------------

        forecasts = daily_forecast_service.get_daily_forecast(
            location=location,
            db=db,
        )

        logger.info(
            "Retrieved %d daily forecast records for '%s'",
            len(forecasts),
            city,
        )

        # -------------------------------------------------
        # Response
        # -------------------------------------------------

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
                        forecast.precipitation_probability_max
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
                        forecast.wind_direction_dominant
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

    except ValueError as exc:
        db.rollback()

        logger.warning(
            "Invalid daily forecast request for '%s': %s",
            city,
            exc,
        )

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except SQLAlchemyError as exc:
        db.rollback()

        logger.exception(
            "DATABASE ERROR while fetching daily forecast for '%s'",
            city,
        )

        raise HTTPException(
            status_code=500,
            detail="Database error while retrieving daily forecast.",
        )

    except Exception as exc:
        db.rollback()

        logger.exception(
            "ERROR while fetching daily forecast for '%s': %s",
            city,
            exc,
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve daily forecast.",
        )