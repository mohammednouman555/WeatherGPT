def calculate_risk_trend(
    risk_scores: list[float],
) -> str:
    if len(risk_scores) < 2:
        return "Stable"

    first = risk_scores[0]
    last = risk_scores[-1]

    difference = last - first

    if difference >= 10:
        return "Increasing"

    if difference <= -10:
        return "Decreasing"

    return "Stable"


def find_peak_hazard(
    hourly_results: list[dict],
) -> dict:
    if not hourly_results:
        raise ValueError(
            "No hourly risk results available."
        )

    peak_result = max(
        hourly_results,
        key=lambda result: result["overall_risk"],
    )

    hazards = {
        "Rain": peak_result["rain_risk"],
        "Wind": peak_result["wind_risk"],
        "Heat": peak_result["heat_risk"],
        "Visibility": peak_result["visibility_risk"],
    }

    weather_hazard = peak_result.get(
        "weather_hazard"
    )

    weather_severity = peak_result.get(
        "weather_severity",
        0,
    )

    if (
        weather_hazard
        and weather_hazard != "None"
        and weather_hazard != "Unknown"
    ):
        hazards[weather_hazard] = (
            weather_severity * 20
        )

    peak_hazard = max(
        hazards,
        key=hazards.get,
    )

    peak_hazard_value = hazards[
        peak_hazard
    ]

    # If there is no meaningful hazard,
    # report None instead of selecting the
    # largest low-level component.
    if peak_hazard_value <= 25:
        return {
            "peak_hazard": "None",
            "peak_hazard_value": 0.0,
            "peak_hazard_time": peak_result[
                "forecast_time"
            ],
        }

    return {
        "peak_hazard": peak_hazard,
        "peak_hazard_value": peak_hazard_value,
        "peak_hazard_time": peak_result[
            "forecast_time"
        ],
    }