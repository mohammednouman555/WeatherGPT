from typing import Any

from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse, WeatherExplanationRequest
from app.services.conversation_service import conversation_store
from app.services.llm_service import chat_with_weather_context, generate_weather_explanation


router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("/explain")
def explain_weather(request: WeatherExplanationRequest):
    """Backward-compatible one-shot WeatherGPT explanation endpoint."""
    try:
        explanation = generate_weather_explanation(
            city=request.city,
            activity=request.activity,
            weather=request.weather,
            risk=request.risk,
            decision=request.decision,
            hourly_forecast=request.hourly_forecast,
            preferences=request.preferences.model_dump(),
        )
        return {
            "success": True,
            "city": request.city,
            "activity": request.activity,
            "explanation": explanation,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"LLM service error: {exc}") from exc


@router.post("/message", response_model=ChatResponse)
def chat_message(request: ChatRequest):
    """Conversational WeatherGPT endpoint with short-term context."""
    try:
        reply, conversation_id = chat_with_weather_context(
            message=request.message,
            city=request.city,
            activity=request.activity,
            weather=request.weather,
            hourly_forecast=request.hourly_forecast,
            risk=request.risk,
            decision=request.decision,
            preferences=request.preferences.model_dump(),
            conversation_id=request.conversation_id,
        )
        return ChatResponse(
            conversation_id=conversation_id,
            city=request.city,
            activity=request.activity,
            reply=reply,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"LLM service error: {exc}") from exc


@router.delete("/conversation/{conversation_id}")
def clear_conversation(conversation_id: str):
    conversation_store.clear(conversation_id)
    return {"success": True, "conversation_id": conversation_id}
