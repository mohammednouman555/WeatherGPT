class AlertDecisionService:

    RISK_MESSAGES = {
        "Low": {
            "title": "Low Weather Risk",
            "message": (
                "Weather conditions are generally suitable "
                "for your activity."
            ),
            "priority": "Low",
        },
        "Moderate": {
            "title": "Moderate Weather Risk",
            "message": (
                "Weather conditions may affect your activity. "
                "Exercise caution."
            ),
            "priority": "Medium",
        },
        "High": {
            "title": "High Weather Risk",
            "message": (
                "Weather conditions may significantly affect "
                "your activity. Consider delaying or modifying "
                "your plans."
            ),
            "priority": "High",
        },
        "Severe": {
            "title": "Severe Weather Risk",
            "message": (
                "Weather conditions are potentially dangerous. "
                "Avoid the activity if possible."
            ),
            "priority": "Critical",
        },
    }

    HAZARD_MESSAGES = {
        "Rain": (
            "Rain may affect visibility, road conditions, "
            "and travel safety."
        ),
        "Thunderstorm": (
            "Thunderstorms may involve lightning, strong "
            "winds, and sudden heavy rain."
        ),
        "Heat": (
            "High temperatures may cause heat stress "
            "and discomfort."
        ),
        "Wind": (
            "Strong winds may make outdoor activities "
            "and travel more difficult."
        ),
        "Fog": (
            "Reduced visibility may make travel hazardous."
        ),
        "Snow": (
            "Snow and icy conditions may affect travel "
            "and outdoor activities."
        ),
        "Dust": (
            "Dusty conditions may reduce visibility "
            "and affect air quality."
        ),
    }

    def generate_decision(
        self,
        risk_result: dict,
    ) -> dict:

        risk_level = risk_result.get(
            "peak_risk_level",
            "Low",
        )

        peak_risk = risk_result.get(
            "peak_risk",
            0,
        )

        peak_hazard = risk_result.get(
            "peak_hazard",
            "None",
        )

        risk_info = self.RISK_MESSAGES.get(
            risk_level,
            self.RISK_MESSAGES["Low"],
        )

        hazard_message = self.HAZARD_MESSAGES.get(
            peak_hazard,
            "",
        )

        recommendation = risk_info["message"]

        if hazard_message:
            recommendation = (
                f"{recommendation} {hazard_message}"
            )

        return {
            "risk_level": risk_level,
            "risk_score": peak_risk,
            "hazard": peak_hazard,
            "title": risk_info["title"],
            "message": recommendation,
            "priority": risk_info["priority"],
        }