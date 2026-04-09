"""
General-purpose utility functions for mvp_site.

File Protocol (for modifications in this file)
- GOAL: Introduce a tiny arithmetic helper `add_safe` that performs
  defensive addition across ints, floats, and numeric strings,
  returning a caller-provided default on invalid inputs.
- MODIFICATION: Add `add_safe` alongside existing utilities;
  keep behavior minimal and predictable.
- NECESSITY: Many call sites work with numeric-like data. Centralizing
  safe addition reduces duplication and edge-case bugs.
- INTEGRATION PROOF: Tests live in `mvp_site/tests/test_utils.py` and
  import from this module. The helper complements
  `normalize_status_code` in scope and style.
"""

from typing import Any
import math


def normalize_status_code(value: Any, default: int = 200) -> int:
    """
    Coerce value to a valid HTTP status code integer (100-599).

    Accepts int, float, or numeric string. Returns default when the
    value is missing, non-numeric, or outside the valid 100-599 range.

    Args:
        value: The value to normalize (int, str, or other).
        default: Fallback integer when normalization fails (default: 200).

    Returns:
        A valid HTTP status code integer, or ``default`` on failure.

    Examples:
        >>> normalize_status_code(404)
        404
        >>> normalize_status_code("500")
        500
        >>> normalize_status_code(None)
        200
        >>> normalize_status_code("bad", default=503)
        503
    """
    if value is None:
        return default
    try:
        code = int(value)
    except (ValueError, TypeError):
        return default
    if 100 <= code <= 599:
        return code
    return default


def add_safe(a: Any, b: Any, *, default: float | int = 0) -> float | int:
    """
    Safely add two numeric-like values with defensive coercion.

    Accepts ints, floats, and numeric strings (e.g., "2", "2.5").
    Returns ``default`` when either input is ``None`` or cannot be
    interpreted as a finite number. If both inputs are integral after
    coercion, returns an ``int``; otherwise returns a ``float``.

    Args:
        a: First addend (int|float|str or numeric-like).
        b: Second addend (int|float|str or numeric-like).
        default: Value to return when coercion/validation fails.

    Returns:
        int if both inputs are integral post-coercion, else float. ``default`` on error.

    Examples:
        >>> add_safe(2, 3)
        5
        >>> add_safe("2", "3")
        5
        >>> add_safe(0.1, 0.2)
        0.30000000000000004
        >>> add_safe("bad", 1, default=999)
        999
    """

    def _to_number(x: Any) -> float | int:
        # Explicit None check
        if x is None:
            raise ValueError("None is not numeric")

        # Fast path for plain numbers (avoid treating bool as int)
        if isinstance(x, (int, float)) and not isinstance(x, bool):
            return x

        # Strings: try int first (for type preservation), then float
        if isinstance(x, str):
            s = x.strip()
            if s == "":
                raise ValueError("empty string")
            try:
                # If it looks like an integer, prefer int
                if not any(ch in s.lower() for ch in (".", "e")):
                    return int(s)
            except (ValueError, TypeError):
                pass
            # Fallback to float for decimals/scientific notation
            return float(s)

        # Other types (e.g., numpy numerics) — attempt float(x)
        return float(x)

    try:
        a_num = _to_number(a)
        b_num = _to_number(b)

        # Validate finiteness
        a_finite = (math.isfinite(a_num) if isinstance(a_num, float) else True)
        b_finite = (math.isfinite(b_num) if isinstance(b_num, float) else True)
        if not (a_finite and b_finite):
            return default

        # Type: keep int if both are int; else float
        if isinstance(a_num, int) and isinstance(b_num, int):
            return a_num + b_num
        return float(a_num) + float(b_num)
    except Exception:
        return default
