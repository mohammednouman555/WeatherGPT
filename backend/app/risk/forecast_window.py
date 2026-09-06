"""
Forecast risk window analysis for WeatherGPT.

Analyzes multiple hourly forecasts within a requested
time window and identifies average risk, peak risk,
and the highest-risk forecast hour.
"""

from datetime import datetime

from app.risk.forecast_risk import ForecastRiskEngine

from app.risk.trend import (
    calculate_risk_trend,
    find_peak_hazard,
)


class ForecastWindowEngine:

    def __init__(self):
        self.forecast_engine = ForecastRiskEngine()

    def calculate_risk_window(
        self,
        forecasts: list[dict],
        start_time: datetime,
        end_time: datetime,
        activity: str | None = None,
        warning_color: str | None = None,
    ) -> dict:
        """
        Calculate risk across a forecast time window.
        """

        if not forecasts:
            raise ValueError(
                "No forecast data available."
            )

        window_forecasts = [
            forecast
            for forecast in forecasts
            if start_time
            <= forecast["forecast_time"]
            <= end_time
        ]

        if not window_forecasts:
            raise ValueError(
                "No forecasts found within the requested time window."
            )

        hourly_results = []

        for forecast in window_forecasts:
            result = self.forecast_engine.calculate_hourly_risk(
                forecast=forecast,
                activity=activity,
                warning_color=warning_color,
            )

            hourly_results.append(result)

        risk_scores = [
            result["overall_risk"]
            for result in hourly_results
        ]

        average_risk = (
            sum(risk_scores) / len(risk_scores)
        )

        peak_result = max(
            hourly_results,
            key=lambda result: result["overall_risk"],
        )

        trend = calculate_risk_trend(
            risk_scores
        )

        peak_hazard = find_peak_hazard(
            hourly_results
        )

        return {
            "start_time": start_time,
            "end_time": end_time,
            "hours_analyzed": len(
                hourly_results
            ),
            "average_risk": round(
                average_risk,
                2,
            ),
            "peak_risk": peak_result[
                "overall_risk"
            ],
            "peak_risk_level": peak_result[
                "risk_level"
            ],
            "peak_risk_time": peak_result[
                "forecast_time"
            ],
            "risk_trend": trend,
            "peak_hazard": peak_hazard[
                "peak_hazard"
            ],
            "peak_hazard_value": peak_hazard[
                "peak_hazard_value"
            ],
            "peak_hazard_time": peak_hazard[
                "peak_hazard_time"
            ],
            "hourly_results": hourly_results,
        }