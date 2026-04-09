"""
Unified API Layer for WorldArchitect.AI

This module provides consistent JSON interfaces for both Flask and MCP server usage,
extracting shared business logic and standardizing input/output formats.

Architecture:
- Unified functions handle the core game logic
- Consistent JSON input/output structures
- Centralized error handling and response formatting
- Support for both user_id extraction (Flask auth) and explicit parameters (MCP)

Concurrency:
- Async functions use asyncio.to_thread() for blocking I/O operations
- This prevents blocking the shared event loop during Gemini/Firestore calls
- Critical for allowing concurrent requests (e.g., loading campaigns while actions process)
"""

# ruff: noqa: E402, PLR0911, PLR0912, PLR0915, UP038

import asyncio
import collections
import copy
import json
import os
import re
import tempfile
import time
import uuid
from datetime import datetime, timezone
from typing import Any

from pydantic import ValidationError

# Apply clock skew patch BEFORE importing Firebase to handle time-ahead issues
from mvp_site.clock_skew_credentials import apply_clock_skew_patch

# Import the service account loader
from mvp_site.service_account_loader import get_service_account_credentials

apply_clock_skew_patch()

import firebase_admin
from firebase_admin import credentials

# WorldArchitect imports
from mvp_site import (
    campaign_upgrade,
    constants,
    dice_integrity,
    document_generator,
    firestore_service,
    llm_service,
    logging_util,
    preventive_guards,
    rate_limiting,
    settings_validation,
    structured_fields_utils,
    world_time,
)
from mvp_site.action_resolution_utils import add_action_resolution_to_response
from mvp_site.agent_prompts import (
    build_temporal_correction_prompt,
    build_temporal_warning_message,
    extract_llm_instruction_hints,
)
from mvp_site.agents import (
    SPICY_TOGGLE_ENABLE_PHRASES as enable_spicy_phrases,  # noqa: N811
)
from mvp_site.agents import (
    SPICY_TOGGLE_EXIT_PHRASES as exit_spicy_phrases,  # noqa: N811
)
from mvp_site.agents import (
    _normalize_spicy_toggle_input,
    mode_advances_time,
)
from mvp_site.custom_types import CampaignId, UserId
from mvp_site.debug_hybrid_system import clean_json_artifacts, process_story_for_display
from mvp_site.firestore_service import (
    _redact_settings_for_log,
    _truncate_log_json,
    get_user_settings,
    update_state_with_changes,
)
from mvp_site.game_state import (
    GameState,
    coerce_int,
    level_from_xp,
    validate_and_correct_state,
    xp_needed_for_level,
)
from mvp_site.prompt_utils import _build_campaign_prompt as _build_campaign_prompt_impl
from mvp_site.serialization import json_default_serializer
from mvp_site.session_header_utils import (
    ensure_session_header_resources as _ensure_session_header_resources,
)

# Initialize Firebase if not already initialized.
# In mock/test mode, missing credentials should not be fatal.
# WORLDAI_* vars take precedence for WorldArchitect.AI repo-specific config.
_MOCK_SERVICES_MODE = os.getenv("MOCK_SERVICES_MODE", "").strip().lower() in {
    "1",
    "true",
    "yes",
    "y",
    "on",
}
_TEST_MODE = os.getenv("TEST_MODE", "mock").strip().lower()
_ALLOW_MISSING_FIREBASE = _MOCK_SERVICES_MODE or _TEST_MODE == "mock"


def is_mock_services_mode() -> bool:
    """Check if mock services mode is enabled.

    Evaluated at runtime to support dynamic environment changes in tests.
    """
    return os.getenv("MOCK_SERVICES_MODE", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "y",
        "on",
    }


try:
    firebase_admin.get_app()
except ValueError:
    try:
        worldai_creds_path = os.getenv("WORLDAI_GOOGLE_APPLICATION_CREDENTIALS")
        worldai_creds_path = (
            os.path.expanduser(worldai_creds_path) if worldai_creds_path else None
        )

        # Try loading credentials (file first, then env vars fallback)
        try:
            creds_dict = get_service_account_credentials(
                file_path=worldai_creds_path,
                fallback_to_env=True,
                require_env_vars=False,
            )
            logging_util.info("Successfully loaded service account credentials")
            firebase_admin.initialize_app(credentials.Certificate(creds_dict))
        except Exception as creds_error:
            # Fallback to default credentials (for GCP environments)
            logging_util.warning(
                f"Failed to load explicit credentials: {creds_error}. "
                "Attempting default application credentials."
            )
            firebase_admin.initialize_app()

        logging_util.info("Firebase initialized successfully in world_logic.py")
    except Exception as e:
        if _ALLOW_MISSING_FIREBASE:
            logging_util.warning(
                "Failed to initialize Firebase in mock/test mode; continuing without Firebase: %s",
                e,
            )
        else:
            logging_util.critical(f"Failed to initialize Firebase: {e}")
            raise

# --- Constants ---
KEY_ERROR = "error"
KEY_SUCCESS = "success"
KEY_CAMPAIGN_ID = "campaign_id"
KEY_PROMPT = "prompt"

# Random constants moved to prompt_utils.py to avoid duplication
KEY_SELECTED_PROMPTS = "selected_prompts"
KEY_USER_INPUT = "user_input"
KEY_RESPONSE = "response"
KEY_TRACEBACK = "traceback"

# Temporal validation constants
# DISABLED: Set to 0 to prevent multiple LLM calls for temporal correction
# Previously was 2, but this causes 3 LLM calls total when time goes backward
# This ensures we only make one LLM call per request, accepting the first response
MAX_TEMPORAL_CORRECTION_ATTEMPTS = 0  # Max retries before accepting response

_extract_world_time_from_response = world_time.extract_world_time_from_response
_check_temporal_violation = world_time.check_temporal_violation
_apply_timestamp_to_world_time = world_time.apply_timestamp_to_world_time
_format_world_time_for_prompt = world_time.format_world_time_for_prompt


def _get_agent_name_from_mode(agent_mode: str | None) -> str:
    """Convert agent_mode constant to human-readable agent name for test compatibility.

    Args:
        agent_mode: Agent mode constant (e.g., MODE_CAMPAIGN_UPGRADE)

    Returns:
        Human-readable agent name (e.g., "CampaignUpgradeAgent") or "unknown" if mode is None
    """
    if not agent_mode:
        return "unknown"

    # Map mode constants to agent class names
    mode_to_agent = {
        constants.MODE_GOD: "GodModeAgent",
        constants.MODE_THINK: "PlanningAgent",
        constants.MODE_CHARACTER: "StoryModeAgent",
        constants.MODE_COMBAT: "CombatAgent",
        constants.MODE_REWARDS: "RewardsAgent",
        constants.MODE_INFO: "InfoAgent",
        constants.MODE_CAMPAIGN_UPGRADE: "CampaignUpgradeAgent",
        constants.MODE_CHARACTER_CREATION: "CharacterCreationAgent",
        constants.MODE_FACTION: "FactionManagementAgent",
        constants.MODE_DIALOG: "DialogAgent",
        constants.MODE_DIALOG_HEAVY: "HeavyDialogAgent",
    }

    return mode_to_agent.get(agent_mode, f"UnknownAgent({agent_mode})")


def _resolve_empty_narrative(
    final_narrative: str | None,
    llm_response_obj: Any,
    mode: str | None,
    user_input: str | None = None,
) -> str:
    """Resolve empty narrative fallbacks using centralized god mode detection.

    Uses constants.is_god_mode() for case-insensitive mode check AND prefix detection.
    This ensures consistency with GodModeAgent.matches_input() and other callers.

    For god mode requests, empty narrative is EXPECTED and should stay empty.
    The frontend uses god_mode_response field directly for display.
    """
    if final_narrative and isinstance(final_narrative, str):
        return final_narrative

    # Use centralized god mode detection (case-insensitive + prefix check)
    is_god_mode_request = constants.is_god_mode(user_input or "", mode)

    # God mode: empty narrative is expected - frontend uses god_mode_response
    if is_god_mode_request:
        logging_util.info(
            "✅ GOD_MODE: Empty narrative expected, frontend uses god_mode_response"
        )
        return ""

    # Non-god mode: empty narrative is unexpected, try to recover
    structured_response = getattr(llm_response_obj, "structured_response", None)
    logging_util.warning(
        "⚠️ EMPTY_NARRATIVE in process_action_unified: narrative_text=%s, "
        "type=%s, has_structured_response=%s",
        final_narrative,
        type(final_narrative),
        structured_response is not None,
    )
    if structured_response and hasattr(structured_response, "narrative"):
        return structured_response.narrative or "[Error: Empty narrative from LLM]"
    return "[Error: Empty narrative from LLM]"


def _extract_xp_from_player_data(pc_data: dict[str, Any]) -> int:
    """Extract XP value from player_character_data dict.

    Handles int, float, and string formats (including commas like "2,700").
    Returns 0 if XP cannot be parsed or is not present.

    Args:
        pc_data: Player character data dictionary

    Returns:
        Integer XP value, or 0 if not found/parseable
    """
    if not isinstance(pc_data, dict):
        return 0

    def _parse_numeric(val: Any) -> int:
        if isinstance(val, (int, float)):
            return int(val)
        if isinstance(val, str):
            # Remove commas and whitespace, then try to parse
            cleaned = val.replace(",", "").replace(" ", "").strip()
            if not cleaned:
                return 0
            try:
                return int(float(cleaned))
            except (ValueError, TypeError):
                return 0
        return 0

    exp = pc_data.get("experience")
    if isinstance(exp, dict):
        return _parse_numeric(exp.get("current", 0))
    if exp is not None:
        return _parse_numeric(exp)
    xp = pc_data.get("xp")
    if xp is None:
        xp = pc_data.get("xp_current")
    if xp is not None:
        return _parse_numeric(xp)
    return 0


def _annotate_entry(entry: dict[str, Any], turn: int, scene: int) -> None:
    """Add turn/scene to a dict entry if not already present."""
    if "turn_generated" not in entry:
        entry["turn_generated"] = turn
    if "scene_generated" not in entry:
        entry["scene_generated"] = scene


def _normalize_append_list_field(container: dict[str, Any], key: str) -> None:
    """Convert {'append': [...]} list-operation payloads to plain lists for display."""
    value = container.get(key)
    if not isinstance(value, dict) or "append" not in value:
        return

    append_value = value.get("append")
    if isinstance(append_value, list):
        container[key] = append_value
    elif append_value is None:
        container[key] = []
    else:
        container[key] = [append_value]


def _scene_number_from_turn(turn_number: Any) -> int | None:
    """Convert a player turn number to the persisted user_scene_number format."""
    if not isinstance(turn_number, int) or turn_number <= 0:
        return None
    return turn_number


def _scene_matches_event_metadata(event: Any, scene_number: int) -> bool:
    """Check whether an event belongs to a specific user scene."""
    if not isinstance(event, dict) or not isinstance(scene_number, int):
        return False

    scene_generated = event.get("scene_generated")
    if isinstance(scene_generated, int):
        return scene_generated == scene_number

    turn_generated = event.get("turn_generated")
    if isinstance(turn_generated, int):
        # Primary mapping: user_scene_number is one-to-one with player turn.
        mapped_scene = _scene_number_from_turn(turn_generated)
        if mapped_scene == scene_number:
            return True

        # Legacy compatibility: older data may have used 2-turn scene buckets.
        return ((turn_generated + 1) // 2) == scene_number

    # If no provenance metadata is present, do not assume the event matches this scene.
    return False


def normalize_world_events_for_story_payload(world_events: Any) -> Any:
    """Normalize living-world append operation syntax for UI/story-entry payloads."""
    if not isinstance(world_events, dict):
        return world_events

    def _coerce_event_list(value: Any) -> list[Any]:
        if isinstance(value, list):
            return value
        if value is None:
            return []
        return [value]

    normalized = copy.deepcopy(world_events)
    _normalize_append_list_field(normalized, "background_events")
    _normalize_append_list_field(normalized, "rumors")

    # Some model outputs use a top-level append payload:
    # {"world_events": {"append": [...]}}  # noqa: ERA001
    # Normalize it into background_events for UI/story consumers.
    if "append" in normalized:
        appended_events = _coerce_event_list(normalized.pop("append"))
        existing_background_events = normalized.get("background_events")
        if isinstance(existing_background_events, list):
            normalized["background_events"] = (
                existing_background_events + appended_events
            )
        elif existing_background_events is None:
            normalized["background_events"] = appended_events
        else:
            normalized["background_events"] = [
                existing_background_events
            ] + appended_events

    return normalized


def _filter_story_entry_world_events_to_scene(
    world_events: Any, user_scene_number: int, current_turn: int | None = None
) -> Any:
    """Keep only world_events generated for the entry's scene."""
    if not isinstance(world_events, dict) or not isinstance(user_scene_number, int):
        return world_events

    filtered = copy.deepcopy(world_events)

    def _matches_story_scene(event: Any) -> bool:
        if (
            isinstance(current_turn, int)
            and isinstance(event, dict)
            and event.get("turn_generated") == current_turn
        ):
            return True
        return _scene_matches_event_metadata(event, user_scene_number)

    background_events = filtered.get("background_events")
    if isinstance(background_events, list):
        filtered["background_events"] = [
            event for event in background_events if _matches_story_scene(event)
        ]
        for event in filtered["background_events"]:
            if isinstance(event, dict):
                event["scene_generated"] = user_scene_number

    rumors = filtered.get("rumors")
    if isinstance(rumors, list):
        filtered["rumors"] = [rumor for rumor in rumors if _matches_story_scene(rumor)]
        for rumor in filtered["rumors"]:
            if isinstance(rumor, dict):
                rumor["scene_generated"] = user_scene_number

    # faction_updates and time_events are dicts of named entries (each value is a dict)
    for field in ("faction_updates", "time_events"):
        container = filtered.get(field)
        if isinstance(container, dict):
            filtered[field] = {
                k: v for k, v in container.items() if _matches_story_scene(v)
            }
            for v in filtered[field].values():
                if isinstance(v, dict):
                    v["scene_generated"] = user_scene_number

    # complications and scene_event are single dicts — keep if scene matches, else remove
    for field in ("complications", "scene_event"):
        entry = filtered.get(field)
        if isinstance(entry, dict) and not _matches_story_scene(entry):
            del filtered[field]
        elif isinstance(entry, dict):
            entry["scene_generated"] = user_scene_number

    return filtered


def _try_backfill_story_entry_world_events(
    structured_fields: dict[str, Any],
    *,
    updated_game_state_dict: dict[str, Any],
    player_turn: int | None,  # noqa: ARG001
    user_scene_number: int | None,
) -> None:
    """Backfill per-entry world_events from current game state when LLM omits them."""
    if not isinstance(structured_fields, dict):
        return
    if "world_events" in structured_fields:
        return
    state_updates_field = structured_fields.get("state_updates")
    if isinstance(state_updates_field, dict) and "world_events" in state_updates_field:
        return
    if not isinstance(updated_game_state_dict, dict):
        return
    if not isinstance(user_scene_number, int):
        return

    game_world_events = updated_game_state_dict.get("world_events")
    if not isinstance(game_world_events, dict):
        return

    normalized_world_events = normalize_world_events_for_story_payload(
        game_world_events
    )
    filtered_world_events = _filter_story_entry_world_events_to_scene(
        normalized_world_events,
        user_scene_number,
        current_turn=None,  # Backfill should be scene-scoped, not turn-scoped.
    )
    if not isinstance(filtered_world_events, dict):
        return

    has_background_events = bool(filtered_world_events.get("background_events"))
    has_rumors = bool(filtered_world_events.get("rumors"))
    if not (has_background_events or has_rumors):
        return

    structured_fields["world_events"] = filtered_world_events
    if isinstance(state_updates_field, dict):
        if "world_events" not in state_updates_field:
            state_updates_field["world_events"] = copy.deepcopy(filtered_world_events)
    else:
        structured_fields["state_updates"] = {
            "world_events": copy.deepcopy(filtered_world_events)
        }


def annotate_world_events_with_turn_scene(
    game_state_dict: dict[str, Any],
    player_turn: int,
    scene_number: int | None = None,
) -> dict[str, Any]:
    """Annotate living world entries with turn and scene numbers.

    Adds turn_generated and scene_generated to living world entries for UI display.

    NOTE: This function intentionally checks both nested and top-level locations.
    Living world data can appear in different locations based on LLM schema version:
    1. Under world_events.X (nested) - older schema
    2. At top level: rumors, faction_updates, etc. (direct) - newer schema

    These are DIFFERENT data structures, not duplicates. Even if the same object
    existed in both (by reference), annotation is idempotent (same turn/scene values).

    Args:
        game_state_dict: The game state dictionary to annotate
        player_turn: Player turn number (matches LLM cadence, not story entry count)
        scene_number: Optional explicit scene number to use instead of turn-based calculation

    Returns:
        The annotated game state dictionary
    """
    turn = player_turn
    if scene_number is not None:
        scene = scene_number
    else:
        # Keep scene annotation aligned with persisted user_scene_number.
        scene = _scene_number_from_turn(player_turn) or 1

    def annotate_list(items: Any) -> None:
        """Annotate a list of dict entries."""
        if isinstance(items, dict) and "append" in items:
            append_value = items.get("append")
            if isinstance(append_value, list):
                items = append_value
            elif append_value is None:
                items = []
            else:
                items = [append_value]
        if not isinstance(items, list):
            return
        for item in items:
            if isinstance(item, dict):
                _annotate_entry(item, turn, scene)

    def annotate_dict_values(container: Any) -> None:
        """Annotate all dict values in a container."""
        if not isinstance(container, dict):
            return
        for value in container.values():
            if isinstance(value, dict):
                _annotate_entry(value, turn, scene)

    def annotate_single(entry: Any) -> None:
        """Annotate a single dict entry."""
        if isinstance(entry, dict):
            _annotate_entry(entry, turn, scene)

    # 1. Annotate world_events.background_events (nested under world_events)
    world_events = game_state_dict.get("world_events")
    if isinstance(world_events, dict):
        annotate_list(world_events.get("background_events"))
        # Also check for nested versions (some schemas nest everything under world_events)
        annotate_list(world_events.get("rumors"))
        annotate_dict_values(world_events.get("faction_updates"))
        annotate_dict_values(world_events.get("time_events"))
        annotate_single(world_events.get("complications"))
        annotate_single(world_events.get("scene_event"))

    # 2. Annotate top-level living world fields (per schema, these are direct on state_updates)
    annotate_list(game_state_dict.get("rumors"))
    annotate_dict_values(game_state_dict.get("faction_updates"))
    annotate_dict_values(game_state_dict.get("time_events"))
    annotate_single(game_state_dict.get("complications"))
    annotate_single(game_state_dict.get("scene_event"))

    return game_state_dict


def _maybe_update_living_world_tracking(
    updated_game_state_dict: dict[str, Any],
    *,
    current_game_state: GameState | None,
    turn_number: int,
    mode: str,
    agent_mode: str | None = None,
    is_god_mode: bool,
    is_think_mode: bool,
    should_freeze_time: bool = False,
    state_changes_this_turn: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Update living world tracking after a successful LLM response."""
    _ = state_changes_this_turn
    if is_god_mode or is_think_mode or should_freeze_time:
        return updated_game_state_dict

    effective_mode = agent_mode or mode
    if not mode_advances_time(effective_mode):
        return updated_game_state_dict

    if not current_game_state or turn_number < 1:
        return updated_game_state_dict

    check_trigger = getattr(current_game_state, "check_living_world_trigger", None)
    if not callable(check_trigger):
        return updated_game_state_dict

    # Guard against non-dict world_data to prevent AttributeError
    world_data = updated_game_state_dict.get("world_data")
    current_time = (
        world_data.get("world_time") if isinstance(world_data, dict) else None
    )
    result = check_trigger(turn_number, current_time=current_time)
    if not isinstance(result, tuple) or len(result) != 3:
        return updated_game_state_dict

    should_trigger, trigger_reason, current_time = result
    if not should_trigger:
        return updated_game_state_dict

    # Always update both tracking fields when any trigger fires
    # Turn tracking uses modulo (in living_world.py), so no interference
    updated_game_state_dict["last_living_world_turn"] = turn_number
    if isinstance(current_time, dict):
        updated_game_state_dict["last_living_world_time"] = copy.deepcopy(current_time)
    else:
        updated_game_state_dict["last_living_world_time"] = None

    logging_util.info(
        f"🌍 LIVING_WORLD: Recorded trigger for turn {turn_number} ({trigger_reason})"
    )

    return updated_game_state_dict


def _warn_if_living_world_events_missing(
    *,
    updated_game_state_dict: dict[str, Any],
    state_changes_to_apply: dict[str, Any] | None,
    structured_fields: dict[str, Any] | None,
    is_god_mode: bool,
    is_think_mode: bool,
    mode: str,
    agent_mode: str | None,
) -> None:
    """Warn when living world events are absent on turns where they should fire.

    Living world instruction fires every turn. This check surfaces LLM omissions
    and non-standard schemas early so they can be diagnosed.
    """
    if is_god_mode or is_think_mode:
        return

    effective_mode = agent_mode or mode
    if not mode_advances_time(effective_mode):
        return

    turn_number = (
        updated_game_state_dict.get("turn_number")
        or updated_game_state_dict.get("player_turn")
        or 0
    )
    if not isinstance(turn_number, int) or turn_number < 1:
        return

    sf_we = (
        structured_fields.get("world_events")
        if isinstance(structured_fields, dict)
        else None
    )
    sc_we = (
        state_changes_to_apply.get("world_events")
        if isinstance(state_changes_to_apply, dict)
        else None
    )
    has_world_events = (isinstance(sf_we, dict) and sf_we) or (
        isinstance(sc_we, dict) and sc_we
    )

    if not has_world_events:
        logging_util.warning(
            "🌍 LIVING_WORLD_MISSING: world_events absent on turn %d "
            "(mode=%s agent_mode=%s). Living world instruction fires every turn — "
            "LLM did not include state_updates.world_events.",
            turn_number,
            mode,
            agent_mode,
        )
    else:
        we = sf_we or sc_we
        if isinstance(we, dict) and "background_events" not in we:
            logging_util.warning(
                "🌍 LIVING_WORLD_SCHEMA: world_events on turn %d missing "
                "'background_events' key. Got keys: %s. "
                "LLM may be using a non-standard schema.",
                turn_number,
                list(we.keys()),
            )


def _increment_turn_counter(
    game_state_dict: dict[str, Any],
    *,
    is_god_mode: bool = False,
    should_freeze_time: bool = False,
) -> dict[str, Any]:
    """
    Centralized function to increment the canonical turn counter.

    This is the single source of truth for advancing game turns. Use this function
    instead of directly manipulating player_turn or turn_number fields.

    Args:
        game_state_dict: The game state dictionary to update
        is_god_mode: Whether the current action is god mode (doesn't advance time)
        should_freeze_time: Whether time should be frozen for this action

    Returns:
        Updated game_state_dict with turn counter incremented (if time advances)
    """
    # Normalize turn counters FIRST (before any early return)
    # This ensures downstream consumers always see numeric values
    raw_turn_number = game_state_dict.get("turn_number")
    try:
        current_turn_number = (
            int(raw_turn_number) if raw_turn_number is not None else None
        )
    except (TypeError, ValueError):
        current_turn_number = None

    raw_player_turn = game_state_dict.get("player_turn")
    try:
        current_player_turn = (
            int(raw_player_turn) if raw_player_turn is not None else None
        )
    except (TypeError, ValueError):
        current_player_turn = None

    # Determine the canonical turn from both counters.
    # Use the highest valid value to prevent stale/missing turn_number values
    # from regressing player_turn (e.g. turn_number=0, player_turn=5).
    candidates = [
        turn
        for turn in (current_turn_number, current_player_turn)
        if isinstance(turn, int) and turn >= 0
    ]
    canonical_turn = max(candidates) if candidates else 0

    # Ensure canonical turn is non-negative
    canonical_turn = max(canonical_turn, 0)

    # Don't advance turn counter if god mode or time is frozen
    # But we still normalized above so downstream consumers see numeric values
    if is_god_mode or should_freeze_time:
        game_state_dict["turn_number"] = canonical_turn
        game_state_dict["player_turn"] = canonical_turn
        return game_state_dict

    new_turn = canonical_turn + 1

    # Update turn_number (canonical)
    game_state_dict["turn_number"] = new_turn

    # Sync player_turn for backward compatibility
    game_state_dict["player_turn"] = new_turn

    return game_state_dict


# Temporal correction prompts centralized in agent_prompts.py
# Use build_temporal_correction_prompt() and build_temporal_warning_message()


def truncate_game_state_for_logging(
    game_state_dict: dict[str, Any], max_lines: int = 20
) -> str:
    """
    Truncates a game state dictionary for logging to improve readability.
    Uses the enhanced _truncate_log_json function from firestore_service.
    """
    return _truncate_log_json(
        game_state_dict, max_lines=max_lines, json_serializer=json_default_serializer
    )


def _has_rewards_narrative(narrative: str | None) -> bool:
    """Heuristic check for user-visible rewards in narrative text."""
    if not narrative:
        return False

    narrative_lower = narrative.lower()
    indicators = (
        "reward",
        "rewards",
        "xp",
        "experience",
        "level up",
        "level-up",
        "levelup",
        "loot",
        "gold",
        "treasure",
        "awarded",
        "gained",
        "victory",
    )
    if any(indicator in narrative_lower for indicator in indicators):
        return True

    # Common box markers used by RewardsAgent (format may vary)
    return "══" in narrative or "──" in narrative


def _has_rewards_context(
    state_dict: dict[str, Any], original_state_dict: dict[str, Any] | None = None
) -> bool:
    """Detect whether the current state suggests rewards should be visible."""
    combat_state = state_dict.get("combat_state", {}) or {}
    encounter_state = state_dict.get("encounter_state", {}) or {}
    rewards_pending = state_dict.get("rewards_pending") or {}

    if combat_state.get("combat_summary"):
        return True

    encounter_summary = encounter_state.get("encounter_summary")
    if isinstance(encounter_summary, dict) and encounter_summary:
        return True

    if rewards_pending:
        return True

    if original_state_dict is not None:
        # Use robust XP extractor to handle multiple field formats
        player_data = state_dict.get("player_character_data") or {}
        original_player_data = original_state_dict.get("player_character_data") or {}

        current_xp = _extract_xp_robust(player_data)
        original_xp = _extract_xp_robust(original_player_data)
        if current_xp > original_xp:
            return True

    return False


def _detect_rewards_discrepancy(
    state_dict: dict[str, Any],
    original_state_dict: dict[str, Any] | None = None,
    warnings_out: list[str] | None = None,
) -> list[str]:
    """

    Detect rewards state discrepancies and AUTO-SET the rewards_processed flag.

    ARCHITECTURAL CHANGE (2026-01-22): Server now owns the rewards_processed flag
    as it is an administrative flag, not LLM-generated content. When rewards are
    detected (combat/encounter ended with summary, or XP increased), the server
    immediately sets rewards_processed=true in state_dict.

    This follows "Server Owns Admin Flags, LLM Owns Content" principle.
    See .beads/server-owned-rewards-flag.md for rationale.

    Previous approach (LLM self-correction via system_corrections) failed because:
    - Prose instructions get buried in 16KB prompts
    - LLM prioritizes narrative over administrative flags
    - No schema enforcement made it optional

    Detects and AUTO-FIXES:
    1. Combat just ended (combat_phase in COMBAT_FINISHED_PHASES and combat_summary exists)
       but rewards_processed=False → SET TO TRUE
    2. Encounter completed (encounter_completed=True and encounter_summary exists)
       but rewards_processed=False → SET TO TRUE
    3. XP increased from the previous state but rewards_processed=False → SET TO TRUE
    Also emits warnings when XP increases while rewards_processed=True (possible double-processing).

    Args:
        state_dict: The game state dict after updates are applied (MUTATED IN PLACE)
        original_state_dict: Optional original state before the update (for XP comparison)
        warnings_out: Optional list to append non-blocking warning messages

    Returns:
        List of discrepancy messages (now typically empty, since server fixes them)

    """
    discrepancies: list[str] = []

    # CRITICAL: Ensure we get actual dict references or create new ones that will persist
    # Pattern: get existing dict or create new one, then ensure it's set in state_dict
    if "combat_state" not in state_dict or not isinstance(
        state_dict.get("combat_state"), dict
    ):
        state_dict["combat_state"] = {}
    combat_state = state_dict["combat_state"]

    if "encounter_state" not in state_dict or not isinstance(
        state_dict.get("encounter_state"), dict
    ):
        state_dict["encounter_state"] = {}
    encounter_state = state_dict["encounter_state"]

    # Check 1: Combat just ended with summary but rewards_processed=False
    combat_phase = combat_state.get("combat_phase", "")
    combat_summary = combat_state.get("combat_summary")
    combat_rewards_processed = combat_state.get("rewards_processed", False)

    if (
        combat_phase in constants.COMBAT_FINISHED_PHASES
        and combat_summary
        and not combat_rewards_processed
    ):
        # SERVER AUTO-SET: rewards_processed is an administrative flag owned by server
        combat_state["rewards_processed"] = True
        logging_util.info(
            "🏆 SERVER_AUTO_SET: rewards_processed=true "
            "(combat_phase=%s with combat_summary)",
            combat_phase,
        )

    # Check 2: Encounter completed with summary but rewards_processed=False
    encounter_completed = encounter_state.get("encounter_completed", False)
    encounter_summary = encounter_state.get("encounter_summary")
    encounter_rewards_processed = encounter_state.get("rewards_processed", False)

    if encounter_completed and encounter_summary and not encounter_rewards_processed:
        # SERVER AUTO-SET: rewards_processed is an administrative flag owned by server
        encounter_state["rewards_processed"] = True
        logging_util.info(
            "🏆 SERVER_AUTO_SET: rewards_processed=true "
            "(encounter_completed with encounter_summary)"
        )

    # Check 3: XP increased during combat; ensure flag is set.
    # Only check when combat JUST ended this turn (phase transitioned),
    # not when combat_phase=ended is stale from a previous encounter.
    original_combat_state = (original_state_dict or {}).get("combat_state") or {}
    original_combat_phase = original_combat_state.get("combat_phase", "")
    combat_just_ended = (
        combat_phase in constants.COMBAT_FINISHED_PHASES
        and original_combat_phase not in constants.COMBAT_FINISHED_PHASES
    )
    combat_still_ended = (
        combat_phase in constants.COMBAT_FINISHED_PHASES
        and original_combat_phase in constants.COMBAT_FINISHED_PHASES
    )
    if (
        original_state_dict is not None
        and combat_phase in constants.COMBAT_FINISHED_PHASES
    ):
        player_data = state_dict.get("player_character_data")
        if not isinstance(player_data, dict):
            player_data = {}
        original_player_data = original_state_dict.get("player_character_data")
        if not isinstance(original_player_data, dict):
            original_player_data = {}
        original_combat_rewards_processed = original_combat_state.get(
            "rewards_processed", False
        )

        current_xp = _extract_xp_robust(player_data)
        original_xp = _extract_xp_robust(original_player_data)

        if current_xp > original_xp:
            if not combat_state.get("rewards_processed", False):
                # SERVER AUTO-SET: XP increased means rewards were awarded
                combat_state["rewards_processed"] = True
                logging_util.info(
                    "🏆 SERVER_AUTO_SET: rewards_processed=true "
                    "(XP increased %d -> %d during combat_phase=%s)",
                    original_xp,
                    current_xp,
                    combat_phase,
                )
            elif original_combat_rewards_processed and combat_just_ended:
                # Only warn if combat JUST ended this turn — stale combat_phase
                # should not trigger false positives for unrelated XP (training, skill checks)
                warning = (
                    "REWARDS_STATE_WARNING: XP increased "
                    f"({original_xp} -> {current_xp}) during combat_phase={combat_phase}, "
                    "but rewards_processed=True. Ensure rewards are not being double-processed."
                )
                logging_util.warning(
                    "🏆 REWARDS_DISCREPANCY: XP increased (%d -> %d) even though "
                    "rewards_processed=True during combat_phase=%s; investigate potential "
                    "double-processing",
                    original_xp,
                    current_xp,
                    combat_phase,
                )
                if warnings_out is not None:
                    warnings_out.append(warning)
            elif original_combat_rewards_processed and combat_still_ended:
                # Stale combat state — XP increase is from non-combat activity
                logging_util.info(
                    "🏆 REWARDS_INFO: XP increased (%d -> %d) with stale "
                    "combat_phase=%s (combat was already ended last turn). "
                    "Likely non-combat XP award (training, skill check).",
                    original_xp,
                    current_xp,
                    combat_phase,
                )

    # Check 4: XP increased during encounter without flag.
    # Check if encounter_completed JUST became true this turn.
    original_encounter_state_check = (original_state_dict or {}).get(
        "encounter_state"
    ) or {}
    original_encounter_completed = original_encounter_state_check.get(
        "encounter_completed", False
    )
    encounter_just_completed = encounter_completed and not original_encounter_completed
    encounter_still_completed = encounter_completed and original_encounter_completed
    if original_state_dict is not None and encounter_completed:
        player_data = state_dict.get("player_character_data")
        if not isinstance(player_data, dict):
            player_data = {}
        original_player_data = original_state_dict.get("player_character_data")
        if not isinstance(original_player_data, dict):
            original_player_data = {}
        original_encounter_state = original_state_dict.get("encounter_state") or {}
        original_encounter_rewards_processed = original_encounter_state.get(
            "rewards_processed", False
        )

        current_xp = _extract_xp_robust(player_data)
        original_xp = _extract_xp_robust(original_player_data)

        if current_xp > original_xp:
            if not encounter_state.get("rewards_processed", False):
                # SERVER AUTO-SET: XP increased means rewards were awarded
                encounter_state["rewards_processed"] = True
                logging_util.info(
                    "🏆 SERVER_AUTO_SET: rewards_processed=true "
                    "(XP increased %d -> %d during encounter)",
                    original_xp,
                    current_xp,
                )
            elif original_encounter_rewards_processed and encounter_just_completed:
                # Only warn if encounter JUST completed this turn
                warning = (
                    "REWARDS_STATE_WARNING: XP increased "
                    f"({original_xp} -> {current_xp}) during encounter, "
                    "but rewards_processed=True. Ensure rewards are not being double-processed."
                )
                logging_util.warning(
                    "🏆 REWARDS_DISCREPANCY: XP increased (%d -> %d) even though "
                    "rewards_processed=True during encounter; investigate potential "
                    "double-processing",
                    original_xp,
                    current_xp,
                )
                if warnings_out is not None:
                    warnings_out.append(warning)
            elif original_encounter_rewards_processed and encounter_still_completed:
                # Stale encounter state — XP increase is from non-encounter activity
                logging_util.info(
                    "🏆 REWARDS_INFO: XP increased (%d -> %d) with stale "
                    "encounter_completed=True (encounter was already completed last turn). "
                    "Likely non-encounter XP award (training, skill check).",
                    original_xp,
                    current_xp,
                )

    # Check 5: Fallback for narrative-only rewards (no combat/encounter state flags)
    # This catches cases where LLM awards XP through pure narrative without setting
    # encounter_completed or combat_phase. See .beads/narrative-only-xp-rewards-flag.md
    if original_state_dict:
        player_data = state_dict.get("player_character_data")
        if not isinstance(player_data, dict):
            player_data = {}
        original_player_data = original_state_dict.get("player_character_data")
        if not isinstance(original_player_data, dict):
            original_player_data = {}

        current_xp = _extract_xp_robust(player_data)
        original_xp = _extract_xp_robust(original_player_data)

        if current_xp > original_xp:
            # Check if EITHER combat_state OR encounter_state has rewards_processed flag
            combat_processed = combat_state.get("rewards_processed", False)
            encounter_processed = encounter_state.get("rewards_processed", False)
            in_combat = combat_state.get("in_combat", False)

            if not combat_processed and not encounter_processed and not in_combat:
                # XP increased but no rewards_processed flag set anywhere, AND combat is not active
                # This is likely a narrative reward - default to encounter_state
                # (encounter_state is the semantic home for non-combat rewards)
                # Skip if in_combat=true to avoid incorrectly triggering during multi-enemy combat
                encounter_state["rewards_processed"] = True
                logging_util.info(
                    "🏆 SERVER_AUTO_SET: rewards_processed=true "
                    "(XP increased %d -> %d, fallback for narrative/uncategorized rewards)",
                    original_xp,
                    current_xp,
                )

    return discrepancies


REWARD_CORRECTION_PREFIX = "REWARDS_STATE_ERROR"


def _is_reward_correction(message: Any) -> bool:
    """Return True for reward-related system correction strings."""
    return isinstance(message, str) and message.startswith(REWARD_CORRECTION_PREFIX)


def _filter_reward_corrections(corrections: list[Any] | None) -> list[str]:
    """Filter to reward-related system correction strings."""
    if not corrections:
        return []
    return [message for message in corrections if _is_reward_correction(message)]


def _normalize_system_corrections(value: Any) -> list[str]:
    """Coerce arbitrary pending corrections to a clean list[str] (drop non-strings)."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            if isinstance(item, str) and item.strip():
                out.append(item)
        return out
    return []


def _extract_xp_robust(player_data: dict[str, Any]) -> int:
    """Extract XP from player_character_data, handling multiple field formats.

    Tries in order:
    1. experience.current (canonical format)
    2. xp (flat format)
    3. xp_current (flat variant)

    Also handles comma-formatted strings like "1,500".

    Args:
        player_data: The player_character_data dict

    Returns:
        XP as integer, or 0 if not found
    """
    # Try canonical format first.
    # Legacy states may store "experience" as a scalar instead of {"current": ...}.
    xp_raw = None
    experience = player_data.get("experience")
    if isinstance(experience, dict):
        xp_raw = experience.get("current")
    elif experience is not None:
        xp_raw = experience

    # Try flat formats if canonical not found
    if xp_raw is None:
        xp_raw = player_data.get("xp") or player_data.get("xp_current")

    # Handle comma-formatted strings (e.g., "1,500" -> 1500)
    if isinstance(xp_raw, str):
        xp_raw = xp_raw.replace(",", "")

    return coerce_int(xp_raw, 0)


def _is_state_flag_true(value: Any) -> bool:
    """Return True only for explicit boolean true or case-insensitive 'true'."""
    if value is True:
        return True
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return False


def _is_state_flag_false(value: Any) -> bool:
    """Return True for explicit boolean false or case-insensitive 'false'."""
    if value is False:
        return True
    if isinstance(value, str):
        return value.strip().lower() == "false"
    return False


def _infer_level_up_target_from_xp(
    game_state_dict: dict[str, Any],
    rewards_box: dict[str, Any] | None = None,
) -> int | None:
    """
    Infer the canonical level-up target from XP in authoritative game state.

    Uses player_character_data XP when available. If XP is absent, falls back to
    rewards_box.current_xp for backward compatibility.
    """
    player_data = game_state_dict.get("player_character_data") or {}
    if not isinstance(player_data, dict):
        player_data = {}

    current_level = coerce_int(player_data.get("level"), 1)
    if current_level is None:
        current_level = 1
    current_level = max(1, current_level)

    current_xp = _extract_xp_robust(player_data)
    if current_xp <= 0 and isinstance(rewards_box, dict):
        rewards_box_xp = coerce_int(rewards_box.get("current_xp"), default=None)
        if rewards_box_xp is not None:
            current_xp = rewards_box_xp

    if current_xp <= 0:
        return None

    expected_level = level_from_xp(current_xp)
    if expected_level <= current_level:
        return None

    return expected_level


def _resolve_level_up_signal(
    game_state_dict: dict[str, Any],
    rewards_box: dict[str, Any] | None = None,
) -> tuple[bool, int | None, bool]:
    """
    Resolve whether level-up UI should be active and what target level to target.

    Returns:
        (is_level_up_active, resolved_new_level, rewards_box_signal_accepted)
    """
    rewards_pending = game_state_dict.get("rewards_pending") or {}
    level_up_from_rewards_pending = _is_state_flag_true(
        rewards_pending.get("level_up_available")
    )

    custom_campaign_state = game_state_dict.get("custom_campaign_state") or {}
    level_up_in_progress_value = custom_campaign_state.get("level_up_in_progress")
    level_up_pending_value = custom_campaign_state.get("level_up_pending")
    level_up_in_progress = _is_state_flag_true(level_up_in_progress_value)
    level_up_pending = _is_state_flag_true(level_up_pending_value)

    level_up_from_rewards_box = isinstance(rewards_box, dict) and _is_state_flag_true(
        rewards_box.get("level_up_available")
    )
    inferred_new_level = _infer_level_up_target_from_xp(game_state_dict, rewards_box)
    rewards_box_signal_accepted = (
        level_up_from_rewards_box and inferred_new_level is not None
    )
    if level_up_from_rewards_box and not rewards_box_signal_accepted:
        logging_util.info(
            "📈 LEVELUP_INJECT: ignoring rewards_box.level_up_available=true "
            "because server XP state does not support level-up"
        )

    resolved_new_level = coerce_int(rewards_pending.get("new_level"), default=None)

    level_up_active = (
        level_up_from_rewards_pending
        or rewards_box_signal_accepted
        or level_up_in_progress
        or level_up_pending
    )

    # Explicit false flags in campaign state take precedence over stale signals.
    if _is_state_flag_false(level_up_in_progress_value):
        level_up_active = False
    if _is_state_flag_false(level_up_pending_value) and not level_up_in_progress:
        level_up_active = False

    if level_up_active:  # noqa: SIM102
        if resolved_new_level is None and inferred_new_level is not None:
            resolved_new_level = inferred_new_level

    return level_up_active, resolved_new_level, rewards_box_signal_accepted


def _should_emit_level_up_rewards_box(
    game_state_dict: dict[str, Any],
    rewards_box: dict[str, Any] | None,
) -> bool:
    """Only emit level-up rewards_box when canonical level-up state is active."""
    if not isinstance(rewards_box, dict):
        return True
    if not _is_state_flag_true(rewards_box.get("level_up_available")):
        return True

    level_up_active, _, _ = _resolve_level_up_signal(game_state_dict, rewards_box)
    return level_up_active


def _check_and_set_level_up_pending(
    state_dict: dict[str, Any], original_state_dict: dict[str, Any] | None = None
) -> dict[str, Any]:
    """
    Server-side level-up detection: Set rewards_pending when XP now supports a higher level.

    This ensures level-up is offered to the player even when XP is awarded outside
    the normal rewards pipeline (e.g., God Mode, narrative milestones) or when a
    previous level-up was missed. Comparison uses the original state (pre-update)
    to avoid relying on validation that may auto-correct the stored level.

    The LLM receives rewards_pending in game state context and generates level-up
    rewards boxes per rewards_system_instruction.md when level_up_available=True.

    Args:
        state_dict: The game state dict after updates are applied
        original_state_dict: Original state before the update (for XP comparison)

    Returns:
        The game state dict with rewards_pending set if level-up is available
    """
    if original_state_dict is None:
        return state_dict

    # Get current and original XP using robust extractor
    player_data = state_dict.get("player_character_data") or {}
    current_xp = _extract_xp_robust(player_data)

    original_player_data = original_state_dict.get("player_character_data") or {}
    original_xp = _extract_xp_robust(original_player_data)

    # Get stored level from ORIGINAL state (before validation auto-correction)
    # This ensures we detect level-ups even when validation already corrected the level
    # in the current state. Falls back to current state's level if original not available.
    original_level = coerce_int(original_player_data.get("level"), None)
    current_level = coerce_int(player_data.get("level"), 1)
    stored_level = original_level if original_level is not None else current_level

    # Calculate what level SHOULD be based on XP
    expected_level = level_from_xp(current_xp)

    # If expected level is NOT higher than stored level, NO level-up needed
    if expected_level <= stored_level:
        # CRITICAL: Clear stale level-up notifications if:
        # 1. Player actually leveled up (stored_level >= pending new_level), OR
        # 2. XP dropped below the threshold for the pending level-up
        existing_rewards = state_dict.get("rewards_pending") or {}
        if existing_rewards.get("level_up_available") is True:
            existing_new_level = coerce_int(
                existing_rewards.get("new_level"), default=0
            )
            # Get XP threshold for the pending level-up
            xp_threshold_for_pending = xp_needed_for_level(existing_new_level)
            if stored_level >= existing_new_level:
                # Player reached or exceeded the pending level → clear the notification
                logging_util.info(
                    f"📈 LEVEL_UP_CHECK: Clearing stale level-up notification "
                    f"(stored_level={stored_level} >= pending new_level={existing_new_level})"
                )
                state_dict.pop("rewards_pending", None)
            elif current_xp < xp_threshold_for_pending:
                # XP dropped below threshold for pending level-up → clear stale notification
                logging_util.info(
                    f"📈 LEVEL_UP_CHECK: Clearing stale level-up notification "
                    f"(XP {current_xp} < threshold {xp_threshold_for_pending} for level {existing_new_level})"
                )
                state_dict.pop("rewards_pending", None)
        return state_dict

    # Check if rewards_pending already exists and handles this level-up
    existing_rewards = state_dict.get("rewards_pending") or {}
    if existing_rewards.get("level_up_available") is True:
        existing_new_level = coerce_int(
            existing_rewards.get("new_level"), default=stored_level
        )
        if expected_level <= existing_new_level:
            # Already have an equal-or-higher pending level-up; avoid resetting flags
            logging_util.debug(
                "📈 LEVEL_UP_CHECK: existing level_up_available covers current level"
            )
            return state_dict

        # XP has pushed the player to a higher level than the pending notification;
        # refresh rewards_pending to surface the higher target level.
        logging_util.info(
            "📈 LEVEL_UP_CHECK: Upgrading pending level-up notification "
            f"from {existing_new_level} to {expected_level}"
        )

    # Set rewards_pending to trigger RewardsAgent (either new or upgraded)
    xp_delta = current_xp - original_xp
    logging_util.info(
        f"📈 LEVEL_UP_CHECK: Level-up available! "
        f"XP {original_xp} → {current_xp} ({'+' if xp_delta >= 0 else ''}{xp_delta}), "
        f"stored_level={stored_level}, expected_level={expected_level}. "
        f"Setting rewards_pending.level_up_available=True"
    )

    existing_rewards = state_dict.get("rewards_pending") or {}

    # Clear stale completion/cancel/in-progress flags when a new level-up becomes available.
    # Otherwise future level-ups can stay blocked after a previous completion.
    custom_state = state_dict.get("custom_campaign_state")
    if isinstance(custom_state, dict) and (
        custom_state.get("level_up_complete")
        or custom_state.get("level_up_cancelled")
        or custom_state.get("level_up_in_progress") is False
        or custom_state.get("level_up_pending") is False
    ):
        custom_state = dict(custom_state)
        custom_state["level_up_complete"] = False
        custom_state["level_up_cancelled"] = False
        # Clear stale level_up_in_progress=False to prevent routing block
        if custom_state.get("level_up_in_progress") is False:
            custom_state.pop("level_up_in_progress", None)
        # Clear stale level_up_pending=False to prevent routing block
        if custom_state.get("level_up_pending") is False:
            custom_state.pop("level_up_pending", None)
        state_dict["custom_campaign_state"] = custom_state
        logging_util.info(
            "📈 LEVEL_UP_CHECK: Cleared stale level-up flags for new level-up"
        )

    # CRITICAL FIX: Don't resurrect already-processed rewards
    # If existing rewards were already processed, clear them before merging new level-up
    if existing_rewards.get("processed") is True:
        # Old rewards already processed - start fresh for this level-up
        merged_items = []
        preserved_xp = 0
        preserved_gold = 0
    else:
        # Old rewards not yet processed - merge them with this level-up
        merged_items = list(existing_rewards.get("items") or [])
        preserved_xp = existing_rewards.get("xp", 0)
        preserved_gold = existing_rewards.get("gold", 0)

    new_source_id = f"level_up_{stored_level}_to_{expected_level}"

    state_dict["rewards_pending"] = {
        "source": "level_up",
        # Always align source_id with the current target level (upgrade-safe)
        "source_id": new_source_id,
        # XP has already been applied to state; preserve any existing rewards XP (if not processed)
        "xp": preserved_xp,
        "gold": preserved_gold,
        "items": merged_items,
        "level_up_available": True,
        "new_level": expected_level,
        # Always reset processed to False so RewardsAgent prompts for the higher level
        "processed": False,
    }

    return state_dict


async def _process_rewards_followup(
    mode: str,
    llm_response_obj: Any,
    updated_game_state_dict: dict[str, Any],
    original_state_as_dict: dict[str, Any],
    original_world_time: dict[str, Any] | None,
    story_context: list[dict[str, Any]],
    selected_prompts: list[str],
    use_default_world: bool,
    user_id: str,
    prevention_extras: dict[str, Any],
) -> tuple[dict[str, Any], Any, dict[str, Any]]:
    """
    Process rewards follow-up if needed after primary action.

    This function checks if RewardsAgent needs to run as a follow-up to ensure
    user-visible rewards output. It prevents double invocation by checking if
    rewards_box already exists in the response.

    Args:
        mode: The original action mode (MODE_CHARACTER, MODE_COMBAT, etc.)
        llm_response_obj: The primary LLM response object
        updated_game_state_dict: Current game state dict after primary updates
        original_state_as_dict: Original state dict before the action
        original_world_time: Original world time for validation
        story_context: Story context for LLM calls
        selected_prompts: Selected prompts for LLM calls
        use_default_world: Whether using default world
        user_id: User ID for LLM calls
        prevention_extras: Dict to accumulate prevention extras

    Returns:
        Tuple of (updated_game_state_dict, llm_response_obj, prevention_extras)
    """
    rewards_already_in_response = (
        hasattr(llm_response_obj, "structured_response")
        and llm_response_obj.structured_response is not None
        and getattr(llm_response_obj.structured_response, "rewards_box", None)
        is not None
    )

    if mode == constants.MODE_REWARDS or rewards_already_in_response:
        # Rewards already handled, no warning needed
        return updated_game_state_dict, llm_response_obj, prevention_extras

    rewards_warnings: list[str] = []

    # Check if rewards followup WOULD have triggered
    post_update_state = GameState.from_dict(updated_game_state_dict)
    rewards_visible = _has_rewards_narrative(llm_response_obj.narrative_text)
    rewards_expected = _has_rewards_context(
        updated_game_state_dict, original_state_dict=original_state_as_dict
    )
    rewards_pending = (
        post_update_state.has_pending_rewards() if post_update_state else False
    )

    if not post_update_state or not (
        rewards_pending or (rewards_expected and not rewards_visible)
    ):
        return updated_game_state_dict, llm_response_obj, prevention_extras

    logging_util.info(
        "🏆 REWARDS_FOLLOWUP: Invoking RewardsAgent "
        f"(pending={rewards_pending}, visible={rewards_visible}, expected={rewards_expected})"
    )

    # LATENCY TRACKING: Rewards followup LLM call
    rewards_start = time.perf_counter()
    logging_util.info(
        "⏱️ LATENCY_LLM_REWARDS_START: Starting rewards followup LLM inference"
    )

    rewards_response_obj = await asyncio.to_thread(
        llm_service.continue_story,
        "continue",  # neutral prompt for rewards mode
        constants.MODE_REWARDS,
        story_context,
        post_update_state,
        selected_prompts,
        use_default_world,
        user_id,
    )

    rewards_duration = time.perf_counter() - rewards_start
    logging_util.info(
        f"⏱️ LATENCY_LLM_REWARDS_END: Rewards followup LLM inference completed in {rewards_duration:.2f}s"
    )

    rewards_state_changes, rewards_prevention_extras = (
        preventive_guards.enforce_preventive_guards(
            post_update_state, rewards_response_obj, constants.MODE_REWARDS
        )
    )

    if rewards_pending:
        # Apply preventive guards and update state with rewards response
        rewards_state_changes = _apply_timestamp_to_world_time(rewards_state_changes)
        rewards_state_changes = world_time.ensure_progressive_world_time(
            rewards_state_changes, is_god_mode=False
        )
        rewards_new_world_time = (
            rewards_state_changes.get("world_data", {}) or {}
        ).get("world_time")

        updated_game_state_dict = update_state_with_changes(
            updated_game_state_dict, rewards_state_changes
        )
        updated_game_state_dict = validate_game_state_updates(
            updated_game_state_dict,
            new_time=rewards_new_world_time,
            original_time=original_world_time,
            original_state_dict=original_state_as_dict,
        )
        # Detect rewards discrepancies (will be injected into next prompt)
        rewards_discrepancies = _detect_rewards_discrepancy(
            updated_game_state_dict,
            original_state_dict=original_state_as_dict,
            warnings_out=rewards_warnings,
        )
        if rewards_discrepancies:
            prevention_extras.setdefault("system_corrections", []).extend(
                rewards_discrepancies
            )
        if rewards_warnings:
            prevention_extras.setdefault("system_warnings", []).extend(rewards_warnings)
        # Check for level-up after rewards processing
        updated_game_state_dict = _check_and_set_level_up_pending(
            updated_game_state_dict,
            original_state_dict=original_state_as_dict,
        )
        updated_game_state_dict, rewards_corrections = validate_and_correct_state(
            updated_game_state_dict,
            previous_world_time=original_world_time,
            return_corrections=True,
        )
        # Store rewards corrections so they reach system_warnings in main flow
        if rewards_corrections:
            prevention_extras.setdefault("rewards_corrections", []).extend(
                rewards_corrections
            )
    else:
        # Rewards already applied; detect any discrepancies for next prompt
        rewards_discrepancies = _detect_rewards_discrepancy(
            updated_game_state_dict,
            original_state_dict=original_state_as_dict,
            warnings_out=rewards_warnings,
        )
        if rewards_discrepancies:
            prevention_extras.setdefault("system_corrections", []).extend(
                rewards_discrepancies
            )
        if rewards_warnings:
            prevention_extras.setdefault("system_warnings", []).extend(rewards_warnings)
        # Check for level-up in case XP was awarded in this follow-up
        updated_game_state_dict = _check_and_set_level_up_pending(
            updated_game_state_dict,
            original_state_dict=original_state_as_dict,
        )

    # Merge prevention extras for response visibility
    prevention_extras.update(rewards_prevention_extras)

    # Append rewards narrative to original narrative for user visibility
    primary_text = llm_response_obj.narrative_text or ""
    rewards_text = rewards_response_obj.narrative_text or ""
    if rewards_text:
        combined = f"{primary_text}\n\n{rewards_text}" if primary_text else rewards_text
        llm_response_obj.narrative_text = combined

    # Merge structured response from rewards follow-up (critical: rewards_box)
    rewards_structured = getattr(rewards_response_obj, "structured_response", None)
    if rewards_structured:
        primary_structured = getattr(llm_response_obj, "structured_response", None)
        if primary_structured is None:
            # No original structured response, use rewards response
            llm_response_obj.structured_response = rewards_structured
        # Merge rewards_box from rewards response into primary
        elif (
            hasattr(rewards_structured, "rewards_box")
            and rewards_structured.rewards_box
        ):
            primary_structured.rewards_box = rewards_structured.rewards_box
            logging_util.info(
                f"🏆 REWARDS_FOLLOWUP: Merged rewards_box into response "
                f"(xp={rewards_structured.rewards_box.get('xp_gained', 'N/A')})"
            )

    return updated_game_state_dict, llm_response_obj, prevention_extras


# =============================================================================
# FREEZE TIME HELPERS
# =============================================================================
# These functions support the freeze_time feature for planning block choices.
# When a choice has freeze_time=true, time advances by only 1 microsecond
# (like Think Mode) but other state changes (level-up, etc.) are allowed.
# =============================================================================


def _extract_recent_planning_blocks(
    story_context: list[dict[str, Any]] | None, lookback: int = 3
) -> list[dict[str, Any]]:
    """
    Extract planning blocks from recent AI responses in story context.

    Args:
        story_context: The story context list of entries
        lookback: How many recent entries to check (default 3)

    Returns:
        List of planning_block dicts from recent AI responses (most recent first)
    """
    if not story_context:
        return []

    planning_blocks = []
    # Look at recent entries in reverse order (most recent first)
    for entry in reversed(story_context[-lookback:]):
        if not isinstance(entry, dict):
            continue
        # Only check AI responses
        if (
            str(entry.get(constants.KEY_ACTOR, "")).lower()
            != constants.ACTOR_GEMINI.lower()
        ):
            continue
        # Extract planning_block from structured fields
        planning_block = entry.get(constants.FIELD_PLANNING_BLOCK)
        if isinstance(planning_block, str):
            try:
                planning_block = (
                    json.loads(planning_block) if planning_block.strip() else None
                )
            except (json.JSONDecodeError, TypeError):
                planning_block = None

        if planning_block and isinstance(planning_block, dict):
            planning_blocks.append(planning_block)

    return planning_blocks


def _enforce_character_creation_modal_lock(
    current_game_state_dict: dict[str, Any],
    state_changes: dict[str, Any],
    user_input: str,
) -> dict[str, Any]:
    """
    Server-side enforcement of character creation and level-up modal locks.

    This function runs AFTER LLM generates response but BEFORE applying state_updates.

    Key Principle: LLM doesn't control routing - Server does.

    The LLM no longer knows about character_creation_completed/in_progress/stage or
    level_up_complete/in_progress flags. Instead, the SERVER detects when user has
    selected an exit choice and enforces the state transition.

    Args:
        current_game_state_dict: Current game state before LLM response
        state_changes: State changes from LLM (from enforce_preventive_guards)
        user_input: User's input text (may contain selected choice ID)

    Returns:
        Modified state_changes with server-enforced state transitions

    Exit Choices (SERVER-SIDE KNOWLEDGE):
        Character Creation:
            - start_adventure: God mode review exit
            - play_character: Manual creation exit
            - finish_character: Manual creation exit (alternative ID)
            - finish_character_creation_start_game: Canonical character-creation finish
            - cancel_creation: Cancel exit
        Level-Up:
            - complete_levelup: Level-up completion exit
            - finish_level_up_return_to_game: Canonical level-up finish
    """

    # Extract current character creation state
    custom_state = current_game_state_dict.get("custom_campaign_state", {})
    if not isinstance(custom_state, dict):
        custom_state = {}

    in_progress = custom_state.get("character_creation_in_progress", False)
    level_up_in_progress = custom_state.get("level_up_in_progress", False)
    stage = custom_state.get("character_creation_stage", "")

    # Not in character creation or level-up? No enforcement needed
    if not in_progress and not level_up_in_progress and stage != "level_up":
        return state_changes

    # Level-up modal is active if either the flag or the stage is set
    level_up_modal_active = bool(level_up_in_progress or stage == "level_up")

    # Don't skip enforcement if level-up is active, even if stage is "complete" or empty
    if not level_up_modal_active:  # noqa: SIM102
        if stage not in ("concept", "mechanics", "personality", "review"):
            return state_changes

    # If both markers are set, prioritize level-up to avoid cross-modal interference.
    character_creation_modal_active = bool(in_progress and not level_up_modal_active)
    active_modal_labels: list[str] = []
    if character_creation_modal_active:
        active_modal_labels.append("character_creation")
    if level_up_modal_active:
        active_modal_labels.append("level_up")
    logging_util.info(
        f"🔒 MODAL_LOCK: Active modal(s)={','.join(active_modal_labels)}, stage={stage}"
    )

    # Define valid exit choices (SERVER-SIDE KNOWLEDGE)
    # LLM doesn't need to know these are "special" - they're just planning_block choices!
    _level_up_exit_choices = {"complete_levelup", "finish_level_up_return_to_game"}
    exit_choice_ids = {
        "start_adventure",  # God mode review exit
        "play_character",  # Manual creation exit
        "finish_character",  # Manual creation exit (alternative)
        "finish_character_creation_start_game",  # Canonical char-creation finish
        "cancel_creation",  # Cancel exit
    } | _level_up_exit_choices

    # Check if user input contains an exit choice selection
    # User selects choices via buttons which sends: "CHOICE:choice_id"
    # STRICT DETECTION: Only structured CHOICE: prefix is accepted (no keyword matching)
    # This prevents false positives like "I don't want to start_adventure yet"
    user_selected_exit = False
    selected_choice_id = None

    # Parse user_input for choice selection
    if isinstance(user_input, str):
        user_input_lower = user_input.lower().strip()

        # Check for CHOICE: prefix (from planning_block selection)
        if user_input_lower.startswith("choice:"):
            # Slice the normalized input to avoid whitespace/casing mismatches.
            choice_part = user_input_lower[7:].strip()  # Remove "choice:" prefix
            selected_choice_id = choice_part
            user_selected_exit = selected_choice_id in exit_choice_ids

    if user_selected_exit:
        # ✅ SERVER ENFORCES EXIT (not LLM!)
        logging_util.info(
            f"✅ MODAL_LOCK: User selected exit choice: {selected_choice_id}"
        )

        # Ensure custom_campaign_state exists in state_changes
        if "custom_campaign_state" not in state_changes:
            state_changes["custom_campaign_state"] = {}

        # Ensure it's a dict (defensive programming)
        if not isinstance(state_changes["custom_campaign_state"], dict):
            state_changes["custom_campaign_state"] = {}

        # DATA-DRIVEN MODAL EXIT: Map exit choices to their completion flags
        # This makes the shared architecture explicit and maintainable
        if selected_choice_id in _level_up_exit_choices:
            # Level-up modal exit
            completion_flags = {
                "level_up_complete": True,
                "level_up_in_progress": False,
                "level_up_pending": False,
                # CRITICAL: Clear character-creation flags to prevent recapture by
                # character-creation lock check (agents.py:2806) which runs first
                "character_creation_in_progress": False,
                "character_creation_completed": True,
                "character_creation_stage": "complete",
            }
            modal_type = "level-up"
            # CRITICAL: Clear rewards_pending at the root transition to fully remove the
            # stale signal — not just flip level_up_available, which leaves other keys
            # in rewards_pending that _has_rewards_context() treats as active.
            # Only mutate if rewards_pending already exists; never create it if absent.
            if "rewards_pending" in current_game_state_dict:
                state_changes["rewards_pending"] = firestore_service.DELETE_TOKEN
        else:
            # Character creation modal exit (all other exit choices)
            completion_flags = {
                "character_creation_completed": True,
                "character_creation_in_progress": False,
                "character_creation_stage": "complete",
            }
            modal_type = "character creation"

        # Apply completion flags (SERVER AUTHORITY - LLM cannot set these!)
        state_changes["custom_campaign_state"].update(completion_flags)
        logging_util.info(
            f"🚪 MODAL_LOCK: Server enforced {modal_type} exit via {selected_choice_id} - modal lock released"
        )

    else:
        # ❌ BLOCK any attempts to exit without proper choice
        logging_util.info(
            "🔒 MODAL_LOCK: No exit choice selected - enforcing modal lock"
        )

        # DATA-DRIVEN MODAL LOCK ENFORCEMENT
        # Only protect flags for currently active modal(s) to avoid cross-activation.
        protected_flags = {}
        if character_creation_modal_active:
            protected_flags.update(
                {
                    "character_creation_completed": {
                        "block_if_truthy": True,
                        "action": "remove",
                        "warning": "character_creation_completed=True without exit choice",
                    },
                    "character_creation_in_progress": {
                        "block_if_falsy": True,
                        "action": "force_true",
                        "warning": "character_creation_in_progress=False without exit choice",
                    },
                    "character_creation_stage": {
                        "block_if_equals": "complete",
                        "action": "restore",
                        "restore_value": stage,
                        "warning": "stage=complete without exit choice",
                    },
                }
            )
        if level_up_modal_active:
            protected_flags.update(
                {
                    "level_up_complete": {
                        "block_if_truthy": True,
                        "action": "remove",
                        "warning": "level_up_complete=True without exit choice",
                    },
                    "level_up_in_progress": {
                        "block_if_falsy": True,
                        "action": "force_true",
                        "warning": "level_up_in_progress=False without exit choice",
                    },
                }
            )

        # Apply protection rules to state_changes (if they exist)
        if "custom_campaign_state" in state_changes:
            custom_updates = state_changes["custom_campaign_state"]

            for flag_name, rules in protected_flags.items():
                if flag_name not in custom_updates:
                    continue

                flag_value = custom_updates[flag_name]
                should_block = False

                # Check blocking conditions
                if (
                    (rules.get("block_if_truthy") and flag_value)
                    or (
                        rules.get("block_if_falsy")
                        and flag_name in custom_updates
                        and not flag_value
                    )
                    or (
                        rules.get("block_if_equals") is not None
                        and flag_value == rules["block_if_equals"]
                    )
                ):
                    should_block = True

                # Apply blocking action if needed
                if should_block:
                    logging_util.warning(
                        f"🚨 MODAL_LOCK: BLOCKED LLM attempt to set {rules['warning']}"
                    )

                    if rules["action"] == "remove":
                        custom_updates.pop(flag_name, None)
                    elif rules["action"] == "force_true":
                        custom_updates[flag_name] = True
                    elif rules["action"] == "restore":
                        custom_updates[flag_name] = rules["restore_value"]

    return state_changes


def _should_freeze_time_for_selected_choice(
    user_input: str, story_context: list[dict[str, Any]] | None
) -> bool:
    """
    Check if the user selected a planning block choice with freeze_time=true.

    When a choice has freeze_time=true, time should only advance by 1 microsecond
    (like Think Mode). This is used for meta-game decisions like level-up choices
    that don't represent in-game time passing.

    Args:
        user_input: The user's input text
        story_context: The story context to extract recent planning blocks from

    Returns:
        True if the selected choice has freeze_time=true, False otherwise
    """
    if user_input is None or story_context is None:
        return False

    selected_choice = _get_selected_choice_from_story_context(user_input, story_context)
    # Use explicit `is True` check to handle legacy string values like "false" from Firestore
    # In Python, non-empty strings like "false" are truthy, which would incorrectly trigger this
    if isinstance(selected_choice, dict) and selected_choice.get("freeze_time") is True:
        choice_key = selected_choice.get("key", "unknown")
        logging_util.info(
            f"🕐 FREEZE_TIME: User selected choice '{choice_key}' with freeze_time=true"
        )
        return True

    return False


def _get_selected_choice_from_story_context(
    user_input: str, story_context: list[dict[str, Any]] | None
) -> dict | None:
    """Return the selected planning-block choice (with key) from recent story context."""
    if user_input is None or story_context is None:
        return None

    recent_planning_blocks = _extract_recent_planning_blocks(story_context)
    if not recent_planning_blocks:
        return None

    selected_choice = document_generator.get_selected_choice(
        user_input, recent_planning_blocks
    )
    return selected_choice if isinstance(selected_choice, dict) else None


def _apply_freeze_time_state_changes(
    state_changes: dict[str, Any],
    *,
    original_world_time: dict[str, Any] | None,
    allow_state_changes: bool,
) -> dict[str, Any]:
    """Apply time-freeze behavior with a single microsecond tick."""
    base_changes = state_changes if allow_state_changes else {}
    return _filter_time_changes_for_freeze_time_choice(
        base_changes, original_world_time=original_world_time
    )


def _filter_time_changes_for_freeze_time_choice(
    state_changes: dict[str, Any],
    *,
    original_world_time: dict[str, Any] | None,
) -> dict[str, Any]:
    """
    For freeze_time choices, allow normal state updates but prevent time advancement.

    This strips all world_time/timestamp updates and replaces them with a single
    microsecond tick derived from the original world_time.
    """

    def _next_microsecond() -> int:
        if not isinstance(original_world_time, dict):
            return 1
        raw = original_world_time.get("microsecond", 0)
        try:
            micro = int(raw)
        except (TypeError, ValueError):
            micro = 0
        if micro >= 999_999:
            return 999_999
        micro = max(micro, 0)
        return micro + 1

    frozen_microsecond = _next_microsecond()

    if not isinstance(state_changes, dict):
        return {"world_data": {"world_time": {"microsecond": frozen_microsecond}}}

    filtered: dict[str, Any] = dict(state_changes)

    # Remove dotted-key time updates that would be normalized later by update_state_with_changes().
    for key in list(filtered.keys()):
        if key == "world_data.world_time":
            filtered.pop(key, None)
            continue
        if key.startswith("world_data.world_time."):
            filtered.pop(key, None)
            continue
        if key in ("world_data.timestamp", "world_data.timestamp_iso"):
            filtered.pop(key, None)

    world_data = filtered.get("world_data")
    if not isinstance(world_data, dict):
        world_data = {}

    world_data_filtered = dict(world_data)
    world_data_filtered.pop("timestamp", None)
    world_data_filtered.pop("timestamp_iso", None)
    world_data_filtered.pop("world_time", None)
    world_data_filtered["world_time"] = {"microsecond": frozen_microsecond}
    filtered["world_data"] = world_data_filtered

    return filtered


def _inject_levelup_choices_if_needed(
    planning_block: dict[str, Any] | str | None,
    game_state_dict: dict[str, Any],
    rewards_box: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """
    Server-side enforcement of level-up choices in planning_block.

    When rewards_pending.level_up_available=true OR rewards_box.level_up_available=true,
    the LLM SHOULD include level_up_now and continue_adventuring choices. However, the LLM
    sometimes prioritizes narrative/tactical choices, especially during active gameplay.
    The LLM may also explicitly clear rewards_pending via state_updates=null while still
    returning rewards_box.level_up_available=true (indicator shows but no choices injected).

    This function ensures users ALWAYS have clickable level-up buttons when
    level-up is available, preventing the "text shown but no buttons" failure mode.

    Args:
        planning_block: The planning_block from LLM response (dict, JSON string, or None)
        game_state_dict: Current game state dict to check for level_up_available
        rewards_box: Optional rewards_box from current LLM response. When
            rewards_box.level_up_available=true but game_state.rewards_pending is null
            (LLM explicitly cleared it via state_updates), this fallback signal ensures
            injection still occurs so the level-up indicator always has clickable buttons.

    Returns:
        The planning_block dict with level-up choices injected if needed,
        or None if input was None and no injection needed.
    """
    rewards_pending = game_state_dict.get("rewards_pending") or {}
    level_up_from_rewards_pending = _is_state_flag_true(
        rewards_pending.get("level_up_available")
    )
    level_up_active, resolved_new_level, rewards_box_signal_accepted = (
        _resolve_level_up_signal(game_state_dict, rewards_box)
    )

    def _ensure_level_up_first(block: dict[str, Any] | None) -> None:
        if not isinstance(block, dict):
            return
        result_choices = block.get("choices")
        if not isinstance(result_choices, list) or len(result_choices) <= 1:
            return
        lu_idx = next(
            (
                i
                for i, c in enumerate(result_choices)
                if isinstance(c, dict) and c.get("id") == "level_up_now"
            ),
            None,
        )
        if lu_idx is not None and lu_idx != 0:
            result_choices.insert(0, result_choices.pop(lu_idx))

    if not level_up_active:
        # No level-up available - return as-is
        if isinstance(planning_block, str):
            try:
                return json.loads(planning_block) if planning_block.strip() else None
            except (json.JSONDecodeError, TypeError):
                return None
        return planning_block

    # Level-up is available (from canonical signal) - ensure choices are present.
    # Synthesize rewards_pending from rewards_box when primary signal is missing.
    if (
        not level_up_from_rewards_pending
        and rewards_box_signal_accepted
        and isinstance(resolved_new_level, int)
    ):
        player_data = game_state_dict.get("player_character_data") or {}
        current_level = coerce_int(player_data.get("level"), 1)
        rewards_pending = {
            "level_up_available": True,
            "new_level": resolved_new_level,
        }
        logging_util.info(
            "📈 LEVELUP_INJECT: rewards_pending=null but rewards_box.level_up_available=true; "
            "synthesizing rewards_pending for injection "
            f"(current_level={current_level}, new_level={resolved_new_level})"
        )

    new_level = (
        rewards_pending.get("new_level")
        if isinstance(rewards_pending.get("new_level"), (int, str))
        else resolved_new_level
    )
    if new_level is None:
        new_level = "?"
    player_data = game_state_dict.get("player_character_data") or {}
    player_class = (
        player_data.get("class_name") or player_data.get("class") or "Character"
    )

    planning_block = campaign_upgrade.normalize_planning_block_choices(
        planning_block, log_prefix="📈 SERVER_LEVELUP_INJECTION"
    )
    choices = planning_block["choices"]
    if not isinstance(choices, list):
        # normalize_planning_block_choices should always return list-format, but
        # keep this guard to avoid hard failures on unexpected payloads.
        choices = []
        planning_block["choices"] = choices

    def _find_choice(choice_id: str) -> dict[str, Any] | None:
        for choice in choices:
            if isinstance(choice, dict) and choice.get("id") == choice_id:
                return choice
        return None

    # Check if level-up choices are already present (exact IDs required by protocol)
    has_level_up_now = _find_choice("level_up_now") is not None
    has_continue_adventuring = _find_choice("continue_adventuring") is not None

    # ALWAYS enforce freeze_time on any existing level-up choices
    # (LLM might provide choices without freeze_time flag)
    # This must happen BEFORE the early return to handle edge case where
    # only one choice is provided - we still need to enforce freeze_time on it
    modified = False
    enforced_keys: list[str] = []
    # Use `is not True` to handle legacy string values like "false" from Firestore
    # which would be truthy but shouldn't prevent enforcement
    level_up_choice = _find_choice("level_up_now")
    if (
        isinstance(level_up_choice, dict)
        and level_up_choice.get("freeze_time") is not True
    ):
        level_up_choice["freeze_time"] = True
        enforced_keys.append("level_up_now")
        modified = True
    continue_choice = _find_choice("continue_adventuring")
    if (
        isinstance(continue_choice, dict)
        and continue_choice.get("freeze_time") is not True
    ):
        continue_choice["freeze_time"] = True
        enforced_keys.append("continue_adventuring")
        modified = True
    if modified:
        logging_util.info(
            "📈 SERVER_LEVELUP_INJECTION: Enforced freeze_time on "
            f"LLM-provided level-up choices ({', '.join(enforced_keys)})"
        )

    if has_level_up_now and has_continue_adventuring:
        # Already has the required choices with freeze_time enforced.
        # Normalize to array-of-objects and ensure level_up_now is first.
        result = campaign_upgrade.normalize_choices_to_array(planning_block)
        _ensure_level_up_first(result)
        return result

    # Inject missing level-up choices
    logging_util.info(
        f"📈 SERVER_LEVELUP_INJECTION: Injecting level-up choices for level {new_level} "
        f"(had level_up_now={has_level_up_now}, continue_adventuring={has_continue_adventuring})"
    )

    if not has_level_up_now:
        choices.append(
            {
                "id": "level_up_now",
                "text": f"Level Up to Level {new_level}",
                "description": f"Apply level {new_level} {player_class} benefits immediately",
                "risk_level": "safe",
                "freeze_time": True,  # Level-up is a meta-game decision, no in-game time passes
            }
        )

    if not has_continue_adventuring:
        choices.append(
            {
                "id": "continue_adventuring",
                "text": "Continue Adventuring",
                "description": "Level up later and continue the story",
                "risk_level": "safe",
                "freeze_time": True,  # Deferring level-up is also a meta-game decision
            }
        )

    # Add thinking if not present
    if "thinking" not in planning_block:
        planning_block["thinking"] = (
            f"Level-up to {new_level} is available. "
            "The player can level up now or continue adventuring."
        )

    # Normalize choices to array-of-objects for the frontend schema.
    result = campaign_upgrade.normalize_choices_to_array(planning_block)

    # Enforce level_up_now as the FIRST choice so the level-up prompt is
    # always prominently shown regardless of LLM ordering or injection order.
    _ensure_level_up_first(result)

    return result


def _inject_modal_finish_choice_if_needed(
    planning_block: dict[str, Any] | str | None,
    game_state_dict: dict[str, Any],
) -> dict[str, Any] | str | None:
    """Ensure modal flows always include a canonical finish choice as the last option."""
    custom_state_raw = game_state_dict.get("custom_campaign_state")
    custom_state = custom_state_raw if isinstance(custom_state_raw, dict) else {}
    rewards_pending_raw = game_state_dict.get("rewards_pending")
    rewards_pending = (
        rewards_pending_raw if isinstance(rewards_pending_raw, dict) else {}
    )

    # Capture fresh signal from rewards_pending before applying stale flag guards.
    level_up_in_progress_value = custom_state.get("level_up_in_progress")
    level_up_pending_value = custom_state.get("level_up_pending")
    level_up_from_rewards_value = rewards_pending.get("level_up_available")

    level_up_in_progress_flag = _is_state_flag_true(level_up_in_progress_value)
    level_up_pending_flag = _is_state_flag_true(level_up_pending_value)
    level_up_from_rewards_flag = _is_state_flag_true(level_up_from_rewards_value)

    level_up_active = (
        level_up_in_progress_flag or level_up_pending_flag or level_up_from_rewards_flag
    )

    # Apply same stale flag guards as get_agent_for_input
    # to ensure consistent level-up active detection across routing and injection.
    # Explicit False flags ALWAYS take precedence over stale rewards_pending data
    if _is_state_flag_false(level_up_in_progress_value):
        # Explicitly False (not just missing) - stale guard
        # This takes precedence over any stale rewards_pending.level_up_available signal
        level_up_active = False

    if _is_state_flag_false(level_up_pending_value) and not level_up_in_progress_flag:
        # Pending explicitly False AND not actively in progress - stale guard
        # This takes precedence over any stale rewards_pending.level_up_available signal
        level_up_active = False

    # XP-based stale guard: pending flag alone should not reactivate level-up when
    # XP is below threshold and there is no active rewards_pending signal.
    if (
        level_up_active
        and level_up_pending_flag
        and not level_up_in_progress_flag
        and not level_up_from_rewards_flag
    ):
        player_data = game_state_dict.get("player_character_data") or {}
        if isinstance(player_data, dict):
            current_level = coerce_int(player_data.get("level"), 1)
            current_level = max(1, current_level)
            current_xp = _extract_xp_robust(player_data)
            next_level_xp = constants.get_xp_for_level(current_level + 1)
            if current_xp < next_level_xp:
                logging_util.info(
                    "🔓 MODAL_FINISH_STALE_FLAG: Ignoring stale level_up_pending "
                    "(XP below next-level threshold and no rewards_pending signal)"
                )
                level_up_active = False

    level_up_exited = bool(
        custom_state.get("level_up_complete") or custom_state.get("level_up_cancelled")
    )
    character_creation_active = bool(custom_state.get("character_creation_in_progress"))

    if level_up_active and not level_up_exited:
        finish_key = "finish_level_up_return_to_game"
        finish_choice = {
            "text": "Finish Level-Up and Return to Game",
            "description": (
                "Complete level-up now, apply all selected updates, and return to active gameplay"
            ),
            "risk_level": "safe",
            "freeze_time": True,
        }
        mode_label = "level_up"
    elif character_creation_active:
        finish_key = "finish_character_creation_start_game"
        finish_choice = {
            "text": "Finish Character Creation and Start Game",
            "description": "Finalize this character and start the adventure.",
            "risk_level": "safe",
        }
        mode_label = "character_creation"
    else:
        if isinstance(planning_block, str):
            try:
                return json.loads(planning_block) if planning_block.strip() else None
            except (json.JSONDecodeError, TypeError):
                return None
        return planning_block

    planning_block = campaign_upgrade.normalize_planning_block_choices(
        planning_block, log_prefix="✅ SERVER_MODAL_FINISH_INJECTION"
    )
    choices = planning_block["choices"]
    if not isinstance(choices, list):
        choices = []
        planning_block["choices"] = choices

    # Remove ONLY the exact canonical finish key (by id), then append it last.
    # Do not remove other finish-ish options the LLM might generate.
    existing_finish_choice: dict[str, Any] | None = None
    reordered_choices: list[dict[str, Any]] = []
    for existing in choices:
        if not isinstance(existing, dict):
            continue
        if existing.get("id") == finish_key:
            if existing_finish_choice is None:
                existing_finish_choice = dict(existing)
            continue
        reordered_choices.append(existing)

    if isinstance(existing_finish_choice, dict):
        merged_choice = {**finish_choice, **existing_finish_choice}
        # Server-owned presentation: keep canonical text/description stable.
        merged_choice["id"] = finish_key
        merged_choice["text"] = finish_choice["text"]
        merged_choice["description"] = finish_choice["description"]
        finish_choice = merged_choice
    else:
        finish_choice = {**finish_choice, "id": finish_key}

    reordered_choices.append(finish_choice)
    planning_block["choices"] = reordered_choices

    if "thinking" not in planning_block or not planning_block.get("thinking"):
        planning_block["thinking"] = (
            "Provide the remaining choices for this modal flow. "
            f"Always include the {mode_label} finish option as the final choice."
        )

    # Normalize choices to array-of-objects for the frontend schema.
    return campaign_upgrade.normalize_choices_to_array(planning_block)


def _inject_campaign_upgrade_choice_if_needed(
    planning_block: dict[str, Any] | str | None,
    game_state_dict: dict[str, Any],
    agent_mode: str | None,
) -> dict[str, Any] | str | None:
    return campaign_upgrade.inject_campaign_upgrade_choice_if_needed(
        planning_block, game_state_dict, agent_mode
    )


def _inject_levelup_narrative_if_needed(
    narrative: str | None,
    planning_block: dict[str, Any] | None,
    game_state_dict: dict[str, Any],
    rewards_box: dict[str, Any] | None = None,
) -> str:
    """
    Ensure level-up prompt/options/benefits are visible in narrative text.

    This prevents the "choices only in planning_block" failure mode where the
    UI might not render structured choices, leaving the player unaware of the
    available level-up and its benefits.
    """
    narrative_text = narrative or ""
    level_up_active, resolved_new_level, _ = _resolve_level_up_signal(
        game_state_dict, rewards_box
    )
    if not level_up_active:
        return narrative_text

    rewards_pending = game_state_dict.get("rewards_pending") or {}
    new_level = (
        resolved_new_level
        if resolved_new_level is not None
        else rewards_pending.get("new_level", "?")
    )
    player_data = game_state_dict.get("player_character_data") or {}
    current_level = player_data.get("level", "?")
    lower = narrative_text.lower()

    banner_present = "level up available!" in lower
    prompt_present = "would you like to level up" in lower
    immediate_present = (
        "level up immediately" in lower
        or "level up now" in lower
        or "level up to level" in lower
    )
    later_present = (
        "continue adventuring" in lower
        or "continue your journey" in lower
        or "continue the adventure" in lower
    )
    continue_difference_present = ("continue" in lower or "continuing" in lower) and (
        "defer" in lower
        or "later" in lower
        or "remain level" in lower
        or "stay level" in lower
    )
    benefit_keywords = (
        "gain",
        "unlock",
        "bonus",
        "increase",
        "extra",
        "improve",
        "add",
        "advantage",
        "feature",
        "proficiency",
        "hp",
        "hit points",
    )
    benefits_present = any(k in lower for k in benefit_keywords)

    if (
        banner_present
        and prompt_present
        and immediate_present
        and later_present
        and benefits_present
        and continue_difference_present
    ):
        return narrative_text

    lines: list[str] = []
    if not banner_present:
        lines.append(
            f"**LEVEL UP AVAILABLE!** You have earned enough experience to reach Level {new_level}!"
        )

    if not benefits_present:
        benefit_text = None
        if isinstance(planning_block, dict):
            choices = planning_block.get("choices")
            # Support both array-of-objects (normalized) and dict (legacy) formats
            if isinstance(choices, list):
                for choice in choices:
                    if isinstance(choice, dict) and choice.get("id") == "level_up_now":
                        description = choice.get("description")
                        if isinstance(description, str) and description.strip():
                            benefit_text = description.strip()
                        break
            elif isinstance(choices, dict):
                level_up_choice = choices.get("level_up_now", {})
                if isinstance(level_up_choice, dict):
                    description = level_up_choice.get("description")
                    if isinstance(description, str) and description.strip():
                        benefit_text = description.strip()
        if not benefit_text:
            benefit_text = (
                "Gain new class features, increased proficiency, and more HP."
            )
        lines.append(f"Benefits: {benefit_text}")

    if not prompt_present:
        lines.append("Would you like to level up now?")

    if not (immediate_present and later_present):
        lines.append("Options: 1. Level up immediately  2. Continue adventuring")

    if not continue_difference_present:
        lines.append(
            f"If you continue adventuring, you remain Level {current_level} and defer these benefits until you choose to level up."
        )

    if not lines:
        return narrative_text

    separator = "\n\n" if narrative_text.strip() else ""
    injected_block = "\n".join(lines)
    return f"{narrative_text}{separator}{injected_block}"


def _validate_monotonic_counters(
    updated_state_dict: dict[str, Any],
    original_state_dict: dict[str, Any] | None = None,
) -> None:
    """
    Validate that monotonic counters (XP, gold, territory, turn_number, faction_power) never decrease.

    Args:
        updated_state_dict: The game state dict after updates
        original_state_dict: Optional original state dict before updates.
            If None, validation is skipped (can't compare without baseline).

    Logs warnings if counters decrease, but does not auto-correct (requires manual review).
    """
    if original_state_dict is None:
        return  # Can't validate without baseline

    def _extract_int_value(data: dict[str, Any], path: list[str]) -> int | None:
        """Extract integer value from nested dict path, returning None if not found."""
        current = data
        for key in path:
            if not isinstance(current, dict):
                return None
            current = current.get(key)
            if current is None:
                return None
        if isinstance(current, (int, float)):
            return int(current)
        if isinstance(current, str):
            try:
                return int(float(current.replace(",", "").strip()))
            except (ValueError, AttributeError):
                return None
        return None

    # Extract XP from player_character_data
    original_xp = (
        _extract_int_value(
            original_state_dict,
            ["data", "game_state", "player_character_data", "experience", "current"],
        )
        or _extract_int_value(
            original_state_dict, ["data", "game_state", "player_character_data", "xp"]
        )
        or _extract_int_value(
            original_state_dict,
            ["data", "game_state", "player_character_data", "xp_current"],
        )
    )
    updated_xp = (
        _extract_int_value(
            updated_state_dict,
            ["data", "game_state", "player_character_data", "experience", "current"],
        )
        or _extract_int_value(
            updated_state_dict, ["data", "game_state", "player_character_data", "xp"]
        )
        or _extract_int_value(
            updated_state_dict,
            ["data", "game_state", "player_character_data", "xp_current"],
        )
    )

    if original_xp is not None and updated_xp is not None and updated_xp < original_xp:
        logging_util.warning(
            f"🔥🔴 MONOTONIC VIOLATION: XP decreased from {original_xp} to {updated_xp}. "
            f"This is impossible - XP should only increase or remain stable."
        )

    # Extract character gold (player_character_data.gold)
    original_char_gold = _extract_int_value(
        original_state_dict, ["data", "game_state", "player_character_data", "gold"]
    ) or _extract_int_value(
        original_state_dict,
        ["data", "game_state", "player_character_data", "resources", "gold"],
    )
    updated_char_gold = _extract_int_value(
        updated_state_dict, ["data", "game_state", "player_character_data", "gold"]
    ) or _extract_int_value(
        updated_state_dict,
        ["data", "game_state", "player_character_data", "resources", "gold"],
    )

    # Note: Character gold CAN decrease (spending), so we only warn if it decreases dramatically
    # (>50% drop) which might indicate a bug
    if (
        original_char_gold is not None
        and updated_char_gold is not None
        and original_char_gold > 0
        and updated_char_gold < original_char_gold * 0.5
    ):
        logging_util.warning(
            f"⚠️ MONOTONIC WARNING: Character gold dropped dramatically from {original_char_gold} "
            f"to {updated_char_gold} (>50% decrease). Verify this is intentional spending."
        )

    # Extract faction gold
    original_faction_gold = _extract_int_value(
        original_state_dict,
        ["custom_campaign_state", "faction_minigame", "resources", "gold"],
    )
    updated_faction_gold = _extract_int_value(
        updated_state_dict,
        ["custom_campaign_state", "faction_minigame", "resources", "gold"],
    )

    # Note: Gold CAN decrease (spending), so we only warn if it decreases dramatically
    # (>50% drop) which might indicate a bug
    if (
        original_faction_gold is not None
        and updated_faction_gold is not None
        and original_faction_gold > 0
        and updated_faction_gold < original_faction_gold * 0.5
    ):
        logging_util.warning(
            f"⚠️ MONOTONIC WARNING: Faction gold dropped dramatically from {original_faction_gold} "
            f"to {updated_faction_gold} (>50% decrease). Verify this is intentional spending."
        )

    # Extract territory
    original_territory = _extract_int_value(
        original_state_dict,
        ["custom_campaign_state", "faction_minigame", "resources", "territory"],
    )
    updated_territory = _extract_int_value(
        updated_state_dict,
        ["custom_campaign_state", "faction_minigame", "resources", "territory"],
    )

    if (
        original_territory is not None
        and updated_territory is not None
        and updated_territory < original_territory
    ):
        logging_util.warning(
            f"⚠️ MONOTONIC WARNING: Territory decreased from {original_territory} to {updated_territory}. "
            f"Territory should only increase (conquest) or remain stable (losses are tracked separately)."
        )

    # Extract turn_number
    original_turn = _extract_int_value(
        original_state_dict,
        ["custom_campaign_state", "faction_minigame", "turn_number"],
    )
    updated_turn = _extract_int_value(
        updated_state_dict,
        ["custom_campaign_state", "faction_minigame", "turn_number"],
    )

    if (
        original_turn is not None
        and updated_turn is not None
        and updated_turn < original_turn
    ):
        logging_util.warning(
            f"🔥🔴 MONOTONIC VIOLATION: Turn number decreased from {original_turn} to {updated_turn}. "
            f"This is impossible - turn numbers should only increase."
        )

    # Extract faction_power (FP)
    original_fp = _extract_int_value(
        original_state_dict,
        ["custom_campaign_state", "faction_minigame", "faction_power"],
    )
    updated_fp = _extract_int_value(
        updated_state_dict,
        ["custom_campaign_state", "faction_minigame", "faction_power"],
    )

    if original_fp is not None and updated_fp is not None and updated_fp < original_fp:
        logging_util.warning(
            f"🔥🔴 MONOTONIC VIOLATION: Faction Power (FP) decreased from {original_fp:,} to {updated_fp:,}. "
            f"FP should only increase unless explicit losses occur (combat casualties, territory loss)."
        )


def _inject_spicy_mode_choice_if_needed(
    planning_block: dict[str, Any] | str | None,
    llm_response_obj: Any,
    user_settings: dict[str, Any] | None,
) -> dict[str, Any] | str | None:
    """
    Server-side injection of spicy mode toggle choices based on LLM detection.

    When the LLM detects sexual/intimate content, it sets recommend_spicy_mode=true.
    This function injects a choice to enable spicy mode in the planning block.

    When spicy mode is already enabled and the LLM detects the scene is ending,
    it sets recommend_exit_spicy_mode=true. This function injects a choice to
    disable spicy mode.

    Args:
        planning_block: The planning_block from LLM response
        llm_response_obj: The structured response object (has recommend_* fields)
        user_settings: Current user settings dict (to check if spicy_mode is enabled)

    Returns:
        The planning_block dict with spicy mode choices injected if needed,
        or None if input was None and no injection needed.
    """
    if llm_response_obj is None:
        return planning_block

    # Get the recommendation flags from the LLM response
    recommend_spicy = getattr(llm_response_obj, "recommend_spicy_mode", None)
    recommend_exit_spicy = getattr(llm_response_obj, "recommend_exit_spicy_mode", None)

    # Check if spicy mode is currently enabled in user settings
    current_spicy_mode = (user_settings or {}).get("spicy_mode", False)

    # Determine if we need to inject any choices
    should_inject_enable = recommend_spicy is True and not current_spicy_mode
    should_inject_disable = recommend_exit_spicy is True and current_spicy_mode

    if not should_inject_enable and not should_inject_disable:
        # No injection needed; return the planning_block unchanged
        return planning_block

    planning_block = campaign_upgrade.normalize_planning_block_choices(
        planning_block, log_prefix="🌶️ SERVER_SPICY_INJECTION"
    )
    choices = planning_block["choices"]
    if not isinstance(choices, list):
        choices = []
        planning_block["choices"] = choices

    def _has_choice(target_id: str) -> bool:
        for existing in choices:
            if isinstance(existing, dict) and existing.get("id") == target_id:
                return True
        return False

    # Inject enable spicy mode choice
    if should_inject_enable and not _has_choice("enable_spicy_mode"):
        logging_util.info(
            "🌶️ SERVER_SPICY_INJECTION: Injecting enable_spicy_mode choice "
            "(LLM detected intimate content)"
        )
        choices.append(
            {
                "id": "enable_spicy_mode",
                "text": "Enable Spicy Mode",
                "description": "Switch to mature content mode for intimate scenes. Uses a specialized AI model.",
                "risk_level": "safe",
            }
        )

    # Inject disable spicy mode choice
    if should_inject_disable and not _has_choice("disable_spicy_mode"):
        logging_util.info(
            "🌶️ SERVER_SPICY_INJECTION: Injecting disable_spicy_mode choice "
            "(LLM detected scene ending)"
        )
        choices.append(
            {
                "id": "disable_spicy_mode",
                "text": "Exit Spicy Mode",
                "description": "Return to normal mode. The intimate scene appears to be concluding.",
                "risk_level": "safe",
            }
        )

    # Add thinking if not present
    if "thinking" not in planning_block:
        if should_inject_enable:
            planning_block["thinking"] = (
                "The scene is progressing toward intimate content. "
                "Spicy Mode is available for mature content handling."
            )
        elif should_inject_disable:
            planning_block["thinking"] = (
                "The intimate scene appears to be concluding. "
                "You can exit Spicy Mode to return to normal gameplay."
            )

    return planning_block


def validate_game_state_updates(
    updated_state_dict: dict[str, Any],
    new_time: dict[str, Any] | None = None,
    original_time: dict[str, Any] | None = None,
    original_state_dict: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate and auto-correct game state updates.

    Applies XP/level validation and time monotonicity checks to the state dict.
    This should be called after update_state_with_changes() but before
    persisting to Firestore.

    Args:
        updated_state_dict: The game state dict after updates are applied
        new_time: Optional new world_time to validate for monotonicity
        original_time: Optional original world_time from before the update.
            Required for accurate time monotonicity checking since
            updated_state_dict already has new_time merged in.
        original_state_dict: Optional original state dict before updates.
            Used for monotonic counter validation (XP, gold, territory, turn_number).

    Returns:
        The validated (and potentially corrected) state dict

    Validation Applied:
        1. XP/Level consistency: Ensures level matches XP thresholds (D&D 5e)
        2. Missing level persistence: Computes and saves level if absent
        3. Type coercion: Handles string values from JSON/LLM responses
        4. Time monotonicity: Warns if time goes backward (if new_time provided)
        5. Monotonic counters: Warns if XP, territory, or turn_number decrease (if original_state_dict provided)
    """
    # Create temporary GameState for validation
    temp_state = GameState.from_dict(updated_state_dict)
    if temp_state is None:
        logging_util.warning(
            "validate_game_state_updates: Could not create GameState, skipping validation"
        )
        return updated_state_dict

    # Validate XP/Level consistency (auto-corrects mismatches)
    xp_result = temp_state.validate_xp_level(strict=False)
    if xp_result.get("corrected"):
        logging_util.info(
            f"XP/Level validation corrected: expected_level={xp_result.get('expected_level')}, "
            f"provided_level={xp_result.get('provided_level')}"
        )
    if xp_result.get("computed_level"):
        logging_util.info(
            f"XP/Level validation computed missing level: {xp_result.get('computed_level')}"
        )

    # Validate monotonic counters (XP, gold, territory, turn_number)
    _validate_monotonic_counters(updated_state_dict, original_state_dict)

    # Validate time monotonicity if new_time is provided
    # Use original_time for comparison if provided, otherwise compare against
    # temp_state (which already has new_time merged, so it would compare to itself)
    if new_time and original_time is not None:
        # Temporarily set the original time for accurate comparison
        if temp_state.world_data:
            saved_time = temp_state.world_data.get("world_time")
            temp_state.world_data["world_time"] = original_time
            time_result = temp_state.validate_time_monotonicity(new_time, strict=False)
            # Restore the new time after validation
            temp_state.world_data["world_time"] = saved_time
            if time_result.get("warning"):
                logging_util.warning(
                    f"Time validation warning: {time_result.get('message')}"
                )
    elif new_time:
        # Fallback: compare against current state (may be inaccurate if already merged)
        time_result = temp_state.validate_time_monotonicity(new_time, strict=False)
        if time_result.get("warning"):
            logging_util.warning(
                f"Time validation warning: {time_result.get('message')}"
            )

    # Return the validated state dict (includes any corrections made)
    return temp_state.to_dict()


def _prepare_game_state(
    user_id: UserId, campaign_id: CampaignId
) -> tuple[GameState, bool, int]:
    """
    Load and prepare game state, including legacy cleanup.
    Extracted from main.py to maintain exact functionality.
    """
    current_game_state_doc = firestore_service.get_campaign_game_state(
        user_id, campaign_id
    )

    if current_game_state_doc:
        current_game_state = GameState.from_dict(current_game_state_doc.to_dict())
        if current_game_state is None:
            logging_util.warning(
                "PREPARE_GAME_STATE: GameState.from_dict returned None, using default state"
            )
            current_game_state = GameState(user_id=user_id)
    else:
        # game_states subcollection absent — campaign predates it or write failed.
        # Create an initial state so future turns have a real base (rev-lwuz5 lazy-init).
        current_game_state = GameState(user_id=user_id)
        logging_util.warning(
            "PREPARE_GAME_STATE: game_states subcollection absent for campaign %s — "
            "creating initial state. Living World will use empty context this turn.",
            campaign_id,
        )
        firestore_service.update_campaign_game_state(
            user_id, campaign_id, current_game_state.to_dict()
        )

    # Perform cleanup on a dictionary copy
    cleaned_state_dict, was_cleaned, num_cleaned = _cleanup_legacy_state(
        current_game_state.to_dict()
    )

    # Ensure faction_minigame suggestion tracking fields exist
    if "custom_campaign_state" not in cleaned_state_dict:
        cleaned_state_dict["custom_campaign_state"] = {}
    custom_state = cleaned_state_dict["custom_campaign_state"]
    if not isinstance(custom_state, dict):
        custom_state = {}
        cleaned_state_dict["custom_campaign_state"] = custom_state

    if "faction_minigame" not in custom_state:
        custom_state["faction_minigame"] = {}
    faction_minigame = custom_state["faction_minigame"]
    if not isinstance(faction_minigame, dict):
        faction_minigame = {}
        custom_state["faction_minigame"] = faction_minigame

    # Ensure suggestion tracking fields exist (default to False if missing)
    if "suggestion_given" not in faction_minigame:
        faction_minigame["suggestion_given"] = False
    if "strong_suggestion_given" not in faction_minigame:
        faction_minigame["strong_suggestion_given"] = False

    # Archive finished combat to history and clear active state at action START
    # This prevents stale combat_summary from being seen by LLM on next action
    # while allowing the previous action's response to include combat_summary
    #
    # IMPORTANT: Only clean if rewards_processed=True, otherwise RewardsAgent
    # needs to trigger first to display the rewards box and process XP/loot.
    combat_state = cleaned_state_dict.get("combat_state", {})
    # Use centralized constant for combat finished phases
    combat_phase = combat_state.get("combat_phase", "")
    rewards_processed = combat_state.get("rewards_processed", False)

    if (
        not combat_state.get("in_combat", True)
        and combat_phase in constants.COMBAT_FINISHED_PHASES
        and combat_state.get("combat_summary")
    ):
        if not rewards_processed:
            # Keep combat state intact for RewardsAgent to trigger
            logging_util.info(
                f"Combat ended but rewards_processed=False, keeping combat_summary for RewardsAgent. "
                f"xp_awarded={combat_state['combat_summary'].get('xp_awarded')}"
            )
        else:
            # Rewards already processed, safe to archive and clean
            combat_history = combat_state.get("combat_history", [])
            archived_entry = {
                **combat_state["combat_summary"],
                "session_id": combat_state.get("combat_session_id"),
                "archived_at": datetime.now(timezone.utc).isoformat(),  # noqa: UP017
            }
            combat_history.append(archived_entry)

            logging_util.info(
                f"Archived finished combat to history: session_id={combat_state.get('combat_session_id')}, "
                f"xp_awarded={combat_state['combat_summary'].get('xp_awarded')}"
            )

            # Clear active combat state for clean LLM context
            combat_state["combat_history"] = combat_history
            combat_state["combat_summary"] = None
            combat_state["combat_phase"] = "idle"
            combat_state["combat_session_id"] = None
            combat_state["combatants"] = {}
            combat_state["initiative_order"] = []
            combat_state["current_round"] = None
            combat_state["rewards_processed"] = False  # Reset for next combat
            cleaned_state_dict["combat_state"] = combat_state
            # Clear reward-related pending_system_corrections - they've been consumed by the LLM
            # which fixed the issue (evidenced by rewards_processed=True)
            pending_corrections = _normalize_system_corrections(
                cleaned_state_dict.get("pending_system_corrections")
            )

            remaining_corrections = [
                message
                for message in pending_corrections
                if not _is_reward_correction(message)
            ]
            if remaining_corrections:
                cleaned_state_dict["pending_system_corrections"] = remaining_corrections
            else:
                cleaned_state_dict.pop("pending_system_corrections", None)
            was_cleaned = True

            # Persist the cleaned state immediately so LLM sees clean context
            firestore_service.update_campaign_game_state(
                user_id, campaign_id, cleaned_state_dict
            )

    if was_cleaned:
        # Ensure user_id is preserved in cleaned state
        cleaned_state_dict["user_id"] = user_id
        current_game_state = GameState.from_dict(cleaned_state_dict)
        if current_game_state is None:
            logging_util.error(
                "PREPARE_GAME_STATE: GameState.from_dict returned None after cleanup, using default state"
            )
            current_game_state = GameState(user_id=user_id)
        firestore_service.update_campaign_game_state(
            user_id, campaign_id, current_game_state.to_dict()
        )
        logging_util.info(
            f"Cleaned {num_cleaned} legacy state entries for campaign {campaign_id}"
        )

    return current_game_state, was_cleaned, num_cleaned


def _compute_spicy_mode_exit_settings(user_settings: dict[str, Any]) -> dict[str, Any]:
    """
    Compute settings updates when exiting spicy mode.

    Detects if the user manually changed their LLM provider/model while in spicy mode.
    If so, preserves the manual change instead of restoring pre-spicy settings.

    Args:
        user_settings: Current user settings dict (must have spicy_mode=True)

    Returns:
        Dict of settings to update when exiting spicy mode
    """
    settings_to_update = {"spicy_mode": False}

    current_provider = user_settings.get("llm_provider", "gemini")
    pre_spicy_provider = user_settings.get("pre_spicy_provider", "gemini")
    pre_spicy_model = user_settings.get("pre_spicy_model")

    # Detect manual provider change during spicy mode
    # User manually changed if:
    # 1. Provider changed from openrouter to something else, OR
    # 2. OpenRouter model changed from SPICY_OPENROUTER_MODEL to something else
    manual_provider_change = current_provider != "openrouter"
    manual_model_change = (
        current_provider == "openrouter"
        and user_settings.get("openrouter_model") != constants.SPICY_OPENROUTER_MODEL
    )

    if manual_provider_change or manual_model_change:
        # User manually changed provider/model during spicy mode
        # Preserve their choice, don't restore pre-spicy settings
        logging_util.info(
            f"🌶️ SPICY_EXIT: Preserving manual change to {current_provider} "
            f"(was {pre_spicy_provider} before spicy mode)"
        )
        # Only update spicy_mode flag, keep everything else as-is
        return settings_to_update

    # No manual change detected - restore pre-spicy settings
    logging_util.info(
        f"🌶️ SPICY_EXIT: Restoring pre-spicy provider {pre_spicy_provider}"
    )

    if pre_spicy_provider == "openrouter":
        settings_to_update.update(
            {
                "llm_provider": pre_spicy_provider,
                "openrouter_model": pre_spicy_model
                or constants.DEFAULT_OPENROUTER_MODEL,
            }
        )
    elif pre_spicy_provider == "cerebras":
        settings_to_update.update(
            {
                "llm_provider": pre_spicy_provider,
                "cerebras_model": pre_spicy_model or constants.DEFAULT_CEREBRAS_MODEL,
            }
        )
    elif pre_spicy_provider == "openclaw":
        if (
            isinstance(pre_spicy_model, str)
            and pre_spicy_model.startswith("openclaw/")
            and len(pre_spicy_model) > len("openclaw/")
        ):
            model_to_restore = pre_spicy_model
        else:
            model_to_restore = constants.DEFAULT_OPENCLAW_MODEL
        settings_to_update.update(
            {
                "llm_provider": pre_spicy_provider,
                "openclaw_model": model_to_restore,
            }
        )
    else:
        settings_to_update.update(
            {
                "llm_provider": pre_spicy_provider,
                "gemini_model": pre_spicy_model or constants.DEFAULT_GEMINI_MODEL,
            }
        )

    return settings_to_update


def _prepare_game_state_with_user_settings(
    user_id: UserId, campaign_id: CampaignId
) -> tuple[GameState, bool, int, dict[str, Any] | None]:
    """
    Prepare game state and fetch user settings in the same worker thread.

    This reduces thread scheduling overhead in hot paths that already need to
    load game state, while keeping all blocking calls off the event loop.
    """
    current_game_state, was_cleaned, num_cleaned = _prepare_game_state(
        user_id, campaign_id
    )
    user_settings = get_user_settings(user_id)
    if not isinstance(user_settings, dict):
        user_settings = None
    current_game_state.user_settings = user_settings
    return current_game_state, was_cleaned, num_cleaned, user_settings


def _persist_turn_to_firestore(
    user_id: UserId,
    campaign_id: CampaignId,
    *,
    mode: str,
    user_input: str,
    ai_response_text: str,
    structured_fields: dict[str, Any],
    updated_game_state_dict: dict[str, Any],
    sequence_id: int | None = None,
    user_scene_number: int | None = None,
) -> None:
    """
    Persist a completed turn (state + story entries) in a single worker thread.

    This reduces asyncio.to_thread() scheduling overhead in hot paths while
    keeping all Firestore I/O off the event loop.
    """
    firestore_service.update_campaign_game_state(
        user_id, campaign_id, updated_game_state_dict
    )
    if isinstance(structured_fields, dict):
        if sequence_id is not None and "sequence_id" not in structured_fields:
            structured_fields["sequence_id"] = sequence_id
        if (
            user_scene_number is not None
            and "user_scene_number" not in structured_fields
        ):
            structured_fields["user_scene_number"] = user_scene_number

        # Embed a compact game_state snapshot for per-entry traceability (rev-lw5lk).
        # Omit bulk fields (npc_data, entity_tracking, item_registry) to stay well
        # under the Firestore 1 MB document limit — those are in game_states/current_state.
        _custom = updated_game_state_dict.get("custom_campaign_state", {})
        structured_fields["game_state_snapshot"] = {
            "turn_number": updated_game_state_dict.get("turn_number"),
            "player_turn": updated_game_state_dict.get("player_turn"),
            "player_character_data": {
                k: updated_game_state_dict.get("player_character_data", {}).get(k)
                for k in ("hp_current", "hp_max", "level", "experience", "name")
                if updated_game_state_dict.get("player_character_data", {}).get(k)
                is not None
            },
            "custom_campaign_state": (
                {k: v for k, v in _custom.items() if k not in {"story_history"}}
                if isinstance(_custom, dict)
                else {}
            ),
        }

    firestore_service.add_story_entry(
        user_id,
        campaign_id,
        constants.ACTOR_USER,
        user_input,
        mode,
    )
    firestore_service.add_story_entry(
        user_id,
        campaign_id,
        constants.ACTOR_GEMINI,
        ai_response_text,
        mode,  # Preserve mode so think/god responses can be identified when story is retrieved
        structured_fields,
    )


def _prefix_scene_number_in_narrative(
    narrative_text: str, user_scene_number: int | None
) -> str:
    """Prefix persisted AI narrative with visible Scene # when available."""
    if (
        not isinstance(narrative_text, str)
        or not narrative_text
        or not isinstance(user_scene_number, int)
        or user_scene_number <= 0
    ):
        return narrative_text

    stripped = narrative_text.lstrip()
    if re.match(r"^Scene\s+#\d+:", stripped, re.IGNORECASE):
        return narrative_text

    return f"Scene #{user_scene_number}: {stripped}"


def _update_campaign_game_state(
    user_id: UserId, campaign_id: CampaignId, state_dict: dict[str, Any]
) -> None:
    firestore_service.update_campaign_game_state(user_id, campaign_id, state_dict)


def _load_campaign_and_continue_story(
    user_id: UserId,
    campaign_id: CampaignId,
    *,
    llm_input: str,
    mode: str,
    current_game_state: GameState,
    include_raw_llm_payloads: bool,
) -> tuple[dict[str, Any] | None, list[dict[str, Any]], Any]:
    """Fetch campaign data/story context and run provider-appropriate continuation."""
    campaign_data, story_context = firestore_service.get_campaign_by_id(
        user_id, campaign_id
    )
    if not campaign_data:
        return None, [], None

    story_context = story_context or []
    _maybe_force_level_up_character_creation(
        llm_input, story_context, current_game_state
    )
    selected_prompts = campaign_data.get("selected_prompts", [])
    use_default_world = campaign_data.get("use_default_world", False)

    provider_selection = llm_service.select_provider_and_model(user_id)
    use_streaming_path = (
        provider_selection.provider == constants.LLM_PROVIDER_GEMINI
        and provider_selection.model.startswith("gemini-3")
    )
    # Keep test-bypass flows on the legacy codepath unless explicitly overridden.
    # Many end-to-end unit tests patch non-streaming provider calls and expect that path.
    testing_auth_bypass = os.environ.get("TESTING_AUTH_BYPASS", "").lower() == "true"
    mock_services_mode = os.environ.get("MOCK_SERVICES_MODE", "").lower() == "true"
    force_streaming_in_bypass = (
        os.environ.get("FORCE_STREAMING_PATH", "").lower() == "true"
    )
    if testing_auth_bypass and not force_streaming_in_bypass:
        use_streaming_path = False
    if mock_services_mode and not force_streaming_in_bypass:
        # Mock mode is deterministic in non-streaming path for smoke + unit testing.
        use_streaming_path = False

    if not use_streaming_path:
        logging_util.info(
            "↩️ NON_STREAMING_PATH: Using continue_story for provider/model "
            f"{provider_selection.provider}/{provider_selection.model}"
        )
        llm_response_obj = llm_service.continue_story(
            llm_input,
            mode,
            story_context,
            current_game_state,
            selected_prompts,
            use_default_world,
            user_id,
            campaign_id=campaign_id,
            include_raw_llm_payloads=include_raw_llm_payloads,
        )
        return campaign_data, story_context, llm_response_obj

    logging_util.info(
        "🌊 STREAMING_PATH: Using continue_story_streaming for provider/model "
        f"{provider_selection.provider}/{provider_selection.model}"
    )
    # Persistence contract:
    # - This function only builds an LLMResponse from streaming output (no Firestore writes).
    # - Callers persist exactly once (user + AI) in the normal world_logic flow.
    stream_done_payload: dict[str, Any] | None = None
    stream_error_payload: dict[str, Any] | None = None

    for event in llm_service.continue_story_streaming(
        llm_input,
        mode,
        story_context,
        current_game_state,
        selected_prompts,
        use_default_world,
        user_id,
        campaign_id=campaign_id,
    ):
        event_type = getattr(event, "type", None)
        event_payload = getattr(event, "payload", None)
        if not isinstance(event_payload, dict):
            event_payload = {}
        if event_type == "done":
            stream_done_payload = event_payload
        elif event_type == "error":
            stream_error_payload = event_payload

    if stream_done_payload is None:
        error_message = "Streaming generation failed before completion."
        if stream_error_payload and stream_error_payload.get("message"):
            error_message = str(stream_error_payload.get("message"))
        raise llm_service.LLMRequestError(error_message, status_code=422)

    raw_response_text = stream_done_payload.get("raw_response_text")
    if not isinstance(raw_response_text, str) or not raw_response_text.strip():
        raw_response_text = ""

    # Build response object from streaming output (single execution path).
    structured_response_obj = None
    if raw_response_text:
        try:
            _, structured_response_obj = llm_service.parse_structured_response(
                raw_response_text,
                requires_action_resolution=False,
            )
        except Exception as e:
            logging_util.warning(
                f"STREAMING_ONLY_PATH: Failed to parse streaming raw response: {e}"
            )

    narrative_text = stream_done_payload.get("full_narrative")
    if not isinstance(narrative_text, str):
        narrative_text = ""

    model_used = stream_done_payload.get("model_used")
    if not isinstance(model_used, str) or not model_used.strip():
        model_used = provider_selection.model
    provider_used = stream_done_payload.get("provider_used")
    if not isinstance(provider_used, str) or not provider_used.strip():
        provider_used = provider_selection.provider
    agent_mode = stream_done_payload.get("agent_mode")
    if not isinstance(agent_mode, str):
        agent_mode = None

    if structured_response_obj is not None:
        llm_response_obj = llm_service.LLMResponse.create_from_structured_response(
            structured_response_obj,
            model=model_used,
            combined_narrative_text=narrative_text,
            provider=provider_used,
            agent_mode=agent_mode,
            raw_response_text=raw_response_text,
        )
    else:
        llm_response_obj = llm_service.LLMResponse.create_legacy(
            narrative_text,
            model=model_used,
            provider=provider_used,
            agent_mode=agent_mode,
            raw_response_text=raw_response_text,
        )

    # Preserve include_raw_llm_payloads compatibility for testing evidence.
    if include_raw_llm_payloads:
        metadata = llm_response_obj.processing_metadata
        if not isinstance(metadata, dict):
            metadata = {}
            llm_response_obj.processing_metadata = metadata
        metadata.setdefault("raw_response_text", raw_response_text)

    return campaign_data, story_context, llm_response_obj


def _maybe_force_level_up_character_creation(
    user_input: str,
    story_context: list[dict[str, Any]],
    current_game_state: GameState,
) -> None:
    """If user chose level_up_now, force CharacterCreationAgent for this request."""
    selected_choice = _get_selected_choice_from_story_context(user_input, story_context)
    if not selected_choice:
        return

    if selected_choice.get("key") != "level_up_now":
        return

    custom_state = getattr(current_game_state, "custom_campaign_state", None) or {}
    if not isinstance(custom_state, dict):
        custom_state = {}

    custom_state["level_up_pending"] = True
    custom_state["character_creation_in_progress"] = True
    custom_state.setdefault("character_creation_stage", "level_up")
    current_game_state.custom_campaign_state = custom_state
    logging_util.info(
        "🎭 LEVEL_UP_SELECTION: Forcing CharacterCreationAgent via level_up_pending"
    )


def _cleanup_legacy_state(
    state_dict: dict[str, Any],
) -> tuple[dict[str, Any], bool, int]:
    """
    Clean up legacy fields from game state.
    Extracted from main.py to maintain compatibility.
    """
    cleaned_dict = state_dict.copy()
    was_cleaned = False
    num_cleaned = 0

    # Define legacy fields that should be removed
    legacy_fields = [
        "party_data",  # Old party system
        "legacy_prompt_data",  # Old prompt format
        "deprecated_settings",  # Old settings format
    ]

    # Remove legacy fields
    for field in legacy_fields:
        if field in cleaned_dict:
            del cleaned_dict[field]
            was_cleaned = True
            num_cleaned += 1

    return cleaned_dict, was_cleaned, num_cleaned


def _strip_game_state_fields(
    story_entries: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Strip game state information from story entries when debug mode is OFF.
    Extracted from main.py to maintain compatibility.
    """
    if not story_entries:
        return story_entries

    # Fields to strip when debug mode is OFF
    game_state_fields = {
        "entities_mentioned",
        "entities",
        "state_updates",
        "debug_info",
    }

    stripped_story = []
    for entry in story_entries:
        # Create a copy without the game state fields
        stripped_entry = {
            key: value for key, value in entry.items() if key not in game_state_fields
        }
        stripped_story.append(stripped_entry)

    return stripped_story


def _has_visible_living_world_data(
    world_events: Any,
    faction_updates: Any,
    time_events: Any,
    rumors: Any,
    scene_event: Any,
    complications: Any,
) -> bool:
    """Return True when living-world payload would render in the frontend."""
    normalized_world_events = normalize_world_events_for_story_payload(world_events)
    has_background_events = (
        isinstance(normalized_world_events, dict)
        and isinstance(
            normalized_world_events.get("background_events"),
            list,
        )
        and any(
            isinstance(event, dict)
            for event in normalized_world_events.get("background_events", [])
        )
    )
    has_faction_updates = (
        isinstance(faction_updates, dict)
        and bool(faction_updates)
        and any(isinstance(update, dict) for update in faction_updates.values())
    )
    has_time_events = (
        isinstance(time_events, dict)
        and bool(time_events)
        and any(isinstance(event, dict) for event in time_events.values())
    )
    if isinstance(rumors, dict):
        if "append" in rumors:
            container = {"rumors": rumors}
            _normalize_append_list_field(container, "rumors")
            rumors = container["rumors"]
        else:
            rumors = [rumors]
    has_rumors = isinstance(rumors, list) and any(
        isinstance(rumor, dict) for rumor in rumors
    )
    has_scene_event = isinstance(scene_event, dict) and bool(
        scene_event.get("type")
        or scene_event.get("description")
        or scene_event.get("actor")
    )
    has_complications = isinstance(complications, dict) and (
        complications.get("triggered") is True
        or complications.get("triggered") == "true"
    )
    return bool(
        has_background_events
        or has_faction_updates
        or has_time_events
        or has_rumors
        or has_scene_event
        or has_complications
    )


def inject_persisted_living_world_fallback(
    story_entries: list[dict[str, Any]],
    game_state: dict[str, Any] | None,
    debug_mode: bool,
) -> list[dict[str, Any]]:
    """Inject persisted living-world state into matching Gemini scene entries on reload.

    Frontend rendering currently reads living-world updates from each story entry payload.
    Firestore persistence stores cumulative living-world state under game_state.world_events.
    On page reload, a story entry may not include its per-turn living-world delta.
    This helper bridges that gap by injecting scene-matching persisted payload into
    each Gemini entry that has no visible living-world content.
    """
    if not debug_mode or not story_entries or not isinstance(game_state, dict):
        return story_entries

    persisted_world_events = normalize_world_events_for_story_payload(
        game_state.get("world_events")
    )
    if not isinstance(persisted_world_events, dict):
        return story_entries

    persisted_faction_updates = game_state.get("faction_updates")
    if not isinstance(persisted_faction_updates, dict):
        persisted_faction_updates = persisted_world_events.get("faction_updates")

    persisted_time_events = game_state.get("time_events")
    if not isinstance(persisted_time_events, dict):
        persisted_time_events = persisted_world_events.get("time_events")

    persisted_rumors = game_state.get("rumors")
    if persisted_rumors is None:
        persisted_rumors = persisted_world_events.get("rumors")
    if isinstance(persisted_rumors, dict):
        if "append" in persisted_rumors:
            container = {"rumors": persisted_rumors}
            _normalize_append_list_field(container, "rumors")
            persisted_rumors = container["rumors"]
        else:
            persisted_rumors = [persisted_rumors]
    elif persisted_rumors is not None and not isinstance(persisted_rumors, list):
        persisted_rumors = [persisted_rumors]

    persisted_scene_event = game_state.get("scene_event")
    if not isinstance(persisted_scene_event, dict):
        persisted_scene_event = persisted_world_events.get("scene_event")

    persisted_complications = game_state.get("complications")
    if not isinstance(persisted_complications, dict):
        persisted_complications = persisted_world_events.get("complications")

    if not _has_visible_living_world_data(
        persisted_world_events,
        persisted_faction_updates,
        persisted_time_events,
        persisted_rumors,
        persisted_scene_event,
        persisted_complications,
    ):
        return story_entries

    def _scene_matches(entry: Any, scene_number: int) -> bool:
        return _scene_matches_event_metadata(entry, scene_number)

    def _filter_dict_values_for_scene(container: Any, scene_number: int) -> Any:
        if not isinstance(container, dict):
            return {}
        return {
            key: value
            for key, value in container.items()
            if _scene_matches(value, scene_number)
        }

    def _filter_single_for_scene(entry: Any, scene_number: int) -> Any:
        if isinstance(entry, dict) and _scene_matches(entry, scene_number):
            return entry
        return {}

    def _filter_world_events_for_scene(
        world_events: Any, scene_number: int
    ) -> dict[str, Any]:
        if not isinstance(world_events, dict):
            return {}
        filtered_world_events = copy.deepcopy(world_events)
        background_events = filtered_world_events.get("background_events")
        if isinstance(background_events, list):
            filtered_world_events["background_events"] = [
                event
                for event in background_events
                if _scene_matches(event, scene_number)
            ]
        rumors_from_world_events = filtered_world_events.get("rumors")
        if isinstance(rumors_from_world_events, list):
            filtered_world_events["rumors"] = [
                rumor
                for rumor in rumors_from_world_events
                if _scene_matches(rumor, scene_number)
            ]
        return filtered_world_events

    def _build_filtered_payload_for_scene(
        scene_number: int,
    ) -> tuple[
        dict[str, Any],
        dict[str, Any],
        dict[str, Any],
        list[Any],
        dict[str, Any],
        dict[str, Any],
    ]:
        filtered_world_events = _filter_world_events_for_scene(
            persisted_world_events, scene_number
        )
        filtered_faction_updates = _filter_dict_values_for_scene(
            persisted_faction_updates, scene_number
        )
        filtered_time_events = _filter_dict_values_for_scene(
            persisted_time_events, scene_number
        )
        filtered_rumors = (
            [rumor for rumor in persisted_rumors if _scene_matches(rumor, scene_number)]
            if isinstance(persisted_rumors, list)
            else []
        )
        filtered_scene_event = _filter_single_for_scene(
            persisted_scene_event, scene_number
        )
        filtered_complications = _filter_single_for_scene(
            persisted_complications, scene_number
        )
        return (
            filtered_world_events,
            filtered_faction_updates,
            filtered_time_events,
            filtered_rumors,
            filtered_scene_event,
            filtered_complications,
        )

    updated_story: list[dict[str, Any]] | None = None

    for idx, entry in enumerate(story_entries):
        if not isinstance(entry, dict):
            continue
        if str(entry.get("actor", "")).lower() != constants.ACTOR_GEMINI.lower():
            continue

        state_updates = entry.get("state_updates")
        if not isinstance(state_updates, dict):
            state_updates = {}

        entry_world_events = state_updates.get("world_events")
        if not isinstance(entry_world_events, dict):
            entry_world_events = entry.get("world_events")

        entry_faction_updates = state_updates.get("faction_updates")
        if not isinstance(entry_faction_updates, dict):
            entry_faction_updates = entry.get("faction_updates")

        entry_time_events = state_updates.get("time_events")
        if not isinstance(entry_time_events, dict):
            entry_time_events = entry.get("time_events")

        entry_rumors = state_updates.get("rumors")
        if entry_rumors is None:
            entry_rumors = entry.get("rumors")
        if isinstance(entry_rumors, dict):
            if "append" in entry_rumors:
                container = {"rumors": entry_rumors}
                _normalize_append_list_field(container, "rumors")
                entry_rumors = container["rumors"]
            else:
                entry_rumors = [entry_rumors]
        elif entry_rumors is not None and not isinstance(entry_rumors, list):
            entry_rumors = [entry_rumors]

        entry_scene_event = state_updates.get("scene_event")
        if not isinstance(entry_scene_event, dict):
            entry_scene_event = entry.get("scene_event")

        entry_complications = state_updates.get("complications")
        if not isinstance(entry_complications, dict):
            entry_complications = entry.get("complications")

        normalized_entry_world_events = normalize_world_events_for_story_payload(
            entry_world_events
        )
        scene_number = entry.get("user_scene_number")
        scoped_entry_world_events = normalized_entry_world_events
        if isinstance(scene_number, int) and scene_number > 0:
            scoped_entry_world_events = _filter_world_events_for_scene(
                normalized_entry_world_events,
                scene_number,
            )
        if _has_visible_living_world_data(
            scoped_entry_world_events,
            entry_faction_updates,
            entry_time_events,
            entry_rumors,
            entry_scene_event,
            entry_complications,
        ):
            if (
                isinstance(entry_world_events, dict)
                and isinstance(scoped_entry_world_events, dict)
                and scoped_entry_world_events != entry_world_events
            ):
                if updated_story is None:
                    updated_story = list(story_entries)
                updated_entry = dict(entry)
                updated_state_updates = dict(state_updates)
                updated_state_updates["world_events"] = copy.deepcopy(
                    scoped_entry_world_events
                )
                updated_entry["state_updates"] = updated_state_updates
                updated_entry["world_events"] = copy.deepcopy(scoped_entry_world_events)
                updated_story[idx] = updated_entry
            continue

        if not isinstance(scene_number, int) or scene_number <= 0:
            continue

        (
            filtered_world_events,
            filtered_faction_updates,
            filtered_time_events,
            filtered_rumors,
            filtered_scene_event,
            filtered_complications,
        ) = _build_filtered_payload_for_scene(scene_number)

        if not _has_visible_living_world_data(
            filtered_world_events,
            filtered_faction_updates,
            filtered_time_events,
            filtered_rumors,
            filtered_scene_event,
            filtered_complications,
        ):
            continue

        if updated_story is None:
            updated_story = list(story_entries)
        updated_entry = dict(entry)
        updated_state_updates = dict(state_updates)
        updated_state_updates["world_events"] = copy.deepcopy(filtered_world_events)
        if filtered_faction_updates:
            updated_state_updates["faction_updates"] = copy.deepcopy(
                filtered_faction_updates
            )
        if filtered_time_events:
            updated_state_updates["time_events"] = copy.deepcopy(filtered_time_events)
        if filtered_rumors:
            updated_state_updates["rumors"] = copy.deepcopy(filtered_rumors)
        if filtered_scene_event:
            updated_state_updates["scene_event"] = copy.deepcopy(filtered_scene_event)
        if filtered_complications:
            updated_state_updates["complications"] = copy.deepcopy(
                filtered_complications
            )
        updated_entry["state_updates"] = updated_state_updates
        updated_entry["world_events"] = copy.deepcopy(filtered_world_events)
        updated_story[idx] = updated_entry

    return updated_story if updated_story is not None else story_entries


# Helper function moved to prompt_utils.py to eliminate duplication


def _build_campaign_prompt(
    character: str, setting: str, description: str, old_prompt: str
) -> str:
    """
    Build campaign prompt from parameters.
    Unified logic from main.py and world_logic.py.
    """
    # Use the extracted implementation from prompt_utils.py
    return _build_campaign_prompt_impl(character, setting, description, old_prompt)


def _parse_god_mode_data_string(god_mode_data: str) -> dict[str, Any] | None:
    """
    Parse god_mode_data string format into god_mode dict format.

    String format: "Character: X | Setting: Y | Description: Z"
    Dict format: {"character": {...}, "setting": "...", "description": "..."}

    Args:
        god_mode_data: String in format "Character: X | Setting: Y | Description: Z"

    Returns:
        Dict with god_mode structure, or None if parsing fails
    """
    if not god_mode_data or not isinstance(god_mode_data, str):
        return None

    try:
        # Split by " | " to get Character, Setting, Description parts
        parts = [p.strip() for p in god_mode_data.split(" | ")]

        parsed = {}
        character_str = ""
        setting_str = ""
        description_str = ""

        for part in parts:
            if part.startswith("Character:"):
                character_str = part.replace("Character:", "").strip()
            elif part.startswith("Setting:"):
                setting_str = part.replace("Setting:", "").strip()
            elif part.startswith("Description:"):
                description_str = part.replace("Description:", "").strip()

        # If description contains the full text, use it
        if description_str:
            parsed["description"] = description_str

        if setting_str:
            parsed["setting"] = setting_str

        # Extract character info from character_str and description
        # Look for character details in the description (name, class, level, stats, etc.)
        character_dict = {}

        # Extract character name from character_str (first part before any additional info)
        if character_str:
            # Character string might be just "Ser Arion" or "Ser Arion val Valerion"
            character_dict["name"] = character_str.split(",")[0].strip()

        # Parse description for character details
        # The description contains markdown-formatted character info
        full_text_original = god_mode_data
        full_text = full_text_original.lower()

        # Extract name from **Name:** pattern (more reliable than character_str)
        name_match = re.search(r"\*\*name:\*\*\s*([^\n*]+)", full_text, re.IGNORECASE)
        if name_match:
            character_dict["name"] = name_match.group(1).strip()
        elif character_str:
            character_dict["name"] = character_str.split(",")[0].strip()

        # Extract class/level (support both "Level X Class" and "Class: X")
        # Use [ \t]+ (not \s+) between tokens to prevent crossing line boundaries.
        class_match = re.search(
            r"\*\*class:\*\*[ \t]*level[ \t]+(\d+)[ \t]+([^\n*|,]+)",
            full_text_original,
            re.IGNORECASE,
        )
        if not class_match:
            class_match = re.search(
                r"level[ \t]+(\d+)[ \t]+([^\n|,]+)",
                full_text_original,
                re.IGNORECASE,
            )
        if class_match:
            character_dict["level"] = int(class_match.group(1))
            # Extract class name (might have parenthetical like "Paladin (Oath of the Crown)")
            class_name = class_match.group(2).strip()
            # Remove parenthetical if present
            class_name = re.sub(r"\s*\([^)]+\)", "", class_name)
            character_dict["class"] = class_name.title()
        else:
            # Fallback for prompts that only include class label without level
            class_only_match = re.search(
                r"\*\*class:\*\*\s*([^\n*|,]+)",
                full_text_original,
                re.IGNORECASE,
            )
            if not class_only_match:
                # Word boundary ensures we don't match Subclass: or Multiclass:
                # Requiring colon prevents matching 'class features', 'class level', etc.
                class_only_match = re.search(
                    r"\bclass\s*:\s*([^\n|,*]+)",
                    full_text_original,
                    re.IGNORECASE,
                )
            if class_only_match:
                class_name = class_only_match.group(1).strip()
                class_name = re.sub(r"\s*\([^)]+\)", "", class_name)
                class_name = re.sub(
                    r"^level\s+\d+\s+", "", class_name, flags=re.IGNORECASE
                )
                class_name = class_name.strip()
                if class_name:
                    character_dict["class"] = class_name.title()

        # Extract race if mentioned
        race_match = re.search(r"\*\*race:\*\*\s*([^\n*]+)", full_text, re.IGNORECASE)
        if not race_match:
            race_match = re.search(r"race[:\s]+(\w+)", full_text, re.IGNORECASE)
        if race_match:
            race_name = race_match.group(1).strip()
            # Remove markdown formatting
            race_name = re.sub(r"\*\*", "", race_name)
            character_dict["race"] = race_name.capitalize()

        # Extract background if mentioned
        background_match = re.search(
            r"\*\*background:\*\*\s*([^\n*]+)", full_text, re.IGNORECASE
        )
        if background_match:
            bg_name = background_match.group(1).strip()
            # Remove markdown formatting
            bg_name = re.sub(r"\*\*", "", bg_name)
            character_dict["background"] = bg_name

        # Extract stats from flexible blocks (supports full 6-stat prompts)
        stat_patterns = {
            "strength": r"(?:\bstr\b|\bstrength\b)",
            "dexterity": r"(?:\bdex\b|\bdexterity\b)",
            "constitution": r"(?:\bcon\b|\bconstitution\b)",
            "intelligence": r"(?:\bint\b|\bintelligence\b)",
            "wisdom": r"(?:\bwis\b|\bwisdom\b)",
            "charisma": r"(?:\bcha\b|\bcharisma\b)",
        }
        parsed_stats: dict[str, int] = {}
        for stat_name, stat_pattern in stat_patterns.items():
            stat_match = re.search(
                rf"{stat_pattern}\s*[:=]?\s*(\d+)", full_text, re.IGNORECASE
            )
            if stat_match:
                parsed_stats[stat_name] = int(stat_match.group(1))

        if parsed_stats:
            character_dict["base_attributes"] = parsed_stats
            character_dict["attributes"] = parsed_stats.copy()

        # Extract HP if mentioned
        hp_match = re.search(r"\*\*hp:\*\*\s*(\d+)", full_text, re.IGNORECASE)
        if not hp_match:
            hp_match = re.search(r"hp[:\s]+(\d+)", full_text, re.IGNORECASE)
        if hp_match:
            hp_value = int(hp_match.group(1))
            character_dict["hp_max"] = hp_value
            character_dict["hp_current"] = hp_value

        # Extract AC if mentioned
        ac_match = re.search(r"\*\*ac:\*\*\s*(\d+)", full_text, re.IGNORECASE)
        if not ac_match:
            ac_match = re.search(r"ac[:\s]+(\d+)", full_text, re.IGNORECASE)
        if ac_match:
            character_dict["ac"] = int(ac_match.group(1))

        # Only create god_mode dict if we found character info
        if character_dict:
            parsed["character"] = character_dict
            return parsed

        # If no character info found but we have character string, create minimal character
        if character_str:
            parsed["character"] = {"name": character_str}
            return parsed

        # Return parsed dict if we have setting or description, even without character
        # This prevents user-provided campaign settings from being lost
        if parsed.get("setting") or parsed.get("description"):
            return parsed

        return None

    except Exception as e:
        logging_util.warning(f"Failed to parse god_mode_data string: {e}")
        return None


def _handle_debug_mode_command(
    user_input: str,
    current_game_state: GameState,
    user_id: UserId,
    campaign_id: CampaignId,
    include_raw_llm_payloads: bool = False,
) -> dict[str, Any] | None:
    """
    Handle debug mode commands.
    Simplified version for unified API.

    Note: Processes debug commands regardless of debug_mode setting,
    but filters output based on debug_mode in the response.
    """

    user_input_stripped = user_input.strip()

    # Check if debug mode is enabled for filtering responses
    debug_mode_enabled = (
        hasattr(current_game_state, "debug_mode") and current_game_state.debug_mode
    )

    debug_disabled_response = {
        KEY_SUCCESS: True,
        KEY_RESPONSE: "Debug mode is not enabled",
    }

    try:
        # GOD_ASK_STATE
        if user_input_stripped == "GOD_ASK_STATE":
            if not debug_mode_enabled:
                return debug_disabled_response
            return _handle_ask_state_command(
                user_input, current_game_state, user_id, campaign_id
            )

        # GOD_MODE_SET
        if user_input_stripped.startswith("GOD_MODE_SET:"):
            if not debug_mode_enabled:
                return debug_disabled_response
            return _handle_set_command(
                user_input, current_game_state, user_id, campaign_id
            )

        # GOD_MODE_UPDATE_STATE
        if user_input_stripped.startswith("GOD_MODE_UPDATE_STATE:"):
            if not debug_mode_enabled:
                return debug_disabled_response
            return _handle_update_state_command(
                user_input,
                user_id,
                campaign_id,
                include_raw_llm_payloads=include_raw_llm_payloads,
            )

    except Exception as e:
        logging_util.error(f"Debug command failed: {e}")
        return {KEY_ERROR: f"Debug command failed: {str(e)}"}

    return None


# --- Unified API Functions ---


async def create_campaign_unified(request_data: dict[str, Any]) -> dict[str, Any]:
    """
    Unified campaign creation logic for both Flask and MCP.

    Uses asyncio.to_thread() for blocking I/O operations to prevent blocking
    the shared event loop.

    Args:
        request_data: Dictionary containing:
            - user_id: User ID
            - title: Campaign title
            - character: Character description (optional)
            - setting: Setting description (optional)
            - description: Campaign description (optional)
            - prompt: Legacy prompt format (optional)
            - selected_prompts: List of selected prompts (optional)
            - custom_options: List of custom options (optional)

    Returns:
        Dictionary with success/error status and campaign data
    """
    try:
        # Extract parameters
        user_id = request_data.get("user_id")
        title = request_data.get("title")
        character = request_data.get("character", "")
        setting = request_data.get("setting", "")
        description = request_data.get("description", "")
        old_prompt = request_data.get("prompt", "")
        selected_prompts = request_data.get("selected_prompts", [])
        custom_options = request_data.get("custom_options", [])
        god_mode = request_data.get("god_mode")
        god_mode_data = request_data.get("god_mode_data")

        # Parse god_mode_data (string format) into god_mode (dict format) if needed
        # Real users send god_mode_data as string: "Character: X | Setting: Y | Description: Z"
        # Code expects god_mode as dict: {"character": {...}, "setting": "...", "description": "..."}
        if not god_mode and god_mode_data and isinstance(god_mode_data, str):
            logging_util.info("Parsing god_mode_data string format into god_mode dict")
            god_mode = _parse_god_mode_data_string(god_mode_data)
            if god_mode:
                logging_util.info(
                    f"Parsed god_mode_data: character={god_mode.get('character', {}).get('name', 'Unknown')}"
                )
                # Extract character/setting/description from parsed god_mode for prompt building
                if not character and god_mode.get("character", {}).get("name"):
                    character = god_mode["character"]["name"]
                if not setting and god_mode.get("setting"):
                    setting = god_mode["setting"]
                if not description and god_mode.get("description"):
                    description = god_mode["description"]

        # Validate required fields
        if not user_id:
            return {KEY_ERROR: "User ID is required"}
        if not title:
            return {KEY_ERROR: "Title is required"}

        # Build campaign prompt (may generate random values if character/setting are empty)
        try:
            prompt = _build_campaign_prompt(character, setting, description, old_prompt)
        except ValueError as e:
            return {KEY_ERROR: str(e)}

        # CRITICAL FIX: Extract character/setting from prompt if they were randomly generated
        # When user leaves fields blank, _build_campaign_prompt generates random values
        # We need to extract those values to build god_mode
        if not character or not setting:
            # Parse prompt to extract character/setting (format: "Character: X | Setting: Y")
            char_match = re.search(r"Character:\s*([^|]+)", prompt)
            setting_match = re.search(r"Setting:\s*([^|]+)", prompt)
            if char_match:
                character = char_match.group(1).strip()
                logging_util.info(f"Extracted character from prompt: {character}")
            if setting_match:
                setting = setting_match.group(1).strip()
                logging_util.info(f"Extracted setting from prompt: {setting}")

        # ALSO: Build god_mode dict from separate character/setting/description fields (frontend format)
        # Frontend sends character/setting/description as separate fields, not god_mode_data string
        # This also handles randomly generated values from _build_campaign_prompt
        if not god_mode and (character or setting or description):
            logging_util.info(
                "Building god_mode dict from separate character/setting/description fields"
            )
            god_mode = {}
            if setting:
                god_mode["setting"] = setting
            if description:
                god_mode["description"] = description
            if character:
                # Build minimal character dict - LLM will interpret the string
                # We just need god_mode["character"] to be a dict so is_god_mode_with_character is True
                character_dict = {}
                if isinstance(character, str):
                    # Store the full character string - LLM will interpret it
                    # This could be "Ser Arion", "A devout cleric...", "Level 1 Fighter", etc.
                    character_dict["name"] = character.strip()
                    # If description exists, combine it (LLM sees full context)
                    if description:
                        character_dict["description"] = description.strip()
                elif isinstance(character, dict):
                    character_dict = character
                if character_dict:
                    god_mode["character"] = character_dict
                    logging_util.info(
                        f"Built god_mode from separate fields: character={character_dict.get('name', 'Unknown')}"
                    )

        # Always use D&D system
        attribute_system = constants.ATTRIBUTE_SYSTEM_DND

        # Get user settings to apply debug mode and faction_minigame_enabled during campaign creation (blocking I/O)
        user_settings = await asyncio.to_thread(get_user_settings, user_id)
        debug_mode = (
            user_settings.get("debug_mode", constants.DEFAULT_DEBUG_MODE)
            if user_settings
            else constants.DEFAULT_DEBUG_MODE
        )
        faction_minigame_enabled = (
            user_settings.get("faction_minigame_enabled", False)
            if user_settings
            else False
        )

        # Create initial game state with user's debug mode preference
        # ALWAYS start in character creation mode, even if God Mode includes character data
        # Extract God Mode character template if provided
        player_character_data = {}
        character_creation_stage = "concept"  # Default stage

        # Initialize entity tracking with player character if provided
        entity_tracking = {}
        if god_mode and isinstance(god_mode, dict):
            god_mode_character = god_mode.get("character")
            if god_mode_character and isinstance(god_mode_character, dict):
                # Populate player_character_data with template fields
                player_character_data = god_mode_character.copy()
                # Set stage to "review" since character data is pre-populated
                character_creation_stage = "review"
                player_name = player_character_data.get("name")
                logging_util.info(
                    f"God Mode character template detected: {player_name or 'Unknown'}"
                )

                # CHAR-9ss fix: Initialize starting equipment based on class/background
                # Use (get() or "") to handle None values that bypass default
                character_class = (player_character_data.get("class") or "").lower()
                background = (player_character_data.get("background") or "").lower()

                # Basic starting equipment by class (D&D 5e SRD)
                class_equipment = {
                    "wizard": [
                        "Spellbook",
                        "Component pouch",
                        "Quarterstaff",
                        "Scholar's pack",
                    ],
                    "fighter": [
                        "Chain mail",
                        "Longsword",
                        "Shield",
                        "Dungeoneer's pack",
                        "Javelin (2)",
                    ],
                    "rogue": [
                        "Leather armor",
                        "Shortsword (2)",
                        "Dagger",
                        "Thieves' tools",
                        "Burglar's pack",
                    ],
                    "cleric": [
                        "Chain mail",
                        "Mace",
                        "Shield",
                        "Holy symbol",
                        "Priest's pack",
                    ],
                }

                # Get starting equipment for this class
                equipment = []
                for class_name, items in class_equipment.items():
                    if class_name in character_class:
                        equipment.extend(items)
                        break

                # Add background-specific items
                if "sage" in background:
                    equipment.extend(
                        [
                            "Ink (1 ounce bottle)",
                            "Quill",
                            "Small knife",
                            "Letter from dead colleague",
                        ]
                    )
                elif "soldier" in background:
                    equipment.extend(
                        ["Insignia of rank", "Trophy from fallen enemy", "Dice set"]
                    )
                elif "criminal" in background:
                    equipment.extend(["Crowbar", "Dark common clothes", "Pouch (15gp)"])

                # Add basic adventuring gear
                equipment.extend(
                    [
                        "Backpack",
                        "Bedroll",
                        "Mess kit",
                        "Tinderbox",
                        "Torch (10)",
                        "Rations (10 days)",
                        "Waterskin",
                        "Rope (50 feet)",
                        "Coin pouch (10gp)",
                    ]
                )

                # Initialize starting items on the canonical equipment schema.
                # Avoid using legacy inventory (list) here because it can be hidden once
                # slot-based equipment exists.
                if equipment:
                    existing_equipment = player_character_data.get("equipment")
                    existing_inventory = player_character_data.get("inventory")
                    equipment_has_items = (
                        isinstance(existing_equipment, dict)
                        and any(
                            value not in (None, {}, [], "")
                            for value in existing_equipment.values()
                        )
                    ) or (
                        isinstance(existing_equipment, list)
                        and bool(existing_equipment)
                    )
                    inventory_has_items = existing_inventory not in (None, {}, [], "")

                    # Seed starter gear even when templates prefill equipment={} placeholders.
                    if not equipment_has_items and not inventory_has_items:
                        seeded_equipment = (
                            dict(existing_equipment)
                            if isinstance(existing_equipment, dict)
                            else {}
                        )
                        backpack_items = []
                        for item in equipment:
                            name = item
                            stats = None
                            match = re.match(
                                r"^(?P<name>.+?)\s*\((?P<stats>.+)\)\s*$", str(item)
                            )
                            if match:
                                name = match.group("name").strip()
                                stats = match.group("stats").strip()
                            backpack_items.append(
                                {"name": str(name), "stats": stats, "equipped": False}
                            )

                        seeded_equipment["backpack"] = backpack_items
                        player_character_data["equipment"] = seeded_equipment
                        logging_util.info(
                            f"✅ Initialized {len(equipment)} starting items for {character_class} (equipment.backpack)"
                        )

                # Add player character to active_entities for entity tracking
                if player_name:
                    entity_tracking = {
                        "active_entities": [player_name],
                        "present_entities": [],
                    }
                    logging_util.info(
                        f"✅ Added '{player_name}' to active_entities (God Mode character)"
                    )

        # Build custom_campaign_state with both character creation and faction_minigame
        custom_campaign_state = {
            "attribute_system": attribute_system,
            "character_creation_in_progress": True,
            "character_creation_stage": character_creation_stage,
        }

        # Initialize faction_minigame structure if user has feature enabled in settings
        # Per-campaign default: OFF - user must explicitly enable for each campaign
        if faction_minigame_enabled:
            custom_campaign_state["faction_minigame"] = {
                "enabled": False,  # Per-campaign default: OFF (requires explicit enablement)
                "tutorial_completed": False,
                "tutorial_progress": {},
                "suggestion_given": False,  # Track if suggestion was given at 100+ troops
                "strong_suggestion_given": False,  # Track if strong recommendation was given at 500+ troops
            }

        # Store god_mode data in custom_campaign_state for system instruction inclusion
        if god_mode and isinstance(god_mode, dict):
            custom_campaign_state["god_mode"] = god_mode
            logging_util.info(
                f"✅ Stored god_mode in custom_campaign_state (setting: {len(god_mode.get('setting', ''))} chars)"
            )

        # Extract companions from god_mode if present
        npc_data_from_god_mode = {}
        if god_mode and isinstance(god_mode, dict) and "companions" in god_mode:
            companions_dict = god_mode.get("companions", {})
            if isinstance(companions_dict, dict):
                # CRITICAL: Ensure all companions have relationship="companion" field
                # so they're detected by build_companion_instruction() filter
                npc_data_from_god_mode = {}
                for name, npc in companions_dict.items():
                    if isinstance(npc, dict):
                        npc_copy = npc.copy()
                        npc_copy["relationship"] = (
                            "companion"  # Required for companion detection
                        )
                        npc_data_from_god_mode[name] = npc_copy
                logging_util.info(
                    f"🎭 GOD MODE: Found {len(npc_data_from_god_mode)} companions in god_mode: {list(npc_data_from_god_mode.keys())}"
                )

        initial_game_state = GameState(
            user_id=user_id,
            custom_campaign_state=custom_campaign_state,
            player_character_data=player_character_data,
            entity_tracking=entity_tracking,
            debug_mode=debug_mode,
            npc_data=npc_data_from_god_mode,  # Pass directly - GameState handles empty dict default
        ).to_dict()

        # Verify companions are in the state dict
        if npc_data_from_god_mode:
            state_npc_data = initial_game_state.get("npc_data", {})
            if not isinstance(state_npc_data, dict):
                state_npc_data = {}
            # Merge companions into state (in case GameState didn't preserve them)
            state_npc_data.update(npc_data_from_god_mode)
            initial_game_state["npc_data"] = state_npc_data
            logging_util.info(
                f"🎭 GOD MODE: Verified {len(state_npc_data)} companions in initial_game_state: {list(state_npc_data.keys())}"
            )

        generate_companions = "companions" in custom_options
        use_default_world = "defaultWorld" in custom_options

        # CRITICAL UX FIX: For God Mode campaigns with pre-populated characters,
        # generate character creation narrative IMMEDIATELY so user can review.
        # Only skip for empty character creation (user will build from scratch).
        is_god_mode_with_character = (
            god_mode
            and isinstance(god_mode, dict)
            and god_mode.get("character")
            and isinstance(god_mode.get("character"), dict)
        )

        # DEBUG LOGGING: Track why placeholder might be shown
        logging_util.info("🔍 CHARACTER CREATION DECISION:")
        logging_util.info(
            f"  character_creation_in_progress: {initial_game_state['custom_campaign_state']['character_creation_in_progress']}"
        )
        logging_util.info(f"  god_mode exists: {god_mode is not None}")
        logging_util.info(f"  god_mode type: {type(god_mode)}")
        logging_util.info(f"  god_mode value: {god_mode}")
        if god_mode:
            logging_util.info(
                f"  god_mode.get('character'): {god_mode.get('character')}"
            )
            logging_util.info(
                f"  character is dict: {isinstance(god_mode.get('character'), dict) if god_mode.get('character') else False}"
            )
        logging_util.info(f"  is_god_mode_with_character: {is_god_mode_with_character}")

        if (
            initial_game_state["custom_campaign_state"][
                "character_creation_in_progress"
            ]
            and not is_god_mode_with_character
        ):
            # Empty character creation - skip opening story, let user build character in Turn 1
            logging_util.info(
                "Skipping opening story generation - empty character creation mode active"
            )
            opening_story_text = (
                "[Character Creation Mode - Story begins after character is complete]"
            )
            # Keep Firestore structured field payload shape consistent, even when
            # we skip opening story generation.
            opening_story_structured_fields = {
                constants.FIELD_SESSION_HEADER: "",
                constants.FIELD_PLANNING_BLOCK: {},
                constants.FIELD_DICE_ROLLS: [],
                constants.FIELD_DICE_AUDIT_EVENTS: [],
                constants.FIELD_RESOURCES: "",
                constants.FIELD_DEBUG_INFO: {},
                constants.FIELD_GOD_MODE_RESPONSE: "",
                constants.FIELD_DIRECTIVES: {},
            }
        else:
            # Generate opening story using LLM (CRITICAL: blocking I/O - 10-30+ seconds!)
            # For God Mode campaigns with character data, use CharacterCreationAgent
            # For regular campaigns, use StoryModeAgent
            # CRITICAL: If companions are in initial_game_state (from god_mode), ensure generate_companions is True
            # so the LLM knows to include them in the narrative
            if npc_data_from_god_mode and not generate_companions:
                generate_companions = True
                logging_util.info(
                    f"🎭 GOD MODE: Enabling generate_companions=True because {len(npc_data_from_god_mode)} companions found in god_mode"
                )

            try:
                opening_story_response = await asyncio.to_thread(
                    llm_service.get_initial_story,
                    prompt,
                    user_id,
                    selected_prompts,
                    generate_companions,
                    use_default_world,
                    use_character_creation_agent=is_god_mode_with_character,  # Use CharacterCreationAgent for God Mode with character
                    initial_npc_data=npc_data_from_god_mode
                    if npc_data_from_god_mode
                    else None,  # Pass companions from god_mode
                )
            except llm_service.PayloadTooLargeError as e:
                logging_util.error(f"Payload too large during campaign creation: {e}")
                return create_error_response(
                    "Story context is too large. Please start a new campaign or reduce story history.",
                    status_code=422,
                )
            except llm_service.LLMRequestError as e:
                logging_util.error(f"LLM request failed during campaign creation: {e}")
                status_code = getattr(e, "status_code", None) or 422
                return create_error_response(str(e), status_code)

            if hasattr(opening_story_response, "narrative_text"):
                opening_story_text = opening_story_response.narrative_text
            elif isinstance(opening_story_response, dict):
                opening_story_text = (
                    opening_story_response.get("narrative_text")
                    or opening_story_response.get("story_text")
                    or ""
                )
            else:
                opening_story_text = str(opening_story_response or "")

            # Extract state updates from opening story and merge into initial_game_state.
            # Accept both LLMResponse-like objects and dict-based mock/legacy responses.
            if hasattr(opening_story_response, "get_state_updates"):
                state_updates = opening_story_response.get_state_updates()
            elif isinstance(opening_story_response, dict):
                state_updates = opening_story_response.get("state_updates", {})
            else:
                state_updates = {}

            if isinstance(state_updates, dict) and state_updates:
                initial_game_state = update_state_with_changes(
                    initial_game_state, state_updates
                )
                logging_util.info("Merged LLM state updates into initial game state")

            # Extract structured fields
            if isinstance(opening_story_response, dict):
                fields = {
                    constants.FIELD_SESSION_HEADER: opening_story_response.get(
                        constants.FIELD_SESSION_HEADER, ""
                    ),
                    constants.FIELD_PLANNING_BLOCK: opening_story_response.get(
                        constants.FIELD_PLANNING_BLOCK,
                        opening_story_response.get("planning_block", {}),
                    ),
                    constants.FIELD_DICE_ROLLS: opening_story_response.get(
                        constants.FIELD_DICE_ROLLS, []
                    ),
                    constants.FIELD_DICE_AUDIT_EVENTS: opening_story_response.get(
                        constants.FIELD_DICE_AUDIT_EVENTS, []
                    ),
                    constants.FIELD_RESOURCES: opening_story_response.get(
                        constants.FIELD_RESOURCES, ""
                    ),
                    constants.FIELD_DEBUG_INFO: opening_story_response.get(
                        constants.FIELD_DEBUG_INFO, {}
                    ),
                    constants.FIELD_GOD_MODE_RESPONSE: opening_story_response.get(
                        constants.FIELD_GOD_MODE_RESPONSE, ""
                    ),
                    constants.FIELD_DIRECTIVES: opening_story_response.get(
                        constants.FIELD_DIRECTIVES, {}
                    ),
                }
            else:
                fields = structured_fields_utils.extract_structured_fields(
                    opening_story_response
                )

            # Ensure planning_block is a dict (prevent string "empty" values from extraction)
            if constants.FIELD_PLANNING_BLOCK in fields:
                if not isinstance(fields[constants.FIELD_PLANNING_BLOCK], dict):
                    fields[constants.FIELD_PLANNING_BLOCK] = {}
            else:
                fields[constants.FIELD_PLANNING_BLOCK] = {}

            opening_story_structured_fields = _ensure_session_header_resources(
                fields,
                initial_game_state,
            )

        # Create campaign in Firestore (blocking I/O - run in thread)
        campaign_id = await asyncio.to_thread(
            firestore_service.create_campaign,
            user_id,
            title,
            prompt,
            opening_story_text,
            initial_game_state,
            selected_prompts,
            use_default_world,
            opening_story_structured_fields,
        )

        return {
            KEY_SUCCESS: True,
            KEY_CAMPAIGN_ID: campaign_id,
            "title": title,
            "opening_story": opening_story_text,
            "game_state": initial_game_state,
            "attribute_system": attribute_system,
        }

    except Exception as e:
        logging_util.error(f"Campaign creation failed: {e}")
        return {KEY_ERROR: f"Failed to create campaign: {str(e)}"}


def _generate_faction_header_from_state(game_state: Any) -> str:
    """
    Generate the standard faction status header from game state.
    Format: [FACTION STATUS] Turn X | Rank #Y/201 | FP: Z,ZZZ

    Handles both GameState objects and dict representations.
    """
    # Try to get faction_minigame data from multiple possible shapes
    faction_data: dict[str, Any] | None = None

    # 1) Dict-based game_state (common in world_logic flows)
    if isinstance(game_state, dict):
        # Check custom_campaign_state (canonical location)
        custom_state = game_state.get("custom_campaign_state")
        if isinstance(custom_state, dict):
            faction_data = custom_state.get("faction_minigame")

        # Fallback to direct key (if flattened)
        if not isinstance(faction_data, dict):
            faction_data = game_state.get("faction_minigame")

        # Fallback to nested game_state.data structure
        if not isinstance(faction_data, dict):
            faction_data = (game_state.get("game_state") or {}).get("faction_minigame")

    # 2) GameState-like objects
    if faction_data is None:
        # Check custom_campaign_state attribute
        if hasattr(game_state, "custom_campaign_state"):
            custom_state = getattr(game_state, "custom_campaign_state", None)
            if isinstance(custom_state, dict):
                faction_data = custom_state.get("faction_minigame")

        # Check faction_minigame attribute
        if faction_data is None and hasattr(game_state, "faction_minigame"):
            faction_data = getattr(game_state, "faction_minigame", None)

        # Check data dict attribute
        if (
            faction_data is None
            and hasattr(game_state, "data")
            and isinstance(game_state.data, dict)
        ):
            faction_data = game_state.data.get("game_state", {}).get("faction_minigame")

    if not isinstance(faction_data, dict):
        return ""

    # Check if enabled
    if not faction_data.get("enabled", False):
        return ""

    # Construct header parts
    try:
        turn = coerce_int(faction_data.get("turn_number"), 1)
        rank = coerce_int(faction_data.get("ranking"), 201)
        fp = coerce_int(faction_data.get("faction_power"), 0)

        units = faction_data.get("units", {}) or {}
        if not isinstance(units, dict):
            units = {}

        soldiers = coerce_int(units.get("soldiers", 0), 0)
        spies = coerce_int(units.get("spies", 0), 0)
        elites = coerce_int(units.get("elites", 0), 0)
        elite_level = coerce_int(units.get("elite_avg_level", 0), 0)

        resources = faction_data.get("resources", {}) or {}
        if not isinstance(resources, dict):
            resources = {}

        territory = coerce_int(resources.get("territory", 0), 0)
        citizens = coerce_int(resources.get("citizens", 0), 0)
        max_citizens = coerce_int(resources.get("max_citizens", 0), 0)
        gold = coerce_int(resources.get("gold", 0), 0)
        arcana = coerce_int(resources.get("arcana", 0), 0)
        max_arcana = coerce_int(resources.get("max_arcana", 0), 0)

        return (
            f"[FACTION STATUS] Turn {turn} | Rank #{rank}/201 | FP: {fp:,}\n"
            f"⚔️ Soldiers: {soldiers:,} | 🕵️ Spies: {spies} | 👑 Elites: {elites} (Avg Lvl {elite_level})\n"
            f"🏰 Territory: {territory:,} | 🏛️ Citizens: {citizens:,}/{max_citizens:,} | "
            f"💰 Gold: {gold:,} | ✨ Arcana: {arcana:,}/{max_arcana:,}"
        )

    except Exception as e:
        logging_util.error(f"Failed to generate faction header: {e}")
        return ""


def _ensure_faction_header_if_enabled(
    response_payload: dict[str, Any], game_state_dict: dict[str, Any]
) -> dict[str, Any]:
    """
    Ensure faction_header is present if minigame is enabled.

    This acts as a safety net if the LLM fails to generate the mandatory field.
    """
    # If header already exists, do nothing
    if response_payload.get("faction_header"):
        return response_payload

    # Generate header from state
    header = _generate_faction_header_from_state(game_state_dict)

    if header:
        response_payload["faction_header"] = header
        logging_util.info("🏰 INJECTED FACTION HEADER (LLM missed it)")

    return response_payload


async def process_action_unified(request_data: dict[str, Any]) -> dict[str, Any]:
    """
    Unified story processing logic for both Flask and MCP.

    Uses asyncio.to_thread() for blocking I/O operations to prevent blocking
    the shared event loop. This allows concurrent requests (e.g., loading a
    campaign while an action is being processed).

    Args:
        request_data: Dictionary containing:
            - user_id: User ID
            - campaign_id: Campaign ID
            - user_input: User action/input
            - mode: Interaction mode (optional, defaults to 'character')

    Returns:
        Dictionary with success/error status and story response
    """

    def _is_god_mode_return_to_story(text: str, mode: str | None = None) -> bool:
        """Check if text is a return-to-story command from god mode.

        Works with both:
        1. "GOD MODE: return to story" prefix (any mode)
        2. "return to story" without prefix (when mode='god')
        """
        if not isinstance(text, str):
            return False
        stripped = text.strip()

        # Check if we have the GOD MODE: prefix
        has_prefix = stripped.upper().startswith("GOD MODE:")

        # If we have the prefix, extract remainder; otherwise use full text
        if has_prefix:
            remainder = stripped[len("GOD MODE:") :].strip().lower()
        elif mode and mode.lower() == constants.MODE_GOD:
            # No prefix but we're in god mode via parameter - check full text
            remainder = stripped.lower()
        else:
            # No prefix and not in god mode - not a return command
            return False

        remainder = remainder.rstrip(".! ")
        tokens = [t for t in remainder.split() if t]
        if not tokens:
            return False
        # Allow polite suffixes like "please"/"now" but prevent matching unrelated commands.
        suffix_ok = {"please", "now"}
        if tokens[:3] == ["return", "to", "story"]:
            return all(t in suffix_ok for t in tokens[3:])
        if tokens[:4] == ["return", "to", "story", "mode"]:
            return all(t in suffix_ok for t in tokens[4:])
        if tokens[:3] == ["exit", "god", "mode"]:
            return all(t in suffix_ok for t in tokens[3:])
        if tokens[:3] == ["return", "to", "game"]:
            return all(t in suffix_ok for t in tokens[3:])
        if tokens[:2] == ["resume", "story"]:
            return all(t in suffix_ok for t in tokens[2:])
        return False

    campaign_id = request_data.get("campaign_id")
    logging_util.set_campaign_id(campaign_id)

    # LATENCY TRACKING: Record start time
    start_time = time.perf_counter()
    logging_util.info("⏱️ LATENCY_START: process_action_unified started")

    try:
        # Extract parameters
        user_id = request_data.get("user_id")
        user_input = request_data.get("user_input")
        mode = request_data.get("mode", constants.MODE_CHARACTER)
        # Security: Strict boolean check - bool("false") = True, so check explicitly
        raw_payloads_raw = request_data.get("include_raw_llm_payloads", False)
        include_raw_llm_payloads = raw_payloads_raw is True or (
            isinstance(raw_payloads_raw, str) and raw_payloads_raw.lower() == "true"
        )

        # Validate mode type (defensive: client could send dict/list/int instead of string)
        if not isinstance(mode, str):
            logging_util.warning(
                f"⚠️ Invalid mode type received: {type(mode).__name__} = {mode!r}, defaulting to {constants.MODE_CHARACTER}"
            )
            mode = constants.MODE_CHARACTER

        # Validate required fields
        if not user_id:
            return {KEY_ERROR: "User ID is required"}
        if not campaign_id:
            return {KEY_ERROR: "Campaign ID is required"}
        if user_input is None:
            return {KEY_ERROR: "User input is required"}
        if not isinstance(user_input, str):
            return {KEY_ERROR: "User input must be a string"}

        # Preserve raw input for Firestore + temporal correction prompts
        original_user_input = user_input

        # If this is a GOD MODE return command, treat as story mode transition.
        # Supports both "GOD MODE: return to story" prefix and plain "return to story" when mode='god'
        if _is_god_mode_return_to_story(user_input, mode):
            user_input = "Return to story."
            mode = constants.MODE_CHARACTER

        # Load and prepare game state + user settings.
        #
        # In mock services mode, Firestore is in-memory and non-blocking, so
        # running directly avoids thread scheduling overhead that can make
        # concurrency tests flaky.

        # LATENCY TRACKING: Game state preparation
        prep_start = time.perf_counter()
        logging_util.info(
            "⏱️ LATENCY_PREP_START: Preparing game state and user settings"
        )

        if is_mock_services_mode():
            (
                current_game_state,
                was_cleaned,
                num_cleaned,
                user_settings,
            ) = _prepare_game_state_with_user_settings(user_id, campaign_id)
        else:
            (
                current_game_state,
                was_cleaned,
                num_cleaned,
                user_settings,
            ) = await asyncio.to_thread(
                _prepare_game_state_with_user_settings, user_id, campaign_id
            )

        prep_duration = time.perf_counter() - prep_start
        logging_util.info(
            f"⏱️ LATENCY_PREP_END: Game state preparation completed in {prep_duration:.2f}s"
        )

        if user_settings and "debug_mode" in user_settings:
            current_game_state.debug_mode = user_settings["debug_mode"]

        # Handle specialized Spicy Mode toggle commands from UI choices or verbatim input
        normalized_input = _normalize_spicy_toggle_input(user_input)

        is_enable_spicy = normalized_input in enable_spicy_phrases
        is_exit_spicy = normalized_input in exit_spicy_phrases

        if is_enable_spicy or is_exit_spicy:
            new_spicy_state = is_enable_spicy
            logging_util.info(
                f"🌶️ SERVER_SPICY_TOGGLE: User requested spicy_mode={new_spicy_state} "
                f"via input='{user_input.strip()}'"
            )

            # Update user settings in Firestore
            settings_to_update = {"spicy_mode": new_spicy_state}

            # Guard against None user_settings (user may have no saved settings yet)
            safe_settings = user_settings or {}
            current_spicy_mode = safe_settings.get("spicy_mode", False)

            # Only perform provider/model switch on ACTUAL transitions to avoid clobbering
            if new_spicy_state and not current_spicy_mode:
                # Entering Spicy Mode: save current provider/model and switch to Grok
                pre_spicy_provider = safe_settings.get("llm_provider", "gemini")

                # Determine provider-specific model to save
                if pre_spicy_provider == "openrouter":
                    pre_spicy_model = safe_settings.get(
                        "openrouter_model", constants.DEFAULT_OPENROUTER_MODEL
                    )
                elif pre_spicy_provider == "cerebras":
                    pre_spicy_model = safe_settings.get(
                        "cerebras_model", constants.DEFAULT_CEREBRAS_MODEL
                    )
                elif pre_spicy_provider == "openclaw":
                    pre_spicy_model = safe_settings.get(
                        "openclaw_model", constants.DEFAULT_OPENCLAW_MODEL
                    )
                    if (
                        not isinstance(pre_spicy_model, str)
                        or not pre_spicy_model.startswith("openclaw/")
                        or len(pre_spicy_model) <= len("openclaw/")
                    ):
                        pre_spicy_model = constants.DEFAULT_OPENCLAW_MODEL
                else:
                    pre_spicy_model = safe_settings.get(
                        "gemini_model", constants.DEFAULT_GEMINI_MODEL
                    )

                settings_to_update.update(
                    {
                        "llm_provider": "openrouter",
                        "openrouter_model": constants.SPICY_OPENROUTER_MODEL,
                        # Preserve previous settings for restoration
                        "pre_spicy_provider": pre_spicy_provider,
                        "pre_spicy_model": pre_spicy_model,
                    }
                )
            elif not new_spicy_state and current_spicy_mode:
                # Exiting Spicy Mode: compute exit settings with manual change detection
                exit_settings = _compute_spicy_mode_exit_settings(safe_settings)
                settings_to_update.update(exit_settings)

            await asyncio.to_thread(
                firestore_service.update_user_settings, user_id, settings_to_update
            )

            # Update local user_settings and current_game_state for immediate use in this turn
            if user_settings is not None:
                user_settings.update(settings_to_update)
            else:
                user_settings = settings_to_update
                current_game_state.user_settings = user_settings

            # Re-apply debug mode if it was changed (unlikely here but safe)
            if "debug_mode" in user_settings:
                current_game_state.debug_mode = user_settings["debug_mode"]

            # EARLY RETURN: Spicy toggle commands don't need LLM processing.
            # Just return a confirmation response to avoid getting a narrative
            # response that treats the toggle command as roleplay input.
            toggle_action = "enabled" if new_spicy_state else "disabled"
            confirmation_message = f"🌶️ Spicy mode {toggle_action}."

            logging_util.info(
                "🌶️ SPICY_TOGGLE_EARLY_RETURN: Returning confirmation without LLM processing"
            )

            return {
                KEY_SUCCESS: True,
                "narrative": confirmation_message,
                "response": confirmation_message,
                "story": [{"text": confirmation_message}],
                "game_state": current_game_state.to_dict()
                if hasattr(current_game_state, "to_dict")
                else {},
                "mode": mode,
                "user_input": user_input,
                "agent_mode": constants.MODE_CHARACTER,
                "agent_used": "StoryModeAgent",
                "spicy_mode_toggled": True,
                "spicy_mode_enabled": new_spicy_state,
            }

        # Apply faction_minigame_enabled setting to game state (if user_settings loaded)
        if user_settings and "faction_minigame_enabled" in user_settings:
            faction_minigame_enabled = user_settings.get(
                "faction_minigame_enabled", False
            )
            # Initialize or update faction_minigame in custom_campaign_state
            if not hasattr(
                current_game_state, "custom_campaign_state"
            ) or not isinstance(current_game_state.custom_campaign_state, dict):
                current_game_state.custom_campaign_state = {}

            # Ensure faction_minigame structure exists with suggestion tracking fields
            if "faction_minigame" not in current_game_state.custom_campaign_state:
                current_game_state.custom_campaign_state["faction_minigame"] = {}

            faction_minigame = current_game_state.custom_campaign_state[
                "faction_minigame"
            ]
            if not isinstance(faction_minigame, dict):
                faction_minigame = {}
                current_game_state.custom_campaign_state["faction_minigame"] = (
                    faction_minigame
                )

            # Ensure suggestion tracking fields exist (default to False)
            if "suggestion_given" not in faction_minigame:
                faction_minigame["suggestion_given"] = False
            if "strong_suggestion_given" not in faction_minigame:
                faction_minigame["strong_suggestion_given"] = False

            if faction_minigame_enabled:
                # User has feature available - ensure structure exists
                # Preserve existing enabled state (per-campaign default: False)
                if "enabled" not in faction_minigame:
                    faction_minigame["enabled"] = False  # Per-campaign default
                if "tutorial_completed" not in faction_minigame:
                    faction_minigame["tutorial_completed"] = False
                if "tutorial_progress" not in faction_minigame:
                    faction_minigame["tutorial_progress"] = {}
            # User setting disabled - disable minigame if not already enabled
            # Don't overwrite a player-requested enabled state
            # Use strict boolean check to handle string "false" edge cases
            elif faction_minigame.get("enabled") is not True:
                faction_minigame["enabled"] = False

        # Handle debug mode commands (only when applicable; avoids unnecessary
        # thread scheduling overhead for normal gameplay).
        user_input_stripped = user_input.strip()
        if user_input_stripped == "GOD_ASK_STATE" or user_input_stripped.startswith(
            ("GOD_MODE_SET:", "GOD_MODE_UPDATE_STATE:")
        ):
            debug_response = await asyncio.to_thread(
                _handle_debug_mode_command,
                user_input,
                current_game_state,
                user_id,
                campaign_id,
                include_raw_llm_payloads=include_raw_llm_payloads,
            )
            if debug_response:
                return debug_response

        # Extract current world_time and location for temporal validation
        # CRITICAL: world_data can be None or non-dict in existing saves - normalize to {} first
        world_data = getattr(current_game_state, "world_data", None)
        if not isinstance(world_data, dict):
            world_data = {}
        old_world_time = world_data.get("world_time")
        old_location = world_data.get("current_location_name")

        # Process regular game action with LLM (CRITICAL: blocking I/O - 10-30+ seconds!)
        # This is the most important call to run in a thread to prevent blocking
        # TEMPORAL VALIDATION LOOP: Retry if LLM generates backward time
        # EXCEPTION: GOD MODE commands can intentionally move time backward
        #
        # NOTE: is_god_mode and is_think_mode are determined by agent selection inside
        # llm_service.continue_story. The LLMResponse returns agent_mode as the single
        # source of truth. We set these AFTER the LLM call based on llm_response_obj.agent_mode.
        llm_input = user_input  # Separate variable for LLM calls
        temporal_correction_attempts = 0
        llm_response_obj = None
        new_world_time: dict[str, Any] | None = None

        while temporal_correction_attempts <= MAX_TEMPORAL_CORRECTION_ATTEMPTS:
            try:
                # Always reload campaign_data and story_context from Firestore for each request.
                # This ensures:
                # 1. story_context includes the latest story entries (including previous commands)
                # 2. campaign_data reflects any changes (selected_prompts, use_default_world, etc.)
                #
                # No caching is needed because:
                # - MAX_TEMPORAL_CORRECTION_ATTEMPTS = 0 (loop only runs once per request)
                # - Campaign data is just one document read (cheap)
                # - Story context must be fresh (includes latest entries)
                # - Caching adds complexity and risk of stale data bugs

                # LATENCY TRACKING: Primary LLM call
                llm_start = time.perf_counter()
                logging_util.info(
                    f"⏱️ LATENCY_LLM_PRIMARY_START: Starting primary LLM inference (attempt {temporal_correction_attempts + 1})"
                )

                (
                    campaign_data,
                    story_context,
                    llm_response_obj,
                ) = await asyncio.to_thread(
                    _load_campaign_and_continue_story,
                    user_id,
                    campaign_id,
                    llm_input=llm_input,
                    mode=mode,
                    current_game_state=current_game_state,
                    include_raw_llm_payloads=include_raw_llm_payloads,
                )

                llm_duration = time.perf_counter() - llm_start
                logging_util.info(
                    f"⏱️ LATENCY_LLM_PRIMARY_END: Primary LLM inference completed in {llm_duration:.2f}s"
                )

                if not campaign_data or llm_response_obj is None:
                    return {
                        KEY_ERROR: "Campaign not found",
                        "status_code": 404,
                    }
                selected_prompts = campaign_data.get("selected_prompts", [])
                use_default_world = campaign_data.get("use_default_world", False)
            except llm_service.PayloadTooLargeError as e:
                logging_util.error(f"Payload too large during story continuation: {e}")
                return create_error_response(
                    "Story context is too large. Please start a new campaign or reduce story history.",
                    status_code=422,
                )
            except llm_service.LLMRequestError as e:
                logging_util.error(f"LLM request failed during story continuation: {e}")
                status_code = getattr(e, "status_code", None) or 422
                return create_error_response(str(e), status_code)

            # Get mode from LLM response - agent selection is the single source of truth
            # This replaces duplicate is_god_mode/is_think_mode detection
            is_god_mode = llm_response_obj.agent_mode == constants.MODE_GOD
            is_think_mode = llm_response_obj.agent_mode == constants.MODE_THINK
            is_character_creation_mode = (
                llm_response_obj.agent_mode == constants.MODE_CHARACTER_CREATION
            )
            is_level_up_mode = llm_response_obj.agent_mode == constants.MODE_LEVEL_UP

            # Check for temporal violation (time going backward)
            # EXCEPTION: Skip validation for GOD MODE (backward time is intentional)
            new_world_time = _extract_world_time_from_response(llm_response_obj)

            if is_god_mode or not _check_temporal_violation(
                old_world_time, new_world_time
            ):
                # No violation - time is moving forward (or GOD MODE allows backward), accept response
                if is_god_mode and _check_temporal_violation(
                    old_world_time, new_world_time
                ):
                    logging_util.info(
                        f"⏪ GOD_MODE: Allowing backward time travel from "
                        f"{_format_world_time_for_prompt(old_world_time)} to "
                        f"{_format_world_time_for_prompt(new_world_time)}"
                    )
                elif temporal_correction_attempts > 0:
                    logging_util.info(
                        f"✅ TEMPORAL_CORRECTION: Response accepted after {temporal_correction_attempts} correction(s)"
                    )
                break

            # Temporal violation detected!
            temporal_correction_attempts += 1

            if temporal_correction_attempts > MAX_TEMPORAL_CORRECTION_ATTEMPTS:
                # Max retries exceeded - log warning and accept the response anyway
                # NOTE: Correction FAILED - we're accepting a bad response, not a successful fix
                logging_util.warning(
                    f"❌ TEMPORAL_CORRECTION_FAILED: Max correction attempts ({MAX_TEMPORAL_CORRECTION_ATTEMPTS}) exceeded. "
                    f"Giving up and accepting response with backward time: {_format_world_time_for_prompt(new_world_time)} "
                    f"< {_format_world_time_for_prompt(old_world_time)}"
                )
                break

            # Extract new location for error message
            new_state_updates = (
                llm_response_obj.get_state_updates()
                if hasattr(llm_response_obj, "get_state_updates")
                else {}
            )
            new_location = new_state_updates.get("world_data", {}).get(
                "current_location_name", old_location
            )

            # Log the violation and retry
            logging_util.warning(
                f"🚨 TEMPORAL_VIOLATION (attempt {temporal_correction_attempts}/{MAX_TEMPORAL_CORRECTION_ATTEMPTS}): "
                f"Time went backward from {_format_world_time_for_prompt(old_world_time)} to "
                f"{_format_world_time_for_prompt(new_world_time)}. Requesting regeneration."
            )

            # Build correction prompt for next LLM call (does NOT overwrite user_input)
            llm_input = build_temporal_correction_prompt(
                original_user_input,
                old_world_time,
                new_world_time,
                old_location,
                new_location,
            )

        # Convert LLMResponse to dict format for compatibility
        # Apply preventive guards to enforce continuity safeguards
        state_changes, prevention_extras = preventive_guards.enforce_preventive_guards(
            current_game_state, llm_response_obj, mode
        )

        # CRITICAL: Enforce character creation modal lock (server-side routing control)
        # This MUST run after preventive guards but BEFORE applying state_updates
        # Server controls routing flags, not LLM
        state_changes = _enforce_character_creation_modal_lock(
            current_game_state.to_dict(),
            state_changes,
            original_user_input,
        )

        # Surface critical LLM response-quality issues to users (and logs) without retries.
        llm_metadata = getattr(llm_response_obj, "processing_metadata", {}) or {}
        llm_missing_fields = llm_metadata.get("llm_missing_fields", [])
        if isinstance(llm_missing_fields, list) and llm_missing_fields:
            warnings_out = prevention_extras.setdefault("system_warnings", [])
            if "dice_integrity" in llm_missing_fields:
                warnings_out.append(
                    "Dice integrity warning: dice output could not be verified. Consider retrying this action."
                )
            if "dice_rolls" in llm_missing_fields:
                warnings_out.append(
                    "Dice rolls missing for an action that required them. Consider retrying this action."
                )

        # Allow LLMs to return a single timestamp string while we maintain the
        # structured world_time object expected by the engine.
        state_changes = _apply_timestamp_to_world_time(state_changes)

        # Normalize any world_time values without inventing new timestamps; the
        # LLM remains responsible for choosing timeline values.
        state_changes = world_time.ensure_progressive_world_time(
            state_changes,
            is_god_mode=is_god_mode,
        )
        new_world_time = state_changes.get("world_data", {}).get("world_time")

        # Add temporal violation error as god_mode_response for user-facing display
        # Note: new_world_time is already extracted in the temporal validation loop above
        temporal_violation_detected = _check_temporal_violation(
            old_world_time, new_world_time
        )

        if temporal_violation_detected and not is_god_mode:
            old_time_str = _format_world_time_for_prompt(old_world_time)
            new_time_str = _format_world_time_for_prompt(new_world_time)
            # User-facing error message as god_mode_response
            god_mode_response = (
                f"⚠️ **TEMPORAL ANOMALY DETECTED**\n\n"
                f"The AI generated a response where time moved backward:\n"
                f"- **Previous time:** {old_time_str}\n"
                f"- **Response time:** {new_time_str}\n\n"
                f"This may indicate the AI lost track of the story timeline. "
                f"The response was accepted but timeline consistency may be affected."
            )

            prevention_extras["god_mode_response"] = god_mode_response

            logging_util.warning(
                f"⚠️ TEMPORAL_VIOLATION surfaced to user: {new_time_str} < {old_time_str}"
            )

            prevention_extras["temporal_correction_warning"] = prevention_extras[
                "god_mode_response"
            ]
            prevention_extras["temporal_correction_attempts"] = 1

        # Add temporal correction warning if corrections were needed (legacy path when retries enabled)
        elif temporal_correction_attempts > 0:
            temporal_warning = build_temporal_warning_message(
                temporal_correction_attempts,
                max_attempts=MAX_TEMPORAL_CORRECTION_ATTEMPTS,
            )
            if temporal_correction_attempts > MAX_TEMPORAL_CORRECTION_ATTEMPTS:
                logging_util.warning(
                    f"⚠️ TEMPORAL_WARNING (exceeded): {temporal_correction_attempts} attempts, max was {MAX_TEMPORAL_CORRECTION_ATTEMPTS}"
                )
            else:
                logging_util.info(
                    f"✅ TEMPORAL_WARNING added to response: {temporal_correction_attempts} correction(s) fixed the issue"
                )

            prevention_extras["temporal_correction_warning"] = temporal_warning
            prevention_extras["temporal_correction_attempts"] = (
                temporal_correction_attempts
            )

        # Extract LLM-requested instruction hints for next turn
        # The LLM can signal it needs detailed sections (e.g., relationships, reputation)
        # via debug_info.meta.needs_detailed_instructions in its response
        get_debug_info = getattr(llm_response_obj, "get_debug_info", None)
        llm_debug_info = get_debug_info() if callable(get_debug_info) else {}
        if not isinstance(llm_debug_info, dict):
            llm_debug_info = {}
        # Wrap in dict as extract_llm_instruction_hints expects {"debug_info": {...}}
        instruction_hints = extract_llm_instruction_hints(
            {"debug_info": llm_debug_info}
        )
        pending_instruction_hints = instruction_hints
        if pending_instruction_hints:
            logging_util.info(
                f"📋 DYNAMIC_PROMPTS: LLM requested detailed sections for next turn: {pending_instruction_hints}"
            )

        response = {
            "story": llm_response_obj.narrative_text,
            "state_changes": state_changes,
        }

        # Capture original time before update for accurate monotonicity validation
        # Note: current_game_state is a GameState instance (has to_dict() method)
        # Preserve an immutable snapshot for XP/level comparisons
        original_state_for_level_check = copy.deepcopy(current_game_state.to_dict())
        # Work on a deep copy so in-place mutations do not affect the original snapshot
        current_state_as_dict = copy.deepcopy(original_state_for_level_check)
        # Use `or {}` to handle both missing and explicitly-null world_data
        # CRITICAL: Deep-copy to prevent mutation by update_state_with_changes
        original_world_time = copy.deepcopy(
            (original_state_for_level_check.get("world_data") or {}).get("world_time")
        )

        # Capture previous combat state for post-combat warning detection
        previous_combat_state = copy.deepcopy(
            original_state_for_level_check.get("combat_state", {})
        )

        # Clear old pending_system_corrections BEFORE merge
        # These were already consumed by llm_service (sent to LLM in this turn)
        # Any NEW corrections from the LLM's state_updates will be preserved by the merge
        current_state_as_dict.pop("pending_system_corrections", None)

        # Only include pending_instruction_hints in state_changes when we have new
        # hints to store OR when we need to clear existing hints from prior turns.
        if pending_instruction_hints or original_state_for_level_check.get(
            "pending_instruction_hints"
        ):
            state_changes["pending_instruction_hints"] = pending_instruction_hints

        # Update game state with changes
        # SAFETY: Different filtering based on mode:
        # - Think Mode: Block ALL state changes except microsecond (pure analysis, no game state)
        # - freeze_time choice: Allow level-up/other state changes, only freeze TIME
        # - Character creation: Allow state changes, freeze TIME to microsecond-only
        # Use state_changes from enforce_preventive_guards (with cooldown/damage guards applied)
        # NOT response.get("state_changes") which is the raw LLM output without guards

        # Check if user selected a freeze_time choice (e.g., level-up)
        is_freeze_time_choice = _should_freeze_time_for_selected_choice(
            user_input, story_context
        )
        should_freeze_time = (
            is_think_mode
            or is_freeze_time_choice
            or is_character_creation_mode
            or is_level_up_mode
        )

        state_changes_to_apply = state_changes
        if is_think_mode:
            # Think mode: block all state changes and freeze time to a microsecond tick
            state_changes_to_apply = _apply_freeze_time_state_changes(
                state_changes_to_apply,
                original_world_time=original_world_time,
                allow_state_changes=False,
            )
            if response.get("state_changes", {}) != state_changes_to_apply:
                logging_util.info(
                    "🧠 THINK_MODE_SAFETY: Blocked non-time state changes in Think Mode"
                )
        elif should_freeze_time:
            # Freeze time for character creation and freeze_time choices.
            state_changes_to_apply = _apply_freeze_time_state_changes(
                state_changes_to_apply,
                original_world_time=original_world_time,
                allow_state_changes=True,
            )
            logging_util.info(
                "🕐 TIME_FREEZE: Applied microsecond-only time advancement"
            )

        if state_changes_to_apply:
            updated_game_state_dict = update_state_with_changes(
                current_state_as_dict, state_changes_to_apply
            )
        else:
            updated_game_state_dict = current_state_as_dict

        # Track player character in active_entities once name is known, to support
        # entity validation and reduce hallucinations in subsequent turns.
        current_custom_state = current_state_as_dict.get("custom_campaign_state") or {}
        if not isinstance(current_custom_state, dict):
            current_custom_state = {}

        custom_state = updated_game_state_dict.get("custom_campaign_state") or {}
        if not isinstance(custom_state, dict):
            custom_state = {}

        was_creating = current_custom_state.get("character_creation_in_progress", False)
        stage = custom_state.get("character_creation_stage")
        is_completed = bool(custom_state.get("character_creation_completed")) or (
            stage == "complete"
        )
        flag_cleared = not bool(
            custom_state.get("character_creation_in_progress", True)
        )

        logging_util.debug(
            f"🔍 Entity tracking check: was_creating={was_creating}, is_completed={is_completed}, flag_cleared={flag_cleared}"
        )

        player_data = updated_game_state_dict.get("player_character_data") or {}
        if not isinstance(player_data, dict):
            player_data = {}

        player_name = player_data.get("name")
        should_track_player = False
        if was_creating and flag_cleared and is_completed:
            # Character creation just completed.
            should_track_player = True
        elif was_creating and stage in ("review", "level_up", "complete"):
            # God Mode templates and later phases have stable character identity.
            should_track_player = True
        elif (not was_creating) and player_name:
            # Story mode or other modes: ensure player is tracked if present.
            should_track_player = True

        if should_track_player and player_name:
            entity_tracking = updated_game_state_dict.get("entity_tracking")
            if not isinstance(entity_tracking, dict):
                entity_tracking = {}
                updated_game_state_dict["entity_tracking"] = entity_tracking

            active_entities = entity_tracking.get("active_entities")
            if not isinstance(active_entities, list):
                active_entities = []
                entity_tracking["active_entities"] = active_entities

            # Add player character if not already present
            if player_name not in active_entities:
                active_entities.append(player_name)
                logging_util.info(
                    f"✅ Added player character '{player_name}' to active_entities"
                )

        # Apply automatic combat cleanup (sync defeated enemies between combat_state and npc_data).
        # Intentional: cleanup runs even during time-freeze/Think/creation paths to keep state consistent.
        # Named NPCs are preserved and marked dead for continuity, while generic enemies are deleted.
        updated_game_state_dict = apply_automatic_combat_cleanup(
            updated_game_state_dict, response.get("state_changes", {})
        )

        # Validate and auto-correct XP/level and time consistency
        # Use `or {}` to handle both missing and explicitly-null world_data in state_changes
        new_world_time = (
            response.get("state_changes", {}).get("world_data") or {}
        ).get("world_time")
        # DISCREPANCY DETECTION: Detect rewards state errors for LLM self-correction
        # Instead of server-side enforcement, we inform the LLM of issues via system_corrections
        # The LLM will fix them in the next inference (LLM Decides, Server Detects principle)
        if mode in (
            constants.MODE_REWARDS,
            constants.MODE_COMBAT,
            constants.MODE_CHARACTER,
            constants.MODE_LEVEL_UP,
        ):
            rewards_warnings: list[str] = []
            rewards_discrepancies = _detect_rewards_discrepancy(
                updated_game_state_dict,
                original_state_dict=original_state_for_level_check,
                warnings_out=rewards_warnings,
            )
            if rewards_discrepancies:
                prevention_extras.setdefault("system_corrections", []).extend(
                    rewards_discrepancies
                )
            if rewards_warnings:
                prevention_extras.setdefault("system_warnings", []).extend(
                    rewards_warnings
                )

        # SERVER-SIDE LEVEL-UP DETECTION: Check for level-up in ALL modes where
        # original_state_dict is available for XP comparison. This ensures
        # level-up is offered even when XP is awarded outside rewards pipeline
        # (e.g., God Mode, narrative milestones, manual XP grants)
        updated_game_state_dict = _check_and_set_level_up_pending(
            updated_game_state_dict, original_state_dict=original_state_for_level_check
        )

        # Validate and auto-correct state before persistence, capturing any corrections made
        updated_game_state_dict, state_corrections = validate_and_correct_state(
            updated_game_state_dict,
            previous_world_time=original_world_time,
            return_corrections=True,
        )

        # If rewards are now pending but we did NOT run RewardsAgent, run it once
        # to ensure user-visible rewards output.
        # NOTE: This must happen BEFORE post-combat detection to avoid false-positive
        # "no XP awarded" warnings when RewardsAgent awards XP in the followup.
        try:
            (
                updated_game_state_dict,
                llm_response_obj,
                prevention_extras,
            ) = await _process_rewards_followup(
                mode=mode,
                llm_response_obj=llm_response_obj,
                updated_game_state_dict=updated_game_state_dict,
                original_state_as_dict=original_state_for_level_check,
                original_world_time=original_world_time,
                story_context=story_context,
                selected_prompts=selected_prompts,
                use_default_world=use_default_world,
                user_id=user_id,
                prevention_extras=prevention_extras,
            )
        except Exception as e:
            logging_util.warning(f"⚠️ REWARDS_FOLLOWUP failed: {e}")

        # Re-validate state after rewards followup to capture any additional corrections
        # This ensures corrections from RewardsAgent state changes are surfaced to user
        updated_game_state_dict, followup_corrections = validate_and_correct_state(
            updated_game_state_dict,
            previous_world_time=original_world_time,
            return_corrections=True,
        )
        # Merge corrections (deduplicate since some may overlap)
        all_corrections = state_corrections + [
            c for c in followup_corrections if c not in state_corrections
        ]

        # Detect post-combat issues AFTER rewards followup to avoid false positives
        # when RewardsAgent awards XP during the followup
        updated_game_state_obj = GameState.from_dict(updated_game_state_dict)
        post_combat_warnings = []
        if updated_game_state_obj:
            # Compare final state against original to detect if XP was ever awarded
            final_pc = updated_game_state_dict.get("player_character_data", {})
            # Use the preserved pre-update snapshot for XP comparison to avoid
            # false negatives when update_state_with_changes mutates the current
            # state dict in-place.
            original_pc = original_state_for_level_check.get(
                "player_character_data", {}
            )
            final_xp = _extract_xp_from_player_data(final_pc)
            original_xp = _extract_xp_from_player_data(original_pc)

            # Only warn if XP didn't increase at all (including from rewards followup)
            xp_increased = final_xp > original_xp
            if not xp_increased:
                post_combat_warnings = updated_game_state_obj.detect_post_combat_issues(
                    previous_combat_state, response.get("state_changes", {})
                )

        # Combine all system warnings (including any from rewards followup)
        rewards_corrections = prevention_extras.get("rewards_corrections", [])
        extra_warnings = prevention_extras.get("system_warnings", [])

        # Extract server-generated system_warnings from LLM response debug_info
        # SECURITY: Only read _server_system_warnings (server-controlled) to prevent LLM spoofing
        # LLM-provided system_warnings in debug_info are ignored for security
        server_system_warnings = []
        if llm_response_obj and hasattr(llm_response_obj, "structured_response"):
            structured_response = llm_response_obj.structured_response
            if structured_response:
                debug_info = getattr(structured_response, "debug_info", None)
                if isinstance(debug_info, dict):
                    server_warnings = debug_info.get("_server_system_warnings", [])
                    if isinstance(server_warnings, list):
                        server_system_warnings = server_warnings

        system_warnings = (
            all_corrections
            + rewards_corrections
            + post_combat_warnings
            + extra_warnings
            + server_system_warnings
        )

        # Deduplicate warnings while preserving order
        if system_warnings:
            system_warnings = list(dict.fromkeys(system_warnings))

        # Increment turn counter using centralized function (single source of truth)
        updated_game_state_dict = _increment_turn_counter(
            updated_game_state_dict,
            is_god_mode=is_god_mode,
            should_freeze_time=should_freeze_time,
        )

        if is_god_mode:
            # GOD MODE: Process directives from LLM response
            # The GodModeAgent analyzes the user's message and returns directives
            # Format: {"directives": {"add": ["rule1", ...], "drop": ["rule2", ...]}}  # noqa: ERA001
            early_structured = structured_fields_utils.extract_structured_fields(
                llm_response_obj
            )
            llm_directives = early_structured.get("directives", {})
            if not isinstance(llm_directives, dict):
                llm_directives = {}

            def _normalize_directive_list(value: Any) -> list[str]:
                if value is None:
                    return []
                if isinstance(value, str):
                    return [value] if value.strip() else []
                if isinstance(value, dict):
                    rule = value.get("rule")
                    return [rule] if isinstance(rule, str) and rule.strip() else []
                if isinstance(value, list):
                    normalized: list[str] = []
                    for item in value:
                        if isinstance(item, str):
                            if item.strip():
                                normalized.append(item)
                        elif isinstance(item, dict):
                            rule = item.get("rule")
                            if isinstance(rule, str) and rule.strip():
                                normalized.append(rule)
                    return normalized
                return []

            directives_to_add = _normalize_directive_list(llm_directives.get("add"))
            directives_to_drop = _normalize_directive_list(llm_directives.get("drop"))

            ccs = updated_game_state_dict.setdefault("custom_campaign_state", {}) or {}
            directives_list = ccs.setdefault("god_mode_directives", [])

            # Ensure god_mode_directives is a list (handle legacy dict format)
            if not isinstance(directives_list, list):
                logging_util.warning(
                    f"god_mode_directives was {type(directives_list).__name__}, converting to list"
                )
                directives_list = []
                ccs["god_mode_directives"] = directives_list

            # Process directives to drop (remove matching rules)
            if directives_to_drop:
                drop_lower = [d.strip().lower() for d in directives_to_drop if d]
                original_count = len(directives_list)

                def _get_rule_lower(d: Any) -> str:
                    """Safely extract and lowercase a rule, handling None values."""
                    if isinstance(d, dict):
                        rule = d.get("rule")
                        return rule.strip().lower() if isinstance(rule, str) else ""
                    return str(d).strip().lower() if d else ""

                directives_list[:] = [
                    d for d in directives_list if _get_rule_lower(d) not in drop_lower
                ]
                dropped_count = original_count - len(directives_list)
                if dropped_count > 0:
                    logging_util.info(f"GOD MODE: Dropped {dropped_count} directives")

            def _should_reject_directive(rule: str) -> bool:
                """
                Filter out directives that should not be saved.

                IMPORTANT: We only reject directives that are STATE VALUES or ONE-TIME EVENTS.
                BEHAVIORAL RULES (like "always apply Guidance", "always use advantage") MUST be kept.

                Reject:
                - State values that change: "Level is X", "HP is Y", "Gold is Z"
                - One-time events: "You just killed X", "You defeated Y"
                - Formatting: "Always include X in header" (handled by system prompts)

                Keep:
                - Behavioral rules: "Always apply Guidance", "Always use Enhance Ability"
                - Persistent mechanics: "Apply advantage to Stealth", "Always use Foresight"
                - Ongoing effects: "Maintain X buff", "Track Y condition" (if behavioral)
                """
                rule_lower = rule.lower().strip()

                # AI sometimes prefixes directives with "Rule: "
                # We strip it for matching against our patterns
                if rule_lower.startswith("rule:"):
                    rule_lower = rule_lower[5:].strip()

                # Reject patterns: State values (numbers that change)
                # These are specific values, not behavioral rules
                state_value_patterns = [
                    "level is",  # "Level is 42" - specific value
                    "real level is",  # "Real Level is 15" - specific value
                    "hp is",  # "HP is 50" - specific value
                    "gold is",  # "Gold is 1000" - specific value
                    "xp is",  # "XP is 5000" - specific value
                    "experience is",  # "Experience is 5000" - specific value
                    "soul coin is",  # "Soul Coin is 25k" - specific value
                    "base spell save dc is",  # Calculated value
                    "effective charisma is",  # Calculated value
                ]

                # Reject patterns: One-time events (history, not ongoing rules)
                # These patterns are more specific to catch actual one-time events,
                # not behavioral rules like "Killed enemies should drop loot"
                one_time_patterns = [
                    "you just",  # "You just killed X"
                    "you just killed",  # More specific than just "killed"
                    "you just defeated",  # More specific than just "defeated"
                    "you just completed",  # More specific than just "completed"
                ]

                # Reject patterns: Formatting instructions (system-level, not game rules)
                formatting_patterns = [
                    "always include",  # "Always include XP in header"
                    "format",  # Formatting instructions
                ]

                # Check for state value patterns (must be exact value, not behavioral)
                # e.g., "Level is 42" is bad, but "Level affects X" might be OK
                for pattern in state_value_patterns:
                    if pattern in rule_lower:
                        # Additional check: if it's followed by a number or specific value, reject
                        # But if it's behavioral like "Level affects calculations", allow it
                        pattern_idx = rule_lower.find(pattern)
                        if pattern_idx != -1:
                            after_pattern = rule_lower[
                                pattern_idx + len(pattern) :
                            ].strip()
                            # If followed by a number or "=", it's a state value
                            if after_pattern and (
                                after_pattern[0].isdigit()
                                or after_pattern.startswith("=")
                            ):
                                return True

                # Check for one-time events (with additional context check)
                # Only reject if it's clearly a one-time event, not a behavioral rule
                for pattern in one_time_patterns:
                    if pattern in rule_lower:
                        pattern_idx = rule_lower.find(pattern)
                        if pattern_idx != -1:
                            # Get context from original rule to preserve capitalization for proper noun detection
                            # We find the pattern in rule_lower but apply the same offset to original rule
                            # This is safe since rule_lower has same length as rule
                            after_pattern_orig = rule[
                                rule.lower().find(pattern) + len(pattern) :
                            ].strip()
                            if after_pattern_orig:
                                behavioral_indicators = [
                                    "should",
                                    "grant",
                                    "affect",
                                    "provide",
                                    "give",
                                    "drop",
                                    "always",
                                ]
                                is_behavioral = any(
                                    indicator in after_pattern_orig.lower()
                                    for indicator in behavioral_indicators
                                )
                                if not is_behavioral:
                                    # Check if it looks like a one-time event (specific entity/event)
                                    after_lower = after_pattern_orig.lower()
                                    if (
                                        after_lower.startswith(("the ", "a ", "an "))
                                        or after_pattern_orig[0].isupper()
                                    ):
                                        return True

                # Check for formatting instructions (with context validation)
                # Only reject if it's clearly formatting, not behavioral rules
                for pattern in formatting_patterns:
                    if pattern in rule_lower:
                        pattern_idx = rule_lower.find(pattern)
                        if pattern_idx != -1:
                            after_pattern = rule_lower[
                                pattern_idx + len(pattern) :
                            ].strip()
                            # Formatting patterns are usually about display/headers, not game mechanics
                            # If followed by formatting keywords, reject; otherwise allow behavioral rules
                            formatting_keywords = [
                                "in header",
                                "in title",
                                "in display",
                                "as text",
                                "as string",
                            ]
                            is_formatting = any(
                                keyword in after_pattern
                                for keyword in formatting_keywords
                            )
                            if is_formatting:
                                return True
                            # If it's about game mechanics (bonus, damage, effect), allow it
                            behavioral_keywords = [
                                "bonus",
                                "damage",
                                "effect",
                                "grant",
                                "provide",
                                "apply",
                                "affect",
                            ]
                            if any(
                                keyword in after_pattern
                                for keyword in behavioral_keywords
                            ):
                                continue  # Don't reject - it's a behavioral rule
                            # If pattern is "format" alone without context, be more conservative
                            if pattern == "format" and len(after_pattern) < 10:
                                # Short "format" phrases are likely formatting instructions
                                return True

                # Allow everything else (behavioral rules, persistent mechanics, etc.)
                return False

            for new_rule in directives_to_add:
                if not new_rule or not isinstance(new_rule, str):
                    continue
                # Strip whitespace from new rule
                new_rule_clean = new_rule.strip()
                if not new_rule_clean:
                    continue

                # Filter out problematic directives (server-side validation)
                if _should_reject_directive(new_rule_clean):
                    logging_util.warning(
                        f"GOD MODE: Rejected problematic directive (should be in state_updates, not directives): {new_rule_clean[:100]}"
                    )
                    continue

                # Case-insensitive duplicate check
                existing_rules_lower = [
                    (
                        d.get("rule", "").strip().lower()
                        if isinstance(d, dict)
                        else str(d).strip().lower()
                    )
                    for d in directives_list
                    if (isinstance(d, dict) and d.get("rule"))
                    or (not isinstance(d, dict) and d)
                ]
                if new_rule_clean.lower() not in existing_rules_lower:
                    directives_list.append(
                        {
                            "rule": new_rule_clean,
                            "added": datetime.now(timezone.utc).isoformat(),  # noqa: UP017
                        }
                    )
                    logging_util.info(f"GOD MODE DIRECTIVE ADDED: {new_rule_clean}")

        # Calculate sequence_id and user_scene_number before persistence so they can
        # be stored on the AI story entry in Firestore.
        sequence_id = len(story_context) + 2
        user_scene_number = (
            sum(
                1
                for entry in story_context
                if isinstance(entry, dict)
                and str(entry.get("actor", "")).lower()
                == constants.ACTOR_GEMINI.lower()
            )
            + 1
        )

        agent_mode_used = getattr(llm_response_obj, "agent_mode", None)
        updated_game_state_dict = _maybe_update_living_world_tracking(
            updated_game_state_dict,
            current_game_state=current_game_state,
            turn_number=updated_game_state_dict.get("turn_number", 0),
            mode=mode,
            agent_mode=agent_mode_used,
            is_god_mode=is_god_mode,
            is_think_mode=is_think_mode,
            should_freeze_time=should_freeze_time,
            state_changes_this_turn=state_changes_to_apply,
        )

        # Debug warning: living world instruction fires every turn —
        # warn if world_events are missing when they should be present.
        # structured_fields not yet extracted at this point; use state_changes_to_apply.
        _warn_if_living_world_events_missing(
            updated_game_state_dict=updated_game_state_dict,
            state_changes_to_apply=state_changes_to_apply,
            structured_fields=None,
            is_god_mode=is_god_mode,
            is_think_mode=is_think_mode,
            mode=mode,
            agent_mode=agent_mode_used,
        )

        # Annotate world_events entries with turn/scene numbers for UI display
        player_turn = updated_game_state_dict.get("player_turn", 1)
        updated_game_state_dict = annotate_world_events_with_turn_scene(
            updated_game_state_dict, player_turn, scene_number=user_scene_number
        )

        # Capture any pending_system_corrections set by LLM (e.g. God Mode)
        # At this point, OLD corrections were already cleared earlier in the function
        # right before the state merge, so any present now are NEW from LLM state_updates.
        llm_pending_corrections_list = _normalize_system_corrections(
            updated_game_state_dict.pop("pending_system_corrections", None)
        )

        # PRE-FLIGHT: Initialize current_game_state_dict before any conditional blocks
        # to ensure it is always defined for downstream logic (e.g. modal injection).
        current_game_state_dict = current_game_state.to_dict()

        llm_reward_corrections = _filter_reward_corrections(
            llm_pending_corrections_list
        )
        llm_non_reward_corrections = [
            correction
            for correction in llm_pending_corrections_list
            if not _is_reward_correction(correction)
        ]

        # Combine with validator-generated corrections (reward-related only)
        validator_corrections_list = _normalize_system_corrections(
            prevention_extras.get("system_corrections")
        )

        reward_corrections = llm_reward_corrections + _filter_reward_corrections(
            validator_corrections_list
        )
        # Inject dice fabrication correction into pending_system_corrections
        # so the LLM learns what it did wrong on the NEXT turn (zero-latency self-correction).
        # ARCHITECTURAL FIX: Read from processing_metadata (server-authored) instead of
        # model-supplied debug_info to maintain proper trust boundary.
        dice_fabrication_corrections = []
        if llm_response_obj and hasattr(llm_response_obj, "processing_metadata"):
            processing_metadata = llm_response_obj.processing_metadata or {}
            fab_data = processing_metadata.get("dice_fabrication_correction")
            if isinstance(fab_data, dict):
                fab_rolls = fab_data.get("fabricated_rolls", [])
                code_used = fab_data.get("code_execution_used", False)
                roll_summary = ""
                if isinstance(fab_rolls, list) and fab_rolls:
                    roll_summary = f" Fabricated rolls: {fab_rolls}."
                if code_used is True:
                    dice_fabrication_corrections.append(
                        "CORRECTION: You ran code_execution but did not use "
                        "random.randint() for dice rolls. Your dice values were "
                        f"not RNG-generated.{roll_summary} You MUST call "
                        "random.randint() in code_execution for every dice roll."
                    )
                elif code_used is False:
                    dice_fabrication_corrections.append(
                        "CORRECTION: You did not use the code_execution tool for "
                        "dice rolls. You fabricated dice values directly in your "
                        f"JSON response.{roll_summary} You MUST use the "
                        "code_execution tool with random.randint() for ALL dice "
                        "rolls. Never output dice values without running code."
                    )
                else:
                    dice_fabrication_corrections.append(
                        "CORRECTION: Dice rolls were fabricated or unverifiable. "
                        f"Use code_execution with random.randint() for ALL dice rolls.{roll_summary}"
                    )
                logging_util.warning(
                    "🎲 Injecting dice fabrication correction into "
                    "pending_system_corrections: %s...",
                    dice_fabrication_corrections[0][:100],
                )

        all_corrections = (
            llm_non_reward_corrections
            + reward_corrections
            + dice_fabrication_corrections
        )

        if all_corrections:
            # Deduplicate while preserving order
            # Note: all_corrections is guaranteed to be list[str] thanks to _normalize_system_corrections
            pending_corrections = list(dict.fromkeys(all_corrections))
            updated_game_state_dict["pending_system_corrections"] = pending_corrections
            logging_util.info(
                f"📋 Persisted {len(pending_corrections)} system_corrections "
                "to game_state.pending_system_corrections"
            )

        # Then save the AI response with structured fields if available
        ai_response_text = llm_response_obj.narrative_text

        # GOD MODE: Use god_mode_response as story text since narrative is empty
        # This ensures the LLM sees god mode responses in story history on subsequent turns,
        # preventing context confusion where the model echoes previous responses
        if is_god_mode and not ai_response_text:
            structured_response = getattr(llm_response_obj, "structured_response", None)
            if (
                structured_response
                and hasattr(structured_response, "god_mode_response")
                and structured_response.god_mode_response
            ):
                god_mode_text = structured_response.god_mode_response
                # Type guard: ensure god_mode_response is a string before using
                if isinstance(god_mode_text, str):
                    ai_response_text = god_mode_text
                    preview = (
                        ai_response_text[:50]
                        if len(ai_response_text) > 50
                        else ai_response_text
                    )
                    logging_util.info(
                        f"✅ GOD_MODE: Using god_mode_response for story entry: {preview}..."
                    )

        # Extract structured fields from AI response for storage
        structured_fields = _ensure_session_header_resources(
            structured_fields_utils.extract_structured_fields(llm_response_obj),
            updated_game_state_dict,
        )
        if not isinstance(structured_fields.get(constants.FIELD_PLANNING_BLOCK), dict):
            structured_fields[constants.FIELD_PLANNING_BLOCK] = {}
        structured_fields.update(prevention_extras)

        # Persist server-side level-up injections so stored story entries
        # reflect the same narrative/choices delivered to the user.
        if not is_god_mode:
            _sr = getattr(llm_response_obj, "structured_response", None)
            rewards_box = getattr(_sr, "rewards_box", None)
            if not _should_emit_level_up_rewards_box(
                updated_game_state_dict, rewards_box
            ):
                rewards_box = None
                structured_fields.pop("rewards_box", None)

            injected_planning_block = _inject_levelup_choices_if_needed(
                structured_fields.get("planning_block"),
                updated_game_state_dict,
                rewards_box=rewards_box,
            )
            if injected_planning_block is not None:
                structured_fields["planning_block"] = injected_planning_block

            upgrade_injected_block = _inject_campaign_upgrade_choice_if_needed(
                structured_fields.get("planning_block"),
                updated_game_state_dict,
                getattr(llm_response_obj, "agent_mode", None),
            )
            if upgrade_injected_block is not None:
                structured_fields["planning_block"] = upgrade_injected_block

            injected_narrative = _inject_levelup_narrative_if_needed(
                ai_response_text,
                structured_fields.get("planning_block"),
                updated_game_state_dict,
                rewards_box=rewards_box,
            )
            if injected_narrative != ai_response_text:
                ai_response_text = injected_narrative
                llm_response_obj.narrative_text = injected_narrative

            # SERVER-SIDE SPICY MODE CHOICE INJECTION
            # When LLM detects intimate content, inject enable_spicy_mode choice
            # When LLM detects scene ending (and spicy mode is on), inject disable choice
            spicy_injected_planning_block = _inject_spicy_mode_choice_if_needed(
                structured_fields.get("planning_block"),
                llm_response_obj.structured_response
                if hasattr(llm_response_obj, "structured_response")
                else None,
                user_settings,
            )
            if spicy_injected_planning_block is not None:
                structured_fields["planning_block"] = spicy_injected_planning_block

            modal_finish_injected_block = _inject_modal_finish_choice_if_needed(
                structured_fields.get("planning_block"),
                current_game_state_dict,
            )
            if modal_finish_injected_block is not None:
                structured_fields["planning_block"] = modal_finish_injected_block

        # Annotate THIS TURN's world_events (from LLM response) with turn/scene numbers
        # NOTE: We annotate structured_fields directly, NOT game_state.world_events
        # game_state.world_events is CUMULATIVE (contains all historical events)
        # structured_fields.world_events contains only THIS TURN's new events
        # BUG FIX: Previously copied cumulative game_state.world_events causing duplicates
        llm_world_events = structured_fields.get("world_events")
        if not llm_world_events:
            # Check state_updates for world_events
            llm_world_events = structured_fields.get("state_updates", {}).get(
                "world_events"
            )

        if llm_world_events and isinstance(llm_world_events, dict):
            llm_world_events = normalize_world_events_for_story_payload(
                llm_world_events
            )
            # Annotate the LLM response's world_events with current turn/scene
            annotate_world_events_with_turn_scene(
                {"world_events": llm_world_events},
                player_turn,
                scene_number=user_scene_number,
            )
            # Ensure it's in structured_fields for storage
            structured_fields["world_events"] = llm_world_events
            if "state_updates" in structured_fields:
                structured_fields["state_updates"]["world_events"] = llm_world_events

        # Add faction_header to structured_fields if present (for campaign export)
        # Generate faction header if minigame is enabled (same logic as unified_response)
        # This ensures faction headers appear in exported campaigns
        temp_response_for_header = {}
        temp_response_for_header = _ensure_faction_header_if_enabled(
            temp_response_for_header, updated_game_state_dict
        )
        faction_header = temp_response_for_header.get("faction_header")
        if faction_header:
            structured_fields["faction_header"] = faction_header

        # Write system_warnings to structured_fields so they are persisted
        # to Firestore with the story entry. Without this, _server_system_warnings
        # (dice fabrication warnings etc.) are assembled but never saved.
        if system_warnings:
            structured_fields["system_warnings"] = system_warnings

        structured_fields["sequence_id"] = sequence_id
        structured_fields["user_scene_number"] = user_scene_number

        # If LLM omitted world_events in structured payload, backfill per-entry
        # events from current game_state for this turn/scene.
        _try_backfill_story_entry_world_events(
            structured_fields,
            updated_game_state_dict=updated_game_state_dict,
            player_turn=player_turn,
            user_scene_number=user_scene_number,
        )

        # Ensure persisted story entries only contain living-world events generated
        # for their own scene. This prevents cumulative-history bleed into later scenes.
        world_events_for_entry = structured_fields.get("world_events")
        if isinstance(world_events_for_entry, dict):
            filtered_world_events = _filter_story_entry_world_events_to_scene(
                world_events_for_entry, user_scene_number, current_turn=player_turn
            )
            structured_fields["world_events"] = filtered_world_events
            state_updates_field = structured_fields.get("state_updates")
            if isinstance(state_updates_field, dict):
                state_updates_field["world_events"] = copy.deepcopy(
                    filtered_world_events
                )

        # Persist state + story entries.
        # LATENCY TRACKING: Firestore persistence
        persist_start = time.perf_counter()
        logging_util.info(
            "⏱️ LATENCY_PERSIST_START: Persisting state and story to Firestore"
        )

        if is_mock_services_mode():
            _persist_turn_to_firestore(
                user_id,
                campaign_id,
                mode=mode,
                user_input=user_input,
                ai_response_text=ai_response_text,
                structured_fields=structured_fields,
                updated_game_state_dict=updated_game_state_dict,
                sequence_id=sequence_id,
                user_scene_number=user_scene_number,
            )
        else:
            await asyncio.to_thread(
                _persist_turn_to_firestore,
                user_id,
                campaign_id,
                mode=mode,
                user_input=user_input,
                ai_response_text=ai_response_text,
                structured_fields=structured_fields,
                updated_game_state_dict=updated_game_state_dict,
                sequence_id=sequence_id,
                user_scene_number=user_scene_number,
            )

        persist_duration = time.perf_counter() - persist_start
        logging_util.info(
            f"⏱️ LATENCY_PERSIST_END: Firestore persistence completed in {persist_duration:.2f}s"
        )

        # Get debug mode for narrative text processing
        debug_mode = (
            current_game_state.debug_mode
            if hasattr(current_game_state, "debug_mode")
            else False
        )

        # Extract narrative text with proper debug mode handling
        get_narrative_text = getattr(llm_response_obj, "get_narrative_text", None)
        if callable(get_narrative_text):
            final_narrative = get_narrative_text(debug_mode=debug_mode)
            if not isinstance(final_narrative, str):
                final_narrative = llm_response_obj.narrative_text
        else:
            final_narrative = llm_response_obj.narrative_text

        # Defensive check: ensure narrative is never None or empty
        # NOTE: Use constants.is_god_mode() for case-insensitive + prefix detection.
        # For god mode requests, empty narrative is EXPECTED - admin responses
        # use god_mode_response for display, not narrative prose.
        if not final_narrative or not isinstance(final_narrative, str):
            final_narrative = _resolve_empty_narrative(
                final_narrative, llm_response_obj, mode, user_input
            )

        # Note: With "text" field fix, empty narratives should now be properly handled
        # by the translation layer without needing fallback messages

        # Extract structured fields from LLM response (critical missing fields)
        structured_response = getattr(llm_response_obj, "structured_response", None)

        # Process story for display (convert narrative text to story entries format)
        # Use "text" field to match translation layer expectations in main.py
        story_entries = [{"text": final_narrative}]
        processed_story = process_story_for_display(story_entries, debug_mode)

        # NOTE: Level-up handling is fully delegated to the LLM. The LLM receives
        # rewards_pending in game state context and should recognize level-up eligibility
        # to generate appropriate rewards boxes per rewards_system_instruction.md.

        # Prefer concrete agent class name from debug_info when available.
        # This distinguishes split agents that share the same agent_mode constant.
        debug_info = getattr(structured_response, "debug_info", None)
        debug_agent_name = (
            debug_info.get("agent_name") if isinstance(debug_info, dict) else None
        )

        # Build comprehensive response with all frontend-required fields
        unified_response = {
            KEY_SUCCESS: True,
            "story": processed_story,
            "narrative": final_narrative,  # Add for frontend compatibility
            "response": final_narrative,  # Fallback for older frontend versions
            "game_state": updated_game_state_dict,
            "mode": mode,
            "user_input": user_input,
            "state_cleaned": was_cleaned,
            "entries_cleaned": num_cleaned,
            # CRITICAL: Add missing structured fields that frontend expects
            "sequence_id": sequence_id,
            "user_scene_number": user_scene_number,  # Scene number for current AI response: count of existing Gemini responses + 1
            "debug_mode": debug_mode,  # Add debug_mode for test compatibility
            # agent_mode: single source of truth for which agent was selected
            "agent_mode": getattr(llm_response_obj, "agent_mode", None),
            # agent_used: human-readable agent name for test compatibility
            "agent_used": debug_agent_name
            or _get_agent_name_from_mode(getattr(llm_response_obj, "agent_mode", None)),
            # FIX Bug worktree_logs6-e09: Include budget_warnings in API response
            # Budget warnings generated during context compaction should reach frontend
            "budget_warnings": getattr(llm_response_obj, "budget_warnings", []) or [],
        }

        if include_raw_llm_payloads:
            metadata = getattr(llm_response_obj, "processing_metadata", {}) or {}
            unified_response["processing_metadata"] = copy.deepcopy(metadata)
            if "raw_request_payload" in metadata:
                unified_response["raw_request_payload"] = metadata[
                    "raw_request_payload"
                ]
            if "raw_response_text" in metadata:
                unified_response["raw_response_text"] = metadata["raw_response_text"]

        # Include state updates for all successful responses so consumers and invariants
        # have a stable schema surface (not gated on debug mode).
        state_updates = response.get("state_changes")
        if not isinstance(state_updates, dict):
            state_updates = {}
        unified_response["state_updates"] = copy.deepcopy(state_updates)

        # Add full game state snapshot for schema checks if delta payload does not include it.
        if (
            "game_state" not in unified_response["state_updates"]
            and isinstance(updated_game_state_dict, dict)
            and updated_game_state_dict.get("combat_state") is not None
        ):
            unified_response["state_updates"]["game_state"] = updated_game_state_dict

        # CRITICAL: Also include world_events from structured_fields for living world UI.
        # world_events is often stored in structured_fields but omitted from response.state_changes.
        if structured_fields.get("world_events"):
            unified_response["world_events"] = structured_fields["world_events"]
            if isinstance(structured_fields["world_events"], dict):
                unified_response["state_updates"]["world_events"] = structured_fields[
                    "world_events"
                ]

        # On living-world turns, prefer game-state world events as a fallback when the
        # model omits the delta. This keeps invariant checks deterministic.
        turn_number_for_living_world = updated_game_state_dict.get("turn_number")
        is_living_world_turn = (
            isinstance(turn_number_for_living_world, int)
            and turn_number_for_living_world > 0
            and turn_number_for_living_world % constants.LIVING_WORLD_TURN_INTERVAL == 0
            and not (is_god_mode or is_think_mode)
        )
        if is_living_world_turn:
            state_updates_world_events = unified_response["state_updates"].get(
                "world_events"
            )
            game_world_events = updated_game_state_dict.get("world_events")
            if not isinstance(state_updates_world_events, dict):
                if isinstance(game_world_events, dict):
                    unified_response["state_updates"]["world_events"] = copy.deepcopy(
                        game_world_events
                    )
                    unified_response["world_events"] = copy.deepcopy(game_world_events)
            elif not isinstance(unified_response.get("world_events"), dict):
                unified_response["world_events"] = copy.deepcopy(
                    state_updates_world_events
                )
        # Add structured response fields if available
        if structured_response:
            # entities_mentioned only in debug mode
            if debug_mode and hasattr(structured_response, "entities_mentioned"):
                unified_response["entities_mentioned"] = (
                    structured_response.entities_mentioned
                )
            if hasattr(structured_response, "location_confirmed"):
                unified_response["location_confirmed"] = (
                    structured_response.location_confirmed
                )
            # Use enriched session_header from structured_fields (already processed by
            # _ensure_session_header_resources with normalization, fallback, and format transform)
            # instead of raw structured_response.session_header
            enriched_session_header = structured_fields.get(
                constants.FIELD_SESSION_HEADER
            )
            if enriched_session_header:
                unified_response["session_header"] = enriched_session_header
            elif hasattr(structured_response, "session_header"):
                # Fallback to raw response if structured_fields not available
                unified_response["session_header"] = structured_response.session_header
            # Use structured_fields["planning_block"] if available (includes server-side injections)
            # Otherwise fall back to structured_response.planning_block (raw LLM response)
            if "planning_block" in structured_fields:
                planning_block = structured_fields["planning_block"]
                unified_response["planning_block"] = (
                    planning_block if isinstance(planning_block, dict) else {}
                )
            elif hasattr(structured_response, "planning_block"):
                planning_block = structured_response.planning_block
                unified_response["planning_block"] = (
                    planning_block if isinstance(planning_block, dict) else {}
                )
            # Legacy dice_rolls/dice_audit_events - prefer extraction from action_resolution
            # but allow direct population for backward compatibility
            if hasattr(structured_response, "dice_rolls"):
                unified_response["dice_rolls"] = structured_response.dice_rolls
            if hasattr(structured_response, "dice_audit_events"):
                # Reconcile dice_audit_events with stdout to fix:
                # 1. LLM putting total in rolls field instead of raw roll
                # 2. LLM using "roll" (singular) instead of "rolls" (array) in stdout
                debug_info = (
                    structured_response.debug_info
                    if hasattr(structured_response, "debug_info")
                    else None
                )
                unified_response["dice_audit_events"] = (
                    dice_integrity.reconcile_dice_audit_events_with_stdout(
                        structured_response.dice_audit_events,
                        debug_info,
                    )
                )
            if hasattr(structured_response, "resources"):
                unified_response["resources"] = structured_response.resources
            if hasattr(structured_response, "tool_requests"):
                unified_response["tool_requests"] = structured_response.tool_requests
            # Include action_resolution and outcome_resolution for all responses
            # (was previously gated behind rewards_box check, causing dice rolls
            # to be absent from responses without rewards_box, e.g. mock mode)
            add_action_resolution_to_response(structured_response, unified_response)
        if hasattr(structured_response, "rewards_box"):
            unified_response["rewards_box"] = structured_response.rewards_box
            if hasattr(structured_response, "social_hp_challenge"):
                unified_response["social_hp_challenge"] = (
                    structured_response.social_hp_challenge
                )
            # Spicy mode detection fields
            if (
                hasattr(structured_response, "recommend_spicy_mode")
                and structured_response.recommend_spicy_mode is not None
            ):
                unified_response["recommend_spicy_mode"] = (
                    structured_response.recommend_spicy_mode
                )
            if (
                hasattr(structured_response, "recommend_exit_spicy_mode")
                and structured_response.recommend_exit_spicy_mode is not None
            ):
                unified_response["recommend_exit_spicy_mode"] = (
                    structured_response.recommend_exit_spicy_mode
                )
            # debug_info only in debug mode
            if debug_mode and hasattr(structured_response, "debug_info"):
                unified_response["debug_info"] = structured_response.debug_info
            # God mode response (when applicable)
            if (
                hasattr(structured_response, "god_mode_response")
                and structured_response.god_mode_response
            ):
                unified_response["god_mode_response"] = (
                    structured_response.god_mode_response
                )

        # SERVER-SIDE LEVEL-UP CHOICE INJECTION
        # When level_up_available=true, ensure planning_block has required choices
        # This prevents the "text shown but no buttons" failure mode where users
        # see "LEVEL UP AVAILABLE!" but have no way to click to level up.
        # Skip injection in GOD MODE responses (god: choices required there).
        if not unified_response.get("god_mode_response"):
            rewards_box = unified_response.get("rewards_box")
            if not _should_emit_level_up_rewards_box(
                updated_game_state_dict, rewards_box
            ):
                unified_response.pop("rewards_box", None)
                rewards_box = None

            injected_planning_block = _inject_levelup_choices_if_needed(
                unified_response.get("planning_block"),
                updated_game_state_dict,
                rewards_box=rewards_box,
            )
            if injected_planning_block is not None:
                unified_response["planning_block"] = injected_planning_block

            upgrade_injected_block = _inject_campaign_upgrade_choice_if_needed(
                unified_response.get("planning_block"),
                updated_game_state_dict,
                getattr(llm_response_obj, "agent_mode", None),
            )
            if upgrade_injected_block is not None:
                unified_response["planning_block"] = upgrade_injected_block

            # SERVER-SIDE LEVEL-UP NARRATIVE INJECTION
            injected_narrative = _inject_levelup_narrative_if_needed(
                unified_response.get("narrative"),
                unified_response.get("planning_block"),
                updated_game_state_dict,
                rewards_box=rewards_box,
            )
            if injected_narrative != unified_response.get("narrative"):
                unified_response["narrative"] = injected_narrative
                unified_response["response"] = injected_narrative
                unified_response["story"] = process_story_for_display(
                    [{"text": injected_narrative}], debug_mode
                )

            # SERVER-SIDE SPICY MODE CHOICE INJECTION
            # When LLM detects intimate content, inject enable_spicy_mode choice
            # When LLM detects scene ending (and spicy mode is on), inject disable choice
            spicy_injected_block = _inject_spicy_mode_choice_if_needed(
                unified_response.get("planning_block"),
                structured_response,
                user_settings,
            )
            if spicy_injected_block is not None:
                unified_response["planning_block"] = spicy_injected_block

            modal_finish_block = _inject_modal_finish_choice_if_needed(
                unified_response.get("planning_block"),
                current_game_state_dict,
            )
            if modal_finish_block is not None:
                unified_response["planning_block"] = modal_finish_block

        capture_evidence = os.getenv("CAPTURE_EVIDENCE", "").lower() == "true"
        if capture_evidence:
            metadata = getattr(llm_response_obj, "processing_metadata", {}) or {}
            llm_provider = metadata.get("llm_provider") or getattr(
                llm_response_obj, "provider", None
            )
            llm_model = metadata.get("llm_model") or getattr(
                llm_response_obj, "model", None
            )
            if llm_provider:
                unified_response["llm_provider"] = llm_provider
            if llm_model:
                unified_response["llm_model"] = llm_model
            if "dice_strategy" in metadata:
                unified_response["dice_strategy"] = metadata["dice_strategy"]
            if "raw_response_text" in metadata:
                unified_response["raw_llm_response"] = metadata["raw_response_text"]
            if "tool_results" in metadata:
                unified_response["tool_results"] = metadata["tool_results"]
            if "tool_requests_executed" in metadata:
                unified_response["tool_requests_executed"] = metadata[
                    "tool_requests_executed"
                ]
            # Add equipment_display if present (deterministic extraction from game_state)
            if "equipment_display" in metadata:
                unified_response["equipment_display"] = metadata["equipment_display"]

        # Always check for equipment_display even outside capture_evidence mode
        metadata = getattr(llm_response_obj, "processing_metadata", {}) or {}
        if (
            "equipment_display" in metadata
            and "equipment_display" not in unified_response
        ):
            unified_response["equipment_display"] = metadata["equipment_display"]

        if prevention_extras.get("god_mode_response"):
            # Prefer synthesized god mode responses from preventive guards when present
            # because they fill gaps left by the model.
            unified_response["god_mode_response"] = prevention_extras[
                "god_mode_response"
            ]

        # Add temporal correction warning to response if present
        if prevention_extras.get("temporal_correction_warning"):
            unified_response["temporal_correction_warning"] = prevention_extras[
                "temporal_correction_warning"
            ]
            unified_response["temporal_correction_attempts"] = prevention_extras.get(
                "temporal_correction_attempts", 0
            )

        # Add system corrections for LLM self-correction in next inference
        # These are injected into the next prompt via system_corrections field
        # Filter to only reward-related corrections for persistence
        reward_system_corrections = _filter_reward_corrections(
            prevention_extras.get("system_corrections", [])
        )
        if reward_system_corrections:
            # Deduplicate while preserving order (same as we do for persistence)
            unified_response["system_corrections"] = list(
                dict.fromkeys(reward_system_corrections)
            )
            for correction in unified_response["system_corrections"]:
                logging_util.warning(f"SYSTEM CORRECTION QUEUED: {correction}")

        # Add system warnings from validation corrections and post-combat checks
        if system_warnings:
            unified_response["system_warnings"] = system_warnings
            for warning in system_warnings:
                logging_util.warning(f"SYSTEM WARNING: {warning}")

        # Track story mode sequence ID for character mode.
        #
        # NOTE: Skip in MOCK_SERVICES_MODE to keep tight concurrency tests stable
        # (mock Firestore is in-memory and this field isn't needed for those tests).
        # Read item_exploit_blocked from processing_metadata if item validation detected an exploit
        metadata = getattr(llm_response_obj, "processing_metadata", {}) or {}
        item_exploit_blocked = metadata.get("item_exploit_blocked", False)

        # Initialize final_game_state_dict before conditional block to avoid UnboundLocalError
        # when the if-block is skipped (e.g., non-character mode, mock services, item exploit)
        # This ensures _ensure_faction_header_if_enabled always has a valid state dict
        final_game_state_dict = updated_game_state_dict

        if (
            mode == constants.MODE_CHARACTER
            and not item_exploit_blocked
            and not is_mock_services_mode()
        ):
            story_id_update = {
                "custom_campaign_state": {"last_story_mode_sequence_id": sequence_id}
            }
            # Merge this update with existing state changes from Gemini response
            current_state_changes = response.get("state_changes", {})
            merged_state_changes = update_state_with_changes(
                current_state_changes, story_id_update
            )

            # Keep state_updates aligned with final persisted state updates for
            # character-flow bookkeeping, regardless of debug mode.
            # Merge character updates into existing enriched state_updates instead of
            # replacing to preserve game_state snapshot and living-world fallback world_events.
            unified_response["state_updates"] = update_state_with_changes(
                unified_response["state_updates"], merged_state_changes
            )

            # Also update the game state dict that was already saved
            final_game_state_dict = update_state_with_changes(
                updated_game_state_dict, story_id_update
            )

            # CRITICAL: Persist planning_block to game state for agent selection continuity
            # DialogAgent.matches_game_state() relies on this to detect dialog choices
            if structured_fields.get("planning_block"):
                final_game_state_dict["planning_block"] = structured_fields[
                    "planning_block"
                ]

            # Validate the final state before persisting
            final_game_state_dict = validate_game_state_updates(
                final_game_state_dict,
                original_state_dict=updated_game_state_dict,
            )

            await asyncio.to_thread(
                _update_campaign_game_state,
                user_id,
                campaign_id,
                final_game_state_dict,
            )

            unified_response["game_state"] = final_game_state_dict

        # Inject faction header if missing but required (safety net)
        # Use final_game_state_dict (with LLM state_updates merged) to compute accurate header
        unified_response = _ensure_faction_header_if_enabled(
            unified_response, final_game_state_dict
        )

        # LATENCY TRACKING: Log total processing time
        total_duration = time.perf_counter() - start_time
        logging_util.info(
            f"⏱️ LATENCY_END: process_action_unified completed in {total_duration:.2f}s"
        )

        return unified_response

    except ValidationError:
        # Re-raise ValidationError so mcp_api.py can apply god mode recovery
        raise
    except Exception as e:
        logging_util.error(f"Process action failed: {e}")
        return create_error_response(
            f"Failed to process action: {str(e)}", status_code=500
        )
    finally:
        # LATENCY TRACKING: Log total time even on errors
        if "start_time" in locals():
            total_duration = time.perf_counter() - start_time
            logging_util.info(
                f"⏱️ LATENCY_FINAL: Total processing time {total_duration:.2f}s"
            )
        logging_util.set_campaign_id(None)


async def get_campaign_state_unified(request_data: dict[str, Any]) -> dict[str, Any]:
    """
    Unified campaign state retrieval logic for both Flask and MCP.

    Uses asyncio.to_thread() for blocking I/O operations to prevent blocking
    the shared event loop.

    Args:
        request_data: Dictionary containing:
            - user_id: User ID
            - campaign_id: Campaign ID
            - include_story: Whether to include processed story (optional, default False)

    Returns:
        Dictionary with success/error status and campaign state
    """
    try:
        # Extract parameters
        user_id = request_data.get("user_id")
        campaign_id = request_data.get("campaign_id")
        include_story = request_data.get("include_story", False)

        # Validate required fields
        if not user_id:
            return {KEY_ERROR: "User ID is required"}
        if not campaign_id:
            return {KEY_ERROR: "Campaign ID is required"}

        # Fetch campaign metadata/story and game state concurrently (blocking I/O).
        (
            (campaign_data, story),
            (
                game_state,
                was_cleaned,
                num_cleaned,
                user_settings,
            ),
        ) = await asyncio.gather(
            asyncio.to_thread(
                firestore_service.get_campaign_by_id, user_id, campaign_id
            ),
            asyncio.to_thread(
                _prepare_game_state_with_user_settings, user_id, campaign_id
            ),
        )
        if not campaign_data:
            return {KEY_ERROR: "Campaign not found", "status_code": 404}

        # Clean JSON artifacts from campaign description if present
        if campaign_data and "description" in campaign_data:
            campaign_data["description"] = clean_json_artifacts(
                campaign_data["description"]
            )

        # Also clean other text fields that might have JSON artifacts
        text_fields_to_clean = ["prompt", "title"]
        for field in text_fields_to_clean:
            if (
                campaign_data
                and field in campaign_data
                and isinstance(campaign_data[field], str)
            ):
                campaign_data[field] = clean_json_artifacts(campaign_data[field])

        game_state_dict = game_state.to_dict()

        # Get debug mode from user settings and apply to game state (blocking I/O)
        debug_mode = user_settings.get("debug_mode", False) if user_settings else False
        game_state_dict["debug_mode"] = debug_mode

        result = {
            KEY_SUCCESS: True,
            "campaign": campaign_data,
            "game_state": game_state_dict,
            "user_settings": user_settings,
            "state_cleaned": was_cleaned,
            "entries_cleaned": num_cleaned,
        }

        # Include processed story if requested (for Flask route compatibility)
        if include_story and story:
            processed_story = process_story_for_display(story, debug_mode)

            # Strip game state fields when debug mode is OFF
            if not debug_mode:
                processed_story = _strip_game_state_fields(processed_story)

            result["story"] = processed_story

        return result

    except Exception as e:
        logging_util.error(f"Failed to get campaign state: {e}")
        return {KEY_ERROR: f"Failed to get campaign state: {str(e)}"}


async def update_campaign_unified(request_data: dict[str, Any]) -> dict[str, Any]:
    """
    Unified campaign update logic for both Flask and MCP.

    Uses asyncio.to_thread() for blocking I/O operations to prevent blocking
    the shared event loop.

    Args:
        request_data: Dictionary containing:
            - user_id: User ID
            - campaign_id: Campaign ID
            - updates: Dictionary of updates to apply

    Returns:
        Dictionary with success/error status
    """
    try:
        # Extract parameters
        user_id = request_data.get("user_id")
        campaign_id = request_data.get("campaign_id")
        updates = request_data.get("updates", {})

        # Validate required fields
        if not user_id:
            return {KEY_ERROR: "User ID is required"}
        if not campaign_id:
            return {KEY_ERROR: "Campaign ID is required"}
        if not updates:
            return {KEY_ERROR: "Updates are required"}

        # Check if campaign exists (blocking I/O - run in thread)
        campaign_data, _ = await asyncio.to_thread(
            firestore_service.get_campaign_by_id, user_id, campaign_id
        )
        if not campaign_data:
            return {KEY_ERROR: "Campaign not found", "status_code": 404}

        # Apply updates (blocking I/O - run in thread)
        await asyncio.to_thread(
            firestore_service.update_campaign, user_id, campaign_id, updates
        )

        return {
            KEY_SUCCESS: True,
            "message": f"Campaign updated with {len(updates)} changes",
        }

    except Exception as e:
        logging_util.error(f"Failed to update campaign: {e}")
        return {KEY_ERROR: f"Failed to update campaign: {str(e)}"}


async def export_campaign_unified(request_data: dict[str, Any]) -> dict[str, Any]:
    """
    Unified campaign export logic for both Flask and MCP.

    Uses asyncio.to_thread() for blocking I/O operations to prevent blocking
    the shared event loop.

    Args:
        request_data: Dictionary containing:
            - user_id: User ID
            - campaign_id: Campaign ID
            - format: Export format ('pdf', 'docx', 'txt')
            - filename: Optional filename

    Returns:
        Dictionary with success/error status and export info
    """
    try:
        # Extract parameters
        user_id = request_data.get("user_id")
        campaign_id = request_data.get("campaign_id")
        export_format = request_data.get("format", "pdf").lower()
        filename = request_data.get("filename")

        # Validate required fields
        if not user_id:
            return {KEY_ERROR: "User ID is required"}
        if not campaign_id:
            return {KEY_ERROR: "Campaign ID is required"}
        if export_format not in ["pdf", "docx", "txt"]:
            return {KEY_ERROR: "Format must be one of: pdf, docx, txt"}

        # Get campaign data and story (blocking I/O - run in thread)
        campaign_data, story_context = await asyncio.to_thread(
            firestore_service.get_campaign_by_id, user_id, campaign_id
        )
        if not campaign_data:
            return {KEY_ERROR: "Campaign not found", "status_code": 404}

        # Get campaign title
        campaign_title = campaign_data.get("title", "Untitled Campaign")

        # Generate file path
        temp_dir = os.path.join(tempfile.gettempdir(), "campaign_exports")
        os.makedirs(temp_dir, exist_ok=True)

        if filename:
            safe_file_path = os.path.join(temp_dir, filename)
        else:
            safe_file_path = os.path.join(temp_dir, f"{uuid.uuid4()}.{export_format}")

        # Convert story context to text format using enhanced formatting
        # This uses the same logic as the CLI download script for consistency
        story_text = document_generator.get_story_text_from_context_enhanced(
            story_context, include_scenes=True
        )

        # Generate export file
        try:
            if export_format == "pdf":
                await asyncio.to_thread(
                    document_generator.generate_pdf,
                    story_text,
                    safe_file_path,
                    campaign_title,
                )
            elif export_format == "docx":
                await asyncio.to_thread(
                    document_generator.generate_docx,
                    story_text,
                    safe_file_path,
                    campaign_title,
                )
            elif export_format == "txt":
                await asyncio.to_thread(
                    document_generator.generate_txt,
                    story_text,
                    safe_file_path,
                    campaign_title,
                )

            return {
                KEY_SUCCESS: True,
                "export_path": safe_file_path,
                "format": export_format,
                "campaign_title": campaign_title,
            }
        except Exception as e:
            logging_util.error(f"Document generation failed: {e}")
            return {KEY_ERROR: f"Document generation failed: {str(e)}"}

    except Exception as e:
        logging_util.error(f"Failed to export campaign: {e}")
        return {KEY_ERROR: f"Failed to export campaign: {str(e)}"}


def get_campaigns_for_user_list(user_id: UserId) -> list[dict[str, Any]]:
    """Get campaigns list for a user - synchronous version for tests."""
    campaigns, _, _ = firestore_service.get_campaigns_for_user(user_id)
    return campaigns


async def get_campaigns_list_unified(request_data: dict[str, Any]) -> dict[str, Any]:
    """
    Unified campaigns list retrieval logic for both Flask and MCP.

    Args:
        request_data: Dictionary containing:
            - user_id: User ID
            - limit: Optional maximum number of campaigns to return
            - sort_by: Optional sort field ('created_at' or 'last_played')

    Returns:
        Dictionary with success/error status and campaigns list
    """
    try:
        # Extract parameters
        user_id = request_data.get("user_id")
        limit = request_data.get("limit")
        sort_by = request_data.get("sort_by", "last_played")

        # Validate required fields
        if not user_id:
            return {KEY_ERROR: "User ID is required"}

        # Validate limit parameter with proper error handling
        if limit is not None:
            try:
                limit = int(limit) if limit else None
            except (ValueError, TypeError):
                return {KEY_ERROR: "Invalid limit parameter - must be a valid integer"}

        # Validate sort_by parameter
        valid_sort_fields = ["created_at", "last_played"]
        if sort_by and sort_by not in valid_sort_fields:
            return {
                KEY_ERROR: f"Invalid sort_by parameter - must be one of: {', '.join(valid_sort_fields)}"
            }

        # Get cursor for pagination
        start_after = request_data.get("start_after")

        # Get campaigns with pagination and sorting (blocking I/O - run in thread)
        # Include total count only on first page (when start_after is None)
        include_total = start_after is None
        campaigns, next_cursor, total_count = await asyncio.to_thread(
            firestore_service.get_campaigns_for_user,
            user_id,
            limit,
            sort_by,
            start_after,
            include_total,
        )

        # Clean JSON artifacts from campaign text fields
        if campaigns:
            text_fields_to_clean = ["description", "prompt", "title"]
            for campaign in campaigns:
                for field in text_fields_to_clean:
                    if field in campaign and isinstance(campaign[field], str):
                        campaign[field] = clean_json_artifacts(campaign[field])

        result = {
            KEY_SUCCESS: True,
            "campaigns": campaigns,
        }

        # Include pagination info if there are more results
        if next_cursor:
            result["next_cursor"] = next_cursor
            result["has_more"] = True
        else:
            result["has_more"] = False

        # Include total count if available (only on first page)
        if total_count is not None:
            result["total_count"] = total_count

        return result

    except Exception as e:
        logging_util.error(f"Failed to get campaigns: {e}")
        return {KEY_ERROR: f"Failed to get campaigns: {str(e)}"}


def create_error_response(message: str, status_code: int = 400) -> dict[str, Any]:
    """
    Create standardized error response.

    Args:
        message: Error message
        status_code: HTTP status code (for Flask compatibility)

    Returns:
        Standardized error response dictionary
    """
    return {
        KEY_ERROR: message,
        "status_code": status_code,
        KEY_SUCCESS: False,
    }


def create_success_response(data: dict[str, Any]) -> dict[str, Any]:
    """
    Create standardized success response.

    Args:
        data: Response data

    Returns:
        Standardized success response dictionary
    """
    response = {KEY_SUCCESS: True}
    response.update(data)
    return response


async def get_user_settings_unified(request_data: dict[str, Any]) -> dict[str, Any]:
    """
    Unified user settings retrieval for both Flask and MCP.

    Uses asyncio.to_thread() for blocking I/O operations to prevent blocking
    the shared event loop.

    Args:
        request_data: Dictionary containing:
            - user_id: User ID

    Returns:
        Dictionary with user settings or default settings
    """
    try:
        user_id = request_data.get("user_id")
        if not user_id:
            return create_error_response("User ID is required")

        # Blocking I/O - run in thread
        settings = await asyncio.to_thread(get_user_settings, user_id)

        # Return default settings for new users or database errors
        if settings is None:
            settings = {
                "debug_mode": constants.DEFAULT_DEBUG_MODE,
                "gemini_model": constants.DEFAULT_GEMINI_MODEL,  # Default model (supports code_execution + JSON)
                "llm_provider": constants.DEFAULT_LLM_PROVIDER,
                "openrouter_model": constants.DEFAULT_OPENROUTER_MODEL,
                "cerebras_model": constants.DEFAULT_CEREBRAS_MODEL,
                "openclaw_gateway_port": constants.DEFAULT_OPENCLAW_GATEWAY_PORT,
                "openclaw_gateway_url": "",
                "openclaw_gateway_token": "",
            }

        settings.setdefault("llm_provider", constants.DEFAULT_LLM_PROVIDER)
        settings.setdefault("gemini_model", constants.DEFAULT_GEMINI_MODEL)
        settings.setdefault("openrouter_model", constants.DEFAULT_OPENROUTER_MODEL)
        settings.setdefault("cerebras_model", constants.DEFAULT_CEREBRAS_MODEL)
        settings.setdefault(
            "openclaw_gateway_port", constants.DEFAULT_OPENCLAW_GATEWAY_PORT
        )
        settings.setdefault("openclaw_gateway_url", "")
        settings.setdefault("openclaw_gateway_token", "")
        raw_gateway_url = settings.get("openclaw_gateway_url")
        if not isinstance(raw_gateway_url, str):
            settings["openclaw_gateway_url"] = ""
        raw_gateway_token = settings.get("openclaw_gateway_token")
        if isinstance(raw_gateway_token, str):
            settings["openclaw_gateway_token"] = raw_gateway_token
        else:
            settings["openclaw_gateway_token"] = ""

        # Compute BYOK key flags for UI state.
        safe_settings = settings.copy()
        for key, flag_key in [
            ("gemini_api_key", "has_custom_gemini_key"),
            ("openrouter_api_key", "has_custom_openrouter_key"),
            ("cerebras_api_key", "has_custom_cerebras_key"),
            ("openclaw_api_key", "has_custom_openclaw_key"),
            ("openclaw_gateway_token", "has_custom_openclaw_gateway_token"),
        ]:
            val = safe_settings.get(key)
            # Normalize whitespace-only strings to None
            if isinstance(val, str) and not val.strip():
                val = None

            # Set flag based on presence of value
            safe_settings[flag_key] = val is not None
            # Remove actual API key from response to prevent leaking plaintext secrets.
            safe_settings.pop(key, None)

        return create_success_response(safe_settings)

    except Exception as e:
        logging_util.error(f"Failed to get user settings: {e}")
        return create_error_response(f"Failed to get user settings: {str(e)}")


_BYOK_PROVIDER_FIELD: dict[str, str] = {
    "gemini": "gemini_api_key",
    "openrouter": "openrouter_api_key",
    "cerebras": "cerebras_api_key",
    "openclaw": "openclaw_gateway_token",  # stored under gateway_token, not api_key
}


async def reveal_user_api_key_unified(request_data: dict[str, Any]) -> dict[str, Any]:
    """
    Reveal a stored BYOK API key for an authenticated owner session.

    This endpoint is intentionally explicit and provider-scoped, separate from
    get_user_settings_unified(), which keeps settings payloads redacted by default.
    """
    try:
        user_id = request_data.get("user_id")
        provider = str(request_data.get("provider") or "").strip().lower()
        if not user_id:
            return create_error_response("User ID is required")
        if provider not in _BYOK_PROVIDER_FIELD:
            return create_error_response("Invalid provider", status_code=400)

        key_name = _BYOK_PROVIDER_FIELD[provider]
        settings = await asyncio.to_thread(get_user_settings, user_id) or {}
        key_value = settings.get(key_name)
        if not isinstance(key_value, str) or not key_value.strip():
            return create_error_response(
                f"No stored {provider} API key found", status_code=404
            )

        return create_success_response(
            {
                "provider": provider,
                "api_key": key_value.strip(),
            }
        )
    except Exception as e:
        logging_util.error(f"Failed to reveal BYOK key: {e}")
        return create_error_response(f"Failed to reveal BYOK key: {str(e)}")


async def update_user_settings_unified(request_data: dict[str, Any]) -> dict[str, Any]:
    """
    Unified user settings update for both Flask and MCP.

    Uses asyncio.to_thread() for blocking I/O operations to prevent blocking
    the shared event loop.

    Args:
        request_data: Dictionary containing:
            - user_id: User ID
            - settings: Dictionary of settings to update

    Returns:
        Dictionary with success status and updated settings
    """
    try:
        user_id = request_data.get("user_id")
        settings_data = request_data.get("settings")

        if not user_id:
            return create_error_response("User ID is required")

        if not isinstance(settings_data, dict):
            return create_error_response("Invalid request format")

        if not settings_data:
            return create_error_response("No data provided")

        settings_to_update = {}

        # Log incoming settings for debugging persistence issues
        logging_util.info(
            "update_user_settings_unified: user_id=%s incoming_keys=%s",
            user_id,
            list(settings_data.keys()),
        )

        # Fetch existing settings if model/provider cross-validation needed
        # (avoids unnecessary Firestore read when not updating model/provider)
        existing_settings = None
        if "pre_spicy_model" in settings_data or "pre_spicy_provider" in settings_data:
            existing_settings = await asyncio.to_thread(get_user_settings, user_id)

        # OpenClaw gateway inputs should only be validated/persisted when the
        # user is actually selecting OpenClaw as the active provider.
        target_llm_provider = settings_data.get("llm_provider")
        if (
            target_llm_provider is None
            and (
                "openclaw_gateway_port" in settings_data
                or "openclaw_gateway_url" in settings_data
                or "openclaw_gateway_token" in settings_data
            )
            and existing_settings is None
        ):
            existing_settings = await asyncio.to_thread(get_user_settings, user_id)

        if isinstance(existing_settings, dict) and target_llm_provider is None:
            target_llm_provider = existing_settings.get("llm_provider")

        # Validate all settings with cross-validation using centralized module
        # This handles: individual validation + model/provider compatibility check
        settings_to_update, validation_error = (
            settings_validation.validate_settings_with_cross_validation(
                settings_data,
                existing_settings,
                target_llm_provider=target_llm_provider,
            )
        )
        if validation_error:
            logging_util.warning(
                "update_user_settings_unified: validation failed for user_id=%s: %s",
                user_id,
                validation_error,
            )
            return create_error_response(validation_error)

        # Log faction_minigame_enabled specifically for debugging
        if "faction_minigame_enabled" in settings_to_update:
            logging_util.info(
                "update_user_settings_unified: faction_minigame_enabled=%s queued for user_id=%s",
                settings_to_update["faction_minigame_enabled"],
                user_id,
            )

        # Update settings if there are any valid changes (blocking I/O - run in thread)
        if settings_to_update:
            logging_util.info(
                "update_user_settings_unified: SAVING user_id=%s settings_to_update=%s",
                user_id,
                _redact_settings_for_log(settings_to_update),
            )
            await asyncio.to_thread(
                firestore_service.update_user_settings, user_id, settings_to_update
            )
            rate_limiting.invalidate_user_settings_cache(user_id)
            logging_util.info(
                "Updated user settings for %s: %s",
                user_id,
                _redact_settings_for_log(settings_to_update),
            )
        else:
            logging_util.warning(
                "update_user_settings_unified: NO valid settings to save for user_id=%s (all validation failed?)",
                user_id,
            )

        # Get updated settings to return (blocking I/O - run in thread)
        updated_settings = await asyncio.to_thread(get_user_settings, user_id) or {}

        # Redact BYOK API keys from response (same as GET path)
        safe_settings = updated_settings.copy()
        for key, flag_key in [
            ("gemini_api_key", "has_custom_gemini_key"),
            ("openrouter_api_key", "has_custom_openrouter_key"),
            ("cerebras_api_key", "has_custom_cerebras_key"),
            ("openclaw_api_key", "has_custom_openclaw_key"),
            ("openclaw_gateway_token", "has_custom_openclaw_gateway_token"),
        ]:
            val = safe_settings.get(key)
            # Normalize whitespace-only strings to None
            if isinstance(val, str) and not val.strip():
                val = None

            # Set flag based on presence of value
            safe_settings[flag_key] = val is not None
            # Remove actual API key from response to prevent leaking plaintext secrets.
            safe_settings.pop(key, None)

        return create_success_response({"settings": safe_settings})

    except Exception as e:
        logging_util.error(f"Failed to update user settings: {e}")
        return create_error_response(f"Failed to update user settings: {str(e)}")


def apply_automatic_combat_cleanup(
    updated_state_dict: dict[str, Any], _proposed_changes: dict[str, Any]
) -> dict[str, Any]:
    """
    Automatically cleans up defeated enemies from combat state when combat updates are applied.

    This function should be called after any state update that modifies combat_state.
    It identifies defeated enemies (HP <= 0) and removes them from both combat_state
    and npc_data to maintain consistency.

    Args:
        updated_state_dict: The state dictionary after applying proposed changes
        proposed_changes: The original changes dict to check if combat_state was modified

    Returns:
        Updated state dictionary with defeated enemies cleaned up
    """
    # CRITICAL BUG FIX: Handle case where GameState.from_dict returns None
    temp_game_state = GameState.from_dict(updated_state_dict)
    if temp_game_state is None:
        logging_util.error(
            "COMBAT CLEANUP ERROR: GameState.from_dict returned None, returning original state"
        )
        return updated_state_dict

    # Check if we have combatants data to potentially clean up
    combatants = temp_game_state.combat_state.get("combatants", {})
    if not combatants:
        logging_util.debug(
            "COMBAT CLEANUP CHECK: No combatants found, skipping cleanup"
        )
        return updated_state_dict

    # CRITICAL FIX: Always attempt cleanup if combatants exist
    # This handles ALL cases:
    # 1. Combat ongoing with new defeats
    # 2. Combat ending with pre-existing defeats
    # 3. State updates without explicit combat_state changes but with defeated enemies
    logging_util.debug(
        f"COMBAT CLEANUP CHECK: Found {len(combatants)} combatants, scanning for defeated enemies..."
    )

    # Perform cleanup - this always runs regardless of proposed_changes content
    defeated_enemies = temp_game_state.cleanup_defeated_enemies()
    if defeated_enemies:
        logging_util.info(
            f"AUTOMATIC CLEANUP: Defeated enemies removed: {defeated_enemies}"
        )
        # Return the updated state dict from the game state that had cleanup applied
        return temp_game_state.to_dict()
    logging_util.info("AUTOMATIC CLEANUP: No defeated enemies found to clean up")
    # Return the original state since no cleanup was needed
    return updated_state_dict


def format_game_state_updates(updates: dict[str, Any], for_html: bool = False) -> str:
    """Formats a dictionary of game state updates into a readable string, counting the number of leaf-node changes."""
    if not updates:
        return "No state updates."

    log_lines: list[str] = []

    def recurse_items(d: dict[str, Any], prefix: str = "") -> None:
        for key, value in d.items():
            path = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                recurse_items(value, prefix=path)
            else:
                log_lines.append(f"{path}: {json.dumps(value)}")

    recurse_items(updates)

    count = len(log_lines)
    if count == 0:
        return "No effective state updates were made."

    header = f"Game state updated ({count} {'entry' if count == 1 else 'entries'}):"

    if for_html:
        # Create an HTML list for the chat response
        items_html = "".join([f"<li><code>{line}</code></li>" for line in log_lines])
        return f"{header}<ul>{items_html}</ul>"
    # Create a plain text list for server logs
    items_text = "\n".join([f"  - {line}" for line in log_lines])
    return f"{header}\n{items_text}"


def parse_set_command(payload_str: str) -> dict[str, Any]:
    """
    Parses a multi-line string of `key.path = value` into a nested
    dictionary of proposed changes. Handles multiple .append operations correctly.
    """
    proposed_changes: dict[str, Any] = {}
    append_ops: dict[str, list[Any]] = collections.defaultdict(list)

    for line_raw in payload_str.strip().splitlines():
        line = line_raw.strip()
        if not line or "=" not in line:
            continue

        key_path, value_str = line.split("=", 1)
        key_path = key_path.strip()
        value_str = value_str.strip()

        try:
            value = json.loads(value_str)
        except json.JSONDecodeError:
            logging_util.warning(
                f"Skipping line in SET command due to invalid JSON value: {line}"
            )
            continue

        # Handle .append operations
        if key_path.endswith(".append"):
            base_key = key_path[:-7]  # Remove '.append'
            append_ops[base_key].append(value)
        else:
            # Regular assignment
            keys = key_path.split(".")
            current = proposed_changes
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = value

    # Process append operations
    for base_key, values in append_ops.items():
        keys = base_key.split(".")
        current = proposed_changes
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        final_key = keys[-1]
        if final_key not in current:
            current[final_key] = []
        elif not isinstance(current[final_key], list):
            current[final_key] = [current[final_key]]

        current[final_key].extend(values)

    return proposed_changes


def _handle_ask_state_command(
    user_input: str,
    current_game_state: GameState,
    user_id: UserId,
    campaign_id: CampaignId,
) -> dict[str, Any] | None:
    """
    Handle GOD_ASK_STATE command.

    Returns:
        Response dict or None if not ASK_STATE command
    """
    god_ask_state_command = "GOD_ASK_STATE"

    if user_input.strip() != god_ask_state_command:
        return None

    game_state_dict = current_game_state.to_dict()
    game_state_json = json.dumps(game_state_dict, indent=2, default=str)

    firestore_service.add_story_entry(
        user_id, campaign_id, constants.ACTOR_USER, user_input, constants.MODE_CHARACTER
    )

    response_text = f"```json\n{game_state_json}\n```"
    return {
        KEY_SUCCESS: True,
        KEY_RESPONSE: response_text,
        "game_state": game_state_dict,
    }


def _handle_set_command(
    user_input: str,
    current_game_state: GameState,
    user_id: UserId,
    campaign_id: CampaignId,
) -> dict[str, Any] | None:
    """
    Handle GOD_MODE_SET command.

    Args:
        user_input: User input string
        current_game_state: Current GameState object
        user_id: User ID
        campaign_id: Campaign ID

    Returns:
        Response dict or None if not a SET command
    """
    god_mode_set_command = "GOD_MODE_SET:"
    user_input_stripped = user_input.strip()

    if not user_input_stripped.startswith(god_mode_set_command):
        return None

    payload_str = user_input_stripped[len(god_mode_set_command) :]
    logging_util.info("--- GOD_MODE_SET received for campaign %s ---", campaign_id)
    logging_util.info("GOD_MODE_SET raw payload:\n---\n%s\n---", payload_str)

    logger = logging_util.getLogger()
    debug_enabled = logger.isEnabledFor(logging_util.DEBUG)

    proposed_changes = parse_set_command(payload_str)
    # Enhanced logging with proper truncation (DEBUG-only to avoid eager formatting in INFO mode)
    if debug_enabled:
        logging_util.debug(
            "GOD_MODE_SET parsed changes to be merged:\n%s",
            _truncate_log_json(
                proposed_changes, json_serializer=json_default_serializer
            ),
        )

    if not proposed_changes:
        logging_util.warning("GOD_MODE_SET command resulted in no valid changes.")
        return {
            KEY_SUCCESS: True,
            KEY_RESPONSE: "[System Message: The GOD_MODE_SET command was received, but contained no valid instructions or was empty.]",
        }

    current_state_dict_before_update = current_game_state.to_dict()
    original_state_for_level_check = copy.deepcopy(current_state_dict_before_update)
    if debug_enabled:
        logging_util.debug(
            "GOD_MODE_SET state BEFORE update: %s",
            current_state_dict_before_update,
        )

    # Capture original time before update for accurate monotonicity validation
    # Note: current_game_state is a GameState instance, use dict version
    # Use `or {}` to handle both missing and explicitly-null world_data
    # CRITICAL: Deep-copy to prevent mutation by update_state_with_changes
    original_world_time = copy.deepcopy(
        (current_state_dict_before_update.get("world_data") or {}).get("world_time")
    )

    updated_state = update_state_with_changes(
        current_state_dict_before_update, proposed_changes
    )
    updated_state = apply_automatic_combat_cleanup(updated_state, proposed_changes)

    # Validate XP/level and time consistency before persisting
    # Use `or {}` to handle both missing and explicitly-null world_data
    new_world_time = (proposed_changes.get("world_data") or {}).get("world_time")
    updated_state = validate_game_state_updates(
        updated_state,
        new_time=new_world_time,
        original_time=original_world_time,
        original_state_dict=current_state_dict_before_update,
    )

    if debug_enabled:
        logging_util.debug(
            "GOD_MODE_SET state AFTER update:\n%s",
            _truncate_log_json(updated_state, json_serializer=json_default_serializer),
        )

    # Validate and auto-correct state before persistence
    updated_state = validate_and_correct_state(
        updated_state, previous_world_time=original_world_time
    )

    # SERVER-SIDE LEVEL-UP DETECTION for God Mode SET
    updated_state = _check_and_set_level_up_pending(
        updated_state, original_state_dict=original_state_for_level_check
    )

    firestore_service.update_campaign_game_state(user_id, campaign_id, updated_state)

    # Log the formatted changes for both server and chat
    if debug_enabled:
        log_message_for_log = format_game_state_updates(
            proposed_changes, for_html=False
        )
        logging_util.debug(
            "GOD_MODE_SET changes applied for campaign %s:\n%s",
            campaign_id,
            log_message_for_log,
        )

    log_message_for_chat = format_game_state_updates(proposed_changes, for_html=True)

    logging_util.info("--- GOD_MODE_SET for campaign %s complete ---", campaign_id)

    return {
        KEY_SUCCESS: True,
        KEY_RESPONSE: f"[System Message]<br>{log_message_for_chat}",
    }


def _handle_update_state_command(
    user_input: str,
    user_id: UserId,
    campaign_id: CampaignId,
    include_raw_llm_payloads: bool = False,
) -> dict[str, Any] | None:
    """
    Handle GOD_MODE_UPDATE_STATE command.

    Returns:
        Response dict or None if not UPDATE_STATE command
    """
    god_mode_update_state_command = "GOD_MODE_UPDATE_STATE:"

    if not user_input.strip().startswith(god_mode_update_state_command):
        return None

    json_payload = user_input.strip()[len(god_mode_update_state_command) :]
    try:
        state_changes = json.loads(json_payload)
        if not isinstance(state_changes, dict):
            raise ValueError("Payload is not a JSON object.")

        # Fetch the current state as a dictionary
        current_game_state = firestore_service.get_campaign_game_state(
            user_id, campaign_id
        )
        if not current_game_state:
            return create_error_response(
                "Game state not found for GOD_MODE_UPDATE_STATE", 404
            )

        current_state_dict = current_game_state.to_dict()
        original_state_for_level_check = copy.deepcopy(current_state_dict)
        previous_combat_state = copy.deepcopy(
            current_state_dict.get("combat_state", {})
        )

        # Capture original time before update for accurate monotonicity validation
        # Note: current_game_state is a GameState instance, use dict version
        # Use `or {}` to handle both missing and explicitly-null world_data
        # CRITICAL: Deep-copy to prevent mutation by update_state_with_changes
        original_world_time = copy.deepcopy(
            (current_state_dict.get("world_data") or {}).get("world_time")
        )

        # Perform an update
        updated_state_dict = update_state_with_changes(
            current_state_dict, state_changes
        )
        updated_state_dict = apply_automatic_combat_cleanup(
            updated_state_dict, state_changes
        )

        # Convert to GameState object for validation
        final_game_state = GameState.from_dict(updated_state_dict)
        if final_game_state is None:
            logging_util.error(
                "PROCESS_ACTION: GameState.from_dict returned None after update; rejecting GOD_MODE_UPDATE_STATE"
            )
            return create_error_response(
                "Unable to reconstruct game state after applying changes.", 500
            )

        # Validate and auto-correct state before persistence
        # Surface corrections to user so they see what was actually applied
        validated_state_dict, corrections = validate_and_correct_state(
            final_game_state.to_dict(),
            previous_world_time=original_world_time,
            return_corrections=True,
        )

        # SERVER-SIDE LEVEL-UP DETECTION for God Mode UPDATE_STATE
        validated_state_dict = _check_and_set_level_up_pending(
            validated_state_dict, original_state_dict=original_state_for_level_check
        )

        # Detect post-combat warnings for GOD_MODE_UPDATE_STATE (no rewards followup here)
        # Uses shared _extract_xp_from_player_data helper to avoid duplication with unified flow
        post_combat_warnings: list[str] = []
        try:
            updated_game_state_obj = GameState.from_dict(validated_state_dict)
            if updated_game_state_obj:
                final_xp = _extract_xp_from_player_data(
                    validated_state_dict.get("player_character_data", {})
                )
                original_xp = _extract_xp_from_player_data(
                    original_state_for_level_check.get("player_character_data", {})
                )
                if final_xp <= original_xp:
                    post_combat_warnings = (
                        updated_game_state_obj.detect_post_combat_issues(
                            previous_combat_state, state_changes
                        )
                    )
        except Exception as e:
            logging_util.warning(f"POST_COMBAT warning detection failed: {e}")

        system_warnings = corrections + post_combat_warnings

        firestore_service.update_campaign_game_state(
            user_id, campaign_id, validated_state_dict
        )

        log_message = format_game_state_updates(state_changes, for_html=False)

        # Build response with corrections if any were applied
        response_parts = [
            "[System Message: The following state changes were applied via GOD MODE]",
            log_message,
        ]
        if corrections:
            response_parts.append("\n[Auto-Corrections Applied]")
            for correction in corrections:
                response_parts.append(f"  - {correction}")
        if post_combat_warnings:
            response_parts.append("\n[System Warnings]")
            for warning in post_combat_warnings:
                response_parts.append(f"  - {warning}")

        # NOTE: Level-up handling is fully delegated to the LLM. The LLM receives
        # rewards_pending in game state context and should recognize level-up eligibility
        # to generate appropriate rewards boxes per rewards_system_instruction.md.

        response_payload = {
            KEY_SUCCESS: True,
            KEY_RESPONSE: "\n".join(response_parts),
        }
        if system_warnings:
            response_payload["system_warnings"] = system_warnings
        if include_raw_llm_payloads:
            response_payload["raw_request_payload"] = {"state_changes": state_changes}
            response_payload["raw_response_text"] = response_payload[KEY_RESPONSE]
            debug_info = {
                "agent_name": "GodModeAgent",
                "operation": "GOD_MODE_UPDATE_STATE",
                "system_instruction_files": [],
                "system_instruction_char_count": 0,
            }
            if system_warnings:
                debug_info["_server_system_warnings"] = system_warnings
            response_payload["debug_info"] = debug_info

        return response_payload

    except json.JSONDecodeError:
        return create_error_response(
            "Invalid JSON payload for GOD_MODE_UPDATE_STATE command.", 400
        )
    except ValueError as e:
        return create_error_response(
            f"Error in GOD_MODE_UPDATE_STATE payload: {e}", 400
        )
    except Exception as e:
        return create_error_response(
            f"An unexpected error occurred during GOD_MODE_UPDATE_STATE: {e}", 500
        )
