"""Utility helpers for extracting structured Gemini response fields."""

from __future__ import annotations

import json
from typing import Any, TypeVar

from mvp_site import constants
from mvp_site.action_resolution_utils import (
    get_action_resolution,
    get_outcome_resolution,
)

T = TypeVar("T")


def _get_structured_attr(
    structured_response: Any,
    field_name: str,
    default: T,
    *,
    treat_falsy_as_default: bool = False,
) -> T:
    """Return a structured response attribute or a typed default.

    Gemini can omit fields entirely or explicitly set them to ``None``. We coerce
    ``None`` back to the supplied ``default`` so callers always receive the
    expected type (``str``/``list``/``dict``). ``getattr`` handles the case where
    the attribute does not exist; we only need to guard the ``None`` sentinel.
    """

    value = getattr(structured_response, field_name, default)
    if value is None or (treat_falsy_as_default and not value):
        return default
    return value


def _summarize_mapping(
    value: dict[str, Any], *, sample_limit: int = 20
) -> dict[str, Any]:
    keys = list(value.keys())
    return {"_count": len(keys), "_sample_keys": keys[:sample_limit]}


def _audit_trim_state_update(key: str, value: Any) -> Any:
    """Trim large state_update values to reduce risk of oversized Firestore writes."""
    if key in {"item_registry", "npc_data"} and isinstance(value, dict):
        return _summarize_mapping(value)

    if key in {"combat_state", "encounter_state"} and isinstance(value, dict):
        # Keep a small slice of useful debugging fields plus a key summary.
        keep_keys = {
            "combat_phase",
            "phase",
            "round",
            "turn_index",
            "active_actor_id",
            "encounter_id",
        }
        trimmed = {
            k: v
            for k, v in value.items()
            if k in keep_keys and v not in (None, {}, [], "")
        }
        trimmed.update(_summarize_mapping(value))
        return trimmed

    if key == "player_character_data" and isinstance(value, dict):
        keep_keys = {
            "name",
            "character_name",
            "class",
            "character_class",
            "race",
            "background",
            "level",
            "stats",
            "spells",
            "spell_slots",
            "equipment",
            "inventory",
            "weapons",
        }
        return {
            k: v
            for k, v in value.items()
            if k in keep_keys and v not in (None, {}, [], "")
        }

    return value


_LARGE_CUSTOM_KEYS = frozenset({"story_history"})


def _trim_custom_campaign_state(custom: dict[str, Any]) -> dict[str, Any]:
    """Return custom_campaign_state with known-large fields excluded."""
    return {k: v for k, v in custom.items() if k not in _LARGE_CUSTOM_KEYS}


def _build_traceability_fields(state_updates: dict[str, Any]) -> dict[str, Any]:
    """Build full_state_updates + core_memories_snapshot for per-entry traceability.

    These fields are stored alongside the filtered LW subset so downstream
    consumers can reconstruct full context without reading game_states/current_state.
    story_history is excluded from full_state_updates to stay under the Firestore
    1 MB document limit.
    """
    trimmed = dict(state_updates)
    if isinstance(trimmed.get("custom_campaign_state"), dict):
        trimmed["custom_campaign_state"] = _trim_custom_campaign_state(
            trimmed["custom_campaign_state"]
        )
    fields: dict[str, Any] = {"full_state_updates": trimmed}
    custom = state_updates.get("custom_campaign_state", {})
    if isinstance(custom, dict) and custom.get("core_memories"):
        fields["core_memories_snapshot"] = custom["core_memories"]
    return fields


def _build_state_updates_audit_subset(state_updates: dict[str, Any]) -> dict[str, Any]:
    audit_keys = {
        "custom_campaign_state",
        "player_character_data",
        "item_registry",
        "npc_data",
        "combat_state",
        "encounter_state",
        "rewards_pending",
    }
    audit_subset: dict[str, Any] = {}
    for key in audit_keys:
        if key not in state_updates:
            continue
        value = state_updates.get(key)
        if value in (None, {}, []):
            continue
        audit_subset[key] = _audit_trim_state_update(key, value)
    return audit_subset


def _normalize_resources_for_story_entry(value: Any) -> str:
    """Normalize resources to the StoryEntry contract type (string)."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (dict, list)):
        try:
            return json.dumps(value, ensure_ascii=False, sort_keys=True)
        except (TypeError, ValueError):
            return str(value)
    return str(value)


def extract_structured_fields(gemini_response_obj: Any) -> dict[str, Any]:  # noqa: PLR0912, PLR0915
    """Extract structured fields from a LLMResponse-like object."""

    structured_fields: dict[str, Any] = {}

    sr = getattr(gemini_response_obj, "structured_response", None)
    if sr is not None:
        structured_fields = {
            constants.FIELD_SESSION_HEADER: _get_structured_attr(
                sr, constants.FIELD_SESSION_HEADER, ""
            ),
            constants.FIELD_PLANNING_BLOCK: _get_structured_attr(
                sr, constants.FIELD_PLANNING_BLOCK, ""
            ),
            constants.FIELD_DICE_ROLLS: _get_structured_attr(
                sr, constants.FIELD_DICE_ROLLS, []
            ),
            constants.FIELD_DICE_AUDIT_EVENTS: _get_structured_attr(
                sr, constants.FIELD_DICE_AUDIT_EVENTS, []
            ),
            constants.FIELD_RESOURCES: _normalize_resources_for_story_entry(
                _get_structured_attr(
                    sr, constants.FIELD_RESOURCES, "", treat_falsy_as_default=True
                )
            ),
            constants.FIELD_DEBUG_INFO: _get_structured_attr(
                sr, constants.FIELD_DEBUG_INFO, {}
            ),
            constants.FIELD_GOD_MODE_RESPONSE: _get_structured_attr(
                sr, constants.FIELD_GOD_MODE_RESPONSE, ""
            ),
            constants.FIELD_DIRECTIVES: _get_structured_attr(
                sr, constants.FIELD_DIRECTIVES, {}
            ),
        }

        # Extract action_resolution and outcome_resolution for audit trail persistence.
        # Always include even if empty for Firestore consistency.
        action_resolution = get_action_resolution(sr)

        # Backward compatibility: If action_resolution is empty but dice_rolls contains structured data,
        # canonicalize it into action_resolution format.
        # This handles legacy Think Mode responses that may have used dice_rolls directly before consolidation.
        raw_rolls = structured_fields.get(constants.FIELD_DICE_ROLLS, [])
        if (
            not action_resolution
            and isinstance(raw_rolls, list)
            and raw_rolls
            and isinstance(raw_rolls[0], dict)
        ):
            converted_rolls = []
            for roll in raw_rolls:
                # Map Think Mode fields to action_resolution schema
                # roll -> notation, type -> purpose
                if isinstance(roll, dict):
                    converted_rolls.append(
                        {
                            "notation": roll.get("roll"),
                            "result": roll.get("result"),
                            "dc": roll.get("dc"),
                            "success": roll.get("success"),
                            "purpose": roll.get("type"),
                            # Preserve Think Mode specific fields
                            "dc_category": roll.get("dc_category"),
                            "dc_reasoning": roll.get("dc_reasoning"),
                            "margin": roll.get("margin"),
                            "outcome": roll.get("outcome"),
                        }
                    )

            if converted_rolls:
                action_resolution = {
                    "mechanics": {
                        "rolls": converted_rolls,
                        "type": "planning_check",
                    }
                }

        if not isinstance(action_resolution, dict):
            action_resolution = {}
        if "reinterpreted" not in action_resolution:
            action_resolution["reinterpreted"] = False
        if not isinstance(action_resolution.get("audit_flags"), list):
            action_resolution["audit_flags"] = []

        structured_fields["action_resolution"] = action_resolution

        # Backfill dice_rolls from action_resolution for backward compatibility.
        # Systems that read dice_rolls should see rolls even when they come from
        # code_execution via action_resolution.mechanics.rolls.
        if not raw_rolls and action_resolution:
            mechanics = action_resolution.get("mechanics", {})
            if isinstance(mechanics, dict):
                ar_rolls = mechanics.get("rolls", [])
                if isinstance(ar_rolls, list) and ar_rolls:
                    backfilled_rolls = []
                    for roll in ar_rolls:
                        if isinstance(roll, dict):
                            # Convert action_resolution schema back to dice_rolls format
                            backfilled_rolls.append(
                                {
                                    "roll": roll.get("notation"),
                                    "result": roll.get("result")
                                    if roll.get("result") is not None
                                    else roll.get("total"),
                                    "dc": roll.get("dc"),
                                    "success": roll.get("success"),
                                    "type": roll.get("purpose") or roll.get("label"),
                                    "dc_category": roll.get("dc_category"),
                                    "dc_reasoning": roll.get("dc_reasoning"),
                                    "margin": roll.get("margin"),
                                    "outcome": roll.get("outcome"),
                                }
                            )
                    if backfilled_rolls:
                        structured_fields[constants.FIELD_DICE_ROLLS] = backfilled_rolls

        outcome_resolution = get_outcome_resolution(sr)
        structured_fields["outcome_resolution"] = (
            outcome_resolution  # Always include, even if {}
        )

        # Store a filtered subset of state_updates needed for Living World UI
        # This keeps storage small while still surfacing relevant debug data
        state_updates = _get_structured_attr(sr, constants.FIELD_STATE_UPDATES, {})
        if isinstance(state_updates, dict):
            allowed_keys = {
                "world_events",
                "faction_updates",
                "time_events",
                "rumors",
                "scene_event",
                "complications",
            }
            filtered_state_updates = {
                key: value
                for key, value in state_updates.items()
                if key in allowed_keys and value not in (None, {}, [])
            }

            if filtered_state_updates:
                structured_fields[constants.FIELD_STATE_UPDATES] = (
                    filtered_state_updates
                )

            world_events = filtered_state_updates.get("world_events")
            if world_events and isinstance(world_events, dict):
                structured_fields["world_events"] = world_events

            # Persist a safe audit subset for postmortems (character creation/debugging).
            # Full state_updates can be very large; we keep the keys that help diagnose
            # schema drift for stats/spells/equipment and campaign creation flags.
            audit_subset = _build_state_updates_audit_subset(state_updates)
            if audit_subset:
                structured_fields["state_updates_audit"] = audit_subset

            # Persist full state_updates + core_memories for traceability (rev-lw5lk, rev-lwuz5).
            structured_fields.update(_build_traceability_fields(state_updates))

            # BEAD W2-7m1: Also check for world_events nested inside custom_campaign_state
            # The LLM sometimes incorrectly nests world_events here instead of at top-level.
            # Extract it to prevent split storage between correct and incorrect locations.
            if not world_events or not isinstance(world_events, dict):
                custom_state = state_updates.get("custom_campaign_state", {})
                if isinstance(custom_state, dict):
                    nested_world_events = custom_state.get("world_events")
                    if nested_world_events and isinstance(nested_world_events, dict):
                        structured_fields["world_events"] = nested_world_events
                        # Also add to filtered_state_updates for consistency
                        if constants.FIELD_STATE_UPDATES in structured_fields:
                            structured_fields[constants.FIELD_STATE_UPDATES][
                                "world_events"
                            ] = nested_world_events
                        else:
                            structured_fields[constants.FIELD_STATE_UPDATES] = {
                                "world_events": nested_world_events
                            }

    return structured_fields
