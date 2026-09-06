from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.risk_service import RiskService
from app.services.alert_decision_service import AlertDecisionService

from app.schemas.risk import CityRiskResponse


router = APIRouter(
    prefix="/api/risk",
    tags=["Risk"],
)


risk_service = RiskService()
alert_decision_service = AlertDecisionService()


@router.get(
    "/forecast",
    response_model=CityRiskResponse,
)
def get_forecast_risk(
    city: str,
    start_time: datetime,
    end_time: datetime,
    activity: str | None = None,
    db: Session = Depends(get_db),
):
    """
    Calculate weather risk for a city and
    requested forecast time window.
    """

    if end_time < start_time:
        raise HTTPException(
            status_code=400,
            detail=(
                "end_time must be greater than "
                "or equal to start_time."
            ),
        )

    try:

        result = risk_service.calculate_city_risk(
            city=city,
            start_time=start_time,
            end_time=end_time,
            db=db,
            activity=activity,
        )

        decision = alert_decision_service.generate_decision(
            risk_result=result["risk"]
        )

        result["decision"] = decision

        return result

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Risk calculation failed: {exc}",
        )