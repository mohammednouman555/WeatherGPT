from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ========================================================
    # APPLICATION
    # ========================================================

    app_name: str = "WeatherGPT"
    app_version: str = "1.0.0"
    debug: bool = False

    # ========================================================
    # DATABASE
    # ========================================================

    database_url: str = "sqlite:///./weathergpt.db"

    # ========================================================
    # WEATHER SERVICES
    # ========================================================

    open_meteo_base_url: str = (
        "https://api.open-meteo.com/v1/forecast"
    )

    open_meteo_geocoding_url: str = (
        "https://geocoding-api.open-meteo.com/v1/search"
    )

    imd_warning_base_url: str = (
        "https://mausam.imd.gov.in/api/warnings_district_api.php"
    )

    # ========================================================
    # HTTP SETTINGS
    # ========================================================

    http_timeout_seconds: float = 6.0
    http_connect_timeout_seconds: float = 3.0
    http_retries: int = 2

    # ========================================================
    # CACHE SETTINGS
    # ========================================================

    current_cache_minutes: int = 10
    forecast_cache_minutes: int = 30
    daily_cache_minutes: int = 180
    fallback_max_age_hours: int = 24

    # ========================================================
    # GEMINI
    # ========================================================

    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.1-flash-lite"

    # ========================================================
    # ENVIRONMENT CONFIGURATION
    # ========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()