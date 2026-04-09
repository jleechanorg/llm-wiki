"""
Centralized numeric conversion utilities.

Provides safe type coercion functions to handle various input types (str, float, bool)
and guard against edge cases like NaN and Infinity.
"""

from typing import Any


def coerce_int_safe(value: Any, default: int | None = 0) -> int | None:
    """
    Safely coerce value to int.

    Handles string numbers from JSON/LLM responses, floats, and booleans.
    Guards against NaN (ValueError) and Infinity (OverflowError).

    Args:
        value: The value to coerce (int, str, float, bool, or other)
        default: Default value if coercion fails (can be None)

    Returns:
        Integer value or default
    """
    if value is None:
        return default
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, bool):
        return int(value)
    try:
        return int(float(value))
    except (ValueError, TypeError, OverflowError):
        return default
