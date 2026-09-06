"""
IMD warning interpretation utilities.

This module contains pure functions only.
It does not perform network requests.
"""

WARNING_CODES: dict[int, str] = {
    1: "No Warning",
    2: "Heavy Rain",
    3: "Heavy Snow",
    4: "Thunderstorm & Lightning, Squall etc",
    5: "Hailstorm",
    6: "Dust Storm",
    7: "Dust Raising Winds",
    8: "Strong Surface Winds",
    9: "Heat Wave",
    10: "Hot Day",
    11: "Warm Night",
    12: "Cold Wave",
    13: "Cold Day",
    14: "Ground Frost",
    15: "Fog",
    16: "Very Heavy Rain",
    17: "Extremely Heavy Rain",
}


COLOR_CODES: dict[int, str] = {
    1: "Red",
    2: "Orange",
    3: "Yellow",
    4: "Green",
}


def interpret_warning_code(code: int | None) -> str:
    """
    Convert an IMD warning code into a human-readable description.
    """

    if code is None:
        return "No Warning"

    return WARNING_CODES.get(
        code,
        "Unknown Warning",
    )


def interpret_color_code(code: int | None) -> str:
    """
    Convert an IMD numeric colour code into its official colour.
    """

    if code is None:
        return "Unknown"

    return COLOR_CODES.get(
        code,
        "Unknown",
    )


def normalize_warning_color(
    color: str | None,
) -> str | None:
    """
    Normalize an externally supplied warning colour.
    """

    if color is None:
        return None

    normalized = color.strip().title()

    if normalized not in {
        "Green",
        "Yellow",
        "Orange",
        "Red",
    }:
        raise ValueError(
            "warning_color must be one of: "
            "Green, Yellow, Orange, Red."
        )

    return normalized