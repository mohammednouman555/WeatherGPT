from datetime import datetime

from app.core.database import SessionLocal
from app.services.risk_service import RiskService


risk_service = RiskService()

db = SessionLocal()

try:

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

    result = risk_service.calculate_city_risk(
        city="Hyderabad",
        start_time=start_time,
        end_time=end_time,
        db=db,
        activity="bike",
    )

    print("\n===== WEATHERGPT REAL CITY RISK =====")

    print(
        "Location:",
        result["location"]["name"],
    )

    print(
        "District:",
        result["location"]["district"],
    )

    print(
        "State:",
        result["location"]["state"],
    )

    print(
        "Coordinates:",
        result["location"]["latitude"],
        result["location"]["longitude"],
    )

    risk = result["risk"]

    print("\n===== RISK SUMMARY =====")

    print(
        "Average risk:",
        risk["average_risk"],
    )

    print(
        "Peak risk:",
        risk["peak_risk"],
    )

    print(
        "Risk level:",
        risk["peak_risk_level"],
    )

    print(
        "Peak risk time:",
        risk["peak_risk_time"],
    )

    print(
        "Risk trend:",
        risk["risk_trend"],
    )

    print(
        "Peak hazard:",
        risk["peak_hazard"],
    )

    print(
        "Peak hazard value:",
        risk["peak_hazard_value"],
    )

    print(
        "Peak hazard time:",
        risk["peak_hazard_time"],
    )

    print(
        "Activity:",
        result["activity"],
    )

    print("\n===== HOURLY RESULTS =====")

    for hour in risk["hourly_results"]:

        print(
            hour["forecast_time"],
            "| Risk:",
            hour["overall_risk"],
            "| Level:",
            hour["risk_level"],
            "| Hazard:",
            hour["weather_condition"],
        )

finally:

    db.close()