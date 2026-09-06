from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    __table_args__ = (
        Index(
            "uq_alert_location_source_date_code_color",
            "location_id",
            "source",
            "forecast_date",
            "warning_code",
            "warning_color",
            unique=True,
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id"), nullable=False, index=True
    )
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    forecast_date: Mapped[date] = mapped_column(
        Date, nullable=False, index=True
    )
    alert_type: Mapped[str] = mapped_column(String(100), nullable=False)
    warning_code: Mapped[int] = mapped_column(Integer, nullable=False)
    warning_color: Mapped[str] = mapped_column(String(20), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    issued_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    alert_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
