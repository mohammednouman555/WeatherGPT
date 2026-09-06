from datetime import datetime

from app.risk.forecast_window import ForecastWindowEngine


engine = ForecastWindowEngine()


forecasts = [
    {
        "forecast_time": datetime(
            2026, 9, 4, 17, 0
        ),
        "temperature": 34.0,
        "rainfall": 2.0,
        "wind_speed": 25.0,
        "visibility": 5000.0,
        "weather_condition": "3",
    },
    {
        "forecast_time": datetime(
            2026, 9, 4, 18, 0
        ),
        "temperature": 36.0,
        "rainfall": 8.0,
        "wind_speed": 45.0,
        "visibility": 1800.0,
        "weather_condition": "95",
    },
    {
        "forecast_time": datetime(
            2026, 9, 4, 19, 0
        ),
        "temperature": 37.0,
        "rainfall": 10.0,
        "wind_speed": 60.0,
        "visibility": 1000.0,
        "weather_condition": "95",
    },
]


start_time = datetime(
    2026,
    9,
    4,
    17,
    0,
)

end_time = datetime(
    2026,
    9,
    4,
    19,
    0,
)


result = engine.calculate_risk_window(
    forecasts=forecasts,
    start_time=start_time,
    end_time=end_time,
)


print(result)