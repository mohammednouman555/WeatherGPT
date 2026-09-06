class ActivityContextService:

    ACTIVITY_CONTEXT = {
        "bike": {
            "name": "bike_travel",
            "description": "Motorbike travel",
        },
        "walking": {
            "name": "walking",
            "description": "Walking outdoors",
        },
        "run": {
            "name": "running",
            "description": "Running outdoors",
        },
        "cycling": {
            "name": "cycling",
            "description": "Cycling outdoors",
        },
        "travel": {
            "name": "general_travel",
            "description": "General outdoor travel",
        },
        "outdoor": {
            "name": "outdoor_activity",
            "description": "General outdoor activity",
        },
    }

    ACTIVITY_RISK_FACTORS = {
        "bike": {
            "rain": 1.5,
            "wind": 1.4,
            "heat": 1.2,
            "visibility": 1.6,
        },
        "walking": {
            "rain": 1.2,
            "wind": 1.0,
            "heat": 1.3,
            "visibility": 1.2,
        },
        "run": {
            "rain": 1.2,
            "wind": 1.1,
            "heat": 1.6,
            "visibility": 1.1,
        },
        "cycling": {
            "rain": 1.5,
            "wind": 1.5,
            "heat": 1.3,
            "visibility": 1.5,
        },
        "travel": {
            "rain": 1.4,
            "wind": 1.3,
            "heat": 1.1,
            "visibility": 1.6,
        },
        "outdoor": {
            "rain": 1.2,
            "wind": 1.1,
            "heat": 1.3,
            "visibility": 1.2,
        },
    }

    DEFAULT_FACTORS = {
        "rain": 1.0,
        "wind": 1.0,
        "heat": 1.0,
        "visibility": 1.0,
    }

    def get_activity_context(
        self,
        activity: str | None,
    ) -> dict:

        if not activity:
            return {
                "name": "general_activity",
                "description": "General activity",
                "context_risk": 0.0,
            }

        activity_key = activity.strip().lower()

        context = self.ACTIVITY_CONTEXT.get(
            activity_key,
            {
                "name": activity_key,
                "description": "General activity",
            },
        )

        factors = self.ACTIVITY_RISK_FACTORS.get(
            activity_key,
            self.DEFAULT_FACTORS,
        )

        return {
            "name": context["name"],
            "description": context["description"],
            "context_risk": 0.0,
            "risk_factors": factors,
        }

    def calculate_context_risk(
        self,
        activity: str | None,
        rain_risk: float,
        wind_risk: float,
        heat_risk: float,
        visibility_risk: float,
    ) -> float:

        context = self.get_activity_context(activity)

        factors = context.get(
            "risk_factors",
            self.DEFAULT_FACTORS,
        )

        weighted_risk = (
            rain_risk * factors["rain"]
            + wind_risk * factors["wind"]
            + heat_risk * factors["heat"]
            + visibility_risk * factors["visibility"]
        )

        return round(weighted_risk, 2)