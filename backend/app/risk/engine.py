"""
WeatherGPT Risk Engine.

Combines:
- Numerical weather hazards
- Weather conditions
- Official warnings
- User activity context

into a project-generated weather risk score.
"""

from app.risk.context_risk import calculate_context_risk

from app.risk.hazard import (
    calculate_heat_risk,
    calculate_rain_risk,
    calculate_visibility_risk,
    calculate_weather_condition_hazard,
    calculate_wind_risk,
)

from app.risk.warning_risk import (
    calculate_warning_risk,
    get_warning_priority,
)


class RiskEngine:

    @staticmethod
    def get_risk_level(score: float) -> str:
        """
        Convert the project-generated risk score
        into a human-readable risk level.
        """

        if score < 25:
            return "Low"

        if score < 50:
            return "Moderate"

        if score < 75:
            return "High"

        return "Severe"

    def calculate_risk(
        self,
        temperature: float | None = None,
        rainfall: float | None = None,
        wind_speed: float | None = None,
        visibility: float | None = None,
        weather_code: int | None = None,
        warning_color: str | None = None,
        activity: str | None = None,
    ) -> dict:

        # --------------------------------
        # Basic hazard calculations
        # --------------------------------

        rain_risk = calculate_rain_risk(
            rainfall
        )

        wind_risk = calculate_wind_risk(
            wind_speed
        )

        heat_risk = calculate_heat_risk(
            temperature
        )

        visibility_risk = calculate_visibility_risk(
            visibility
        )

        # --------------------------------
        # Weather condition hazard
        # --------------------------------

        weather_hazard = (
            calculate_weather_condition_hazard(
                weather_code
            )
        )

        # --------------------------------
        # Official warning
        # --------------------------------

        warning_risk = calculate_warning_risk(
            warning_color
        )

        # --------------------------------
        # Context-aware risk
        # --------------------------------

        context_result = calculate_context_risk(
            activity=activity,
            rain_risk=rain_risk,
            wind_risk=wind_risk,
            heat_risk=heat_risk,
            visibility_risk=visibility_risk,
        )

        # --------------------------------
        # Overall risk
        # --------------------------------

        overall_risk = (
            context_result["context_risk"] * 0.60
            + weather_hazard["severity"] * 2.0
            + warning_risk
        )

        overall_risk = min(
            round(overall_risk, 2),
            100.0,
        )

        return {
            "overall_risk": overall_risk,
            "risk_level": self.get_risk_level(
                overall_risk
            ),

            "rain_risk": rain_risk,
            "wind_risk": wind_risk,
            "heat_risk": heat_risk,
            "visibility_risk": visibility_risk,

            "weather_condition": weather_hazard[
                "condition"
            ],

            "weather_hazard": weather_hazard[
                "hazard"
            ],

            "weather_severity": weather_hazard[
                "severity"
            ],

            "warning_color": warning_color,
            "warning_risk": warning_risk,

            "warning_priority": get_warning_priority(
                warning_color
            ),

            "activity": context_result[
                "activity"
            ],

            "activity_description": context_result[
                "activity_description"
            ],

            "context_risk": context_result[
                "context_risk"
            ],
        }