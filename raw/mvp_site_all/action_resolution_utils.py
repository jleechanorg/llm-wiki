"""Helper functions for action_resolution/outcome_resolution handling.

Centralizes the logic for accessing and building action_resolution/outcome_resolution
fields across llm_response.py and world_logic.py to eliminate duplication.
"""

from typing import Any


def extract_dice_rolls_from_action_resolution(
    action_resolution: dict[str, Any],
) -> list[str]:
    """Extract and format dice rolls from action_resolution.mechanics.rolls.

    Converts structured roll objects from action_resolution.mechanics.rolls
    into formatted strings for the legacy dice_rolls field (for UI display).

    Format: "notation = total (purpose)" or "notation = total vs DC dc - Success/Failure (purpose)"

    Args:
        action_resolution: action_resolution dict (may be empty)

    Returns:
        list[str]: Formatted dice roll strings, empty list if no rolls found
    """
    if not action_resolution or not isinstance(action_resolution, dict):
        return []

    mechanics = action_resolution.get("mechanics", {})
    if not isinstance(mechanics, dict):
        return []

    rolls = mechanics.get("rolls", [])
    if not isinstance(rolls, list):
        return []

    formatted_rolls = []
    for roll in rolls:
        if not isinstance(roll, dict):
            continue

        notation = roll.get("notation", "")
        result = roll.get("result")
        total = roll.get("total")
        purpose = roll.get("purpose", "")
        dc = roll.get("dc")
        success = roll.get("success")

        if not notation or (result is None and total is None):
            continue

        display_total = total if isinstance(total, int) else result

        # Format: "notation = total (purpose)"
        roll_str = f"{notation} = {display_total}"

        # Add DC and success/failure if present
        if dc is not None:
            roll_str += f" vs DC {dc}"
            if success is True:
                roll_str += " - Success"
            elif success is False:
                roll_str += " - Failure"

        # Add purpose if present
        if purpose:
            roll_str += f" ({purpose})"

        formatted_rolls.append(roll_str)

    return formatted_rolls


def extract_dice_audit_events_from_action_resolution(
    action_resolution: dict[str, Any],
) -> list[dict[str, Any]]:
    """Extract audit events from action_resolution.mechanics.audit_events.

    Args:
        action_resolution: action_resolution dict (may be empty)

    Returns:
        list[dict[str, Any]]: Audit event dicts, empty list if none found
    """
    if not action_resolution or not isinstance(action_resolution, dict):
        return []

    mechanics = action_resolution.get("mechanics", {})
    if not isinstance(mechanics, dict):
        return []

    audit_events = mechanics.get("audit_events", [])
    if isinstance(audit_events, list):
        dict_events = [event for event in audit_events if isinstance(event, dict)]
        if dict_events:
            return dict_events
        string_events = [event for event in audit_events if isinstance(event, str)]
        if string_events and not mechanics.get("rolls"):
            return [
                {
                    "source": "code_execution",
                    "label": event,
                    "notation": "",
                    "rolls": [],
                    "modifier": 0,
                    "total": None,
                }
                for event in string_events
            ]

    rolls = mechanics.get("rolls", [])
    if not isinstance(rolls, list):
        return []

    formatted_events: list[dict[str, Any]] = []
    for roll in rolls:
        if not isinstance(roll, dict):
            continue
        notation = roll.get("notation")
        if not notation:
            continue

        result = roll.get("result")
        total = roll.get("total")
        modifier = roll.get("modifier")
        raw_rolls = roll.get("rolls")

        if not isinstance(raw_rolls, list) or not raw_rolls:
            if isinstance(result, int):
                raw_rolls = [result]
            else:
                raw_rolls = []

        if modifier is None and isinstance(total, int) and isinstance(result, int):
            modifier = total - result
        if modifier is None:
            modifier = 0

        if total is None and isinstance(result, int) and isinstance(modifier, int):
            total = result + modifier

        event = {
            "source": roll.get("source") or "code_execution",
            "label": roll.get("label") or roll.get("purpose") or "Dice Roll",
            "notation": notation,
            "rolls": raw_rolls,
            "modifier": modifier,
            "total": total,
        }

        if roll.get("dc") is not None:
            event["dc"] = roll.get("dc")
        if roll.get("dc_reasoning") is not None:
            event["dc_reasoning"] = roll.get("dc_reasoning")
        if roll.get("success") is not None:
            event["success"] = roll.get("success")

        formatted_events.append(event)

    return formatted_events


def has_action_resolution_dice(action_resolution: dict[str, Any] | None) -> bool:
    """Return True if action_resolution.mechanics has rolls or audit_events."""
    if not action_resolution or not isinstance(action_resolution, dict):
        return False

    mechanics = action_resolution.get("mechanics", {})
    if not isinstance(mechanics, dict):
        return False

    rolls = mechanics.get("rolls", [])
    audit_events = mechanics.get("audit_events", [])
    return (isinstance(rolls, list) and len(rolls) > 0) or (
        isinstance(audit_events, list) and len(audit_events) > 0
    )


def normalize_action_resolution_rolls(action_resolution: dict[str, Any]) -> None:
    """Normalize action_resolution.mechanics.rolls in place.

    Normalizations:
    - Populate missing totals from result or rolls when possible
    - Map 'label' to 'purpose' for frontend compatibility (frontend expects 'purpose')
    """
    if not action_resolution or not isinstance(action_resolution, dict):
        return
    mechanics = action_resolution.get("mechanics", {})
    if not isinstance(mechanics, dict):
        return
    rolls = mechanics.get("rolls", [])
    if not isinstance(rolls, list):
        return

    for roll in rolls:
        if not isinstance(roll, dict):
            continue

        # Normalize label -> purpose for frontend compatibility
        # The frontend expects 'purpose' but code execution may produce 'label'
        if roll.get("label") and not roll.get("purpose"):
            roll["purpose"] = roll["label"]

        # Populate missing total from result
        if roll.get("total") is not None:
            continue

        result = roll.get("result")
        if isinstance(result, int):
            roll["total"] = result
            continue

        raw_rolls = roll.get("rolls")
        modifier = roll.get("modifier")
        if isinstance(raw_rolls, list) and raw_rolls and isinstance(modifier, int):
            roll_sum = sum(r for r in raw_rolls if isinstance(r, int))
            roll["total"] = roll_sum + modifier


def get_action_resolution(structured_response: Any) -> dict[str, Any]:
    """Get action_resolution from structured response with backward compat fallback.

    Checks action_resolution first (new field), falls back to outcome_resolution
    (legacy field) for backward compatibility.

    Args:
        structured_response: NarrativeResponse object or any object with action_resolution/outcome_resolution attributes

    Returns:
        dict: action_resolution dict, or empty dict if neither field present
    """
    if structured_response is None:
        return {}

    # Check action_resolution first (new field)
    if hasattr(structured_response, "action_resolution"):
        ar = structured_response.action_resolution
        # Use is not None to preserve empty dict {} as present
        if ar is not None:
            return ar

    # Fall back to outcome_resolution for backward compatibility
    if hasattr(structured_response, "outcome_resolution"):
        or_val = structured_response.outcome_resolution
        if or_val is not None:
            return or_val

    return {}


def get_outcome_resolution(structured_response: Any) -> dict[str, Any]:
    """Get outcome_resolution from structured response (backward compat accessor).

    Direct accessor for outcome_resolution field. Returns empty dict if not present.

    Args:
        structured_response: NarrativeResponse object or any object with outcome_resolution attribute

    Returns:
        dict: outcome_resolution dict, or empty dict if not present
    """
    if structured_response is None:
        return {}

    if hasattr(structured_response, "outcome_resolution"):
        or_val = structured_response.outcome_resolution
        return or_val or {}

    return {}


def add_action_resolution_to_response(
    structured_response: Any, unified_response: dict[str, Any]
) -> None:
    """Add action_resolution and outcome_resolution to unified_response dict.

    Adds both fields to the unified_response dict for API responses.
    Handles type coercion (ensures dict type) and None values (skips them).

    Args:
        structured_response: NarrativeResponse object or any object with action_resolution/outcome_resolution attributes
        unified_response: Dict to add fields to (modified in place)
    """
    if structured_response is None:
        return

    # Include action_resolution (primary field name)
    action_resolution_dict = None
    if hasattr(structured_response, "action_resolution"):
        action_resolution = getattr(structured_response, "action_resolution", None)
        if action_resolution is not None:
            action_resolution_dict = (
                action_resolution if isinstance(action_resolution, dict) else {}
            )
            unified_response["action_resolution"] = action_resolution_dict

    # Keep outcome_resolution for backward compatibility
    if hasattr(structured_response, "outcome_resolution"):
        outcome_resolution = getattr(structured_response, "outcome_resolution", None)
        if outcome_resolution is not None:
            unified_response["outcome_resolution"] = (
                outcome_resolution if isinstance(outcome_resolution, dict) else {}
            )
            # Also try to extract from outcome_resolution if action_resolution not present
            if action_resolution_dict is None:
                action_resolution_dict = (
                    outcome_resolution if isinstance(outcome_resolution, dict) else {}
                )
                unified_response["action_resolution"] = action_resolution_dict

    if action_resolution_dict:
        normalize_action_resolution_rolls(action_resolution_dict)
