from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import DataUnavailableError, ExternalServiceError
from app.data.collectors.open_meteo import OpenMeteoClient
from app.models.location import Location
from app.models.weather import WeatherObservation


class WeatherService:
    def __init__(self):
        self.client = OpenMeteoClient()

    @staticmethod
    def _current_visibility(data: dict, current_time: datetime) -> float | None:
        hourly = data.get("hourly") or {}
        times = hourly.get("time") or []
        values = hourly.get("visibility") or []

        if not times or not values:
            return None

        pairs = []
        for time_value, visibility in zip(times, values):
            try:
                pairs.append((datetime.fromisoformat(time_value), visibility))
            except (TypeError, ValueError):
                continue

        if not pairs:
            return None

        closest_time, visibility = min(
            pairs,
            key=lambda pair: abs(pair[0] - current_time),
        )

        # Avoid using an hourly value that is wildly unrelated to the current
        # observation if a provider response has unusual timestamps.
        if abs(closest_time - current_time) > timedelta(hours=2):
            return None

        return visibility

    def _cached_observation(
        self,
        location: Location,
        db: Session,
    ) -> WeatherObservation | None:
        cutoff = datetime.utcnow() - timedelta(
            hours=settings.fallback_max_age_hours
        )

        return (
            db.query(WeatherObservation)
            .filter(
                WeatherObservation.location_id == location.id,
                WeatherObservation.observed_at >= cutoff,
            )
            .order_by(WeatherObservation.observed_at.desc())
            .first()
        )

    def get_current_weather(
        self,
        location: Location,
        db: Session,
    ) -> WeatherObservation:
        try:
            data = self.client.get_current_weather(
                latitude=location.latitude,
                longitude=location.longitude,
            )
            current = data.get("current")
            if not current or not current.get("time"):
                raise ExternalServiceError(
                    "Open-Meteo returned no current weather data."
                )

            observed_at = datetime.fromisoformat(current["time"])
            visibility = self._current_visibility(data, observed_at)

            observation = WeatherObservation(
                location_id=location.id,
                source="Open-Meteo",
                observed_at=observed_at,
                temperature=current.get("temperature_2m"),
                feels_like=current.get("apparent_temperature"),
                humidity=current.get("relative_humidity_2m"),
                pressure=current.get("pressure_msl"),
                wind_speed=current.get("wind_speed_10m"),
                wind_direction=current.get("wind_direction_10m"),
                rainfall=current.get("rain"),
                visibility=visibility,
                cloud_cover=current.get("cloud_cover"),
                weather_condition=str(current.get("weather_code")),
            )

            db.add(observation)
            db.commit()
            db.refresh(observation)
            return observation

        except (ExternalServiceError, OSError, TimeoutError):
            cached = self._cached_observation(location, db)
            if cached is not None:
                return cached
            raise DataUnavailableError(
                "Current weather is temporarily unavailable and no cached "
                "observation exists."
            )
