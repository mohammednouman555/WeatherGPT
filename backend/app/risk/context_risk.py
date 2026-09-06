"""
Context-aware risk analysis for WeatherGPT.

These are project-level decision-support adjustments,
not official warning classifications.
"""

ACTIVITY_CONTEXTS = {
    "indoor": {
        "rain_multiplier": 0.2,
        "wind_multiplier": 0.2,
        "heat_multiplier": 0.3,
        "visibility_multiplier": 0.2,
        "description": "Indoor activity",
    },
    "walking": {
        "rain_multiplier": 1.0,
        "wind_multiplier": 0.8,
        "heat_multiplier": 0.8,
        "visibility_multiplier": 1.0,
        "description": "Walking",
    },
    "running": {
        "rain_multiplier": 1.1,
        "wind_multiplier": 1.0,
        "heat_multiplier": 1.3,
        "visibility_multiplier": 1.0,
        "description": "Running",
    },
    "cycling": {
        "rain_multiplier": 1.2,
        "wind_multiplier": 1.2,
        "heat_multiplier": 0.9,
        "visibility_multiplier": 1.2,
        "description": "Cycling",
    },
    "bike_travel": {
        "rain_multiplier": 1.3,
        "wind_multiplier": 1.3,
        "heat_multiplier": 0.9,
        "visibility_multiplier": 1.3,
        "description": "Motorbike travel",
    },
    "driving": {
        "rain_multiplier": 1.1,
        "wind_multiplier": 1.0,
        "heat_multiplier": 0.5,
        "visibility_multiplier": 1.3,
        "description": "Driving",
    },
    "outdoor_event": {
        "rain_multiplier": 1.3,
        "wind_multiplier": 1.2,
        "heat_multiplier": 1.1,
        "visibility_multiplier": 0.9,
        "description": "Outdoor event",
    },
    "farming": {
        "rain_multiplier": 1.1,
        "wind_multiplier": 1.2,
        "heat_multiplier": 1.3,
        "visibility_multiplier": 0.8,
        "description": "Farming activity",
    },
    "general_travel": {
        "rain_multiplier": 1.2,
        "wind_multiplier": 1.1,
        "heat_multiplier": 0.8,
        "visibility_multiplier": 1.2,
        "description": "General travel",
    },
    "outdoor_activity": {
        "rain_multiplier": 1.1,
        "wind_multiplier": 1.0,
        "heat_multiplier": 1.1,
        "visibility_multiplier": 1.0,
        "description": "Outdoor activity",
    },
}


def normalize_activity(activity: str | None) -> str:
    if not activity:
        return "general"

    value = activity.lower().strip()

    aliases = {
        "bike": "bike_travel",
        "motorbike": "bike_travel",
        "motorcycle": "bike_travel",
        "biking": "cycling",
        "cycle": "cycling",
        "cycling": "cycling",
        "walk": "walking",
        "walking": "walking",
        "run": "running",
        "running": "running",
        "jog": "running",
        "jogging": "running",
        "car": "driving",
        "drive": "driving",
        "driving": "driving",
        "event": "outdoor_event",
        "outdoor event": "outdoor_event",
        "farm": "farming",
        "farming": "farming",
        "travel": "general_travel",
        "outdoor": "outdoor_activity",
        "outdoors": "outdoor_activity",
        "indoors": "indoor",
        "inside": "indoor",
    }

    return aliases.get(value, value)


def calculate_context_risk(
    activity: str | None,
    rain_risk: float,
    wind_risk: float,
    heat_risk: float,
    visibility_risk: float,
) -> dict:
    normalized_activity = normalize_activity(activity)

    context = ACTIVITY_CONTEXTS.get(
        normalized_activity,
        {
            "rain_multiplier": 1.0,
            "wind_multiplier": 1.0,
            "heat_multiplier": 1.0,
            "visibility_multiplier": 1.0,
            "description": "General activity",
        },
    )

    adjusted_rain = min(
        rain_risk * context["rain_multiplier"], 100.0
    )
    adjusted_wind = min(
        wind_risk * context["wind_multiplier"], 100.0
    )
    adjusted_heat = min(
        heat_risk * context["heat_multiplier"], 100.0
    )
    adjusted_visibility = min(
        visibility_risk * context["visibility_multiplier"], 100.0
    )

    context_risk = (
        adjusted_rain * 0.35
        + adjusted_wind * 0.25
        + adjusted_heat * 0.20
        + adjusted_visibility * 0.20
    )

    return {
        "activity": normalized_activity,
        "activity_description": context["description"],
        "context_risk": round(context_risk, 2),
        "adjusted_rain_risk": round(adjusted_rain, 2),
        "adjusted_wind_risk": round(adjusted_wind, 2),
        "adjusted_heat_risk": round(adjusted_heat, 2),
        "adjusted_visibility_risk": round(adjusted_visibility, 2),
    }
