from app.services.alert_decision_service import AlertDecisionService


service = AlertDecisionService()


test_cases = [
    {
        "peak_risk_level": "Low",
        "peak_risk": 10,
        "peak_hazard": "None",
    },
    {
        "peak_risk_level": "Moderate",
        "peak_risk": 47,
        "peak_hazard": "Thunderstorm",
    },
    {
        "peak_risk_level": "High",
        "peak_risk": 72,
        "peak_hazard": "Rain",
    },
    {
        "peak_risk_level": "Severe",
        "peak_risk": 91,
        "peak_hazard": "Heat",
    },
]


print("\n===== ALERT DECISION TEST =====")

for test_case in test_cases:

    result = service.generate_decision(
        risk_result=test_case
    )

    print("\n------------------------------")
    print(f"Risk level: {result['risk_level']}")
    print(f"Risk score: {result['risk_score']}")
    print(f"Hazard: {result['hazard']}")
    print(f"Title: {result['title']}")
    print(f"Priority: {result['priority']}")
    print(f"Message: {result['message']}")