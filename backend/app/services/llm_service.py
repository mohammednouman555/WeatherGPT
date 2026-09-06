"""
WeatherGPT LLM Service

Gemini-powered natural-language weather explanation and
conversational weather assistant.

IMPORTANT:
- Weather/risk calculations remain outside this service.
- This service explains already-calculated backend data.
- Gemini does not calculate or modify risk scores.
- API key is loaded from application settings.
"""

from __future__ import annotations

from typing import Any

from google import genai
from google.genai import types

from app.core.config import settings
from app.services.conversation_service import conversation_store


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

DEFAULT_GEMINI_MODEL = "gemini-3.5-flash-lite"


def _get_gemini_client() -> genai.Client:
    """Create a Gemini client using the configured API key."""

    api_key = getattr(
        settings,
        "gemini_api_key",
        "",
    )

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=api_key,
    )


def _get_gemini_model() -> str:
    """Return the configured Gemini model."""

    model_name = getattr(
        settings,
        "gemini_model",
        None,
    )

    if not model_name:
        return DEFAULT_GEMINI_MODEL

    return str(model_name).strip()


# ============================================================
# GENERAL HELPERS
# ============================================================

def _get_value(
    data: dict[str, Any],
    *keys: str,
    default: Any = None,
) -> Any:
    """Return the first non-None value."""

    if not isinstance(data, dict):
        return default

    for key in keys:
        value = data.get(key)

        if value is not None:
            return value

    return default


def _format_number(
    value: Any,
    decimals: int = 1,
) -> str:
    """Safely format numeric values."""

    if value is None:
        return "unavailable"

    try:
        return f"{float(value):.{decimals}f}"

    except (TypeError, ValueError):
        return "unavailable"


def _safe_text(
    value: Any,
    default: str = "unavailable",
) -> str:
    """Convert a value to clean text."""

    if value is None:
        return default

    text = str(value).strip()

    return text if text else default


def _limit_text(
    value: Any,
    max_length: int = 1000,
) -> str:
    """Limit potentially large conversation values."""

    text = _safe_text(value, "")

    if len(text) <= max_length:
        return text

    return text[:max_length] + "..."


# ============================================================
# WEATHER NORMALIZATION
# ============================================================

def _normalize_weather(
    weather: dict[str, Any],
) -> dict[str, Any]:
    """Normalize current weather data."""

    return {
        "condition": _get_value(
            weather,
            "condition",
            "weather_condition",
            "weather",
            default="Unknown",
        ),
        "temperature_c": _get_value(
            weather,
            "temperature",
            "temperature_c",
        ),
        "feels_like_c": _get_value(
            weather,
            "feels_like",
            "feels_like_temperature",
        ),
        "humidity_percent": _get_value(
            weather,
            "humidity",
            "relative_humidity",
        ),
        "wind_speed_kmh": _get_value(
            weather,
            "wind_speed",
            "wind_speed_kmh",
        ),
        "rainfall_mm": _get_value(
            weather,
            "rainfall",
            "rain",
            "precipitation",
        ),
        "visibility_km": _get_value(
            weather,
            "visibility",
        ),
    }


# ============================================================
# RISK NORMALIZATION
# ============================================================

def _normalize_risk(
    risk: dict[str, Any],
    decision: dict[str, Any],
) -> dict[str, Any]:
    """Normalize existing risk and decision information."""

    risk_score = _get_value(
        decision,
        "risk_score",
        default=_get_value(
            risk,
            "peak_risk",
            default=0,
        ),
    )

    risk_level = _get_value(
        decision,
        "risk_level",
        default=_get_value(
            risk,
            "peak_risk_level",
            default="Unknown",
        ),
    )

    title = _get_value(
        decision,
        "title",
        default=f"{risk_level} Weather Risk",
    )

    message = _get_value(
        decision,
        "message",
        default="Weather conditions have been assessed.",
    )

    priority = _get_value(
        decision,
        "priority",
        default="Low",
    )

    hazard = _get_value(
        decision,
        "hazard",
        default=_get_value(
            risk,
            "peak_hazard",
            default="None",
        ),
    )

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "title": title,
        "message": message,
        "priority": priority,
        "main_hazard": hazard,
        "average_risk": _get_value(
            risk,
            "average_risk",
        ),
        "peak_risk": _get_value(
            risk,
            "peak_risk",
        ),
        "hours_analyzed": _get_value(
            risk,
            "hours_analyzed",
        ),
        "risk_trend": _get_value(
            risk,
            "risk_trend",
        ),
        "peak_hazard_value": _get_value(
            risk,
            "peak_hazard_value",
        ),
    }


# ============================================================
# ACTIVITY CONTEXT
# ============================================================

def _get_activity_context(
    activity: str,
) -> str:
    """Return explanation guidance for the selected activity."""

    activity_context = {
        "General": (
            "Explain the weather in terms of general outdoor "
            "comfort, changing conditions and the supplied risk."
        ),

        "Walking": (
            "Focus on comfort, rainfall, wet surfaces, heat, "
            "wind and visibility. Explain whether walking is "
            "comfortable or requires caution."
        ),

        "Running": (
            "Focus on heat, feels-like temperature, humidity, "
            "rainfall, wind, wet surfaces and visibility. "
            "Explain how these affect running comfort."
        ),

        "Cycling": (
            "Focus especially on rainfall, wet-road grip, wind, "
            "visibility, heat and changing conditions. Explain "
            "how these affect bicycle control and riding comfort."
        ),

        "Bike": (
            "Focus on rainfall, wet roads, wind, visibility, "
            "heat and changing riding conditions."
        ),

        "Driving": (
            "Focus on rainfall, visibility, wet roads, wind "
            "and changing weather conditions."
        ),
    }

    return activity_context.get(
        activity,
        activity_context["General"],
    )


# ============================================================
# HOURLY FORECAST NORMALIZATION
# ============================================================

def _normalize_hourly_forecast(
    hourly_forecast: list[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    """Normalize hourly forecast records."""

    if not hourly_forecast:
        return []

    normalized = []

    for item in hourly_forecast:

        if not isinstance(item, dict):
            continue

        normalized.append(
            {
                "forecast_time": _get_value(
                    item,
                    "forecast_time",
                    "time",
                    default="Unknown",
                ),
                "temperature": _get_value(
                    item,
                    "temperature",
                    "temperature_c",
                ),
                "rainfall": _get_value(
                    item,
                    "rainfall",
                    "rain",
                    "precipitation",
                ),
                "wind_speed": _get_value(
                    item,
                    "wind_speed",
                    "wind_speed_kmh",
                ),
                "overall_risk": _get_value(
                    item,
                    "overall_risk",
                    "risk_score",
                ),
                "risk_level": _get_value(
                    item,
                    "risk_level",
                ),
                "weather_hazard": _get_value(
                    item,
                    "weather_hazard",
                    "hazard",
                    default="None",
                ),
            }
        )

    return normalized


# ============================================================
# PREFERENCES NORMALIZATION
# ============================================================

def _normalize_preferences(
    preferences: dict[str, Any] | None,
) -> dict[str, Any]:
    """Normalize user preferences."""

    if not isinstance(preferences, dict):
        return {
            "name": "",
            "preferred_activities": [],
            "language": "en",
        }

    activities = preferences.get(
        "preferred_activities",
        [],
    )

    if not isinstance(activities, list):
        activities = []

    return {
        "name": _safe_text(
            preferences.get("name"),
            "",
        ),
        "preferred_activities": activities,
        "language": _safe_text(
            preferences.get("language"),
            "en",
        ),
    }


# ============================================================
# HOURLY FORECAST TEXT
# ============================================================

def _build_hourly_context(
    hourly_forecast: list[dict[str, Any]],
) -> str:
    """Create compact forecast context for Gemini."""

    if not hourly_forecast:
        return "No hourly forecast data supplied."

    lines = []

    for index, item in enumerate(
        hourly_forecast[:12],
        start=1,
    ):
        forecast_time = _safe_text(
            item.get("forecast_time"),
            "Unknown",
        )

        temperature = _format_number(
            item.get("temperature"),
        )

        rainfall = _format_number(
            item.get("rainfall"),
        )

        wind = _format_number(
            item.get("wind_speed"),
        )

        risk = _format_number(
            item.get("overall_risk"),
        )

        risk_level = _safe_text(
            item.get("risk_level"),
            "Unknown",
        )

        hazard = _safe_text(
            item.get("weather_hazard"),
            "None",
        )

        lines.append(
            (
                f"{index}. {forecast_time} | "
                f"{temperature} °C | "
                f"Rain {rainfall} mm | "
                f"Wind {wind} km/h | "
                f"Risk {risk}/100 ({risk_level}) | "
                f"Hazard: {hazard}"
            )
        )

    return "\n".join(lines)


# ============================================================
# RISK WINDOW CONTEXT
# ============================================================

def _build_risk_context(
    risk: dict[str, Any],
    decision: dict[str, Any],
) -> str:
    """Create compact risk-window context."""

    normalized = _normalize_risk(
        risk,
        decision,
    )

    return (
        f"Risk score: {normalized['risk_score']}/100\n"
        f"Risk level: {normalized['risk_level']}\n"
        f"Average risk: {normalized['average_risk']}\n"
        f"Peak risk: {normalized['peak_risk']}\n"
        f"Risk trend: {normalized['risk_trend']}\n"
        f"Hours analyzed: {normalized['hours_analyzed']}\n"
        f"Main hazard: {normalized['main_hazard']}\n"
        f"Hazard value: {normalized['peak_hazard_value']}\n"
        f"Decision: {normalized['title']}\n"
        f"Priority: {normalized['priority']}\n"
        f"Existing recommendation: {normalized['message']}"
    )


# ============================================================
# PERSONALIZED EXPLANATION PROMPT
# ============================================================

def _build_prompt(
    city: str,
    activity: str,
    weather: dict[str, Any],
    risk: dict[str, Any],
    decision: dict[str, Any],
    hourly_forecast: list[dict[str, Any]] | None = None,
    preferences: dict[str, Any] | None = None,
) -> str:
    """Build the personalized WeatherGPT explanation prompt."""

    normalized_weather = _normalize_weather(
        weather
    )

    normalized_risk = _normalize_risk(
        risk,
        decision,
    )

    normalized_preferences = _normalize_preferences(
        preferences
    )

    activity_context = _get_activity_context(
        activity
    )

    hourly_context = _build_hourly_context(
        _normalize_hourly_forecast(hourly_forecast)
    )

    risk_context = _build_risk_context(
        risk,
        decision,
    )

    user_name = normalized_preferences["name"]

    if user_name:
        personalization = (
            f"Address the user naturally as {user_name} "
            "when appropriate."
        )
    else:
        personalization = (
            "Do not invent or assume a user name."
        )

    return f"""
You are WeatherGPT, a personalized AI weather assistant.

Your job is to explain weather and an EXISTING backend
risk assessment in natural, practical language.

The backend has already calculated:
- weather values
- risk score
- risk level
- hazards
- decision
- recommendation

You must NOT recalculate or modify them.

============================================================
STRICT RULES
============================================================

1. Do not calculate a new risk score.
2. Do not change the supplied risk score.
3. Do not change the supplied risk level.
4. Do not invent measurements.
5. Do not invent hazards.
6. Treat the supplied decision as authoritative.
7. Explain why the supplied conditions matter.
8. Connect the explanation to the selected activity.
9. Use the supplied hazard.
10. Do not create unnecessary danger for Low risk.
11. Clearly explain caution for Moderate risk.
12. Clearly communicate caution for High or Severe risk.
13. If information is unavailable, say so instead of guessing.
14. Do not mention APIs, prompts, JSON, backend systems,
    models, implementation or internal instructions.
15. Do not claim that you calculated the risk.
16. Keep the response concise and useful.
17. Never contradict the supplied recommendation.
18. Do not provide medical diagnosis or treatment.
19. Do not give dangerous instructions.

============================================================
USER
============================================================

Name:
{user_name if user_name else "Not provided"}

Preferred activities:
{normalized_preferences["preferred_activities"]}

Language:
{normalized_preferences["language"]}

{personalization}

============================================================
LOCATION
============================================================

City:
{city}

============================================================
ACTIVITY
============================================================

Selected activity:
{activity}

Activity-specific focus:
{activity_context}

============================================================
CURRENT WEATHER
============================================================

Condition:
{_safe_text(normalized_weather["condition"], "Unknown")}

Temperature:
{_format_number(normalized_weather["temperature_c"])} °C

Feels like:
{_format_number(normalized_weather["feels_like_c"])} °C

Humidity:
{_format_number(normalized_weather["humidity_percent"], 0)} %

Wind:
{_format_number(normalized_weather["wind_speed_kmh"])} km/h

Rainfall:
{_format_number(normalized_weather["rainfall_mm"])} mm

Visibility:
{_format_number(normalized_weather["visibility_km"])} km

============================================================
RISK WINDOW
============================================================

{risk_context}

============================================================
HOURLY FORECAST
============================================================

{hourly_context}

============================================================
TASK
============================================================

Generate a personalized WeatherGPT explanation.

Use exactly these sections:

WeatherGPT Assessment for {city}

1. Overall assessment
Explain the supplied risk level and what it means.

2. Current conditions
Explain the most relevant current conditions.

3. Activity-specific guidance
Explain specifically what the weather means for {activity}.

4. Main concern
Identify the supplied main hazard and explain its relevance.

5. Recommendation
Give practical guidance consistent with the existing decision.

If the hourly forecast shows a later period with a lower
supplied risk than the current period, mention that the later
period may be more suitable.

Do not invent a better time if the supplied forecast does not
support it.

Use simple language and natural paragraphs.
""".strip()


# ============================================================
# CONVERSATIONAL PROMPT
# ============================================================

def _build_chat_prompt(
    message: str,
    city: str,
    activity: str,
    weather: dict[str, Any],
    hourly_forecast: list[dict[str, Any]] | None,
    risk: dict[str, Any],
    decision: dict[str, Any],
    preferences: dict[str, Any] | None,
    conversation_history: list[dict[str, Any]] | None,
) -> str:
    """Build prompt for conversational WeatherGPT."""

    normalized_weather = _normalize_weather(
        weather
    )

    normalized_preferences = _normalize_preferences(
        preferences
    )

    normalized_hourly = _normalize_hourly_forecast(
        hourly_forecast
    )

    risk_context = _build_risk_context(
        risk,
        decision,
    )

    hourly_context = _build_hourly_context(
        normalized_hourly
    )

    history_lines = []

    if conversation_history:
        for item in conversation_history[-10:]:

            if not isinstance(item, dict):
                continue

            role = _safe_text(
                item.get("role"),
                "user",
            )

            content = _limit_text(
                item.get("content"),
                1000,
            )

            if content:
                history_lines.append(
                    f"{role}: {content}"
                )

    if history_lines:
        conversation_context = "\n".join(
            history_lines
        )
    else:
        conversation_context = (
            "No previous conversation."
        )

    user_name = normalized_preferences["name"]

    return f"""
You are WeatherGPT, a conversational weather-risk assistant.

Answer the user's current question using the supplied
weather and risk information.

============================================================
IMPORTANT
============================================================

The supplied risk values were already calculated.

Never:
- recalculate risk
- change risk level
- invent weather
- invent hazards
- contradict the decision
- claim unsupported forecast information

Use the forecast to answer questions such as:
- "Can I go now?"
- "What about later?"
- "Will it be better at 9 PM?"
- "Should I wait?"
- "When is a better time?"

If a later supplied forecast has lower risk than the current
period, explain that clearly.

If the supplied forecast does not establish a better time,
say that the available data does not show a clearly better
period.

============================================================
USER
============================================================

Name:
{user_name if user_name else "Not provided"}

City:
{city}

Activity:
{activity}

Current question:
{message}

============================================================
CURRENT WEATHER
============================================================

Condition:
{_safe_text(normalized_weather["condition"], "Unknown")}

Temperature:
{_format_number(normalized_weather["temperature_c"])} °C

Feels like:
{_format_number(normalized_weather["feels_like_c"])} °C

Humidity:
{_format_number(normalized_weather["humidity_percent"], 0)} %

Wind:
{_format_number(normalized_weather["wind_speed_kmh"])} km/h

Rainfall:
{_format_number(normalized_weather["rainfall_mm"])} mm

Visibility:
{_format_number(normalized_weather["visibility_km"])} km

============================================================
RISK
============================================================

{risk_context}

============================================================
HOURLY FORECAST
============================================================

{hourly_context}

============================================================
CONVERSATION HISTORY
============================================================

{conversation_context}

============================================================
ANSWER STYLE
============================================================

Answer the user's actual question directly first.

Then provide a short explanation using the supplied
weather and risk information.

Be personalized to:
- city
- activity
- current conditions
- forecast
- user's preferences
- previous conversation

Do not mention internal implementation.

Keep the answer concise but useful.
""".strip()


# ============================================================
# GEMINI GENERATION
# ============================================================

def _generate_with_gemini(
    prompt: str,
) -> str:
    """Send a prompt to Gemini."""

    client = _get_gemini_client()

    model_name = _get_gemini_model()

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.4,
            max_output_tokens=900,
        ),
    )

    text = getattr(
        response,
        "text",
        None,
    )

    if not text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()


# ============================================================
# PUBLIC: ONE-SHOT EXPLANATION
# ============================================================

def generate_weather_explanation(
    city: str,
    activity: str,
    weather: dict[str, Any],
    risk: dict[str, Any],
    decision: dict[str, Any],
    hourly_forecast: list[dict[str, Any]] | None = None,
    preferences: dict[str, Any] | None = None,
) -> str:
    """
    Generate a personalized WeatherGPT explanation.
    """

    city = (
        city.strip()
        if isinstance(city, str) and city.strip()
        else "Unknown location"
    )

    activity = (
        activity.strip()
        if isinstance(activity, str) and activity.strip()
        else "General"
    )

    if not isinstance(weather, dict):
        raise ValueError(
            "Weather data must be a dictionary."
        )

    if not isinstance(risk, dict):
        raise ValueError(
            "Risk data must be a dictionary."
        )

    if not isinstance(decision, dict):
        raise ValueError(
            "Decision data must be a dictionary."
        )

    prompt = _build_prompt(
        city=city,
        activity=activity,
        weather=weather,
        risk=risk,
        decision=decision,
        hourly_forecast=hourly_forecast,
        preferences=preferences,
    )

    return _generate_with_gemini(
        prompt
    )


# ============================================================
# PUBLIC: CONVERSATIONAL WEATHERGPT
# ============================================================

def chat_with_weather_context(
    message: str,
    city: str,
    activity: str = "General",
    weather: dict[str, Any] | None = None,
    hourly_forecast: list[dict[str, Any]] | None = None,
    risk: dict[str, Any] | None = None,
    decision: dict[str, Any] | None = None,
    preferences: dict[str, Any] | None = None,
    conversation_history: list[dict[str, Any]] | None = None,
    conversation_id: str | None = None,
) -> tuple[str, str]:
    """
    Generate a conversational WeatherGPT response using
    current weather, hourly forecast, risk window,
    user preferences and short-term conversation context.
    """

    if not isinstance(message, str) or not message.strip():
        raise ValueError(
            "Chat message cannot be empty."
        )

    city = (
        city.strip()
        if isinstance(city, str) and city.strip()
        else "Unknown location"
    )

    activity = (
        activity.strip()
        if isinstance(activity, str) and activity.strip()
        else "General"
    )

    weather = (
        weather
        if isinstance(weather, dict)
        else {}
    )

    risk = (
        risk
        if isinstance(risk, dict)
        else {}
    )

    decision = (
        decision
        if isinstance(decision, dict)
        else {}
    )

    # Create a new conversation ID when needed.
    if not conversation_id:
        import uuid

        conversation_id = str(uuid.uuid4())

    # Load previous conversation context.
    conversation_history = conversation_store.get(
        conversation_id
    )

    # Build prompt using current weather, risk,
    # forecast and previous conversation.
    prompt = _build_chat_prompt(
        message=message.strip(),
        city=city,
        activity=activity,
        weather=weather,
        hourly_forecast=hourly_forecast,
        risk=risk,
        decision=decision,
        preferences=preferences,
        conversation_history=conversation_history,
    )

    # Ask Gemini for the response.
    reply = _generate_with_gemini(prompt)

    # Store the new conversation turn.
    conversation_store.add(
        conversation_id,
        "user",
        message.strip(),
    )

    conversation_store.add(
        conversation_id,
        "assistant",
        reply,
    )

    return reply, conversation_id