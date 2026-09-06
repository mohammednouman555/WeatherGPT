from app.services.activity_context_service import ActivityContextService


service = ActivityContextService()


print("\n===== ACTIVITY CONTEXT =====")

activities = [
    "bike",
    "walking",
    "run",
    "cycling",
    "travel",
    "outdoor",
    None,
]


for activity in activities:

    result = service.get_activity_context(activity)

    print(f"\nInput: {activity}")
    print(f"Name: {result['name']}")
    print(f"Description: {result['description']}")
    print(f"Risk factors: {result.get('risk_factors')}")


print("\n===== CONTEXT RISK CALCULATION =====")

rain = 10.0
wind = 5.0
heat = 25.0
visibility = 4.0


for activity in ["bike", "walking", "run", "cycling"]:

    context_risk = service.calculate_context_risk(
        activity=activity,
        rain_risk=rain,
        wind_risk=wind,
        heat_risk=heat,
        visibility_risk=visibility,
    )

    print(
        f"{activity}: "
        f"rain={rain}, "
        f"wind={wind}, "
        f"heat={heat}, "
        f"visibility={visibility} "
        f"-> context risk={context_risk}"
    )