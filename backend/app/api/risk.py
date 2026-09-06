import logging

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.risk_service import RiskService
from app.services.alert_decision_service import AlertDecisionService

from app.schemas.risk import CityRiskResponse


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Router
# ---------------------------------------------------------

router = APIRouter(
    prefix="/api/risk",
    tags=["Risk"],
)


# ---------------------------------------------------------
# Services
# ---------------------------------------------------------

risk_service = RiskService()
alert_decision_service = AlertDecisionService()


# =========================================================
# RISK FORECAST
# =========================================================

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

    logger.info(
        "Risk request received: city=%s, start=%s, end=%s, activity=%s",
        city,
        start_time,
        end_time,
        activity,
    )

    # -----------------------------------------------------
    # Validate time range
    # -----------------------------------------------------

    if end_time < start_time:
        raise HTTPException(
            status_code=400,
            detail=(
                "end_time must be greater than "
                "or equal to start_time."
            ),
        )

    try:

        # -------------------------------------------------
        # Calculate risk
        # -------------------------------------------------

        result = risk_service.calculate_city_risk(
            city=city,
            start_time=start_time,
            end_time=end_time,
            db=db,
            activity=activity,
        )

        logger.info(
            "Risk calculation completed successfully for '%s'",
            city,
        )

        # -------------------------------------------------
        # Generate decision
        # -------------------------------------------------

        decision = alert_decision_service.generate_decision(
            risk_result=result["risk"]
        )

        result["decision"] = decision

        logger.info(
            "Risk decision generated successfully for '%s'",
            city,
        )

        # -------------------------------------------------
        # Return response
        # -------------------------------------------------

        return result

    except ValueError as exc:
        db.rollback()

        logger.warning(
            "Invalid risk request for '%s': %s",
            city,
            exc,
        )

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except SQLAlchemyError as exc:
        db.rollback()

        logger.exception(
            "DATABASE ERROR during risk calculation for '%s'",
            city,
        )

        raise HTTPException(
            status_code=500,
            detail="Database error while calculating weather risk.",
        )

    except KeyError as exc:
        db.rollback()

        logger.exception(
            "RISK RESULT ERROR for '%s'. Missing key: %s",
            city,
            exc,
        )

        raise HTTPException(
            status_code=500,
            detail="Invalid risk calculation result.",
        )

    except Exception as exc:
        db.rollback()

        logger.exception(
            "RISK CALCULATION ERROR for '%s': %s",
            city,
            exc,
        )

        raise HTTPException(
            status_code=500,
            detail="Risk calculation failed.",
        )