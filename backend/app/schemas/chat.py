from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class UserPreferences(BaseModel):
    name: str = Field(default="", max_length=100)
    preferred_activities: list[str] = Field(default_factory=list, max_length=10)
    language: str = Field(default="en", max_length=20)


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    conversation_id: str | None = Field(default=None, max_length=100)
    city: str = Field(default="", max_length=150)
    activity: str = Field(default="General", max_length=50)
    weather: dict[str, Any] = Field(default_factory=dict)
    hourly_forecast: list[dict[str, Any]] = Field(default_factory=list, max_length=48)
    risk: dict[str, Any] = Field(default_factory=dict)
    decision: dict[str, Any] = Field(default_factory=dict)
    preferences: UserPreferences = Field(default_factory=UserPreferences)


class ChatResponse(BaseModel):
    success: bool = True
    conversation_id: str
    city: str
    activity: str
    reply: str


class WeatherExplanationRequest(BaseModel):
    city: str = Field(..., min_length=1, max_length=150)
    activity: str = Field(default="General", max_length=50)
    weather: dict[str, Any] = Field(default_factory=dict)
    hourly_forecast: list[dict[str, Any]] = Field(default_factory=list, max_length=48)
    risk: dict[str, Any] = Field(default_factory=dict)
    decision: dict[str, Any] = Field(default_factory=dict)
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    conversation_id: str | None = Field(default=None, max_length=100)
