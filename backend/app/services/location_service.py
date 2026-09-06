from sqlalchemy import func
from sqlalchemy.orm import Session

from app.data.collectors.open_meteo import OpenMeteoClient
from app.models.location import Location


class LocationService:
    def __init__(self):
        self.client = OpenMeteoClient()

    def get_or_create_location(self, city: str, db: Session) -> Location:
        city = city.strip()
        if not city:
            raise ValueError("City must not be empty.")

        # Prefer the database. This prevents repeated geocoding calls.
        location = (
            db.query(Location)
            .filter(func.lower(Location.name) == city.lower())
            .order_by(Location.id.asc())
            .first()
        )

        if location is not None:
            return location

        result = self.client.search_location(city)

        latitude = float(result["latitude"])
        longitude = float(result["longitude"])

        # Coordinates are a second-level duplicate guard.
        location = (
            db.query(Location)
            .filter(
                Location.latitude == latitude,
                Location.longitude == longitude,
            )
            .first()
        )
        if location is not None:
            return location

        location = Location(
            name=result["name"],
            district=result.get("admin2"),
            state=result.get("admin1"),
            country=result.get("country", "India"),
            latitude=latitude,
            longitude=longitude,
        )

        db.add(location)
        db.commit()
        db.refresh(location)
        return location
