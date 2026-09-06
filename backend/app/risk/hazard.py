"""
Individual weather hazard calculations.

Each function converts a weather variable into
a 0-100 project-generated risk score.
"""

from app.risk.weather_codes import interpret_weather_code

from app.risk.thresholds import (
    HEAT_LOW,
    HEAT_MODERATE,
    HEAT_HIGH,
    HEAT_VERY_HIGH,
    RAIN_LOW,
    RAIN_MODERATE,
    RAIN_HIGH,
    RAIN_VERY_HIGH,
    WIND_LOW,
    WIND_MODERATE,
    WIND_HIGH,
    WIND_VERY_HIGH,
    VISIBILITY_LOW,
    VISIBILITY_MODERATE,
    VISIBILITY_HIGH,
    VISIBILITY_VERY_HIGH,
)


def calculate_rain_risk(rainfall: float | None) -> float:
    """
    Calculate rain-related risk from rainfall intensity.

    Returns:
        Risk score from 0 to 100.
    """

    if rainfall is None or rainfall <= RAIN_LOW:
        return 0.0

    if rainfall < RAIN_MODERATE:
        return 20.0

    if rainfall < RAIN_HIGH:
        return 50.0

    if rainfall < RAIN_VERY_HIGH:
        return 75.0

    return 100.0


def calculate_wind_risk(wind_speed: float | None) -> float:
    """
    Calculate wind-related risk.

    wind_speed is expected in km/h.
    """

    if wind_speed is None or wind_speed <= WIND_LOW:
        return 0.0

    if wind_speed < WIND_MODERATE:
        return 25.0

    if wind_speed < WIND_HIGH:
        return 50.0

    if wind_speed < WIND_VERY_HIGH:
        return 75.0

    return 100.0


def calculate_heat_risk(temperature: float | None) -> float:
    """
    Calculate heat-related risk.

    temperature is expected in Celsius.
    """

    if temperature is None or temperature <= HEAT_LOW:
        return 0.0

    if temperature < HEAT_MODERATE:
        return 25.0

    if temperature < HEAT_HIGH:
        return 50.0

    if temperature < HEAT_VERY_HIGH:
        return 75.0

    return 100.0


def calculate_visibility_risk(visibility: float | None) -> float:
    """
    Calculate visibility-related risk.

    visibility is expected in meters.
    """

    if visibility is None:
        return 0.0

    if visibility >= VISIBILITY_LOW:
        return 0.0

    if visibility >= VISIBILITY_MODERATE:
        return 25.0

    if visibility >= VISIBILITY_HIGH:
        return 50.0

    if visibility >= VISIBILITY_VERY_HIGH:
        return 75.0

    return 100.0


def calculate_weather_condition_hazard(
    weather_code: int | None,
) -> dict:
    """
    Analyze the WMO weather code and identify
    the associated hazard.
    """

    weather = interpret_weather_code(weather_code)

    return {
        "condition": weather["condition"],
        "hazard": weather["hazard"],
        "severity": weather["severity"],
    }