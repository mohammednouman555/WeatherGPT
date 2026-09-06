from app.services.llm_service import build_weather_prompt
from app.services.conversation_service import ConversationStore


def test_prompt_contains_activity_and_risk():
    prompt = build_weather_prompt(
        city="Hyderabad",
        activity="Cycling",
        weather={"temperature": 31.5, "condition": "Partly cloudy"},
        risk={"peak_risk": 42.5, "peak_risk_level": "Moderate", "peak_hazard": "Rain"},
        decision={"risk_score": 42.5, "risk_level": "Moderate", "message": "Cycling is possible with caution."},
        hourly_forecast=[{"forecast_time": "2026-09-04T20:00:00", "overall_risk": 42.5}],
        preferences={"name": "Nouman", "preferred_activities": ["Cycling"]},
        user_message="Is it better later?",
    )
    assert "Cycling" in prompt
    assert "42.5/100" in prompt
    assert "Is it better later?" in prompt
    assert "preferred activities" in prompt.lower()


def test_conversation_store_keeps_bounded_history():
    store = ConversationStore(max_turns=2)
    store.add("abc", "user", "one")
    store.add("abc", "assistant", "two")
    store.add("abc", "user", "three")
    history = store.get("abc")
    assert len(history) == 2
    assert history[0]["content"] == "two"
    assert history[1]["content"] == "three"
