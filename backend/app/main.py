from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.api.risk import router as risk_router
from app.api.weather import router as weather_router
from app.core.config import settings

from app.core.database import Base, engine
from app import models


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

Base.metadata.create_all(bind=engine)


def ensure_database_indexes():
    """
    Ensure important PostgreSQL indexes exist.

    SQLAlchemy's Base.metadata.create_all() only creates tables
    and objects that do not already exist. It does NOT reliably
    repair missing indexes/constraints in an existing database.

    Render is using an existing PostgreSQL database, so we
    explicitly ensure the forecast unique index exists.
    """

    try:
        with engine.begin() as connection:
            connection.execute(
                text(
                    """
                    CREATE UNIQUE INDEX IF NOT EXISTS
                    uq_forecast_location_time_source
                    ON forecasts (
                        location_id,
                        forecast_time,
                        source
                    )
                    """
                )
            )

        print(
            "DATABASE: Forecast unique index "
            "'uq_forecast_location_time_source' is ready."
        )

    except Exception as exc:
        print(
            "DATABASE WARNING: Could not ensure forecast unique index: "
            f"{exc}"
        )


ensure_database_indexes()


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
INDEX_FILE = STATIC_DIR / "index.html"


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "AI-Powered Hyperlocal Weather Risk "
        "& Decision Intelligence Platform"
    ),
)


# ============================================================
# API ROUTERS
# ============================================================

app.include_router(health_router)
app.include_router(weather_router)
app.include_router(risk_router)
app.include_router(chat_router)


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)


# ============================================================
# DASHBOARD
# ============================================================

app.mount(
    "/dashboard",
    StaticFiles(
        directory=str(STATIC_DIR),
        html=True,
    ),
    name="dashboard",
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return FileResponse(str(INDEX_FILE))