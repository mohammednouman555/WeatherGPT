"""
WMO Weather Code interpretation for WeatherGPT.

The codes are based on the WMO weather interpretation used
by Open-Meteo.

This module translates numerical weather codes into
human-readable conditions and project hazard categories.
"""


WEATHER_CODES = {
    0: {
        "condition": "Clear sky",
        "hazard": "None",
        "severity": 0,
    },
    1: {
        "condition": "Mainly clear",
        "hazard": "None",
        "severity": 0,
    },
    2: {
        "condition": "Partly cloudy",
        "hazard": "None",
        "severity": 0,
    },
    3: {
        "condition": "Overcast",
        "hazard": "None",
        "severity": 0,
    },
    45: {
        "condition": "Fog",
        "hazard": "Visibility",
        "severity": 2,
    },
    48: {
        "condition": "Depositing rime fog",
        "hazard": "Visibility",
        "severity": 2,
    },
    51: {
        "condition": "Light drizzle",
        "hazard": "Rain",
        "severity": 1,
    },
    53: {
        "condition": "Moderate drizzle",
        "hazard": "Rain",
        "severity": 2,
    },
    55: {
        "condition": "Dense drizzle",
        "hazard": "Rain",
        "severity": 3,
    },
    56: {
        "condition": "Light freezing drizzle",
        "hazard": "Freezing",
        "severity": 3,
    },
    57: {
        "condition": "Dense freezing drizzle",
        "hazard": "Freezing",
        "severity": 4,
    },
    61: {
        "condition": "Slight rain",
        "hazard": "Rain",
        "severity": 1,
    },
    63: {
        "condition": "Moderate rain",
        "hazard": "Rain",
        "severity": 2,
    },
    65: {
        "condition": "Heavy rain",
        "hazard": "Rain",
        "severity": 4,
    },
    66: {
        "condition": "Light freezing rain",
        "hazard": "Freezing",
        "severity": 3,
    },
    67: {
        "condition": "Heavy freezing rain",
        "hazard": "Freezing",
        "severity": 4,
    },
    71: {
        "condition": "Slight snow fall",
        "hazard": "Snow",
        "severity": 1,
    },
    73: {
        "condition": "Moderate snow fall",
        "hazard": "Snow",
        "severity": 2,
    },
    75: {
        "condition": "Heavy snow fall",
        "hazard": "Snow",
        "severity": 4,
    },
    77: {
        "condition": "Snow grains",
        "hazard": "Snow",
        "severity": 2,
    },
    80: {
        "condition": "Slight rain showers",
        "hazard": "Rain",
        "severity": 1,
    },
    81: {
        "condition": "Moderate rain showers",
        "hazard": "Rain",
        "severity": 2,
    },
    82: {
        "condition": "Violent rain showers",
        "hazard": "Rain",
        "severity": 4,
    },
    85: {
        "condition": "Slight snow showers",
        "hazard": "Snow",
        "severity": 1,
    },
    86: {
        "condition": "Heavy snow showers",
        "hazard": "Snow",
        "severity": 4,
    },
    95: {
        "condition": "Thunderstorm",
        "hazard": "Thunderstorm",
        "severity": 4,
    },
    96: {
        "condition": "Thunderstorm with slight hail",
        "hazard": "Thunderstorm",
        "severity": 4,
    },
    99: {
        "condition": "Thunderstorm with heavy hail",
        "hazard": "Thunderstorm",
        "severity": 5,
    },
}


def interpret_weather_code(weather_code: int | None) -> dict:
    """
    Convert a WMO weather code into structured information.
    """

    if weather_code is None:
        return {
            "condition": "Unknown",
            "hazard": "Unknown",
            "severity": 0,
        }

    return WEATHER_CODES.get(
        weather_code,
        {
            "condition": "Unknown",
            "hazard": "Unknown",
            "severity": 0,
        },
    )