"""
Official warning risk processing for WeatherGPT.

This module converts warning information from an authoritative
source such as IMD into a project-level risk contribution.

It does NOT generate or claim official warnings.
"""


WARNING_COLOR_SCORES = {
    "Green": 0,
    "Yellow": 15,
    "Orange": 30,
    "Red": 40,
}


def calculate_warning_risk(
    warning_color: str | None,
) -> float:
    """
    Convert an official warning color into a project-generated
    risk contribution.

    These scores are internal WeatherGPT values and are NOT
    official IMD risk scores.
    """

    if not warning_color:
        return 0.0

    normalized_color = warning_color.strip().title()

    return float(
        WARNING_COLOR_SCORES.get(
            normalized_color,
            0,
        )
    )


def get_warning_priority(
    warning_color: str | None,
) -> str:
    """
    Convert warning color into an internal priority label.
    """

    if not warning_color:
        return "None"

    normalized_color = warning_color.strip().title()

    priority = {
        "Green": "Low",
        "Yellow": "Moderate",
        "Orange": "High",
        "Red": "Very High",
    }

    return priority.get(
        normalized_color,
        "Unknown",
    )