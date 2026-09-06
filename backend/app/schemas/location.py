from pydantic import BaseModel


class LocationResult(BaseModel):
    name: str
    latitude: float
    longitude: float

    district: str | None = None
    state: str | None = None
    country: str | None = None

    timezone: str | None = None