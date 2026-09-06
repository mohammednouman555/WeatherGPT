from __future__ import annotations

from typing import Any

import httpx

from app.core.config import settings
from app.core.exceptions import ExternalServiceError


class OpenMeteoClient:
    """Small synchronous client with connection pooling and bounded retries."""

    def __init__(self) -> None:
        self.weather_url = settings.open_meteo_base_url
        self.geocoding_url = settings.open_meteo_geocoding_url

        self._client = httpx.Client(
            timeout=httpx.Timeout(
                timeout=settings.http_timeout_seconds,
                connect=settings.http_connect_timeout_seconds,
            ),
            limits=httpx.Limits(
                max_connections=10,
                max_keepalive_connections=5,
            ),
            headers={"User-Agent": "WeatherGPT/1.0"},
            follow_redirects=True,
        )

    def close(self) -> None:
        self._client.close()

    def _get_json(self, url: str, params: dict[str, Any]) -> dict:
        last_error: Exception | None = None

        for attempt in range(settings.http_retries + 1):
            try:
                response = self._client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if not isinstance(data, dict):
                    raise ValueError("Weather provider returned invalid JSON.")

                return data

            except (httpx.TimeoutException, httpx.TransportError) as exc:
                last_error = exc
                if attempt < settings.http_retries:
                    continue
                break

            except httpx.HTTPStatusError as exc:
                detail = exc.response.text[:300]
                raise ExternalServiceError(
                    f"Open-Meteo returned HTTP {exc.response.status_code}: {detail}"
                ) from exc

            except ValueError as exc:
                raise ExternalServiceError(
                    "Open-Meteo returned an invalid response."
                ) from exc

        raise ExternalServiceError(
            "Open-Meteo is temporarily unavailable."
        ) from last_error

    def search_location(self, city: str) -> dict:
        city = city.strip()
        if not city:
            raise ValueError("City must not be empty.")

        data = self._get_json(
            self.geocoding_url,
            {
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json",
                "countryCode": "IN",
            },
        )

        if not data.get("results"):
            raise ValueError(f"Location '{city}' was not found.")

        return data["results"][0]

    def get_current_weather(self, latitude: float, longitude: float) -> dict:
        return self._get_json(
            self.weather_url,
            {
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "apparent_temperature,"
                    "pressure_msl,"
                    "wind_speed_10m,"
                    "wind_direction_10m,"
                    "precipitation,"
                    "rain,"
                    "cloud_cover,"
                    "weather_code"
                ),
                # Visibility is an hourly variable at the provider.
                "hourly": "visibility",
                "forecast_days": 1,
                "timezone": "auto",
            },
        )

    def get_hourly_forecast(self, latitude: float, longitude: float) -> dict:
        return self._get_json(
            self.weather_url,
            {
                "latitude": latitude,
                "longitude": longitude,
                "hourly": (
                    "temperature_2m,"
                    "apparent_temperature,"
                    "relative_humidity_2m,"
                    "pressure_msl,"
                    "wind_speed_10m,"
                    "wind_direction_10m,"
                    "precipitation,"
                    "precipitation_probability,"
                    "visibility,"
                    "cloud_cover,"
                    "weather_code"
                ),
                "forecast_days": 2,
                "timezone": "auto",
            },
        )

    def get_daily_forecast(self, latitude: float, longitude: float) -> dict:
        return self._get_json(
            self.weather_url,
            {
                "latitude": latitude,
                "longitude": longitude,
                "daily": (
                    "weather_code,"
                    "temperature_2m_max,"
                    "temperature_2m_min,"
                    "apparent_temperature_max,"
                    "apparent_temperature_min,"
                    "precipitation_sum,"
                    "rain_sum,"
                    "precipitation_hours,"
                    "precipitation_probability_max,"
                    "wind_speed_10m_max,"
                    "wind_gusts_10m_max,"
                    "wind_direction_10m_dominant,"
                    "sunrise,"
                    "sunset"
                ),
                "forecast_days": 7,
                "timezone": "auto",
            },
        )
