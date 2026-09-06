from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class DailyForecast(Base):
    __tablename__ = "daily_forecasts"

    __table_args__ = (
        Index(
            "uq_daily_forecast_location_date_source",
            "location_id",
            "forecast_date",
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
    forecast_date: Mapped[date] = mapped_column(
        Date, nullable=False, index=True
    )

    temperature_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    temperature_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    feels_like_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    feels_like_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    precipitation_sum: Mapped[float | None] = mapped_column(Float, nullable=True)
    rain_sum: Mapped[float | None] = mapped_column(Float, nullable=True)
    precipitation_probability_max: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    precipitation_hours: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    wind_speed_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    wind_gusts_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    wind_direction_dominant: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    sunrise: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    sunset: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    weather_condition: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )
