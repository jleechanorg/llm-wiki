"""Centralized utilities for faction minigame state access.

This module provides a single source of truth for:
1. Extracting faction_minigame dict from various game_state structures
2. Checking if faction minigame is enabled (strict boolean validation)
3. Handling all known game_state navigation paths
4. Provider-agnostic extraction from prompt_contents (LLM request format)
5. Detecting faction minigame enable actions in user_action

Eliminates duplication across agents.py, gemini_provider.py, and LLM provider modules.
"""

import json
from typing import Any

from mvp_site.dice import DICE_ROLL_TOOLS
from mvp_site.faction.tools import FACTION_TOOLS


def get_faction_minigame_dict(  # noqa: PLR0911, PLR0912
    game_state: Any,
) -> dict[str, Any] | None:
    """Extract faction_minigame dict from any game_state structure.

    Handles all known paths (checked in precedence order):
    1. game_state.custom_campaign_state["faction_minigame"] (canonical location - dict access)
    2. game_state.faction_minigame (direct attribute on GameState object, fallback)
    3. game_state.data["game_state"]["custom_campaign_state"]["faction_minigame"] (data wrapper, canonical)
    4. game_state.data["game_state"]["faction_minigame"] (data wrapper, fallback)
    5. game_state["custom_campaign_state"]["faction_minigame"] (dict-based game_state, canonical)
    6. game_state["faction_minigame"] (dict-based game_state, fallback)

    Precedence: custom_campaign_state is checked BEFORE direct faction_minigame
    to match world_logic.py canonical behavior (lines 2940-2947).

    Args:
        game_state: GameState object, dict, or any structure containing faction data

    Returns:
        faction_minigame dict if found, None otherwise
    """
    if game_state is None:
        return None

    # Try nested attribute: game_state.custom_campaign_state.faction_minigame
    if hasattr(game_state, "custom_campaign_state"):
        custom_state = getattr(game_state, "custom_campaign_state", None)
        if isinstance(custom_state, dict):
            faction_minigame = custom_state.get("faction_minigame")
            if isinstance(faction_minigame, dict):
                return faction_minigame

    # Try direct attribute access fallback: game_state.faction_minigame
    if hasattr(game_state, "faction_minigame"):
        faction_minigame = getattr(game_state, "faction_minigame", None)
        if isinstance(faction_minigame, dict):
            return faction_minigame

    # Try data wrapper: game_state.data.game_state.faction_minigame
    if hasattr(game_state, "data"):
        data = getattr(game_state, "data", None)
        # Handle data as dict
        if isinstance(data, dict):
            nested_game_state = data.get("game_state")
            if isinstance(nested_game_state, dict):
                # Try custom_campaign_state first (canonical location per world_logic.py)
                custom_state = nested_game_state.get("custom_campaign_state", {})
                if isinstance(custom_state, dict):
                    faction_minigame = custom_state.get("faction_minigame")
                    if isinstance(faction_minigame, dict):
                        return faction_minigame
                # Fallback to direct path if custom_campaign_state not found
                faction_minigame = nested_game_state.get("faction_minigame")
                if isinstance(faction_minigame, dict):
                    return faction_minigame
        # Handle data as object with game_state attribute
        elif data is not None and hasattr(data, "game_state"):
            nested_game_state = getattr(data, "game_state", None)
            if isinstance(nested_game_state, dict):
                # Try custom_campaign_state first (canonical location per world_logic.py)
                custom_state = nested_game_state.get("custom_campaign_state", {})
                if isinstance(custom_state, dict):
                    faction_minigame = custom_state.get("faction_minigame")
                    if isinstance(faction_minigame, dict):
                        return faction_minigame
                # Fallback to direct path if custom_campaign_state not found
                faction_minigame = nested_game_state.get("faction_minigame")
                if isinstance(faction_minigame, dict):
                    return faction_minigame

    # Try dict access: game_state["faction_minigame"]
    if isinstance(game_state, dict):
        # Check custom_campaign_state first (canonical location per world_logic.py)
        if "custom_campaign_state" in game_state:
            custom_state = game_state["custom_campaign_state"]
            if isinstance(custom_state, dict) and "faction_minigame" in custom_state:
                faction_minigame = custom_state["faction_minigame"]
                if isinstance(faction_minigame, dict):
                    return faction_minigame

        # Fallback to direct dict key if custom_campaign_state not found
        if "faction_minigame" in game_state:
            faction_minigame = game_state["faction_minigame"]
            if isinstance(faction_minigame, dict):
                return faction_minigame

    return None


def is_faction_minigame_enabled(
    game_state: Any,
    check_user_setting: bool = False,
    user_settings: dict[str, Any] | None = None,
) -> bool:
    """Check if faction minigame is enabled with strict boolean validation.

    Two-level control system:
    1. Campaign setting: faction_minigame.enabled must be boolean True (strict)
    2. User setting: faction_minigame_enabled must not be False (optional check)

    This function uses STRICT boolean checking to handle edge cases:
    - String "false" → disabled (even though truthy in Python)
    - String "true" → disabled (only boolean True enables)
    - None → disabled
    - 0 → disabled
    - Boolean True → enabled ✓
    - Boolean False → disabled

    Args:
        game_state: GameState object or dict containing faction_minigame
        check_user_setting: If True, also check user's global enable/disable setting
        user_settings: User settings dict (only used if check_user_setting=True)

    Returns:
        True only if campaign-level enabled is True (and optionally user hasn't disabled)
    """
    # Extract faction_minigame dict using centralized navigation
    faction_minigame = get_faction_minigame_dict(game_state)
    if not isinstance(faction_minigame, dict):
        return False

    # CRITICAL: Use strict identity check (is True) not truthiness check
    # This prevents string "false", string "true", None, 0, etc. from being truthy
    campaign_enabled = faction_minigame.get("enabled") is True

    if not campaign_enabled:
        return False

    # If user setting check requested, verify user hasn't globally disabled.
    # If user_settings wasn't passed explicitly, try extracting it from game_state.
    if check_user_setting:
        effective_user_settings = user_settings
        if effective_user_settings is None:
            if isinstance(game_state, dict):
                candidate = game_state.get("user_settings")
                if isinstance(candidate, dict):
                    effective_user_settings = candidate
            elif hasattr(game_state, "user_settings"):
                candidate = getattr(game_state, "user_settings", None)
                if isinstance(candidate, dict):
                    effective_user_settings = candidate

        if isinstance(effective_user_settings, dict):
            # User can disable globally even if campaign has it enabled
            user_disabled = (
                effective_user_settings.get("faction_minigame_enabled") is False
            )
            if user_disabled:
                return False

    return True


def extract_faction_minigame_state_from_game_state(
    game_state: Any,
) -> tuple[bool, int]:
    """Extract both enabled flag and turn_number from game_state.

    Convenience wrapper that combines enablement check + turn extraction.
    Uses get_faction_minigame_dict() which supports multiple extraction paths:
    - Direct attribute: game_state.faction_minigame
    - Canonical: game_state.custom_campaign_state["faction_minigame"]
    - Data wrappers: game_state.data.game_state.custom_campaign_state.faction_minigame
    - Fallback: game_state["faction_minigame"] or game_state.data["game_state"]["faction_minigame"]

    Args:
        game_state: GameState object or dict

    Returns:
        Tuple of (enabled: bool, turn_number: int) with safe defaults
    """
    faction_minigame = get_faction_minigame_dict(game_state)
    if not isinstance(faction_minigame, dict):
        return (False, 1)

    enabled = faction_minigame.get("enabled") is True

    try:
        turn_number = int(faction_minigame.get("turn_number", 1) or 1)
    except (TypeError, ValueError):
        turn_number = 1

    return (enabled, max(1, turn_number))


def extract_faction_minigame_state_from_prompt_contents(  # noqa: PLR0911
    prompt_contents: list[Any],
) -> tuple[bool, int]:
    """Extract faction_minigame state from prompt_contents (LLM request format).

    Provider-agnostic function for extracting faction minigame state from
    prompt_contents that are sent to LLM providers. Handles multiple formats:
    - JSON string: prompt_contents[0] is a JSON string
    - Dict: prompt_contents[0] is a dict
    - Empty: prompt_contents is empty or None

    For LLM service → provider calls, prompt_contents typically contains exactly one
    JSON string or dict created from LLMRequest data. This extracts faction_minigame
    data from game_state using the centralized extraction function that handles
    multiple paths (see extract_faction_minigame_state_from_game_state for details).

    Args:
        prompt_contents: List of prompt content items (typically JSON string or dict)

    Returns:
        (enabled, turn_number) with safe defaults (False, 1).
    """
    if not prompt_contents:
        return (False, 1)
    first = prompt_contents[0]
    if not isinstance(first, (str, dict)):
        return (False, 1)

    # Handle JSON string format
    if isinstance(first, str):
        if not first.strip():
            return (False, 1)
        try:
            payload = json.loads(first)
        except json.JSONDecodeError:
            return (False, 1)
        if not isinstance(payload, dict):
            return (False, 1)
    # Handle dict format
    elif isinstance(first, dict):
        payload = first
    else:
        return (False, 1)

    game_state = payload.get("game_state")
    if not isinstance(game_state, dict):
        return (False, 1)

    # Use centralized utility for consistent extraction and validation
    return extract_faction_minigame_state_from_game_state(game_state)


def is_faction_enable_action(prompt_contents: list[Any]) -> bool:  # noqa: PLR0911
    """Check if user_action is enabling the faction minigame.

    Provider-agnostic function for detecting when the user is requesting to
    enable the faction minigame. Uses explicit structured flags or the exact
    enable command to avoid rule-based intent detection.

    Args:
        prompt_contents: List of prompt content items (typically JSON string or dict)

    Returns:
        True if user is requesting to enable the faction minigame
    """
    if not prompt_contents:
        return False
    first = prompt_contents[0]

    # Handle both string (JSON) and dict formats
    payload: dict[str, Any] = {}
    if isinstance(first, str):
        if not first.strip():
            return False
        try:
            payload = json.loads(first)
        except json.JSONDecodeError:
            return False
    elif isinstance(first, dict):
        payload = first
    else:
        return False

    if not isinstance(payload, dict):
        return False

    explicit_enable = payload.get("enable_faction_minigame")
    if isinstance(explicit_enable, bool):
        return explicit_enable

    intent = payload.get("intent")
    if isinstance(intent, dict):
        intent_enable = intent.get("enable_faction_minigame")
        if isinstance(intent_enable, bool):
            return intent_enable

    user_action = payload.get("user_action", "")
    if isinstance(user_action, str):
        # Treat explicit user_action command as enablement; avoid keyword matching.
        user_action_line = user_action.splitlines()[0] if user_action else ""
        return user_action_line.strip().lower() == "enable_faction_minigame"
    return False


def build_expected_faction_tool_requests(
    tool_results: list[dict],
    turn_number: int,
) -> list[dict[str, Any]]:
    """Build faction tool_requests mirroring server-executed tool results.

    Returns empty list when faction power cannot be determined.
    """
    if not isinstance(tool_results, list) or not tool_results:
        return []

    power_result = None
    for tr in tool_results:
        if isinstance(tr, dict) and tr.get("tool") == "faction_calculate_power":
            power_result = tr
            break
    if not power_result:
        return []

    power_args = power_result.get("args", {})
    result = power_result.get("result", {})

    if isinstance(result, dict) and "error" in result:
        return []

    fp_value = None
    if isinstance(result, dict):
        fp_value = result.get("faction_power")
    if fp_value is None:
        return []

    try:
        safe_turn_number = int(turn_number or 1)
    except (TypeError, ValueError):
        safe_turn_number = 1

    return [
        {
            "tool": "faction_calculate_power",
            "args": power_args,
        },
        {
            "tool": "faction_calculate_ranking",
            "args": {
                "player_faction_power": fp_value,
                "turn_number": safe_turn_number,
            },
        },
    ]


def build_native_tools_for_prompt_contents(prompt_contents: list[Any]) -> list[dict]:
    """Build native tool list for provider native-tool flows.

    Tool selection is orchestrator-owned:
    - Always include dice tools
    - Include faction tools when minigame is enabled or being enabled this turn
    """
    tools = list(DICE_ROLL_TOOLS)
    faction_minigame_enabled, _ = extract_faction_minigame_state_from_prompt_contents(
        prompt_contents
    )
    if faction_minigame_enabled or is_faction_enable_action(prompt_contents):
        tools = tools + FACTION_TOOLS
    return tools
