from app.risk.engine import RiskEngine


engine = RiskEngine()


def print_result(title, result):
    print(f"\n===== {title} =====")
    print(f"Overall risk: {result['overall_risk']}")
    print(f"Risk level: {result['risk_level']}")
    print(f"Rain risk: {result['rain_risk']}")
    print(f"Wind risk: {result['wind_risk']}")
    print(f"Heat risk: {result['heat_risk']}")
    print(f"Visibility risk: {result['visibility_risk']}")
    print(f"Weather condition: {result['weather_condition']}")
    print(f"Weather hazard: {result['weather_hazard']}")
    print(f"Weather severity: {result['weather_severity']}")
    print(f"Warning risk: {result['warning_risk']}")
    print(f"Warning priority: {result['warning_priority']}")
    print(f"Activity: {result['activity']}")
    print(f"Context risk: {result['context_risk']}")


# --------------------------------
# TEST 1 — Normal weather
# --------------------------------

result = engine.calculate_risk(
    temperature=25,
    rainfall=0,
    wind_speed=5,
    visibility=10000,
    weather_code=1,
    activity="walking",
)

print_result(
    "NORMAL WEATHER",
    result,
)


# --------------------------------
# TEST 2 — Moderate conditions
# --------------------------------

result = engine.calculate_risk(
    temperature=35,
    rainfall=5,
    wind_speed=20,
    visibility=5000,
    weather_code=61,
    activity="walking",
)

print_result(
    "MODERATE CONDITIONS",
    result,
)


# --------------------------------
# TEST 3 — High-risk conditions
# --------------------------------

result = engine.calculate_risk(
    temperature=40,
    rainfall=15,
    wind_speed=35,
    visibility=2000,
    weather_code=63,
    activity="bike",
)

print_result(
    "HIGH-RISK CONDITIONS",
    result,
)


# --------------------------------
# TEST 4 — Severe conditions
# --------------------------------

result = engine.calculate_risk(
    temperature=45,
    rainfall=50,
    wind_speed=60,
    visibility=500,
    weather_code=95,
    warning_color="Red",
    activity="bike",
)

print_result(
    "SEVERE CONDITIONS",
    result,
)