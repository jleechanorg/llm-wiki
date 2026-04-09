from __future__ import annotations

from typing import Any

from mvp_site import constants, world_time


def evaluate_living_world_trigger(
    *,
    current_turn: int,
    last_turn: int,
    last_time: dict[str, Any] | None,
    current_time: dict[str, Any] | None,
    turn_interval: int = constants.LIVING_WORLD_TURN_INTERVAL,
    time_interval: int = constants.LIVING_WORLD_TIME_INTERVAL,
) -> tuple[bool, str, float | None]:
    """Evaluate living world trigger based on turn or elapsed time.

    Returns:
        tuple: (should_trigger, reason_string, hours_elapsed)
    """
    normalized_last_turn = last_turn
    if normalized_last_turn < 0:
        normalized_last_turn = 0
    elif normalized_last_turn > current_turn:
        # Corrupt/stale tracking can put last_turn ahead of current_turn.
        # Realign to the most recent interval boundary to recover cadence.
        normalized_last_turn = current_turn - (current_turn % turn_interval)
        if normalized_last_turn == current_turn and current_turn > 0:
            normalized_last_turn = max(0, current_turn - turn_interval)

    # Use modulo for turn-based triggers to ensure consistent schedule (turns 3, 6, 9, etc.)
    # This prevents time-based triggers from disrupting the turn-based schedule
    # Also ensure we only trigger once per turn by checking current_turn > normalized_last_turn
    turn_trigger = (
        (current_turn % turn_interval == 0)
        and (current_turn > 0)
        and (current_turn > normalized_last_turn)
    )

    time_trigger = False
    hours_elapsed = None

    if isinstance(last_time, dict) and isinstance(current_time, dict):
        hours_elapsed = world_time.calculate_hours_elapsed(last_time, current_time)
        if hours_elapsed is not None and hours_elapsed >= time_interval:
            time_trigger = True

    # Calculate turns_since_last for reason string
    turns_since_last = current_turn - normalized_last_turn

    trigger_reason = "unknown"
    if turn_trigger and time_trigger:
        trigger_reason = (
            f"turn_and_time ({turns_since_last} turns, {hours_elapsed:.1f}h)"
        )
    elif turn_trigger:
        trigger_reason = f"turn ({turns_since_last} turns)"
    elif time_trigger:
        trigger_reason = f"time ({hours_elapsed:.1f}h elapsed)"

    return (turn_trigger or time_trigger), trigger_reason, hours_elapsed
