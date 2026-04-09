"""Preventive Guards - Continuity Safeguards and State Integrity Enforcement

**THE DEFENSIVE LAYER** that prevents LLM hallucinations from breaking game state consistency.

This module enforces continuity safeguards and state integrity rules to prevent
LLM hallucinations from breaking game state consistency. It is the LAST LINE OF DEFENSE
before state changes are applied to the game.

**CRITICAL ANTI-BLITZ PROTECTION:**
The Social HP integrity enforcement (_ensure_social_hp_integrity) PREVENTS players from
spamming social interactions to rapidly drain NPC HP. Cooldown blocking is SERVER-ENFORCED
and cannot be bypassed through LLM manipulation or prompt engineering.

**MANDATORY Goal:**
Harden structured responses to prevent backtracking, state inconsistencies, and
exploits WITHOUT surfacing errors to users. Provides defensive state changes
augmented with continuity safeguards. This is SILENT enforcement - users never see
the corrections, but game state remains consistent.

**STRICT Scope:**
- ✅ Social HP integrity enforcement (cooldown blocking, damage capping) - ANTI-BLITZ
- ✅ World time consistency and progression (prevents time travel)
- ✅ Location progress tracking (ensures location changes are valid)
- ✅ Core memory deduplication (prevents duplicate memories)
- ✅ Resource checkpoint persistence (ensures resources are tracked)
- ✅ DM notes persistence metadata (preserves DM notes across turns)
- ✅ God mode response extraction (separates god mode from narrative)

**STRICT BOUNDARIES:**
- ✅ MUST: Take raw state_updates from LLM response
- ✅ MUST: Apply continuity safeguards (cooldown blocking, time progression, etc.)
- ✅ MUST: Return augmented state_changes dict with safeguards applied
- ✅ MUST: Enforce Social HP cooldown blocking (damage MUST be 0 if cooldown > 0)
- ✅ MUST: Cap Social HP damage at current HP (prevents over-damage exploits)
- ❌ MUST NOT: Mutate game state directly (callers in world_logic.py apply changes)
- ❌ MUST NOT: Surface errors to users (silent enforcement only)
- ❌ MUST NOT: Skip any safeguard checks (all safeguards MUST run)

**What It Actually Does:**
- Takes raw state_updates from LLM response (may contain hallucinations/exploits)
- Applies continuity safeguards (cooldown blocking, time progression, damage capping)
- Returns augmented state_changes dict with safeguards applied
- Callers in world_logic.py MUST apply these changes to game state

**Key Functions:**
- enforce_preventive_guards: Main entry point - applies ALL safeguards (MUST call all)
- _ensure_social_hp_integrity: Enforces Social HP cooldown and damage caps (ANTI-BLITZ)
- _ensure_world_time: Ensures time progression consistency (prevents time travel)
- _ensure_location_progress: Tracks location changes (ensures valid transitions)
- _ensure_core_memory: Deduplicates core memories (prevents duplicates)
- _ensure_resource_checkpoint: Persists resource checkpoints (ensures tracking)
- _ensure_dm_notes_persistence: Returns merged DM notes for caller-side persistence

**Violation Consequences:**
If safeguards are skipped or bypassed, LLM hallucinations can break game state
consistency, enable exploits (Social HP blitzing), or cause time travel bugs.
ALL safeguards MUST run on EVERY state update.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from mvp_site import constants, logging_util
from mvp_site.faction.tools import execute_faction_tool
from mvp_site.game_state import GameState
from mvp_site.llm_response import LLMResponse
from mvp_site.memory_utils import (
    AUTO_MEMORY_MAX_LENGTH,
    AUTO_MEMORY_PREFIX,
    is_duplicate_memory,
)


def _to_int(value: Any, default: int = 0) -> int:
    """Safely coerce value to int, returning default on failure."""
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def enforce_preventive_guards(
    game_state: GameState, llm_response: LLMResponse, mode: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Harden structured responses to prevent backtracking without surfacing errors.

    Returns a tuple of (state_changes, extras) where ``state_changes`` is a
    defensive copy of the model-provided updates augmented with continuity
    safeguards, and ``extras`` contains auxiliary values (e.g., synthesized
    ``god_mode_response``) that should be added to the unified response and
    stored structured fields.
    """

    raw_state_updates = llm_response.get_state_updates()
    if isinstance(raw_state_updates, dict):
        state_changes: dict[str, Any] = deepcopy(raw_state_updates)
    else:
        logging_util.warning(
            "Preventive guards received non-dict state_updates (%s); using empty dict",
            type(raw_state_updates).__name__,
        )
        state_changes = {}

    # Ensure social_hp_challenge is included in state_changes if present in structured_response
    if (
        hasattr(llm_response, "structured_response")
        and llm_response.structured_response
    ):
        social_challenge = getattr(
            llm_response.structured_response, "social_hp_challenge", None
        )
        if social_challenge:
            # If state_changes already has it (rare), prefer that, otherwise inject from root
            if "social_hp_challenge" not in state_changes:
                state_changes["social_hp_challenge"] = deepcopy(social_challenge)

    extras: dict[str, Any] = {}

    _fill_god_mode_response(mode, llm_response, extras)

    dice_rolls = getattr(llm_response, "dice_rolls", [])
    resources = getattr(llm_response, "resources", "")

    if dice_rolls or resources:
        _ensure_world_time(state_changes, game_state)
        _ensure_core_memory(state_changes, llm_response.narrative_text)

    _ensure_location_progress(state_changes, llm_response, game_state)

    if resources:
        _ensure_resource_checkpoint(state_changes, resources)

    # Persist dm_notes from debug_info across turns without polluting state_updates.
    persisted_dm_notes = _ensure_dm_notes_persistence(llm_response, game_state)
    if persisted_dm_notes:
        extras["persist_debug_info"] = {"dm_notes": persisted_dm_notes}

    # Social HP integrity (cooldowns, damage caps)
    _ensure_social_hp_integrity(state_changes, game_state, llm_response)

    # Faction minigame integrity (enablement rules, unit categorization safety)
    _ensure_faction_minigame_integrity(state_changes, game_state, llm_response)

    return state_changes, extras


def _extract_faction_tool_values(
    debug_info: dict[str, Any],
) -> tuple[int | None, int | None, bool]:
    """Extract FP/ranking from tool_results if present.

    Returns (faction_power, ranking, has_tool_results).
    """
    tool_results = debug_info.get("tool_results")
    if not isinstance(tool_results, list):
        return None, None, False

    fp_value = None
    ranking_value = None
    has_faction_tool = False
    for entry in tool_results:
        if not isinstance(entry, dict):
            continue
        tool_name = entry.get("tool")
        result = entry.get("result", {})
        if not isinstance(result, dict):
            continue
        if tool_name == "faction_calculate_power" and "faction_power" in result:
            has_faction_tool = True
            fp_value = result.get("faction_power")
        if tool_name == "faction_calculate_ranking":
            has_faction_tool = True
            if "ranking" in result:
                ranking_value = result.get("ranking")
            elif "rank" in result:
                ranking_value = result.get("rank")

    fp_int = _to_int(fp_value, 0) if fp_value is not None else None
    if ranking_value is None:
        ranking_int = None
    else:
        try:
            ranking_int = int(ranking_value)
        except (TypeError, ValueError):
            ranking_int = None

    return fp_int, ranking_int, has_faction_tool


def _categorize_units_from_army_data(army_data: dict[str, Any]) -> dict[str, Any]:
    """Derive faction_minigame.units from army_data.forces as a fallback."""
    forces = army_data.get("forces", {})
    if not isinstance(forces, dict):
        return {}

    spy_keywords = ("scout", "spy", "agent", "infil", "assassin", "shadow")
    elite_keywords = (
        "elite",
        "guard",
        "champion",
        "hero",
        "war_mage",
        "mage",
        "paladin",
        "knight",
        "veteran",
    )

    soldiers = 0
    spies = 0
    elites = 0

    for name, force in forces.items():
        if not isinstance(force, dict):
            continue
        force_type = force.get("type") or name
        force_type_str = str(force_type).lower()
        blocks = _to_int(force.get("blocks"), 0)
        count = blocks * 10 if blocks > 0 else _to_int(force.get("count"), 0)
        if count <= 0:
            continue

        if any(keyword in force_type_str for keyword in spy_keywords):
            spies += count
        elif any(keyword in force_type_str for keyword in elite_keywords):
            elites += count
        else:
            soldiers += count

    total = soldiers + spies + elites
    if total <= 0:
        return {}

    elite_avg_level = 6.0 if elites > 0 else 0.0
    return {
        "soldiers": soldiers,
        "spies": spies,
        "elites": elites,
        "elite_avg_level": elite_avg_level,
    }


def _get_army_data_with_fallbacks(
    state_changes: dict[str, Any], game_state: GameState
) -> dict[str, Any]:
    """Retrieve army_data from multiple sources with fallbacks.

    Tries in order: state_changes, game_state attribute, game_state.to_dict().
    Returns empty dict if not found.
    """
    army_data = state_changes.get("army_data")
    if not isinstance(army_data, dict):
        army_data = getattr(game_state, "army_data", None)
    if not isinstance(army_data, dict):
        army_data = game_state.to_dict().get("army_data", {})
    return army_data if isinstance(army_data, dict) else {}


def _get_faction_context(
    faction_updates: dict[str, Any], previous_faction: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any], int]:
    """Extract resources, buildings, and turn_number from faction state.

    Returns (resources, buildings, turn_number) with safe defaults.
    """
    resources = (
        faction_updates.get("resources") or previous_faction.get("resources") or {}
    )
    if not isinstance(resources, dict):
        resources = {}
    buildings = (
        faction_updates.get("buildings") or previous_faction.get("buildings") or {}
    )
    if not isinstance(buildings, dict):
        buildings = {}
    turn_number = _to_int(
        faction_updates.get("turn_number") or previous_faction.get("turn_number"),
        1,
    )
    return resources, buildings, turn_number


def _ensure_faction_minigame_integrity(
    state_changes: dict[str, Any],
    game_state: GameState,
    llm_response: LLMResponse,
) -> None:
    """Enforce faction minigame enablement rules and safe defaults."""

    def _compute_faction_power_and_ranking(
        *,
        soldiers: int,
        spies: int,
        elites: int,
        elite_avg_level: float,
        territory: int,
        fortifications: int,
        turn_number: int,
    ) -> tuple[int | None, int | None]:
        power_result = execute_faction_tool(
            "faction_calculate_power",
            {
                "soldiers": soldiers,
                "spies": spies,
                "elites": elites,
                "elite_avg_level": elite_avg_level,
                "territory": territory,
                "fortifications": fortifications,
            },
        )
        if not isinstance(power_result, dict):
            return None, None
        fp_value = power_result.get("faction_power")
        if fp_value is None:
            return None, None

        fp_int = _to_int(fp_value, 0)
        ranking_value = None
        ranking_result = execute_faction_tool(
            "faction_calculate_ranking",
            {
                "player_faction_power": fp_int,
                "turn_number": turn_number,
            },
        )
        if isinstance(ranking_result, dict):
            ranking_value = ranking_result.get("ranking")

        if fp_int < constants.MIN_RANK_FP:
            ranking_value = None

        return fp_int, ranking_value

    custom_state = state_changes.get("custom_campaign_state")
    if not isinstance(custom_state, dict):
        return

    faction_updates = custom_state.get("faction_minigame")
    if not isinstance(faction_updates, dict):
        return

    previous_custom = getattr(game_state, "custom_campaign_state", {}) or {}
    if not isinstance(previous_custom, dict):
        previous_custom = {}
    previous_faction = previous_custom.get("faction_minigame", {})
    if not isinstance(previous_faction, dict):
        previous_faction = {}

    prev_enabled = bool(previous_faction.get("enabled", False))
    new_enabled = faction_updates.get("enabled", None)
    is_enabling = (new_enabled is True) and (not prev_enabled)
    effective_enabled = new_enabled if new_enabled is not None else prev_enabled

    # Guardrail: on enablement, resources must come from existing state (no invention)
    if (
        "enabled" in faction_updates
        and effective_enabled
        and "resources" in faction_updates
    ):
        prev_resources = previous_faction.get("resources", {})
        if not isinstance(prev_resources, dict):
            prev_resources = {}
        faction_updates["resources"] = {
            "territory": _to_int(prev_resources.get("territory"), 0),
            "citizens": _to_int(prev_resources.get("citizens"), 0),
            "max_citizens": _to_int(prev_resources.get("max_citizens"), 0),
            "gold": _to_int(prev_resources.get("gold"), 0),
            "arcana": _to_int(prev_resources.get("arcana"), 0),
            "max_arcana": _to_int(prev_resources.get("max_arcana"), 0),
        }

    # Guardrail: tutorial should NOT start on explicit enablement updates.
    if "enabled" in faction_updates and faction_updates.get("tutorial_started") is True:
        faction_updates["tutorial_started"] = False
        logging_util.warning(
            "⚠️ FACTION_GUARD: Cleared tutorial_started on enablement "
            "(should trigger next status query)."
        )
        if "tutorial_progress" in faction_updates:
            faction_updates.pop("tutorial_progress", None)
        if "tutorial_completed" in faction_updates:
            faction_updates.pop("tutorial_completed", None)

    recomputed_tools = False
    fallback_enablement = is_enabling or (
        "enabled" in faction_updates and effective_enabled
    )
    if fallback_enablement:
        units = faction_updates.get("units")
        if not isinstance(units, dict):
            units = {}
        total_units = (
            _to_int(units.get("soldiers"), 0)
            + _to_int(units.get("spies"), 0)
            + _to_int(units.get("elites"), 0)
        )
        if total_units == 0:
            army_data = _get_army_data_with_fallbacks(state_changes, game_state)
            total_strength = _to_int(army_data.get("total_strength"), 0)
            categorized = _categorize_units_from_army_data(army_data)
            if categorized and total_strength > 0:
                faction_updates["units"] = categorized
                logging_util.warning(
                    "⚠️ FACTION_GUARD: Auto-categorized units from army_data "
                    "during enablement fallback."
                )

                soldiers = _to_int(categorized.get("soldiers"), 0)
                spies = _to_int(categorized.get("spies"), 0)
                elites = _to_int(categorized.get("elites"), 0)
                elite_avg_level = categorized.get("elite_avg_level", 6.0)
                try:
                    elite_avg_level = float(elite_avg_level)
                except (TypeError, ValueError):
                    elite_avg_level = 6.0

                resources, buildings, turn_number = _get_faction_context(
                    faction_updates, previous_faction
                )
                territory = _to_int(resources.get("territory"), 0)
                forts = _to_int(buildings.get("fortifications"), 0)

                fp_int, ranking_value = _compute_faction_power_and_ranking(
                    soldiers=soldiers,
                    spies=spies,
                    elites=elites,
                    elite_avg_level=elite_avg_level,
                    territory=territory,
                    fortifications=forts,
                    turn_number=turn_number,
                )
                if fp_int is not None:
                    faction_updates["faction_power"] = fp_int
                    faction_updates["ranking"] = ranking_value
                recomputed_tools = True
        elif total_units > 0:
            current_fp = faction_updates.get("faction_power")
            if current_fp is None or _to_int(current_fp, 0) == 0:
                soldiers = _to_int(units.get("soldiers"), 0)
                spies = _to_int(units.get("spies"), 0)
                elites = _to_int(units.get("elites"), 0)
                elite_avg_level = units.get("elite_avg_level", 6.0)
                try:
                    elite_avg_level = float(elite_avg_level)
                except (TypeError, ValueError):
                    elite_avg_level = 6.0

                resources, buildings, turn_number = _get_faction_context(
                    faction_updates, previous_faction
                )
                territory = _to_int(resources.get("territory"), 0)
                forts = _to_int(buildings.get("fortifications"), 0)

                fp_int, ranking_value = _compute_faction_power_and_ranking(
                    soldiers=soldiers,
                    spies=spies,
                    elites=elites,
                    elite_avg_level=elite_avg_level,
                    territory=territory,
                    fortifications=forts,
                    turn_number=turn_number,
                )
                if fp_int is not None:
                    faction_updates["faction_power"] = fp_int
                    faction_updates["ranking"] = ranking_value
                    logging_util.warning(
                        "⚠️ FACTION_GUARD: Backfilled faction_power/ranking from "
                        "LLM-provided units during enablement."
                    )
                    recomputed_tools = True

    # Detect zeroed units when army_data exists (LLM must categorize; server should not decide)
    if effective_enabled and ("units" in faction_updates or is_enabling):
        units = faction_updates.get("units")
        if not isinstance(units, dict):
            units = {}
        total_units = (
            _to_int(units.get("soldiers"), 0)
            + _to_int(units.get("spies"), 0)
            + _to_int(units.get("elites"), 0)
        )
        if total_units == 0:
            army_data = _get_army_data_with_fallbacks(state_changes, game_state)
            total_strength = _to_int(army_data.get("total_strength"), 0)
            if total_strength > 0 and army_data.get("forces"):
                logging_util.warning(
                    "⚠️ FACTION_GUARD: Units remain zero with army_data present; "
                    "LLM must categorize (server will not auto-categorize)."
                )

    # Align FP/ranking with tool results if available
    if not recomputed_tools:
        debug_info = llm_response.get_debug_info()
        fp_value, ranking_value, has_tools = _extract_faction_tool_values(debug_info)
        if has_tools:
            if fp_value is not None:
                faction_updates["faction_power"] = fp_value
            if (
                fp_value is not None
                and fp_value < constants.MIN_RANK_FP
                or ranking_value is None
            ):
                faction_updates["ranking"] = None
            else:
                faction_updates["ranking"] = ranking_value

    # Safety: never persist ranking below the minimum FP threshold
    current_fp = faction_updates.get("faction_power")
    if current_fp is not None:
        fp_int = _to_int(current_fp, 0)
        if fp_int < constants.MIN_RANK_FP:
            faction_updates["ranking"] = None


def _fill_god_mode_response(
    mode: str, llm_response: LLMResponse, extras: dict[str, Any]
) -> None:
    structured = getattr(llm_response, "structured_response", None)
    existing = getattr(structured, constants.FIELD_GOD_MODE_RESPONSE, None)
    if mode == constants.MODE_GOD and not existing:
        extras[constants.FIELD_GOD_MODE_RESPONSE] = llm_response.narrative_text


def _ensure_world_time(state_changes: dict[str, Any], game_state: GameState) -> None:
    world_data = state_changes.setdefault("world_data", {})
    world_time = world_data.get("world_time")
    if isinstance(world_time, dict) and world_time and "hour" in world_time:
        return

    existing = game_state.world_data.get("world_time")
    if isinstance(existing, dict) and existing:
        world_data["world_time"] = deepcopy(existing)
    else:
        world_data["world_time"] = {"hour": 12, "minute": 0, "time_of_day": "midday"}


def _ensure_core_memory(state_changes: dict[str, Any], narrative: str) -> None:
    custom_state = state_changes.setdefault("custom_campaign_state", {})
    core_memories = custom_state.get("core_memories")
    if not isinstance(core_memories, list):
        core_memories = []
    snippet = narrative.strip() if isinstance(narrative, str) else ""
    if snippet:
        entry = f"{AUTO_MEMORY_PREFIX} {snippet}"[:AUTO_MEMORY_MAX_LENGTH]
        # Check for duplicates or near-duplicates using centralized logic
        if not is_duplicate_memory(entry, core_memories):
            core_memories.append(entry)
    custom_state["core_memories"] = core_memories


def _ensure_location_progress(
    state_changes: dict[str, Any],
    llm_response: LLMResponse,
    game_state: GameState,
) -> None:
    get_location_confirmed = getattr(llm_response, "get_location_confirmed", None)
    location = get_location_confirmed() if callable(get_location_confirmed) else None
    if not isinstance(location, str):
        location = ""
    world_data = state_changes.setdefault("world_data", {})
    custom_state = state_changes.setdefault("custom_campaign_state", {})

    if location and location.lower() != "unknown":
        world_data["current_location_name"] = location
        custom_state["last_location"] = location
        return

    # Handle None world_data gracefully
    game_state_world_data = getattr(game_state, "world_data", None)
    if isinstance(game_state_world_data, dict):
        prior_location = game_state_world_data.get("current_location_name")
        if prior_location and "current_location_name" not in world_data:
            world_data["current_location_name"] = prior_location
            custom_state["last_location"] = prior_location


def _ensure_resource_checkpoint(state_changes: dict[str, Any], resources: str) -> None:
    resource_state = state_changes.setdefault("world_resources", {})
    if isinstance(resource_state, dict):
        resource_state["last_note"] = resources


def _ensure_dm_notes_persistence(
    llm_response: LLMResponse,
    game_state: GameState,
) -> list[str]:
    """Collect merged dm_notes for persistence in game_state.debug_info.

    The LLM writes dm_notes to debug_info (top-level response field), but only
    canonical state fields should flow through state_updates. This function
    bridges the gap by returning merged dm_notes for the caller to persist on
    the final game state object directly.

    Existing dm_notes from game_state are preserved and new notes appended.
    """
    llm_debug_info = llm_response.get_debug_info()
    new_dm_notes = llm_debug_info.get("dm_notes", [])

    # Normalize to list
    if isinstance(new_dm_notes, str):
        new_dm_notes = [new_dm_notes] if new_dm_notes.strip() else []
    elif not isinstance(new_dm_notes, list):
        new_dm_notes = []

    if not new_dm_notes:
        return []

    # Get existing dm_notes from game_state
    existing_debug_info = getattr(game_state, "debug_info", {}) or {}
    existing_dm_notes = existing_debug_info.get("dm_notes", [])
    if not isinstance(existing_dm_notes, list):
        existing_dm_notes = []

    # Merge: existing + new (deduplicated)
    merged_notes = list(existing_dm_notes)
    for note in new_dm_notes:
        if isinstance(note, str) and note.strip() and note not in merged_notes:
            merged_notes.append(note)

    return merged_notes


def _ensure_social_hp_integrity(
    state_changes: dict[str, Any], game_state: GameState, llm_response: Any = None
) -> None:
    """Enforce Social HP integrity rules: cooldown blocks damage, damage caps at current HP.

    Applies 5 enforcement rules to prevent exploits and ensure state consistency:

    1. **Cooldown Blocker**: If cooldown is active at start of turn, damage MUST be 0
       (prevents blitzing). Uses HYBRID system: time-based if time advances, turn-based otherwise.
    2. **Damage Cap**: social_hp_damage cannot exceed current social_hp (prevents over-damage)
    3. **HP Recalculation**: Ensures social_hp = old_hp - damage (corrects LLM hallucinations)
    4. **Cooldown Decrement**: HYBRID system:
       - If time advanced: cooldown expires when current_hour >= cooldown_until_hour
       - If time didn't advance: cooldown decrements by 1 each turn
       This ensures cooldown still progresses even when LLM doesn't advance time.

    Cooldown updates on EVERY game turn, not just social turns.
    If LLM doesn't return social_hp_challenge, we still update existing cooldown.

    Mutates state_changes dict in-place. Does NOT mutate game_state directly.

    Args:
        state_changes: Dict containing social_hp_challenge to be validated/enforced
        game_state: Current game state (read-only, used to get previous challenge state)
    """
    # Get previous state
    # GameState attribute/dict access normalization
    old_challenge = getattr(game_state, "social_hp_challenge", {})
    if not isinstance(old_challenge, dict):
        old_challenge = {}

    # Get new challenge from state_changes (may be None if LLM didn't return one OR guardrails cleared it)
    new_challenge_raw = state_changes.get("social_hp_challenge")
    if new_challenge_raw is None:
        # CRITICAL: Distinguish between two cases:
        # 1. LLM didn't return social_hp_challenge (no existing challenge) → create {} for cooldown updates
        # 2. Guardrails intentionally cleared it (existing challenge was cleared OR guardrails triggered) → preserve None/remove it

        # Check if guardrails were triggered (via debug_info in structured_response)
        guardrails_cleared = False
        if llm_response:
            structured_response = getattr(llm_response, "structured_response", None)
            if structured_response:
                debug_info = getattr(structured_response, "debug_info", None)
                if debug_info and debug_info.get("guardrails_triggered"):
                    guardrails_cleared = True

        # Also check if there's an existing challenge that was cleared
        has_existing_challenge = (
            isinstance(old_challenge, dict)
            and old_challenge
            and old_challenge.get(
                "npc_name"
            )  # Has actual challenge data, not just empty dict
        )

        if guardrails_cleared:
            # Guardrails intentionally cleared the challenge - preserve None
            # Remove the key entirely to signal complete removal
            state_changes.pop("social_hp_challenge", None)
            logging_util.info(
                "🛡️ SOCIAL_HP_GUARD: Guardrails cleared challenge, preserving None (removing key)"
            )
            return  # Early return - no cooldown updates needed when challenge is cleared
        if has_existing_challenge:
            # LLM didn't return social_hp_challenge, but there's an existing one
            # We need to continue processing to decrement cooldown on non-social turns
            # Copy existing challenge so we can update cooldown
            new_challenge = old_challenge.copy()
            # If we're carrying over an old challenge, we should check if the NPC is still relevant
            # But for now, we assume if it wasn't explicitly cleared, we should maintain it
            state_changes["social_hp_challenge"] = new_challenge
            logging_util.info(
                "🛡️ SOCIAL_HP_GUARD: LLM didn't return challenge, using existing for cooldown update"
            )
        else:
            # LLM didn't return social_hp_challenge AND no existing challenge
            # No challenge to process - return early to avoid creating orphan partial challenge
            # logging_util.info(
            #    f"🛡️ SOCIAL_HP_GUARD: No challenge from LLM and no existing challenge, skipping"
            # )
            return  # Early return - nothing to process
    elif isinstance(new_challenge_raw, dict):
        new_challenge = new_challenge_raw
    else:
        # Invalid type, create empty dict
        new_challenge = {}
        state_changes["social_hp_challenge"] = new_challenge

    # CRITICAL DEBUG: Log old_challenge state to verify persistence
    logging_util.info(
        f"🛡️ SOCIAL_HP_GUARD: old_challenge state - "
        f"social_hp={old_challenge.get('social_hp')}, "
        f"social_hp_max={old_challenge.get('social_hp_max')}, "
        f"cooldown_remaining={old_challenge.get('cooldown_remaining')}, "
        f"cooldown_until_hour={old_challenge.get('cooldown_until_hour')}, "
        f"old_challenge_keys={list(old_challenge.keys()) if isinstance(old_challenge, dict) else 'N/A'}"
    )

    # Preserve original cooldown value BEFORE any processing (needed for cooldown blocker check)
    # CRITICAL: Verify NPC identity matches. If LLM switched NPCs, we must NOT carry over
    # HP or cooldown from the previous NPC. Treat as a fresh challenge.
    old_npc = old_challenge.get("npc_name", "")
    new_npc = new_challenge.get("npc_name", "")
    # Normalize comparison (case-insensitive, strip whitespace)
    # Allow partial matches (e.g. "Valerius" matches "Lord Valerius")
    norm_old = str(old_npc).strip().lower()
    norm_new = str(new_npc).strip().lower()

    # Check for mismatch: neither contains the other
    if old_npc and new_npc and norm_old not in norm_new and norm_new not in norm_old:
        logging_util.warning(
            f"🛡️ SOCIAL_HP_GUARD: NPC switch detected ('{old_npc}' -> '{new_npc}'). "
            f"Resetting old_challenge tracking to prevent state leak."
        )
        old_challenge = {}
        # Values will be reset to 0/None when extracted from empty dict below

    old_cd_original = _to_int(old_challenge.get("cooldown_remaining"), 0)
    old_cd_until_hour_raw = old_challenge.get("cooldown_until_hour")
    old_cd_until_hour = (
        _to_int(old_cd_until_hour_raw, 0) if old_cd_until_hour_raw is not None else None
    )  # Time-based cooldown
    old_hp_raw = old_challenge.get("social_hp")
    if old_hp_raw is None:
        # If no previous challenge, we need to find the NPC's starting HP
        # Priority: 1) new challenge's social_hp_max, 2) derived from new social_hp + damage, 3) npc_data, 4) default 0
        new_challenge_temp = state_changes.get("social_hp_challenge", {})
        if isinstance(new_challenge_temp, dict):
            old_max = new_challenge_temp.get("social_hp_max")
            new_current = new_challenge_temp.get("social_hp")
            new_damage = _to_int(new_challenge_temp.get("social_hp_damage", 0), 0)

            if old_max is not None:
                old_hp_raw = old_max
            elif new_current is not None:
                # Deduce start-of-turn HP if we have current and damage
                old_hp_raw = _to_int(new_current, 0) + new_damage
            else:
                # Try to get HP from npc_data based on NPC name
                npc_name = new_challenge_temp.get("npc_name", "")
                npc_data = getattr(game_state, "npc_data", {}) or {}
                if isinstance(npc_data, dict):
                    # Search for NPC by name
                    for npc_id, npc in npc_data.items():
                        if isinstance(npc, dict) and npc.get("name") == npc_name:
                            old_hp_raw = npc.get("social_hp_max") or npc.get(
                                "social_hp"
                            )
                            logging_util.info(
                                f"🛡️ SOCIAL_HP_GUARD: Got starting HP from npc_data[{npc_id}]: {old_hp_raw}"
                            )
                            break
                if old_hp_raw is None:
                    old_hp_raw = 0
        else:
            old_hp_raw = 0
    old_hp = _to_int(old_hp_raw, 0)

    # Get current game time for time-based cooldown
    # CRITICAL: Read from game_state.world_data.world_time.hour
    # Note: game_state is loaded fresh from Firestore at the start of process_action_unified,
    # so it should reflect GOD_MODE updates from previous calls
    # CRITICAL: Read from state_changes first (priority), then game_state
    # This handles "natural time advancement" where LLM updates time in the same turn
    # as the social action. game_state only reflects the state at START of turn.

    # 1. Try to get time from state_changes (LLM update)
    state_changes_world_data = state_changes.get("world_data", {})
    current_world_time = (
        state_changes_world_data.get("world_time", {})
        if isinstance(state_changes_world_data, dict)
        else {}
    )
    source = "state_changes"

    # 2. Fallback to game_state if not present in changes
    if (
        not current_world_time
        or not isinstance(current_world_time, dict)
        or "hour" not in current_world_time
    ):
        game_state_world_data = getattr(game_state, "world_data", None)
        if isinstance(game_state_world_data, dict):
            current_world_time = game_state_world_data.get("world_time", {})
            source = "game_state"
        else:
            current_world_time = {}
            source = "game_state (empty)"

    if not isinstance(current_world_time, dict):
        current_world_time = {}

    current_hour = _to_int(current_world_time.get("hour", 0), 0)

    # CRITICAL DEBUG: Always log current_hour extraction for debugging
    # This helps diagnose cases where game_state doesn't reflect GOD_MODE updates
    game_state_world_data = getattr(game_state, "world_data", None)
    game_state_world_time = (
        game_state_world_data.get("world_time", {})
        if isinstance(game_state_world_data, dict)
        else {}
    )
    logging_util.warning(
        f"🛡️ SOCIAL_HP_GUARD: Extracted current_hour={current_hour} from {source}. "
        f"game_state.world_data type: {type(game_state_world_data)}, "
        f"game_state.world_data is None: {game_state_world_data is None}, "
        f"game_state.world_data is empty dict: {game_state_world_data == {}}, "
        f"game_state.world_data keys: {list(game_state_world_data.keys()) if isinstance(game_state_world_data, dict) else 'N/A'}, "
        f"game_state.world_time type: {type(game_state_world_time)}, "
        f"game_state.world_time keys: {list(game_state_world_time.keys()) if isinstance(game_state_world_time, dict) else 'N/A'}, "
        f"game_state.world_time.hour: {game_state_world_time.get('hour', 'MISSING') if isinstance(game_state_world_time, dict) else 'N/A'}, "
        f"state_changes.world_data keys: {list(state_changes_world_data.keys()) if isinstance(state_changes_world_data, dict) else 'N/A'}, "
        f"final current_hour: {current_hour}"
    )

    # Now process the challenge from LLM
    # Check if cooldown is active (hybrid: time-based OR turn-based)
    # CRITICAL: Turn-based cooldowns expire when time advances externally
    # If time has advanced (current_hour > 0) and we had a turn-based cooldown,
    # it should be considered expired (time advancement supersedes turn-based)
    cooldown_active = False
    if old_cd_until_hour is not None:
        # Time-based cooldown: check if current hour < cooldown_until_hour
        # CRITICAL: Handle midnight wraparound (cooldown_until=0, current=23)
        # If cooldown_until < current by more than 12 hours, it wrapped to next day
        if current_hour < old_cd_until_hour:
            # Normal case: cooldown in future (e.g., current=10, until=15)
            cooldown_active = True
            effective_cd = old_cd_until_hour - current_hour
        elif current_hour > old_cd_until_hour:
            # Either expired OR wrapped to next day
            # If diff > 12 hours, it wrapped (e.g., current=23, until=0 → diff=23)
            hours_diff = current_hour - old_cd_until_hour
            if hours_diff > 12:  # Wraparound case
                cooldown_active = True
                effective_cd = (
                    24 - current_hour
                ) + old_cd_until_hour  # Hours until next day's target
            else:  # Expired (e.g., current=15, until=10 → diff=5 < 12)
                cooldown_active = False
                effective_cd = 0
        else:  # current_hour == old_cd_until_hour
            # Reached target hour, cooldown expired
            cooldown_active = False
            effective_cd = 0
    elif old_cd_original > 0:
        # Turn-based cooldown: check if cooldown_remaining > 0
        cooldown_active = True
        effective_cd = old_cd_original
    else:
        effective_cd = 0

    logging_util.info(
        f"🛡️ SOCIAL_HP_GUARD: old_hp={old_hp}, cooldown_active={cooldown_active}, "
        f"effective_cd={effective_cd}, time_based={old_cd_until_hour is not None}, "
        f"current_hour={current_hour}, new_damage={new_challenge.get('social_hp_damage')}, "
        f"old_challenge_empty={len(old_challenge) == 0}"
    )

    # 1. Enforce Cooldown Blocker
    # If cooldown is active at start of turn, damage MUST be 0
    if cooldown_active:
        new_damage = _to_int(new_challenge.get("social_hp_damage", 0), 0)
        if new_damage > 0:
            logging_util.warning(
                f"🛡️ SOCIAL_HP_GUARD: Cooldown active (effective_cd={effective_cd}), blocking damage ({new_damage} -> 0)"
            )
            new_challenge["social_hp_damage"] = 0
            # Re-calculate cooldown: decrement turn-based OR check time-based expiration
            if old_cd_until_hour is not None:
                # Time-based: update remaining hours
                if current_hour >= old_cd_until_hour:
                    new_challenge.pop("cooldown_until_hour", None)
                    new_challenge["cooldown_remaining"] = 0
                else:
                    new_challenge["cooldown_remaining"] = max(
                        1, old_cd_until_hour - current_hour
                    )
            else:
                # Turn-based: decrement
                new_challenge["cooldown_remaining"] = max(0, old_cd_original - 1)
            # Re-calculate HP: should be unchanged
            new_challenge["social_hp"] = old_hp
        # CRITICAL: Always clamp cooldown_remaining to prevent early reset
        # If LLM returns smaller value (e.g., old_cd=2 but sets cooldown_remaining=0),
        # this prevents cooldown from resetting early and re-enabling blitzing
        elif old_cd_until_hour is not None:
            # Time-based: update remaining hours
            if current_hour >= old_cd_until_hour:
                new_challenge.pop("cooldown_until_hour", None)
                new_challenge["cooldown_remaining"] = 0
            else:
                # Time-based: calculate remaining hours from time difference
                new_challenge["cooldown_remaining"] = max(
                    1, old_cd_until_hour - current_hour
                )

        # CRITICAL FIX: Reset HP when cooldown is active, EVEN if explicit damage=0
        # This prevents bypass where LLM sets social_hp directly without social_hp_damage
        # We check if new_hp is less than old_hp. If so, we reset it.
        # We must use _to_int safely and handle None.
        new_hp_check = new_challenge.get("social_hp")
        if new_hp_check is not None and _to_int(new_hp_check, old_hp) < old_hp:
            logging_util.warning(
                f"🛡️ SOCIAL_HP_GUARD: Cooldown active - blocking implicit HP decrease "
                f"({new_hp_check} -> {old_hp})"
            )
            new_challenge["social_hp"] = old_hp

    # 2. Calculate and Enforce Damage    # CRITICAL: LLM may only return new social_hp without explicit social_hp_damage
    # We must calculate damage from HP change to properly trigger cooldown
    new_hp_raw = new_challenge.get("social_hp")
    new_hp = _to_int(new_hp_raw, old_hp) if new_hp_raw is not None else old_hp
    damage = _to_int(new_challenge.get("social_hp_damage", 0), 0)

    logging_util.info(
        f"🛡️ SOCIAL_HP_GUARD: Damage calc check - old_hp={old_hp}, new_hp_raw={new_hp_raw}, "
        f"new_hp={new_hp}, damage={damage}, condition={damage == 0 and old_hp > new_hp}"
    )

    # If LLM didn't set explicit damage but HP decreased, calculate from HP change
    # Note: We re-check this even if we reset it above, just to be sure we have the right damage value
    # If we reset it above, old_hp == new_hp, so damage will be 0, which is correct.
    if damage == 0 and old_hp > new_hp:
        damage = old_hp - new_hp
        new_challenge["social_hp_damage"] = damage
        logging_util.info(
            f"🛡️ SOCIAL_HP_GUARD: Calculated damage from HP change: {old_hp} -> {new_hp} = {damage}"
        )

    # Cap damage at current HP (can't deal more damage than HP remaining)
    if damage > old_hp:
        logging_util.warning(
            f"🛡️ SOCIAL_HP_GUARD: Damage ({damage}) exceeds current HP ({old_hp}), capping."
        )
        damage = old_hp
        new_challenge["social_hp_damage"] = damage

    # 2.5. Trigger Cooldown When Damage Dealt
    # HYBRID SYSTEM: Use time-based if time advances, turn-based otherwise
    # If damage > 0 and cooldown was not active, set cooldown (prevents blitzing)
    # Re-fetch damage as it might have been updated
    final_damage = _to_int(new_challenge.get("social_hp_damage", 0), 0)
    current_cd = _to_int(new_challenge.get("cooldown_remaining", 0), 0)

    # Check if time advanced in THIS turn (check state_changes for new world_time)
    # CRITICAL: Also check if time was advanced externally (current_hour > 0)
    # If current_hour > 0, it means time was advanced externally (GOD_MODE or natural)
    # and we should use current_hour as the authoritative time, not new_hour from state_changes
    # FIX: Handle explicit None for world_data (defensive against LLM returning null)
    world_data = state_changes.get("world_data")
    new_world_time = (
        world_data.get("world_time", {}) if isinstance(world_data, dict) else {}
    )
    if not new_world_time or not isinstance(new_world_time, dict):
        # No time update in state_changes, use current time from game_state
        new_hour = current_hour
    else:
        new_hour = _to_int(new_world_time.get("hour", current_hour), current_hour)

    # CRITICAL: If current_hour > 0, it means time was advanced externally
    # Use current_hour as authoritative (it's from the actual game state)
    # This handles: GOD_MODE advances time, then LLM response doesn't update time
    if current_hour > 0:
        new_hour = max(new_hour, current_hour)

    # CRITICAL: Check if time advanced in THIS turn OR if time was already advanced externally
    # This handles cases where time was advanced via GOD_MODE or natural progression
    # before this damage attempt.
    time_advanced_in_response = new_hour > current_hour

    # Determine if we should use time-based cooldown:
    # 1. If previous cooldown was time-based (old_cd_until_hour exists), continue time-based
    # 2. If time advanced in this LLM response, use time-based
    # 3. If we're setting a NEW cooldown (cooldown not active) and current_hour > 0,
    #    it means time was advanced externally, so use time-based
    #    This handles: turn-based cooldown expired, then time advanced externally, then new damage
    use_time_based = False
    llm_set_turn_based = _to_int(new_challenge.get("cooldown_remaining", 0), 0) > 0
    if old_cd_until_hour is not None:
        # Previous cooldown was time-based, continue using time-based
        use_time_based = True
    elif time_advanced_in_response:
        # Time advanced in this LLM response, use time-based
        use_time_based = True
    elif current_hour > 0 and not cooldown_active:
        # Setting a NEW cooldown (previous one expired or didn't exist) and time has advanced externally
        # This handles:
        # - GOD_MODE time advancement after turn-based cooldown expired
        # - Natural time progression before first damage
        # - Any external time advancement when setting a new cooldown
        # CRITICAL: If time has advanced externally (current_hour > 0) and we're setting a new cooldown,
        # we MUST use time-based cooldown to prevent bypassing via "wait" actions
        use_time_based = True
        logging_util.debug(
            f"🛡️ SOCIAL_HP_GUARD: External time advancement detected (current_hour={current_hour}), "
            f"using time-based cooldown for new cooldown"
        )

    # Use new_hour for time-based cooldown calculation (may be from response or current state)
    time_advanced = use_time_based

    logging_util.warning(
        f"🛡️ SOCIAL_HP_GUARD: Cooldown trigger check - final_damage={final_damage}, "
        f"cooldown_active={cooldown_active}, use_time_based={use_time_based}, "
        f"time_advanced_in_response={time_advanced_in_response}, "
        f"current_hour={current_hour}, new_hour={new_hour}, old_cd_until_hour={old_cd_until_hour}, "
        f"old_cd_original={old_cd_original}"
    )

    if final_damage > 0 and not cooldown_active:
        # Only set cooldown if LLM didn't already set it (respect LLM's cooldown if present)
        # CRITICAL: Check if LLM set a cooldown (either turn-based OR time-based)
        llm_set_time_based = new_challenge.get("cooldown_until_hour") is not None
        llm_set_turn_based = _to_int(new_challenge.get("cooldown_remaining", 0), 0) > 0
        llm_set_cooldown = llm_set_time_based or llm_set_turn_based

        if not llm_set_cooldown:
            # LLM didn't set a cooldown, so we must set one
            # HYBRID: Use time-based if time advanced (in response or externally), turn-based otherwise
            if use_time_based:
                # Time-based: set cooldown_until_hour = max(new_hour, current_hour) + 1
                # This prevents bypassing cooldown by spamming "wait" actions
                # CRITICAL: Use max(new_hour, current_hour) to ensure cooldown is in the future
                # new_hour might be from state_changes (if LLM updated time) or current_hour (if not)
                # We want the later of the two to ensure cooldown expires correctly
                # CRITICAL: Wrap to 0-23 range to prevent invalid hour 24 at midnight
                cooldown_until = (max(new_hour, current_hour) + 1) % 24
                new_challenge["cooldown_until_hour"] = cooldown_until
                new_challenge.pop(
                    "cooldown_remaining", None
                )  # Remove turn-based if present
                logging_util.info(
                    f"🛡️ SOCIAL_HP_GUARD: Damage dealt ({final_damage}), triggering TIME-BASED cooldown "
                    f"(until hour {cooldown_until}, new_hour={new_hour}, current_hour={current_hour}, "
                    f"time_advanced_in_response={time_advanced_in_response}, use_time_based={use_time_based})"
                )
            else:
                # Time didn't advance: use turn-based cooldown
                # Set to 2 so it survives the immediate "blocked" turn and still protects for one more turn:
                # Turn N: Damage dealt, cooldown=2
                # Turn N+1: Blocked/decremented, cooldown=1
                # Turn N+2: Wait/decremented, cooldown=0
                # Turn N+3: Allowed
                new_challenge["cooldown_remaining"] = 2
                new_challenge.pop(
                    "cooldown_until_hour", None
                )  # Remove time-based if present
                logging_util.info(
                    f"🛡️ SOCIAL_HP_GUARD: Damage dealt ({final_damage}), triggering TURN-BASED cooldown "
                    f"(time didn't advance, hour={current_hour}, use_time_based={use_time_based})"
                )
        # LLM already set a cooldown
        # PRIORITY: Time-based cooldown takes precedence when game time exists
        # This ensures cooldown works correctly with natural time progression
        elif use_time_based and llm_set_turn_based and not llm_set_time_based:
            # LLM set turn-based but we should use time-based - override
            # CRITICAL: Wrap to 0-23 range to prevent invalid hour 24 at midnight
            cooldown_until = (max(new_hour, current_hour) + 1) % 24
            new_challenge["cooldown_until_hour"] = cooldown_until
            new_challenge.pop("cooldown_remaining", None)  # Remove turn-based
            logging_util.info(
                f"🛡️ SOCIAL_HP_GUARD: Overriding LLM turn-based with TIME-BASED cooldown "
                f"(until hour {cooldown_until}, current_hour={current_hour})"
            )
        elif llm_set_turn_based:
            # Turn-based: enforce minimum cooldown
            MIN_TURN_BASED_COOLDOWN = 2
            llm_cd = _to_int(new_challenge.get("cooldown_remaining", 0), 0)
            if llm_cd < MIN_TURN_BASED_COOLDOWN:
                logging_util.warning(
                    f"🛡️ SOCIAL_HP_GUARD: LLM set turn-based cooldown too low "
                    f"({llm_cd} < {MIN_TURN_BASED_COOLDOWN}), enforcing minimum"
                )
                new_challenge["cooldown_remaining"] = MIN_TURN_BASED_COOLDOWN
            logging_util.info(
                f"🛡️ SOCIAL_HP_GUARD: Using LLM turn-based cooldown "
                f"(cooldown_remaining={new_challenge.get('cooldown_remaining')})"
            )
        else:
            # LLM set time-based, respect it
            logging_util.info(
                f"🛡️ SOCIAL_HP_GUARD: Using LLM time-based cooldown "
                f"(cooldown_until_hour={new_challenge.get('cooldown_until_hour')})"
            )

    # 2b. CRITICAL: Enforce time-based cooldown ALWAYS when use_time_based=True
    # The LLM may return turn-based cooldown (cooldown_remaining) even when time-based should be used.
    # This can happen on blocked turns or non-damage turns.
    # We MUST convert to time-based to ensure consistent behavior.
    if use_time_based:
        llm_has_turn_based = (
            new_challenge.get("cooldown_remaining") is not None
            and _to_int(new_challenge.get("cooldown_remaining", 0), 0) > 0
        )
        llm_has_time_based = new_challenge.get("cooldown_until_hour") is not None
        old_has_time_based = old_cd_until_hour is not None

        # Preserve old time-based if LLM didn't set one but has active time-based cooldown
        if (
            old_has_time_based
            and not llm_has_time_based
            and current_hour < old_cd_until_hour
        ):
            new_challenge["cooldown_until_hour"] = old_cd_until_hour
            llm_has_time_based = True
            logging_util.debug(
                f"🛡️ SOCIAL_HP_GUARD: Preserving old time-based cooldown (until hour {old_cd_until_hour})"
            )

        # Convert turn-based to time-based if needed
        if llm_has_turn_based and not llm_has_time_based:
            # LLM returned turn-based when we should use time-based - convert
            # CRITICAL: Wrap to 0-23 range to prevent invalid hour 24 at midnight
            cooldown_until = (max(new_hour, current_hour) + 1) % 24
            new_challenge["cooldown_until_hour"] = cooldown_until
            new_challenge.pop("cooldown_remaining", None)
            logging_util.info(
                f"🛡️ SOCIAL_HP_GUARD: Converting LLM turn-based to time-based (until hour {cooldown_until})"
            )
        elif llm_has_time_based and llm_has_turn_based:
            # Has both - remove turn-based, keep time-based
            new_challenge.pop("cooldown_remaining", None)
            logging_util.debug(
                "🛡️ SOCIAL_HP_GUARD: Removed redundant turn-based cooldown (keeping time-based)"
            )

    # 3. Ensure HP Calculation Consistency
    # new_hp = old_hp - damage
    # We trust the cap we just applied
    calculated_hp = max(0, old_hp - damage)
    if new_challenge.get("social_hp") != calculated_hp:
        logging_util.warning(
            f"🛡️ SOCIAL_HP_GUARD: Correcting HP hallucination ({new_challenge.get('social_hp')} -> {calculated_hp})"
        )
        new_challenge["social_hp"] = calculated_hp

    # 3a. CRITICAL: Preserve key fields from old_challenge when missing in new_challenge
    # LLM may return partial social_hp_challenge missing important fields
    # These fields must be preserved for state consistency
    fields_to_preserve = [
        "social_hp_max",
        "npc_tier",
        "npc_name",
        "objective",
        "request_severity",
        "successes_needed",
        "cooldown_until_hour",
    ]
    for field in fields_to_preserve:
        if new_challenge.get(field) is None and old_challenge.get(field) is not None:
            new_challenge[field] = old_challenge[field]

    # 3b. Validate and correct social_hp_max based on npc_tier
    # LLM may hallucinate wrong max HP (e.g., commoner with max=3 instead of 1-2)
    npc_tier = new_challenge.get("npc_tier", "").lower()
    llm_social_hp_max = new_challenge.get("social_hp_max")
    if llm_social_hp_max is not None:
        llm_social_hp_max = _to_int(llm_social_hp_max, 0)

    # Tier-based max HP ranges (from game_state_instruction.md)
    tier_max_ranges = {
        "commoner": (1, 2),
        "merchant": (2, 3),
        "guard": (2, 3),
        "noble": (3, 5),
        "knight": (3, 5),
        "lord": (5, 8),
        "general": (5, 8),
        "king": (8, 12),
        "ancient": (8, 12),
        "god": (15, 20),
        "primordial": (15, 20),
    }

    max_hp = _to_int(
        new_challenge.get("social_hp_max"),
        _to_int(old_challenge.get("social_hp_max"), 0),
    )
    successes_needed = _to_int(
        new_challenge.get("successes_needed"),
        _to_int(old_challenge.get("successes_needed"), 5),
    )
    # Handle compound tiers like "god_primordial" and "king_ancient"
    min_max, max_max = tier_max_ranges.get(npc_tier, (None, None))
    if min_max is None and "_" in npc_tier:
        # Try splitting compound tier (e.g., "god_primordial" → check "god" and "primordial")
        tier_parts = npc_tier.split("_")
        for part in tier_parts:
            if part in tier_max_ranges:
                min_max, max_max = tier_max_ranges[part]
                break
    # Default to commoner range if still no match
    if min_max is None:
        min_max, max_max = (1, 2)
    if llm_social_hp_max is not None and (
        llm_social_hp_max < min_max or llm_social_hp_max > max_max
    ):
        # Correct to the nearest boundary (don't force average unless absolutely needed)
        corrected_max = max(min_max, min(max_max, llm_social_hp_max))

        logging_util.warning(
            f"🛡️ SOCIAL_HP_GUARD: Correcting social_hp_max hallucination "
            f"(tier={npc_tier}, LLM={llm_social_hp_max}, corrected={corrected_max}, "
            f"valid_range={min_max}-{max_max})"
        )
        new_challenge["social_hp_max"] = corrected_max
        # Also update social_hp if it exceeds the corrected max
        if new_challenge.get("social_hp", 0) > corrected_max:
            logging_util.warning(
                f"🛡️ SOCIAL_HP_GUARD: Correcting social_hp to match corrected max "
                f"({new_challenge.get('social_hp')} -> {corrected_max})"
            )
            new_challenge["social_hp"] = corrected_max

    # 5. Ensure resistance_shown is present (REQUIRED field for Social HP challenges)
    # If missing, add a default based on status
    if (
        not new_challenge.get("resistance_shown")
        or not new_challenge.get("resistance_shown", "").strip()
    ):
        status = new_challenge.get("status", "RESISTING")
        npc_name = new_challenge.get("npc_name", "the NPC")
        if status == "RESISTING":
            new_challenge["resistance_shown"] = (
                f"{npc_name} shows resistance to your request."
            )
        elif status == "WAVERING":
            new_challenge["resistance_shown"] = (
                f"{npc_name} is considering your request but remains hesitant."
            )
        elif status == "YIELDING":
            new_challenge["resistance_shown"] = (
                f"{npc_name} is beginning to yield to your request."
            )
        elif status == "SURRENDERED":
            new_challenge["resistance_shown"] = (
                f"{npc_name} has surrendered to your request."
            )
        else:
            new_challenge["resistance_shown"] = f"{npc_name} responds to your request."
        logging_util.warning(
            f"🛡️ SOCIAL_HP_GUARD: Added default resistance_shown (status={status}, npc={npc_name})"
        )

    # CRITICAL DEBUG: Log final state_changes to verify it's being modified
    logging_util.info(
        f"🛡️ SOCIAL_HP_GUARD: Final state_changes['social_hp_challenge'] - "
        f"social_hp={new_challenge.get('social_hp')}, "
        f"social_hp_damage={new_challenge.get('social_hp_damage')}, "
        f"cooldown_remaining={new_challenge.get('cooldown_remaining')}, "
        f"cooldown_until_hour={new_challenge.get('cooldown_until_hour')}, "
        f"social_hp_max={new_challenge.get('social_hp_max')}, "
        f"npc_tier={new_challenge.get('npc_tier')}, "
        f"resistance_shown={new_challenge.get('resistance_shown', 'MISSING')[:50]}"
    )

    # 4. Successes calculation (formula from prompt)
    # successes = social_hp_max - social_hp
    max_hp = _to_int(
        new_challenge.get("social_hp_max"),
        _to_int(old_challenge.get("social_hp_max"), 0),
    )
    if max_hp > 0:
        # Read successes_needed from challenge state (not hardcoded)
        successes_needed = _to_int(
            new_challenge.get("successes_needed"),
            _to_int(old_challenge.get("successes_needed"), 5),
        )
        # Guard against negative values when HP > max_hp (hallucination correction)
        new_challenge["successes"] = min(
            successes_needed, max(0, max_hp - calculated_hp)
        )
