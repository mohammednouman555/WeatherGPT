from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class WeatherObservation(Base):
    __tablename__ = "weather_observations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id"),
        nullable=False,
        index=True
    )

    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    observed_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True
    )

    temperature: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    feels_like: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    humidity: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    pressure: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    wind_speed: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    wind_direction: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    rainfall: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    visibility: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    cloud_cover: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    weather_condition: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )