from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Forecast(Base):
    __tablename__ = "forecasts"

    __table_args__ = (
        Index(
            "uq_forecast_location_time_source",
            "location_id",
            "forecast_time",
            "source",
            unique=True,
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id"), nullable=False, index=True
    )
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    forecast_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, index=True
    )

    temperature: Mapped[float | None] = mapped_column(Float, nullable=True)
    feels_like: Mapped[float | None] = mapped_column(Float, nullable=True)
    humidity: Mapped[float | None] = mapped_column(Float, nullable=True)
    pressure: Mapped[float | None] = mapped_column(Float, nullable=True)
    wind_speed: Mapped[float | None] = mapped_column(Float, nullable=True)
    wind_direction: Mapped[float | None] = mapped_column(Float, nullable=True)
    rainfall: Mapped[float | None] = mapped_column(Float, nullable=True)
    precipitation_probability: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    visibility: Mapped[float | None] = mapped_column(Float, nullable=True)
    cloud_cover: Mapped[float | None] = mapped_column(Float, nullable=True)
    weather_condition: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
