from datetime import datetime

from pydantic import BaseModel


class HourlyRiskItem(BaseModel):
    forecast_time: datetime
    overall_risk: float
    risk_level: str

    rain_risk: float
    wind_risk: float
    heat_risk: float
    visibility_risk: float

    weather_condition: str
    weather_hazard: str
    weather_severity: int

    warning_color: str | None
    warning_risk: float
    warning_priority: str

    activity: str
    activity_description: str
    context_risk: float


class RiskWindowResponse(BaseModel):
    start_time: datetime
    end_time: datetime

    hours_analyzed: int

    average_risk: float
    peak_risk: float
    peak_risk_level: str

    peak_risk_time: datetime

    risk_trend: str

    peak_hazard: str
    peak_hazard_value: float
    peak_hazard_time: datetime

    hourly_results: list[HourlyRiskItem]


class RiskLocationResponse(BaseModel):
    name: str
    district: str | None
    state: str | None
    country: str
    latitude: float
    longitude: float


class AlertDecisionResponse(BaseModel):
    risk_level: str
    risk_score: float
    hazard: str
    title: str
    message: str
    priority: str


class CityRiskResponse(BaseModel):
    location: RiskLocationResponse
    activity: str | None
    risk: RiskWindowResponse
    decision: AlertDecisionResponse