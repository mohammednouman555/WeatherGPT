"""
Forecast-based risk analysis for WeatherGPT.

This module evaluates hourly forecast data and identifies
weather risk for a requested time.
"""

from datetime import datetime

from app.risk.engine import RiskEngine


class ForecastRiskEngine:

    def __init__(self):
        self.risk_engine = RiskEngine()

    @staticmethod
    def extract_weather_code(
        forecast: dict,
    ) -> int | None:
        """
        Extract the WMO weather code from forecast data.

        The database currently stores the WMO code in
        the weather_condition field.
        """

        weather_code = forecast.get("weather_code")

        if weather_code is None:
            weather_code = forecast.get(
                "weather_condition"
            )

        if weather_code is None:
            return None

        try:
            return int(weather_code)
        except (TypeError, ValueError):
            return None

    def calculate_hourly_risk(
        self,
        forecast: dict,
        activity: str | None = None,
        warning_color: str | None = None,
    ) -> dict:
        """
        Calculate risk for one hourly forecast.
        """

        weather_code = self.extract_weather_code(
            forecast
        )

        result = self.risk_engine.calculate_risk(
            temperature=forecast.get(
                "temperature"
            ),
            rainfall=forecast.get(
                "rainfall"
            ),
            wind_speed=forecast.get(
                "wind_speed"
            ),
            visibility=forecast.get(
                "visibility"
            ),
            weather_code=weather_code,
            warning_color=warning_color,
            activity=activity,
        )

        return {
            "forecast_time": forecast.get(
                "forecast_time"
            ),
            **result,
        }

    def find_closest_forecast(
        self,
        forecasts: list[dict],
        target_time: datetime,
    ) -> dict:
        """
        Find the forecast record closest to
        the requested time.
        """

        if not forecasts:
            raise ValueError(
                "No forecast data available."
            )

        return min(
            forecasts,
            key=lambda forecast: abs(
                forecast["forecast_time"]
                - target_time
            ),
        )

    def calculate_forecast_risk(
        self,
        forecasts: list[dict],
        target_time: datetime,
    ) -> dict:
        """
        Calculate risk for the forecast closest
        to the requested target time.
        """

        closest_forecast = (
            self.find_closest_forecast(
                forecasts,
                target_time,
            )
        )

        return self.calculate_hourly_risk(
            closest_forecast
        )