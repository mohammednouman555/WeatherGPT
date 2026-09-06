"""
Thresholds used by the WeatherGPT Risk Engine.

These are project-level decision-support thresholds.
They are NOT official IMD warning thresholds.
"""


# -----------------------------
# Rainfall thresholds (mm/hour)
# -----------------------------

RAIN_LOW = 0.0
RAIN_MODERATE = 2.5
RAIN_HIGH = 7.6
RAIN_VERY_HIGH = 15.0


# -----------------------------
# Wind speed thresholds (km/h)
# -----------------------------

WIND_LOW = 20.0
WIND_MODERATE = 40.0
WIND_HIGH = 60.0
WIND_VERY_HIGH = 80.0


# -----------------------------
# Temperature thresholds (°C)
# -----------------------------

HEAT_LOW = 30.0
HEAT_MODERATE = 35.0
HEAT_HIGH = 40.0
HEAT_VERY_HIGH = 45.0


# -----------------------------
# Visibility thresholds (m)
# -----------------------------

VISIBILITY_LOW = 5000.0
VISIBILITY_MODERATE = 2000.0
VISIBILITY_HIGH = 1000.0
VISIBILITY_VERY_HIGH = 500.0


# -----------------------------
# Precipitation probability (%)
# -----------------------------

PRECIP_PROB_LOW = 20.0
PRECIP_PROB_MODERATE = 50.0
PRECIP_PROB_HIGH = 70.0
PRECIP_PROB_VERY_HIGH = 90.0