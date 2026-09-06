from __future__ import annotations

import httpx

from app.core.config import settings
from app.core.exceptions import ExternalServiceError


class IMDClient:
    """
    Client for the IMD district warning service.

    IMD access is treated as an optional external dependency.
    Failure here must never crash the core WeatherGPT pipeline.
    """

    def __init__(self) -> None:
        self.warning_url = settings.imd_warning_base_url

        self._client = httpx.Client(
            timeout=httpx.Timeout(
                timeout=settings.http_timeout_seconds,
                connect=settings.http_connect_timeout_seconds,
            ),
            limits=httpx.Limits(
                max_connections=5,
                max_keepalive_connections=2,
            ),
            headers={
                "User-Agent": "WeatherGPT/1.0",
            },
            follow_redirects=True,
        )

    def close(self) -> None:
        self._client.close()

    def get_district_warnings(
        self,
        district_id: int,
    ) -> dict:
        """
        Retrieve district warnings from IMD.

        Raises ExternalServiceError instead of leaking
        low-level HTTP/client errors to the API.
        """

        if district_id <= 0:
            raise ValueError(
                "district_id must be a positive integer."
            )

        try:
            response = self._client.get(
                self.warning_url,
                params={"id": district_id},
            )

            if response.status_code == 401:
                raise ExternalServiceError(
                    "IMD warning service is unauthorized. "
                    "Live official warnings are currently unavailable."
                )

            response.raise_for_status()

            data = response.json()

            if not isinstance(data, dict):
                raise ExternalServiceError(
                    "IMD returned an invalid warning response."
                )

            return data

        except ExternalServiceError:
            raise

        except httpx.TimeoutException as exc:
            raise ExternalServiceError(
                "IMD warning service timed out."
            ) from exc

        except httpx.HTTPError as exc:
            raise ExternalServiceError(
                "IMD warning service is temporarily unavailable."
            ) from exc

        except ValueError as exc:
            raise ExternalServiceError(
                "IMD returned invalid warning data."
            ) from exc