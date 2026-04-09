"""
Defines the GameState class, which represents the complete state of a campaign.

Includes:
- D&D 5E mechanics integration for deterministic game logic (dice rolls in mvp_site.dice)
- XP/Level validation using D&D 5e XP thresholds
- Time monotonicity checks to prevent time regression
- Helper functions for XP→Level calculations

The LLM should focus on narrative while code handles all mathematical operations.
"""

from __future__ import annotations

import copy
import datetime
import hashlib
import json
import re
from datetime import UTC
from datetime import datetime as dt
from typing import Any, Literal, overload

from mvp_site import constants, living_world, logging_util, world_time
from mvp_site import dice as dice_module
from mvp_site.campaign_divine import (
    get_campaign_tier as _get_campaign_tier,
    get_highest_stat_modifier as _get_highest_stat_modifier,
    get_pending_upgrade_type as _get_pending_upgrade_type,
    is_campaign_upgrade_available as _is_campaign_upgrade_available,
    is_divine_upgrade_available as _is_divine_upgrade_available,
    is_multiverse_upgrade_available as _is_multiverse_upgrade_available,
)
from mvp_site.dice import DiceRollResult, execute_dice_tool
from mvp_site.faction.tools import FACTION_TOOL_NAMES, execute_faction_tool
from mvp_site.numeric_converters import coerce_int_safe as _coerce_int
from mvp_site.schemas import GameStateModel
from mvp_site.schemas.validation import (
    get_player_character_schema_keys,
    get_social_hp_request_severity_values,
    get_social_hp_skill_values,
    validate_game_state,
)

# Schema migration gating for legacy campaign compatibility.
# Legacy campaigns are migrated once, then strict validation is enforced.
SCHEMA_MIGRATION_VERSION = 1
SCHEMA_MIGRATION_VERSION_FIELD = "schema_migration_version"
SCHEMA_MIGRATED_AT_FIELD = "schema_migrated_at"


def _legacy_session_id_seed(state_dict: dict[str, Any]) -> str:
    """Create a stable seed for legacy migration session IDs.

    The seed is based on key identity-ish fields if present, with a stable
    fallback to a canonicalized payload hash when those identifiers are absent.
    """
    if not isinstance(state_dict, dict):
        return hashlib.sha1(b"invalid-state").hexdigest()[:12]

    # Prefer explicit identifiers when available; these are expected for migrated
    # campaign state loaded from Firestore, which gives us strong uniqueness.
    explicit = state_dict.get("campaign_id") or state_dict.get("user_id")
    if isinstance(explicit, str) and explicit.strip():
        return hashlib.sha1(explicit.strip().encode()).hexdigest()[:12]

    # Fallback to deterministic payload hash for compatibility-only states.
    payload = {
        "world_data": state_dict.get("world_data"),
        "player_character_data": state_dict.get("player_character_data"),
        "combat_state": state_dict.get("combat_state"),
        "narrative": state_dict.get("narrative"),
    }
    return hashlib.sha1(
        json.dumps(payload, sort_keys=True, default=str).encode()
    ).hexdigest()[:12]


def _build_migrated_session_id(
    state_dict: dict[str, Any],
    *,
    migration_seed: str | None = None,
) -> str:
    """Build a per-campaign session id when a legacy state is missing one."""
    if migration_seed:
        seed = migration_seed
    else:
        seed = f"{_legacy_session_id_seed(state_dict)}:{dt.now(UTC).isoformat()}"

    seed_hash = hashlib.sha1(seed.encode()).hexdigest()[:16]
    return f"legacy-migrated-{seed_hash}"

# =============================================================================
# D&D 5e XP THRESHOLDS
# =============================================================================
# Cumulative XP required to reach each level (1-20)
# Source: D&D 5e Player's Handbook / SRD
# =============================================================================

XP_THRESHOLDS = [
    0,  # Level 1
    300,  # Level 2
    900,  # Level 3
    2700,  # Level 4
    6500,  # Level 5
    14000,  # Level 6
    23000,  # Level 7
    34000,  # Level 8
    48000,  # Level 9
    64000,  # Level 10
    85000,  # Level 11
    100000,  # Level 12
    120000,  # Level 13
    140000,  # Level 14
    165000,  # Level 15
    195000,  # Level 16
    225000,  # Level 17
    265000,  # Level 18
    305000,  # Level 19
    355000,  # Level 20
]

XP_BY_CR = {
    0: 10,
    0.125: 25,
    0.25: 50,
    0.5: 100,
    1: 200,
    2: 450,
    3: 700,
    4: 1100,
    5: 1800,
    6: 2300,
    7: 2900,
    8: 3900,
    9: 5000,
    10: 5900,
    11: 7200,
    12: 8400,
    13: 10000,
    14: 11500,
    15: 13000,
    16: 15000,
    17: 18000,
    18: 20000,
    19: 22000,
    20: 25000,
    21: 33000,
    22: 41000,
    23: 50000,
    24: 62000,
    25: 75000,
    26: 90000,
    27: 105000,
    28: 120000,
    29: 135000,
    30: 155000,
}

PROFICIENCY_BY_LEVEL = {
    1: 2,
    2: 2,
    3: 2,
    4: 2,
    5: 3,
    6: 3,
    7: 3,
    8: 3,
    9: 4,
    10: 4,
    11: 4,
    12: 4,
    13: 5,
    14: 5,
    15: 5,
    16: 5,
    17: 6,
    18: 6,
    19: 6,
    20: 6,
}


def coerce_int(value: Any, default: int | None = 0) -> int | None:
    """Public wrapper around :func:`_coerce_int` for safe int coercion."""

    return _coerce_int(value, default)


def _extract_int_like(value: Any) -> int | None:
    """Best-effort int extraction for legacy state fields (gold, counters, etc.)."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        s = value.strip().lower()
        if not s:
            return None
        # Common currency strings: "50", "50gp", "50 gp", "1,000 gp", "12 345 gold".
        # Preserve sign when present and strip common thousands separators.
        match = re.search(r"(?<!\w)([+-]?\d[\d,\s_]*)", s)
        if match is None:
            return None
        token = re.sub(r"[\s,_]", "", match.group(1))
        if token in {"", "+", "-"}:
            return None
        try:
            return int(token)
        except ValueError:
            return None
    return None


def _canonicalize_player_gold_in_place(
    player_character_data: dict[str, Any],
    *,
    corrections_out: list[str] | None = None,
) -> None:
    """Normalize legacy/misplaced gold into the canonical location.

    Canonical: player_character_data.resources.gold
    Legacy (read): player_character_data.gold, player_character_data.equipment.money
    Misplacement (write): player_character_data.equipment.backpack[].stats.gold

    New-first: if canonical exists, it wins; only backfill when canonical is missing.
    """
    if not isinstance(player_character_data, dict):
        return

    resources_obj = player_character_data.get("resources")
    resources: dict[str, Any] | None = resources_obj if isinstance(resources_obj, dict) else None

    if resources is not None:
        canonical_gold = _extract_int_like(resources.get("gold"))
        if canonical_gold is not None and canonical_gold >= 0:
            # Keep canonical authoritative; remove legacy flat field if present (schema compliance).
            player_character_data.pop("gold", None)
            return

    legacy_flat = _extract_int_like(player_character_data.get("gold"))
    if legacy_flat is not None and legacy_flat >= 0:
        if resources is None:
            resources = {}
            player_character_data["resources"] = resources
        resources["gold"] = legacy_flat
        player_character_data.pop("gold", None)
        if corrections_out is not None:
            corrections_out.append(
                "Normalized legacy player_character_data.gold into player_character_data.resources.gold"
            )
        return

    equipment = player_character_data.get("equipment")
    if isinstance(equipment, dict):
        money_str = equipment.get("money")
        parsed = _extract_int_like(money_str)
        if parsed is not None and parsed >= 0:
            if resources is None:
                resources = {}
                player_character_data["resources"] = resources
            resources["gold"] = parsed
            equipment.pop("money", None)
            if corrections_out is not None:
                corrections_out.append(
                    "Normalized legacy player_character_data.equipment.money into player_character_data.resources.gold"
                )
            return

        backpack = equipment.get("backpack")
        if isinstance(backpack, list):
            for idx, item in enumerate(backpack):
                if not isinstance(item, dict):
                    continue
                stats = item.get("stats")
                if not isinstance(stats, dict):
                    continue
                misplaced = _extract_int_like(stats.get("gold"))
                if misplaced is None or misplaced < 0:
                    continue
                if resources is None:
                    resources = {}
                    player_character_data["resources"] = resources
                resources["gold"] = misplaced
                stats.pop("gold", None)
                if corrections_out is not None:
                    corrections_out.append(
                        f"Moved misplaced equipment.backpack[{idx}].stats.gold into player_character_data.resources.gold"
                    )
                return


def _canonicalize_player_gold_state_update_in_place(
    player_character_data: dict[str, Any],
    *,
    corrections_out: list[str] | None = None,
) -> None:
    """Canonicalize gold *updates* into the canonical location.

    This differs from :func:`_canonicalize_player_gold_in_place`:
    - For state_updates coming from an LLM, legacy/misplaced fields are treated as
      authoritative *writes* (not just read fallbacks).
    - If a non-canonical write is present (e.g., equipment.backpack[].stats.gold),
      we MUST move it into resources.gold even if resources.gold already exists.
    """
    if not isinstance(player_character_data, dict):
        return

    resources_obj = player_character_data.get("resources")
    resources: dict[str, Any] | None = resources_obj if isinstance(resources_obj, dict) else None

    # Prefer explicit canonical update if present.
    canonical_update = None
    if resources is not None:
        canonical_update = _extract_int_like(resources.get("gold"))

    # Extract update candidates from legacy/misplaced locations.
    legacy_flat = _extract_int_like(player_character_data.get("gold"))

    money_parsed = None
    backpack_misplaced = None
    backpack_misplaced_idx: int | None = None

    equipment = player_character_data.get("equipment")
    if isinstance(equipment, dict):
        money_parsed = _extract_int_like(equipment.get("money"))
        backpack = equipment.get("backpack")
        if isinstance(backpack, list):
            for idx, item in enumerate(backpack):
                if not isinstance(item, dict):
                    continue
                stats = item.get("stats")
                if not isinstance(stats, dict):
                    continue
                maybe_gold = _extract_int_like(stats.get("gold"))
                if maybe_gold is None or maybe_gold < 0:
                    continue
                backpack_misplaced = maybe_gold
                backpack_misplaced_idx = idx
                break

    # Decide the authoritative update value.
    # For state_updates, non-canonical writes are authoritative and should override
    # any existing canonical value when both are present.
    update_gold = None
    source = None
    if legacy_flat is not None and legacy_flat >= 0:
        update_gold = legacy_flat
        source = "player_character_data.gold"
    elif money_parsed is not None and money_parsed >= 0:
        update_gold = money_parsed
        source = "player_character_data.equipment.money"
    elif backpack_misplaced is not None and backpack_misplaced >= 0:
        update_gold = backpack_misplaced
        source = (
            f"player_character_data.equipment.backpack[{backpack_misplaced_idx}].stats.gold"
        )
    elif canonical_update is not None and canonical_update >= 0:
        update_gold = canonical_update
        source = "player_character_data.resources.gold"

    # If no relevant update is present, nothing to do.
    if update_gold is None:
        return

    if resources is None:
        resources = {}
        player_character_data["resources"] = resources
    resources["gold"] = update_gold

    # Always remove misplaced backpack stats.gold if present (even when canonical update was used).
    if backpack_misplaced_idx is not None and isinstance(equipment, dict):
        backpack = equipment.get("backpack")
        if isinstance(backpack, list) and backpack_misplaced_idx < len(backpack):
            item = backpack[backpack_misplaced_idx]
            if isinstance(item, dict):
                stats = item.get("stats")
                if isinstance(stats, dict):
                    stats.pop("gold", None)

    if corrections_out is not None and source is not None:
        corrections_out.append(
            f"Canonicalized gold update from {source} into player_character_data.resources.gold"
        )


_VALID_SOCIAL_REQUEST_SEVERITY = (
    get_social_hp_request_severity_values()
    or {"information", "favor", "submission"}
)
_VALID_SOCIAL_SKILLS = get_social_hp_skill_values() or {
    "Persuasion",
    "Deception",
    "Intimidation",
    "Insight",
}


def _now_iso_utc() -> str:
    return dt.now(UTC).isoformat()


def _is_rfc3339_datetime(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        dt.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except (ValueError, TypeError):
        return False


def _canonicalize_social_hp_challenge_in_place(
    social_hp_challenge: Any,
    *,
    corrections_out: list[str] | None = None,
) -> None:
    if not isinstance(social_hp_challenge, dict):
        return

    severity_raw = social_hp_challenge.get("request_severity")
    severity = str(severity_raw).strip().lower() if severity_raw is not None else ""
    severity_map = {
        "standard": "information",
        "normal": "information",
        "minor": "information",
        "request": "favor",
        "ask": "favor",
        "aid": "favor",
        "assistance": "favor",
        "demand": "submission",
        "command": "submission",
        "threat": "submission",
        "coercion": "submission",
    }
    normalized_severity = severity_map.get(severity, severity)
    if normalized_severity not in _VALID_SOCIAL_REQUEST_SEVERITY:
        normalized_severity = "information"
    if severity_raw != normalized_severity:
        social_hp_challenge["request_severity"] = normalized_severity
        if corrections_out is not None:
            corrections_out.append(
                "Normalized social_hp_challenge.request_severity to schema enum"
            )

    skill_raw = social_hp_challenge.get("skill_used")
    skill_text = str(skill_raw).strip() if skill_raw is not None else ""
    normalized_skill = None
    if skill_text:
        skill_tokens = re.split(r"[/|,;]+", skill_text)
        direct_map = {
            "persuasion": "Persuasion",
            "deception": "Deception",
            "intimidation": "Intimidation",
            "insight": "Insight",
        }
        synonym_map = {
            "investigation": "Insight",
        }
        for token in skill_tokens:
            candidate = direct_map.get(token.strip().lower())
            if candidate in _VALID_SOCIAL_SKILLS:
                normalized_skill = candidate
                break
        if normalized_skill is None:
            for token in skill_tokens:
                candidate = synonym_map.get(token.strip().lower())
                if candidate in _VALID_SOCIAL_SKILLS:
                    normalized_skill = candidate
                    break
        if normalized_skill is None:
            for candidate in _VALID_SOCIAL_SKILLS:
                if candidate.lower() in skill_text.lower():
                    normalized_skill = candidate
                    break
        if normalized_skill is None:
            titled = skill_text.title()
            if titled in _VALID_SOCIAL_SKILLS:
                normalized_skill = titled
    if normalized_skill is None:
        for candidate in _VALID_SOCIAL_SKILLS:
            if candidate.lower() in skill_text.lower():
                normalized_skill = candidate
                break
    if normalized_skill is None:
        normalized_skill = "Persuasion"

    if skill_raw != normalized_skill:
        social_hp_challenge["skill_used"] = normalized_skill
        if corrections_out is not None:
            corrections_out.append("Normalized social_hp_challenge.skill_used to schema enum")


def _normalize_player_inventory_equipment_in_place(
    player_character_data: dict[str, Any],
    *,
    corrections_out: list[str] | None = None,
) -> None:
    inventory = player_character_data.get("inventory")
    if isinstance(inventory, dict):
        normalized_inventory: list[dict[str, Any]] = []
        for key, value in inventory.items():
            if isinstance(value, dict):
                item = dict(value)
                item.setdefault("id", str(key))
                normalized_inventory.append(item)
            elif isinstance(value, str):
                normalized_inventory.append({"id": str(key), "name": value})
        player_character_data["inventory"] = normalized_inventory
        if corrections_out is not None:
            corrections_out.append("Normalized player_character_data.inventory dict into list")
    elif isinstance(inventory, list):
        normalized_inventory = []
        changed = False
        for item in inventory:
            if isinstance(item, dict):
                normalized_inventory.append(item)
            elif isinstance(item, str):
                normalized_inventory.append({"name": item})
                changed = True
            else:
                changed = True
        if changed:
            player_character_data["inventory"] = normalized_inventory
            if corrections_out is not None:
                corrections_out.append(
                    "Normalized player_character_data.inventory entries into object list"
                )

    equipment = player_character_data.get("equipment")
    if isinstance(equipment, list):
        player_character_data["equipment"] = {"backpack": equipment}
        if corrections_out is not None:
            corrections_out.append("Normalized player_character_data.equipment list into backpack object")
        equipment = player_character_data["equipment"]
    elif equipment is None:
        player_character_data["equipment"] = {}
        equipment = player_character_data["equipment"]

    if isinstance(equipment, dict):
        backpack = equipment.get("backpack")
        if backpack is None:
            return
        if isinstance(backpack, dict):
            normalized_backpack: list[dict[str, Any]] = []
            for key, value in backpack.items():
                if isinstance(value, dict):
                    item = dict(value)
                    item.setdefault("id", str(key))
                    normalized_backpack.append(item)
                elif isinstance(value, str):
                    normalized_backpack.append({"id": str(key), "name": value})
            equipment["backpack"] = normalized_backpack
            if corrections_out is not None:
                corrections_out.append(
                    "Normalized player_character_data.equipment.backpack dict into list"
                )
        elif isinstance(backpack, list):
            normalized_backpack = []
            changed = False
            for item in backpack:
                if isinstance(item, dict):
                    normalized_backpack.append(item)
                elif isinstance(item, str):
                    normalized_backpack.append({"name": item})
                    changed = True
                else:
                    changed = True
            if changed:
                equipment["backpack"] = normalized_backpack
                if corrections_out is not None:
                    corrections_out.append(
                        "Normalized player_character_data.equipment.backpack entries into object list"
                    )


def _canonicalize_player_health_aliases_in_place(
    player_character_data: dict[str, Any],
    *,
    corrections_out: list[str] | None = None,
) -> None:
    """Mirror common health aliases into canonical player_character_data fields."""
    health = player_character_data.get("health")
    if not isinstance(health, dict):
        return

    health_death_saves = health.get("death_saves")
    if "death_saves" not in player_character_data and isinstance(health_death_saves, dict):
        player_character_data["death_saves"] = copy.deepcopy(health_death_saves)
        if corrections_out is not None:
            corrections_out.append(
                "Mirrored player_character_data.health.death_saves to player_character_data.death_saves"
            )

    health_conditions = health.get("conditions")
    if "status_conditions" not in player_character_data and isinstance(
        health_conditions, list
    ):
        player_character_data["status_conditions"] = list(health_conditions)
        if corrections_out is not None:
            corrections_out.append(
                "Mirrored player_character_data.health.conditions to player_character_data.status_conditions"
            )


_PLAYER_CHARACTER_SCHEMA_KEYS = get_player_character_schema_keys()


def _move_non_schema_player_character_fields_in_place(
    player_character_data: dict[str, Any],
    *,
    custom_campaign_state: dict[str, Any] | None = None,
    corrections_out: list[str] | None = None,
) -> None:
    """Move unknown player_character_data fields into custom_campaign_state extras."""
    if not isinstance(player_character_data, dict) or not isinstance(custom_campaign_state, dict):
        return

    extra_keys = [
        key for key in list(player_character_data.keys())
        if key not in _PLAYER_CHARACTER_SCHEMA_KEYS
    ]
    if not extra_keys:
        return

    extras_raw = custom_campaign_state.get("player_character_data_extras")
    extras = extras_raw if isinstance(extras_raw, dict) else {}

    moved_keys: list[str] = []
    for key in extra_keys:
        extras[key] = player_character_data.pop(key)
        moved_keys.append(key)

    custom_campaign_state["player_character_data_extras"] = extras
    if corrections_out is not None and moved_keys:
        corrections_out.append(
            "Moved non-schema player_character_data fields into "
            "custom_campaign_state.player_character_data_extras: "
            + ", ".join(sorted(moved_keys))
        )


def _canonicalize_player_character_data_in_place(
    player_character_data: Any,
    *,
    custom_campaign_state: dict[str, Any] | None = None,
    corrections_out: list[str] | None = None,
) -> None:
    if not isinstance(player_character_data, dict):
        return

    # Normalize nested shape drift observed in production payloads.
    _normalize_player_inventory_equipment_in_place(
        player_character_data, corrections_out=corrections_out
    )
    _canonicalize_player_gold_in_place(player_character_data, corrections_out=corrections_out)
    _canonicalize_player_health_aliases_in_place(
        player_character_data, corrections_out=corrections_out
    )
    _move_non_schema_player_character_fields_in_place(
        player_character_data,
        custom_campaign_state=custom_campaign_state,
        corrections_out=corrections_out,
    )


def _canonicalize_god_mode_directives_in_place(
    custom_campaign_state: Any,
    *,
    corrections_out: list[str] | None = None,
) -> None:
    if not isinstance(custom_campaign_state, dict):
        return
    directives = custom_campaign_state.get("god_mode_directives")
    if directives is None:
        return

    if isinstance(directives, dict):
        directives = list(directives.values())
    elif not isinstance(directives, list):
        directives = []

    normalized: list[dict[str, Any]] = []
    for item in directives:
        if isinstance(item, str):
            if item.strip():
                normalized.append({"rule": item.strip(), "added": _now_iso_utc()})
            continue
        if isinstance(item, dict):
            rule = item.get("rule")
            if not isinstance(rule, str) or not rule.strip():
                continue
            normalized_item = dict(item)
            normalized_item["rule"] = rule.strip()
            added = normalized_item.get("added")
            if added is not None and not _is_rfc3339_datetime(added):
                normalized_item["added_lore"] = str(added)
                normalized_item["added"] = _now_iso_utc()
            normalized.append(normalized_item)

    if custom_campaign_state.get("god_mode_directives") != normalized:
        custom_campaign_state["god_mode_directives"] = normalized
        if corrections_out is not None:
            corrections_out.append("Normalized custom_campaign_state.god_mode_directives to object list")


def _canonicalize_arc_milestones_in_place(
    custom_campaign_state: Any,
    *,
    corrections_out: list[str] | None = None,
) -> None:
    if not isinstance(custom_campaign_state, dict):
        return
    milestones = custom_campaign_state.get("arc_milestones")
    if not isinstance(milestones, dict):
        return

    changed = False
    for milestone_key, milestone_value in list(milestones.items()):
        if not isinstance(milestone_value, dict):
            milestones[milestone_key] = {"status": "in_progress"}
            changed = True
            continue
        updated_at = milestone_value.get("updated_at")
        if updated_at is not None and not _is_rfc3339_datetime(updated_at):
            milestone_value["updated_at_lore"] = str(updated_at)
            milestone_value["updated_at"] = _now_iso_utc()
            changed = True
        completed_at = milestone_value.get("completed_at")
        if completed_at is not None and not _is_rfc3339_datetime(completed_at):
            milestone_value["completed_at_lore"] = str(completed_at)
            milestone_value["completed_at"] = _now_iso_utc()
            changed = True

    if changed and corrections_out is not None:
        corrections_out.append(
            "Normalized custom_campaign_state.arc_milestones timestamp fields to RFC3339"
        )


def canonicalize_state_updates_in_place(
    state_updates: dict[str, Any],
) -> list[str]:
    """Canonicalize common legacy/misplaced fields inside an LLM state_updates dict.

    Returns a list of human-readable corrections applied.
    """
    corrections: list[str] = []
    if not isinstance(state_updates, dict):
        return corrections
    pc = state_updates.get("player_character_data")
    if isinstance(pc, dict):
        _canonicalize_player_character_data_in_place(pc, corrections_out=corrections)
        _canonicalize_player_gold_state_update_in_place(pc, corrections_out=corrections)
    shp = state_updates.get("social_hp_challenge")
    if isinstance(shp, dict):
        _canonicalize_social_hp_challenge_in_place(shp, corrections_out=corrections)
    custom_state = state_updates.get("custom_campaign_state")
    if isinstance(custom_state, dict):
        _canonicalize_god_mode_directives_in_place(
            custom_state, corrections_out=corrections
        )
        _canonicalize_arc_milestones_in_place(custom_state, corrections_out=corrections)
    return corrections


def level_from_xp(xp: int) -> int:
    """
    Calculate character level from cumulative XP using D&D 5e thresholds.

    Args:
        xp: Current cumulative experience points (clamped to 0 if negative).
            Accepts int, str, or float - coerced to int.

    Returns:
        Character level (1-20)

    Examples:
        >>> level_from_xp(0)
        1
        >>> level_from_xp(300)
        2
        >>> level_from_xp(5000)
        4
        >>> level_from_xp(500000)
        20
        >>> level_from_xp("5000")  # String input from JSON
        4
    """
    # Coerce to int for type safety (handles strings from JSON/LLM)
    xp = _coerce_int(xp, 0)
    # Clamp negative XP to 0
    xp = max(0, xp)

    # Find the highest level threshold that XP meets or exceeds
    level = 1
    for i, threshold in enumerate(XP_THRESHOLDS):
        if xp >= threshold:
            level = i + 1
        else:
            break

    return level


def xp_needed_for_level(level: int) -> int:
    """
    Get the cumulative XP required to reach a specific level.

    Args:
        level: Target level (clamped to 1-20 range).
               Accepts int, str, or float - coerced to int.

    Returns:
        Cumulative XP required for that level

    Examples:
        >>> xp_needed_for_level(1)
        0
        >>> xp_needed_for_level(5)
        6500
        >>> xp_needed_for_level(20)
        355000
        >>> xp_needed_for_level("5")  # String input from JSON
        6500
    """
    # Coerce to int for type safety
    level = _coerce_int(level, 1)
    # Clamp level to valid range
    level = max(1, min(20, level))
    return XP_THRESHOLDS[level - 1]


def xp_to_next_level(current_xp: int, current_level: int = None) -> int:
    """
    Calculate XP remaining to reach the next level.

    Args:
        current_xp: Current cumulative XP.
                    Accepts int, str, or float - coerced to int.
        current_level: Optional current level to optimize calculation.

    Returns:
        XP needed to reach next level (0 if at max level 20)

    Examples:
        >>> xp_to_next_level(0)
        300
        >>> xp_to_next_level(150)
        150
        >>> xp_to_next_level(355000)
        0
        >>> xp_to_next_level("150")  # String input from JSON
        150
    """
    # Coerce to int for type safety
    current_xp = _coerce_int(current_xp, 0)
    current_xp = max(0, current_xp)

    if current_level is None:
        current_level = level_from_xp(current_xp)
    else:
        current_level = _coerce_int(current_level, level_from_xp(current_xp))
        current_level = max(1, min(20, current_level))

    # At max level, no more XP needed
    if current_level >= 20:
        return 0

    next_threshold = XP_THRESHOLDS[
        current_level
    ]  # Index is level since we need level+1
    return next_threshold - current_xp


class GameState:
    """
    A class to hold and manage game state data, behaving like a flexible dictionary.
    """

    # NOTE: check_living_world_trigger is defined later in this file (around line 739).
    # The second definition is the canonical one used by all callers.
    # This comment placeholder prevents duplicate method definition confusion.

    def update_living_world_tracking(
        self, turn_number: int, current_time: dict[str, Any] | None
    ) -> None:
        """
        Update tracking for living world events.

        Updates last_living_world_turn and last_living_world_time.

        Args:
            turn_number: The turn number the event occurred on
            current_time: The world_time dict at that turn (if any)
        """
        self.last_living_world_turn = turn_number

        if isinstance(current_time, dict):
            self.last_living_world_time = copy.deepcopy(current_time)
        elif current_time is None:
            # Clear invalid/missing time to force a baseline reset on next valid turn.
            # This prevents stale triggers (e.g. comparing Turn X+1 time vs Turn X-10 time).
            # (PR #3897 review fix)
            self.last_living_world_time = None
        else:
            logging_util.warning(
                "GameState: ignoring invalid current_time in update_living_world_tracking (raw=%r)",
                current_time,
            )
            self.last_living_world_time = None

    def __init__(self, **kwargs: Any) -> None:
        """Initializes the GameState object with arbitrary data."""
        # Set default values for core attributes if they are not provided
        self.game_state_version = kwargs.get("game_state_version", 1)
        self.player_character_data = kwargs.get("player_character_data", {})

        # Ensure experience.current is initialized (required by schema and invariant checks)
        # Defensive initialization: ONLY add experience to empty player_character_data
        # Preserve scalar experience format if already present (don't force conversion)
        if isinstance(self.player_character_data, dict):
            exp = self.player_character_data.get("experience")
            if isinstance(exp, dict) and "current" not in exp:
                # If experience dict exists but missing current, add it
                exp["current"] = 0
            elif exp is None and not self.player_character_data:
                # ONLY add experience if player_character_data is completely empty
                self.player_character_data["experience"] = {"current": 0}
            # Note: scalar experience values are preserved as-is (not converted to dict)

        self.world_data = kwargs.get("world_data", {})
        self.npc_data = kwargs.get("npc_data", {})
        self.user_settings = kwargs.get("user_settings")
        # Item registry: maps item_id (string) → item definition (dict)
        # Example item: helm_telepathy → name "Helm of Telepathy", type "head", stats "30ft telepathy"
        self.item_registry = kwargs.get("item_registry", {})
        self.custom_campaign_state = kwargs.get("custom_campaign_state", {})
        if not isinstance(self.custom_campaign_state, dict):
            self.custom_campaign_state = {}

        if isinstance(self.player_character_data, dict):
            _canonicalize_player_gold_in_place(self.player_character_data)

        _canonicalize_social_hp_challenge_in_place(self.__dict__.get("social_hp_challenge"))
        _canonicalize_god_mode_directives_in_place(self.custom_campaign_state)
        _canonicalize_arc_milestones_in_place(self.custom_campaign_state)

        # Ensure arc_milestones is initialized for tracking narrative arc completion
        # Handle both missing key AND null value from Firestore
        if "arc_milestones" not in self.custom_campaign_state or not isinstance(
            self.custom_campaign_state.get("arc_milestones"), dict
        ):
            self.custom_campaign_state["arc_milestones"] = {}

        # Ensure companion_arcs is initialized for tracking companion personal quest arcs
        # LLM manages arcs via state_updates; we just ensure the dict exists
        if "companion_arcs" not in self.custom_campaign_state or not isinstance(
            self.custom_campaign_state.get("companion_arcs"), dict
        ):
            self.custom_campaign_state["companion_arcs"] = {}

        # Track cadence for companion arc events to align with prompt expectations.
        # Handle both missing key AND null/invalid value from Firestore.
        # Follow same pattern as arc_milestones/active_constraints for consistency.
        raw_next_companion_arc_turn = self.custom_campaign_state.get(
            "next_companion_arc_turn"
        )
        if (
            "next_companion_arc_turn" not in self.custom_campaign_state
            or not isinstance(raw_next_companion_arc_turn, int)
            or isinstance(raw_next_companion_arc_turn, bool)
        ):
            self.custom_campaign_state["next_companion_arc_turn"] = _coerce_int(
                raw_next_companion_arc_turn, constants.COMPANION_ARC_INITIAL_TURN
            )

        # Ensure active_constraints exists for tracking secrecy/deception rules
        # (player OOC constraints such as "don't reveal X to Y") and remains
        # list-typed for prompt rules that append entries.
        if "active_constraints" not in self.custom_campaign_state or not isinstance(
            self.custom_campaign_state.get("active_constraints"), list
        ):
            self.custom_campaign_state["active_constraints"] = []

        # Ensure attribute_system is set (defaults to Destiny system)
        if "attribute_system" not in self.custom_campaign_state:
            self.custom_campaign_state["attribute_system"] = (
                constants.DEFAULT_ATTRIBUTE_SYSTEM
            )

        # Campaign tier progression (mortal → divine → sovereign)
        # Normalize campaign_tier: validate against allowed tiers and default on invalid values
        # Firestore can store null or invalid values, which would break get_campaign_tier()
        allowed_tiers = {
            constants.CAMPAIGN_TIER_MORTAL,
            constants.CAMPAIGN_TIER_DIVINE,
            constants.CAMPAIGN_TIER_SOVEREIGN,
        }
        campaign_tier = self.custom_campaign_state.get("campaign_tier")
        if campaign_tier not in allowed_tiers:
            self.custom_campaign_state["campaign_tier"] = constants.CAMPAIGN_TIER_MORTAL

        # Divine/multiverse progression tracking
        if "divine_potential" not in self.custom_campaign_state:
            self.custom_campaign_state["divine_potential"] = 0
        if "universe_control" not in self.custom_campaign_state:
            self.custom_campaign_state["universe_control"] = 0
        if "divine_upgrade_available" not in self.custom_campaign_state:
            self.custom_campaign_state["divine_upgrade_available"] = False
        if "multiverse_upgrade_available" not in self.custom_campaign_state:
            self.custom_campaign_state["multiverse_upgrade_available"] = False

        self.combat_state = kwargs.get("combat_state", {"in_combat": False})
        # Normalize combat_state to handle LLM-generated malformed data
        self._normalize_combat_state()
        self.last_state_update_timestamp = kwargs.get(
            "last_state_update_timestamp", datetime.datetime.now(datetime.UTC)
        )

        def _coerce_and_log(field_name: str, raw_value: Any, default: int = 0) -> int:
            coerced = _coerce_int(raw_value, default)
            if raw_value is not None and (
                isinstance(raw_value, bool) or not isinstance(raw_value, int)
            ):
                logging_util.warning(
                    "GameState: coercing %s to int (raw=%r, coerced=%r)",
                    field_name,
                    raw_value,
                    coerced,
                )
            return coerced

        # Canonical turn counter (1-indexed, excludes GOD/THINK mode commands).
        # Both turn_number and player_turn are persisted for compatibility.
        raw_turn_number = kwargs.get("turn_number")
        raw_player_turn = kwargs.get("player_turn")
        current_turn_number = _coerce_and_log(
            "turn_number", raw_turn_number, default=0
        )
        current_player_turn = _coerce_and_log(
            "player_turn", raw_player_turn, default=0
        )
        canonical_turn = max(current_turn_number, current_player_turn, 0)
        if (
            raw_turn_number is not None
            and raw_player_turn is not None
            and current_turn_number != current_player_turn
        ):
            logging_util.warning(
                "GameState: turn counter mismatch (turn_number=%s, player_turn=%s); "
                "using canonical=%s",
                current_turn_number,
                current_player_turn,
                canonical_turn,
            )
        self.turn_number = canonical_turn
        self.player_turn = canonical_turn

        # Living World Tracking
        # Tracks when the last background event generation occurred
        # Persisted in Firestore to maintain cadence across sessions
        raw_last_living_world_turn = kwargs.get("last_living_world_turn")
        has_last_living_world_turn = raw_last_living_world_turn is not None
        self.last_living_world_turn = _coerce_and_log(
            "last_living_world_turn", raw_last_living_world_turn
        )
        if not has_last_living_world_turn and isinstance(
            kwargs.get("living_world_state"), dict
        ):
            legacy_living_world_state = kwargs.get("living_world_state", {})
            self.last_living_world_turn = _coerce_and_log(
                "living_world_state.last_turn",
                legacy_living_world_state.get(
                    "last_turn",
                    legacy_living_world_state.get("last_living_world_turn", 0),
                ),
            )

        if self.last_living_world_turn < 0:
            self.last_living_world_turn = 0
        elif self.player_turn > 0 and self.last_living_world_turn > self.player_turn:
            recovered_turn = self.player_turn - (
                self.player_turn % constants.LIVING_WORLD_TURN_INTERVAL
            )
            if recovered_turn == self.player_turn and self.player_turn > 0:
                recovered_turn = max(
                    0, self.player_turn - constants.LIVING_WORLD_TURN_INTERVAL
                )
            logging_util.warning(
                "GameState: last_living_world_turn ahead of player_turn "
                "(last=%s, player_turn=%s); resetting to %s",
                self.last_living_world_turn,
                self.player_turn,
                recovered_turn,
            )
            self.last_living_world_turn = recovered_turn

        # Track game time of last event to support dual-trigger system (turns OR time)
        raw_last_living_world_time = kwargs.get("last_living_world_time")
        has_last_living_world_time = raw_last_living_world_time is not None
        if not has_last_living_world_time and isinstance(
            kwargs.get("living_world_state"), dict
        ):
            legacy_living_world_state = kwargs.get("living_world_state", {})
            raw_last_living_world_time = legacy_living_world_state.get(
                "last_time",
                legacy_living_world_state.get("last_living_world_time"),
            )
        if isinstance(raw_last_living_world_time, dict):
            self.last_living_world_time = copy.deepcopy(raw_last_living_world_time)
        else:
            if raw_last_living_world_time is not None:
                logging_util.warning(
                    "GameState: ignoring invalid last_living_world_time (raw=%r)",
                    raw_last_living_world_time,
                )
            self.last_living_world_time = None
        if self.last_living_world_time is None and isinstance(self.world_data, dict):
            candidate_time = self.world_data.get("world_time")
            if isinstance(
                candidate_time, dict
            ) and world_time._has_required_date_fields(candidate_time):
                # Store a snapshot so future time comparisons are stable.
                self.last_living_world_time = copy.deepcopy(candidate_time)
                logging_util.info(
                    "GameState: initialized last_living_world_time from world_data"
                )

        # Initialize time pressure structures
        self.time_sensitive_events = kwargs.get("time_sensitive_events", {})
        self.npc_agendas = kwargs.get("npc_agendas", {})
        self.world_resources = kwargs.get("world_resources", {})
        self.time_pressure_warnings = kwargs.get("time_pressure_warnings", {})

        # Debug mode flag
        self.debug_mode = kwargs.get("debug_mode", constants.DEFAULT_DEBUG_MODE)

        # LLM-requested instruction hints for next turn
        # Extracted from debug_info.meta.needs_detailed_instructions and used to load
        # detailed prompt sections (e.g., relationships, reputation) on subsequent turns
        self.pending_instruction_hints: list[str] = kwargs.get(
            "pending_instruction_hints", []
        )

        # Dynamically set any other attributes from kwargs
        for key, value in kwargs.items():
            if not hasattr(self, key):
                setattr(self, key, value)

        # Apply time consolidation migration
        self._consolidate_time_tracking()

    def _normalize_combat_state(self) -> None:  # noqa: PLR0912
        """
        Normalize combat_state to handle LLM-generated malformed data.

        Fixes common issues:
        1. initiative_order entries that are strings instead of dicts
        2. combatants that are strings instead of dicts
        3. Coerces HP values to integers

        Only normalizes fields that already exist - does not add new fields.
        """
        if not isinstance(self.combat_state, dict):
            self.combat_state = {"in_combat": False}
            return

        # Normalize initiative_order entries (only if field exists)
        if "initiative_order" in self.combat_state:
            init_order = self.combat_state["initiative_order"]
            if isinstance(init_order, list):
                normalized_order = []
                for entry in init_order:
                    if isinstance(entry, str):
                        # Convert string to dict with name
                        normalized_order.append(
                            {
                                "name": entry,
                                "initiative": 0,
                                "type": "unknown",
                            }
                        )
                    elif isinstance(entry, dict):
                        # Ensure required fields exist
                        normalized_order.append(
                            {
                                "name": entry.get("name", "Unknown"),
                                "initiative": _coerce_int(
                                    entry.get("initiative", 0), 0
                                ),
                                "type": entry.get("type", "unknown"),
                            }
                        )
                    # Skip non-string, non-dict entries
                self.combat_state["initiative_order"] = normalized_order

        # Normalize combatants entries (only if field exists)
        if "combatants" in self.combat_state:
            combatants = self.combat_state["combatants"]
            if isinstance(combatants, list):
                # Convert list to dict format
                combatants_dict = {}
                for c in combatants:
                    if isinstance(c, str):
                        combatants_dict[c] = {
                            "hp_current": 1,
                            "hp_max": 1,
                            "status": [],
                        }
                    elif isinstance(c, dict) and "name" in c:
                        name = c["name"]
                        combatants_dict[name] = {
                            "hp_current": _coerce_int(c.get("hp_current", 1), 1),
                            "hp_max": _coerce_int(c.get("hp_max", 1), 1),
                            "status": c.get("status", []),
                        }
                self.combat_state["combatants"] = combatants_dict
            elif isinstance(combatants, dict):
                # Ensure all combatant values are dicts with coerced ints
                normalized_combatants = {}
                for name, data in combatants.items():
                    if isinstance(data, str):
                        # String value - convert to minimal dict
                        normalized_combatants[name] = {
                            "hp_current": 1,
                            "hp_max": 1,
                            "status": [],
                        }
                    elif isinstance(data, dict):
                        normalized_combatants[name] = {
                            "hp_current": _coerce_int(data.get("hp_current", 1), 1),
                            "hp_max": _coerce_int(data.get("hp_max", 1), 1),
                            "status": data.get("status", []),
                            # Preserve type/role if present
                            **({"type": data["type"]} if "type" in data else {}),
                            **({"role": data["role"]} if "role" in data else {}),
                        }
                    else:
                        # Unknown type - skip
                        continue
                self.combat_state["combatants"] = normalized_combatants

        # Ensure consistency: Remove initiative entries that don't have a corresponding combatant
        # This prevents "orphaned" turns and invalid states where init exists but combatants don't
        if (
            "initiative_order" in self.combat_state
            and "combatants" in self.combat_state
        ):
            init_order = self.combat_state.get("initiative_order")
            combatants = self.combat_state.get("combatants")
            # Guard: Only proceed if types are correct
            if isinstance(init_order, list) and isinstance(combatants, dict):
                combatants_keys = set(combatants.keys())
                self.combat_state["initiative_order"] = [
                    entry
                    for entry in init_order
                    if isinstance(entry, dict) and entry.get("name") in combatants_keys
                ]
        # CRITICAL: Validate schema consistency between initiative_order and combatants
        self._validate_combat_state_consistency()

    def _validate_combat_state_consistency(self) -> None:
        """
        Validate that initiative_order and combatants are consistent.

        Logs warnings for:
        1. initiative_order names that don't exist in combatants (orphaned entries)
        2. combatants keys that don't appear in initiative_order (missing from turn order)
        3. Empty combatants with populated initiative_order (invalid state)
        """
        if not isinstance(self.combat_state, dict):
            return

        init_order = self.combat_state.get("initiative_order", [])
        combatants = self.combat_state.get("combatants", {})

        if not isinstance(init_order, list) or not isinstance(combatants, dict):
            return

        # Get names from initiative_order
        init_names = {
            entry.get("name") for entry in init_order if isinstance(entry, dict)
        }

        # Get keys from combatants
        combatant_keys = set(combatants.keys())

        # Check for orphaned initiative entries (name not in combatants)
        orphaned_init = init_names - combatant_keys
        if orphaned_init:
            logging_util.warning(
                f"⚠️ COMBAT_STATE_MISMATCH: initiative_order has names not in combatants: {orphaned_init}. "
                "Cleanup may fail for these entries."
            )

        # Check for combatants missing from initiative_order
        missing_from_init = combatant_keys - init_names
        if missing_from_init:
            logging_util.warning(
                f"⚠️ COMBAT_STATE_MISMATCH: combatants has keys not in initiative_order: {missing_from_init}. "
                "These combatants won't have a turn."
            )

        # Check for empty combatants with populated initiative_order (INVALID STATE)
        if init_order and not combatants:
            logging_util.error(
                f"🔴 INVALID_COMBAT_STATE: initiative_order has {len(init_order)} entries but combatants is empty. "
                "Combat cleanup will fail. This violates the combat schema."
            )

        # Check for missing combat_summary when combat has ended
        in_combat = self.combat_state.get("in_combat", False)
        combat_phase = self.combat_state.get("combat_phase", "")
        combat_summary = self.combat_state.get("combat_summary")

        if not in_combat and combat_phase == "ended":
            if not combat_summary:
                logging_util.warning(
                    "⚠️ MISSING_COMBAT_SUMMARY: Combat ended (in_combat=false, combat_phase=ended) "
                    "but no combat_summary provided. XP and loot may not be awarded."
                )
            elif isinstance(combat_summary, dict):
                # Validate combat_summary has required fields
                required_fields = ["xp_awarded", "enemies_defeated"]
                missing = [f for f in required_fields if f not in combat_summary]
                if missing:
                    logging_util.warning(
                        f"⚠️ INCOMPLETE_COMBAT_SUMMARY: Missing fields: {missing}. "
                        "XP awards may be incorrect."
                    )
                # Validate xp_awarded is a number
                xp = combat_summary.get("xp_awarded")
                if xp is not None and not isinstance(xp, (int, float)):
                    logging_util.warning(
                        f"⚠️ INVALID_XP_AWARDED: xp_awarded is {type(xp).__name__}, expected int. "
                        f"Value: {xp}"
                    )

    def to_dict(self) -> dict:
        """Serializes the GameState object to a dictionary for Firestore."""
        # Copy all attributes from the instance's __dict__
        data = self.__dict__.copy()

        # Remove any internal cache attributes that shouldn't be serialized
        # These are typically prefixed with underscore and added at runtime
        keys_to_remove = [
            key for key in data if key.startswith("_") and key != "__dict__"
        ]
        keys_to_remove.extend(["user_settings"])
        for key in keys_to_remove:
            data.pop(key, None)

        return data

    @staticmethod
    def _json_serializable(obj: Any) -> Any:
        """Recursively convert datetime objects to ISO strings for JSON Schema validation."""
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        # Firestore SERVER_TIMESTAMP sentinel appears in transient update paths.
        # Convert to an ISO timestamp for schema-validation-only copies.
        if obj.__class__.__name__ == "Sentinel":
            return dt.now(UTC).isoformat()
        if isinstance(obj, dict):
            return {k: GameState._json_serializable(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [GameState._json_serializable(item) for item in obj]
        return obj

    def to_validated_dict(self) -> dict:
        """
        Serializes the GameState, validates against the JSON Schema, and
        returns the Firestore-compatible dict (with raw datetime objects).

        Validation is performed on an ISO-string copy so that JSON Schema
        ``format: date-time`` checks work, but the returned dict preserves
        raw ``datetime`` objects for Firestore native Timestamp storage.

        WARNING ONLY - Schema validation failures generate GCP logs and warnings but do not crash.

        Returns:
            dict: The serialized and validated game state (raw datetimes).
        """
        data = self.to_dict()

        # Validate against an ISO-string copy; discard the copy afterward
        # WARNING ONLY - Non-blocking validation (see CLAUDE.md validation policy)
        data_for_validation = self._json_serializable(data)
        errors = validate_game_state(data_for_validation)
        errors.extend(_validate_post_migration_schema_invariants(data))
        if errors:
            error_msg = "GameState validation failed:\n" + "\n".join(errors)
            logging_util.warning(f"VALIDATION FAILURE (non-blocking): {error_msg}")
            # Continue execution - validation warnings are logged but do not crash

        # Return the original dict with raw datetimes for Firestore compat
        return data

    def to_model(self):
        """
        Exports the GameState to a Pydantic model.

        Returns:
            GameStateModel: The Pydantic model instance.
        """
        data = self.to_dict()
        return GameStateModel.model_validate(data)

    @classmethod
    def from_model(cls, model: Any) -> GameState:
        """
        Creates a GameState instance from a Pydantic model.

        Args:
            model: A GameStateModel instance.

        Returns:
            GameState: The new GameState instance.
        """
        # Use mode='python' to preserve None values (don't exclude them)
        # Preserves intentional None semantics (e.g., rewards_pending=None means "no rewards")
        data = model.model_dump(mode='python')
        return cls(**data)

    def update_from_model(self, model: Any) -> None:
        """
        Updates the internal state from a Pydantic model.

        Re-initializes the instance to ensure all constructor normalization logic runs:
        - campaign_tier validation against allowed tiers
        - arc_milestones/companion_arcs/active_constraints type guarantees
        - combat_state normalization via _normalize_combat_state()
        - Numeric field coercion with logging

        Args:
            model: A GameStateModel instance.
        """
        # Use mode='python' to preserve None values (don't exclude them)
        data = model.model_dump(mode='python')
        # Re-run __init__ to apply all normalization and validation logic
        self.__init__(**data)

    @classmethod
    def from_dict(cls, source: dict[str, Any] | None) -> GameState | None:
        """Creates a GameState object from a dictionary (e.g., from Firestore)."""
        if not source:
            return None

        # The constructor now directly accepts the dictionary.
        return cls(**source)

    def get_combat_state(self) -> dict:
        """
        Get combat_state as a normalized dict.

        This is the standardized way to access combat_state throughout the codebase.
        Always returns a dict (never None), with sensible defaults.

        Returns:
            dict: Combat state with at minimum {"in_combat": False}
        """
        if not hasattr(self, "combat_state"):
            return {"in_combat": False}
        if not isinstance(self.combat_state, dict):
            return {"in_combat": False}
        return self.combat_state

    def is_in_combat(self) -> bool:
        """
        Check if combat is currently active.

        This is the standardized way to check combat status.

        Returns:
            bool: True if in_combat is explicitly True, False otherwise
        """
        combat_state = self.get_combat_state()
        return combat_state.get("in_combat", False) is True

    def get_encounter_state(self) -> dict:
        """
        Get encounter_state as a normalized dict.

        This is the standardized way to access encounter_state throughout the codebase.
        Used for non-combat encounters (heists, social victories, stealth, puzzles).
        Always returns a dict (never None), with sensible defaults.

        Returns:
            dict: Encounter state with at minimum {"encounter_active": False}

        Schema:
            {
                "encounter_active": bool,
                "encounter_id": str,
                "encounter_type": "heist" | "social" | "stealth" | "puzzle" | "quest",
                "difficulty": "easy" | "medium" | "hard" | "deadly",
                "participants": [...],
                "encounter_completed": bool,
                "encounter_summary": {...},
                "rewards_processed": bool
            }
        """
        if not hasattr(self, "encounter_state"):
            return {"encounter_active": False}
        if not isinstance(self.encounter_state, dict):
            return {"encounter_active": False}
        return self.encounter_state

    def check_living_world_trigger(
        self, current_turn: int, *, current_time: dict[str, Any] | None = None
    ) -> tuple[bool, str, dict[str, Any] | None]:
        """
        Determine if living world event should fire based on turn or time.

        Args:
            current_turn: Current turn number (1-indexed)
            current_time: Optional world_time dict passed by caller

        Returns:
            tuple: (should_trigger, reason_string, current_time_dict)
        """
        last_turn = self.last_living_world_turn
        last_time = self.last_living_world_time
        if current_time is not None and not isinstance(current_time, dict):
            logging_util.warning(
                "GameState: ignoring invalid world_time in check_living_world_trigger (raw=%r)",
                current_time,
            )
            current_time = None

        if current_time is None and hasattr(self, "world_data") and isinstance(self.world_data, dict):
            candidate_time = self.world_data.get("world_time")
            if isinstance(candidate_time, dict):
                current_time = candidate_time
            elif candidate_time is not None:
                logging_util.warning(
                    "GameState: ignoring invalid world_time in check_living_world_trigger (raw=%r)",
                    candidate_time,
                )
                current_time = None

        should_trigger, trigger_reason, _hours_elapsed = (
            living_world.evaluate_living_world_trigger(
                current_turn=current_turn,
                last_turn=last_turn,
                last_time=last_time,
                current_time=current_time,
                turn_interval=constants.LIVING_WORLD_TURN_INTERVAL,
                time_interval=constants.LIVING_WORLD_TIME_INTERVAL,
            )
        )

        return should_trigger, trigger_reason, current_time

    def get_rewards_pending(self) -> dict | None:
        """
        Get rewards_pending from game state.

        This is the standardized way to access pending rewards throughout the codebase.
        Used by RewardsAgent to detect when rewards need to be processed.

        Returns:
            dict: Rewards pending data, or None if no rewards pending

        Schema:
            {
                "source": "combat" | "encounter" | "quest" | "milestone",
                "source_id": str,  # combat_session_id or encounter_id
                "xp": int,
                "gold": int,
                "items": [...],
                "level_up_available": bool,
                "processed": bool
            }
        """
        if not hasattr(self, "rewards_pending"):
            return None
        if not isinstance(self.rewards_pending, dict):
            return None
        # Return None if rewards is empty dict
        if not self.rewards_pending:
            return None
        return self.rewards_pending

    def has_pending_rewards(self) -> bool:
        """
        Check if there are any pending rewards from any source.

        Checks:
        1. Explicit rewards_pending field
        2. Combat ended with summary but not processed
        3. Encounter completed with encounter_summary but not processed

        Returns:
            bool: True if rewards are pending and need processing
        """
        # Check explicit rewards_pending
        rewards = self.get_rewards_pending()
        if rewards and not rewards.get("processed", False):
            return True

        # Check combat ended with summary
        combat_state = self.get_combat_state()
        # Use centralized constant for combat finished phases
        if (
            combat_state.get("combat_phase") in constants.COMBAT_FINISHED_PHASES
            and combat_state.get("combat_summary")
            and not combat_state.get("rewards_processed", False)
        ):
            return True

        # Check encounter completed with summary
        encounter_state = self.get_encounter_state()
        encounter_completed = encounter_state.get("encounter_completed", False)
        encounter_summary = encounter_state.get("encounter_summary")
        encounter_processed = encounter_state.get("rewards_processed", False)

        if encounter_completed:
            if not isinstance(encounter_summary, dict):
                logging_util.debug(
                    "🏆 REWARDS_CHECK: Encounter completed but encounter_summary missing/invalid"
                )
            elif encounter_summary.get("xp_awarded") is None:
                logging_util.debug(
                    "🏆 REWARDS_CHECK: Encounter completed but encounter_summary missing xp_awarded"
                )
            elif not encounter_processed:
                return True

        return False

    # =========================================================================
    # Arc Milestone Tracking Methods
    # =========================================================================
    # These methods provide structured tracking for narrative arcs to prevent
    # the LLM from losing track of completed events during context compression.
    # =========================================================================

    def mark_arc_completed(
        self, arc_name: str, phase: str | None = None, metadata: dict | None = None
    ) -> None:
        """
        Mark a narrative arc as completed with timestamp.

        Once an arc is marked completed, it cannot be reverted to in_progress.
        This prevents timeline confusion where the LLM forgets major events.
        Calling this again for the same arc overwrites the previous completion
        record (including completed_at) to allow phase/metadata updates.

        Args:
            arc_name: Unique identifier for the arc (e.g., "wedding_tour")
            phase: Optional phase name when completion occurred
            metadata: Optional additional data to store with the milestone
        """
        milestones = self.custom_campaign_state.get("arc_milestones", {})

        milestone_data = {
            "status": "completed",
            "completed_at": datetime.datetime.now(datetime.UTC).isoformat(),
        }

        if phase is not None:
            milestone_data["phase"] = phase

        if metadata is not None:
            milestone_data["metadata"] = metadata

        milestones[arc_name] = milestone_data
        self.custom_campaign_state["arc_milestones"] = milestones

    def update_arc_progress(self, arc_name: str, phase: str, progress: int = 0) -> None:
        """
        Update the progress of an in-progress arc.

        If the arc is already completed, this method does nothing to prevent
        timeline regression.

        Args:
            arc_name: Unique identifier for the arc
            phase: Current phase of the arc
            progress: Progress percentage (0-100)
        """
        milestones = self.custom_campaign_state.get("arc_milestones", {})
        arc_data = milestones.get(arc_name)

        # Prevent regression of completed arcs
        if isinstance(arc_data, dict) and arc_data.get("status") == "completed":
            logging_util.warning(
                "Attempted to update progress for completed arc '%s' "
                "(phase=%s, progress=%s). Update ignored to prevent timeline regression.",
                arc_name,
                phase,
                progress,
            )
            return  # Arc already completed, don't regress

        progress_value = _coerce_int(progress, 0)
        if progress_value < 0 or progress_value > 100:
            logging_util.warning(
                "Arc progress out of range for '%s': %s. Clamping to 0-100.",
                arc_name,
                progress_value,
            )
            progress_value = max(0, min(100, progress_value))

        milestones[arc_name] = {
            "status": "in_progress",
            "phase": phase,
            "progress": progress_value,
            "updated_at": datetime.datetime.now(datetime.UTC).isoformat(),
        }
        self.custom_campaign_state["arc_milestones"] = milestones

    def is_arc_completed(self, arc_name: str) -> bool:
        """
        Check if a narrative arc has been marked as completed.

        Args:
            arc_name: Unique identifier for the arc

        Returns:
            True if the arc is completed, False otherwise
        """
        milestones = self.custom_campaign_state.get("arc_milestones", {})
        arc_data = milestones.get(arc_name)
        if not isinstance(arc_data, dict):
            return False
        return arc_data.get("status") == "completed"

    def get_arc_phase(self, arc_name: str) -> str | None:
        """
        Get the current phase of a narrative arc.

        Args:
            arc_name: Unique identifier for the arc

        Returns:
            The phase name if set, None otherwise
        """
        milestones = self.custom_campaign_state.get("arc_milestones", {})
        arc_data = milestones.get(arc_name)
        if not isinstance(arc_data, dict):
            return None
        return arc_data.get("phase")

    def get_completed_arcs_summary(self) -> str:
        """
        Generate a summary of completed arcs for inclusion in LLM context.

        This provides deterministic state information to prevent the LLM from
        forgetting that major narrative arcs have concluded.

        Returns:
            Formatted string summarizing completed arcs, empty if none
        """
        milestones = self.custom_campaign_state.get("arc_milestones", {})

        completed = [
            (name, data)
            for name, data in milestones.items()
            if isinstance(data, dict) and data.get("status") == "completed"
        ]

        if not completed:
            return ""

        lines = ["[COMPLETED ARCS - DO NOT REVISIT AS IN-PROGRESS]"]
        for arc_name, data in completed:
            phase = data.get("phase", "final")
            completed_at = data.get("completed_at", "unknown")
            lines.append(
                f"- {arc_name}: COMPLETED (phase: {phase}, at: {completed_at})"
            )

        return "\n".join(lines)

    def get_companion_arcs_summary(self) -> str:
        """
        Generate a summary of companion arcs for LLM context.

        The LLM manages companion arcs via state_updates.companion_arcs.
        This method formats the current state for inclusion in prompts.

        Schema (managed by LLM in state_updates):
        companion_arcs: {
          "companion_name": {
            "arc_type": "lost_family|rival_nemesis|dark_secret|...",
            "phase": "discovery|development|crisis|resolution",
            "callbacks": [{"trigger": "condition", "effect": "what happens"}],
            "history": ["turn 3: saw pendant", "turn 6: learned sister missing"]
          }
        }
        """
        companion_arcs = self.custom_campaign_state.get("companion_arcs", {})
        # Validate companion_arcs is a dict before calling .items()
        # LLM may set it to non-dict types (string/list), which would raise AttributeError
        if not companion_arcs or not isinstance(companion_arcs, dict):
            return ""

        lines = []
        for name, arc in companion_arcs.items():
            if not isinstance(arc, dict):
                continue
            phase = arc.get("phase", constants.COMPANION_ARC_PHASES[0])
            if phase not in constants.COMPANION_ARC_PHASES:
                phase = constants.COMPANION_ARC_PHASES[0]
            arc_type = arc.get("arc_type", "unknown")
            if arc_type not in constants.COMPANION_ARC_TYPES:
                arc_type = "unknown"
            lines.append(f"- {name}: {arc_type} ({phase})")

            # Show recent history
            history = arc.get("history", [])
            if isinstance(history, list):
                for event in history[-2:]:
                    if isinstance(event, dict):
                        event_text = event.get("event") or event.get("description")
                    else:
                        event_text = event
                    if event_text:
                        lines.append(f"  └ {event_text}")

            # Show pending callbacks
            callbacks = arc.get("callbacks", [])
            if isinstance(callbacks, list):
                for cb in callbacks[:2]:
                    if not isinstance(cb, dict) or cb.get("triggered") is True:
                        continue
                    trigger = cb.get("trigger") or cb.get("trigger_condition")
                    effect = cb.get("effect")
                    if trigger or effect:
                        lines.append(
                            f"  ⚡ Callback: {trigger or 'unknown'} → {effect or 'unknown'}"
                        )

        return "\n".join(lines) if lines else ""

    def validate_checkpoint_consistency(self, narrative_text: str) -> list[str]:  # noqa: PLR0912,PLR0915,SIM102
        """
        Validates that critical checkpoint data in the state matches references in the narrative.
        Returns a list of discrepancies found.
        """
        discrepancies = []
        narrative_lower = narrative_text.lower()

        # Check player character HP consistency
        if isinstance(self.player_character_data, dict):
            pc_data = self.player_character_data
            hp_current = pc_data.get("hp_current")
            hp_max = pc_data.get("hp_max")

            # Defensive: persisted game state may contain numeric strings
            hp_current = _coerce_int(hp_current, None)
            hp_max = _coerce_int(hp_max, None)

            if hp_current is not None and hp_max is not None and hp_max > 0:
                # Check for unconscious/death vs HP mismatch
                if (
                    "unconscious" in narrative_lower
                    or "lies unconscious" in narrative_lower
                ) and hp_current > 0:
                    discrepancies.append(
                        f"Narrative mentions unconsciousness but HP is {hp_current}/{hp_max}"
                    )

                if (
                    any(
                        phrase in narrative_lower
                        for phrase in ["completely drained", "drained of life"]
                    )
                    and hp_current > 5
                ):  # Should be very low if "drained of life"
                    discrepancies.append(
                        f"Narrative describes being drained of life but HP is {hp_current}/{hp_max}"
                    )

                hp_percentage = (hp_current / hp_max) * 100

                # Check for narrative/state HP mismatches
                if hp_percentage < 25:  # Critically wounded
                    if not any(
                        word in narrative_lower
                        for word in [
                            "wounded",
                            "injured",
                            "hurt",
                            "bleeding",
                            "pain",
                            "unconscious",
                        ]
                    ):
                        discrepancies.append(
                            f"State shows character critically wounded ({hp_current}/{hp_max} HP) but narrative doesn't reflect injury"
                        )
                elif hp_percentage > 90 and any(
                    word in narrative_lower
                    for word in [
                        "wounded",
                        "injured",
                        "bleeding",
                        "dying",
                        "unconscious",
                    ]
                ):
                    discrepancies.append(
                        f"Narrative describes character as injured but state shows healthy ({hp_current}/{hp_max} HP)"
                    )
            elif hp_current is not None and hp_max == 0:
                # Skip validation only during character creation when HP is not yet initialized
                campaign_state = self.world_data.get("campaign_state", "")
                character_creation = self.custom_campaign_state.get(
                    "character_creation", {}
                )
                is_character_creation = (
                    campaign_state == "character_creation"
                    or character_creation.get("in_progress", False)
                )
                if not is_character_creation:
                    discrepancies.append(
                        f"Character has invalid HP state: {hp_current}/{hp_max} (hp_max should not be 0 outside character creation)"
                    )

        # Check location consistency
        current_location = self.world_data.get(
            "current_location_name"
        ) or self.world_data.get("current_location")
        if current_location:
            # Handle dict location objects by extracting name
            if isinstance(current_location, dict):
                current_location = current_location.get("name", "")

            # Ensure we have a string before calling lower()
            if isinstance(current_location, str):
                location_lower = current_location.lower()
            else:
                location_lower = str(current_location).lower()

            # If narrative mentions being in a specific place that doesn't match state
            if "forest" in narrative_lower and "tavern" in location_lower:
                discrepancies.append(
                    f"State location '{current_location}' conflicts with narrative mentioning forest"
                )
            elif "tavern" in narrative_lower and "forest" in location_lower:
                discrepancies.append(
                    f"State location '{current_location}' conflicts with narrative mentioning tavern"
                )

        # Check active missions consistency
        active_missions = self.custom_campaign_state.get("active_missions", [])
        if active_missions:
            for mission in active_missions:
                if isinstance(mission, dict):
                    mission_name = (
                        mission.get("name") or mission.get("title") or str(mission)
                    )
                else:
                    mission_name = str(mission)

                mission_lower = mission_name.lower()

                # Check for specific mission completion phrases
                if "dragon" in mission_lower and any(
                    phrase in narrative_lower
                    for phrase in ["dragon finally defeated", "dragon defeated"]
                ):
                    discrepancies.append(
                        f"Mission '{mission_name}' appears completed in narrative but still active in state"
                    )

                if "treasure" in mission_lower and any(
                    phrase in narrative_lower
                    for phrase in ["treasure secured", "treasure found"]
                ):
                    discrepancies.append(
                        f"Mission '{mission_name}' appears completed in narrative but still active in state"
                    )

        return discrepancies

    # Combat Management Methods

    def start_combat(self, combatants_data: list[dict[str, Any]]) -> None:
        """
        Initialize combat state with given combatants.

        Args:
            combatants_data: List of dicts with keys: name, initiative, type, hp_current, hp_max
        """
        logging_util.info(
            f"COMBAT STARTED - Participants: {[c['name'] for c in combatants_data]}"
        )

        # Sort by initiative (highest first)
        sorted_combatants = sorted(
            combatants_data, key=lambda x: x["initiative"], reverse=True
        )

        self.combat_state = {
            "in_combat": True,
            "current_round": 1,
            "current_turn_index": 0,
            "initiative_order": [
                {
                    "name": c["name"],
                    "initiative": c["initiative"],
                    "type": c.get("type", "unknown"),
                }
                for c in sorted_combatants
            ],
            "combatants": {
                c["name"]: {
                    "hp_current": c.get("hp_current", 1),
                    "hp_max": c.get("hp_max", 1),
                    "status": c.get("status", []),
                }
                for c in sorted_combatants
            },
            "combat_log": [],
        }

        initiative_list = [f"{c['name']}({c['initiative']})" for c in sorted_combatants]
        logging_util.info(f"COMBAT INITIALIZED - Initiative order: {initiative_list}")

    def end_combat(self) -> None:
        """End combat and reset combat state."""
        if self.combat_state.get("in_combat", False):
            final_round = self.combat_state.get("current_round", 0)
            participants = list(self.combat_state.get("combatants", {}).keys())

            # Clean up defeated enemies before ending combat
            defeated_enemies = self.cleanup_defeated_enemies()
            if defeated_enemies:
                logging_util.info(
                    f"COMBAT CLEANUP: Defeated enemies removed during combat end: {defeated_enemies}"
                )

            logging_util.info(
                f"COMBAT ENDED - Duration: {final_round} rounds, Participants: {participants}"
            )

        # Reset combat state
        self.combat_state = {
            "in_combat": False,
            "current_round": 0,
            "current_turn_index": 0,
            "initiative_order": [],
            "combatants": {},
            "combat_log": [],
        }

    def _is_named_npc(self, npc: dict[str, Any]) -> bool:
        """Return True if the NPC should be preserved (named/important).

        Uses centralized constants from mvp_site.constants for maintainability.
        """
        role_raw = npc.get("role")
        # Use centralized helper for role classification
        has_named_role = not constants.is_generic_enemy_role(role_raw)
        has_story = npc.get("backstory") or npc.get("background")
        return bool(has_named_role or has_story or npc.get("is_important"))

    def cleanup_defeated_enemies(self) -> list[str]:  # noqa: PLR0912,PLR0915
        """
        Identifies and removes defeated enemies from both combat_state and npc_data.
        Returns a list of defeated enemy names for logging.

        CRITICAL: This function works regardless of in_combat status to handle
        cleanup during combat end transitions.
        """
        defeated_enemies = []

        # Check if we have any combatants to clean up
        combatants = self.combat_state.get("combatants", {})
        if not combatants:
            return defeated_enemies

        # Handle both dict and list formats for combatants
        # AI sometimes generates combatants as a list instead of dict
        if isinstance(combatants, list):
            # Convert list format to dict format for processing
            combatants_dict = {}
            for combatant in combatants:
                if isinstance(combatant, dict) and "name" in combatant:
                    name = combatant["name"]
                    combatants_dict[name] = combatant
            combatants = combatants_dict
            # Update the combat_state with the normalized dict format
            self.combat_state["combatants"] = combatants_dict

        # Find defeated enemies (HP <= 0)
        for name, combat_data in combatants.items():
            hp_current = _coerce_int(combat_data.get("hp_current", 0), 0) or 0
            if hp_current <= 0:
                # Check if this is an enemy (not PC, companion, or ally)
                enemy_type_raw: Any = None
                for init_entry in self.combat_state.get("initiative_order", []):
                    if init_entry["name"] == name:
                        enemy_type_raw = init_entry.get("type")
                        break

                if enemy_type_raw is None:
                    # Fallback to combatant metadata when initiative entry is missing
                    enemy_type_raw = combat_data.get("type") or combat_data.get("role")

                if enemy_type_raw is None and name in self.npc_data:
                    # Final fallback to npc_data for classification
                    npc_record = self.npc_data[name]
                    enemy_type_raw = npc_record.get("role") or npc_record.get("type")

                enemy_type = (
                    enemy_type_raw.lower().strip()
                    if isinstance(enemy_type_raw, str)
                    else enemy_type_raw
                )

                # Use centralized constants for friendly type detection
                if enemy_type is None or enemy_type == "unknown":
                    # Attempt to infer friendliness from player or NPC metadata before defaulting to enemy cleanup
                    player_name = (
                        self.player_character_data.get("name")
                        if isinstance(self.player_character_data, dict)
                        else None
                    )
                    if player_name and name == player_name:
                        logging_util.info(
                            f"COMBAT CLEANUP: Skipping {name} removal because combatant matches player character with missing/unknown type"
                        )
                        continue

                    npc_record = (
                        self.npc_data.get(name)
                        if isinstance(self.npc_data, dict)
                        else None
                    )
                    npc_role_raw = (
                        npc_record.get("role") if isinstance(npc_record, dict) else None
                    )
                    npc_type_raw = (
                        npc_record.get("type") if isinstance(npc_record, dict) else None
                    )
                    npc_role = (
                        npc_role_raw.lower().strip()
                        if isinstance(npc_role_raw, str)
                        else npc_role_raw
                    )
                    npc_type = (
                        npc_type_raw.lower().strip()
                        if isinstance(npc_type_raw, str)
                        else npc_type_raw
                    )

                    if constants.is_friendly_combatant(
                        npc_role
                    ) or constants.is_friendly_combatant(npc_type):
                        logging_util.info(
                            f"COMBAT CLEANUP: Skipping {name} removal because npc_data marks combatant as friendly "
                            f"(role/type: {npc_role or npc_type}) despite missing initiative type"
                        )
                        continue

                    # Default to treating missing/unknown types as generic enemies to avoid leaving defeated foes targetable
                    logging_util.warning(
                        f"COMBAT CLEANUP: Defaulting {name} to generic enemy because type is missing/unknown "
                        f"(initiative entry absent or incomplete)"
                    )
                    enemy_type = "enemy"

                if constants.is_friendly_combatant(enemy_type):
                    logging_util.info(
                        f"COMBAT CLEANUP: Skipping {name} because combatant is friendly ({enemy_type})"
                    )
                    continue

                defeated_enemies.append(name)
                logging_util.info(
                    f"COMBAT CLEANUP: Marking {name} ({enemy_type}) as defeated"
                )

        # Remove defeated enemies from combat tracking
        for enemy_name in defeated_enemies:
            # Remove from combat_state combatants
            if enemy_name in self.combat_state.get("combatants", {}):
                del self.combat_state["combatants"][enemy_name]
                logging_util.info(
                    f"COMBAT CLEANUP: Removed {enemy_name} from combat_state.combatants"
                )

            # Remove from initiative order
            self.combat_state["initiative_order"] = [
                entry
                for entry in self.combat_state.get("initiative_order", [])
                if entry["name"] != enemy_name
            ]

            # Handle NPC data - mark named NPCs as dead, delete generic enemies
            if enemy_name in self.npc_data:
                npc = self.npc_data[enemy_name]
                # Check if this is a named/important NPC (has role, backstory, or is explicitly important)
                # Named NPCs should be preserved with dead status for narrative continuity
                if self._is_named_npc(npc):
                    # Mark as dead instead of deleting - preserve for narrative continuity
                    if "status" not in npc:
                        npc["status"] = []
                    elif not isinstance(npc["status"], list):
                        status_value = npc["status"]
                        npc["status"] = [] if status_value is None else [status_value]
                    if "dead" not in npc["status"]:
                        npc["status"].append("dead")
                    npc["hp_current"] = 0
                    logging_util.info(
                        f"COMBAT CLEANUP: Marked {enemy_name} as dead in npc_data (named NPC preserved)"
                    )
                else:
                    # Generic enemies can be deleted
                    del self.npc_data[enemy_name]
                    logging_util.info(
                        f"COMBAT CLEANUP: Removed {enemy_name} from npc_data (generic enemy)"
                    )

        return defeated_enemies

    def _consolidate_time_tracking(self) -> None:
        """
        Consolidate time tracking from separate fields into a single object.
        Migrates old time_of_day field into world_time object if needed.
        """
        if not hasattr(self, "world_data") or not self.world_data:
            return

        world_data = self.world_data

        # Check if we have the old separate time_of_day field
        if "time_of_day" in world_data:
            # Migrate time_of_day into world_time object
            old_time_of_day = world_data["time_of_day"]

            # Ensure world_time exists and is a dict
            if "world_time" not in world_data:
                # Create world_time with reasonable defaults based on time_of_day
                hour = self._estimate_hour_from_time_of_day(old_time_of_day)
                world_data["world_time"] = {
                    "hour": hour,
                    "minute": 0,
                    "second": 0,
                    "microsecond": 0,
                    "time_of_day": old_time_of_day,
                }
            elif not isinstance(world_data["world_time"], dict):
                world_data["world_time"] = {
                    "hour": 12,
                    "minute": 0,
                    "second": 0,
                    "microsecond": 0,
                }
                world_data["world_time"]["time_of_day"] = old_time_of_day
            else:
                # world_time exists and is dict, just add time_of_day
                world_data["world_time"]["time_of_day"] = old_time_of_day

            # Remove the old field
            del world_data["time_of_day"]
            logging_util.info(
                f"Migrated time_of_day '{old_time_of_day}' into world_time object"
            )

        # Only process world_time if it already exists
        if "world_time" in world_data and isinstance(world_data["world_time"], dict):
            # Ensure microsecond field exists (default to 0 for existing campaigns)
            if "microsecond" not in world_data["world_time"]:
                world_data["world_time"]["microsecond"] = 0
                logging_util.info("Added microsecond field to world_time (default: 0)")

            # Calculate time_of_day from hour if not present
            if "time_of_day" not in world_data["world_time"]:
                try:
                    hour = int(world_data["world_time"].get("hour", 12))
                except (ValueError, TypeError):
                    hour = 12  # Default to midday if conversion fails
                world_data["world_time"]["time_of_day"] = self._calculate_time_of_day(
                    hour
                )
                logging_util.info(
                    f"Calculated time_of_day as '{world_data['world_time']['time_of_day']}' from hour {hour}"
                )

    def _calculate_time_of_day(self, hour: int) -> str:  # noqa: PLR0911
        """
        Calculate descriptive time of day from hour value.

        Args:
            hour: Hour value (0-23)

        Returns:
            String description of time of day (lowercase canonical form)
        """
        if 0 <= hour <= 4:
            return "deep night"
        if 5 <= hour <= 6:
            return "dawn"
        if 7 <= hour <= 11:
            return "morning"
        if 12 <= hour <= 13:
            return "midday"
        if 14 <= hour <= 17:
            return "afternoon"
        if 18 <= hour <= 19:
            return "evening"
        if 20 <= hour <= 23:
            return "night"
        return "unknown"

    def _estimate_hour_from_time_of_day(self, time_of_day: str) -> int:
        """
        Estimate a reasonable hour value from a time of day description.
        Used for migration when we have time_of_day but no hour.

        Args:
            time_of_day: String description like "Morning", "Evening", etc.

        Returns:
            Integer hour value (0-23)
        """
        time_mapping = {
            "deep night": 2,  # Middle of deep night
            "dawn": 6,  # Dawn hour
            "morning": 9,  # Mid-morning
            "midday": 12,  # Noon
            "afternoon": 15,  # Mid-afternoon
            "evening": 18,  # Early evening
            "night": 21,  # Mid-night
        }

        # Normalize and look up
        normalized = time_of_day.lower().strip()
        return time_mapping.get(normalized, 12)  # Default to noon if unknown

    # =========================================================================
    # XP/Level Validation Methods
    # =========================================================================

    def validate_xp_level(self, strict: bool = False) -> dict[str, Any]:  # noqa: PLR0912,PLR0915
        """
        Validate that the player's level matches their XP using D&D 5e thresholds.

        In default mode (strict=False):
        - Auto-corrects level mismatches and logs warnings
        - Clamps invalid XP/level values to valid ranges

        In strict mode (strict=True):
        - Raises ValueError on XP/level mismatch

        Args:
            strict: If True, raise ValueError on mismatches instead of auto-correcting

        Returns:
            Dict with validation results (flags describe the original input; corrected
            fields describe applied fixes):
            - valid: True if XP/level matched before any corrections or were missing
            - corrected: True if level was auto-corrected
            - expected_level: Computed level from XP
            - provided_level: Original level value
            - clamped_xp: XP after clamping (if negative)
            - clamped_level: Level after clamping (if out of range)

        Raises:
            ValueError: In strict mode, if XP/level mismatch is detected
        """
        result: dict[str, Any] = {"valid": True}

        pc_data = self.player_character_data
        if not isinstance(pc_data, dict) or not pc_data:
            return result  # No structured player data to validate

        # Get XP value - handle different possible structures
        # Supports: experience.current (dict), experience (scalar int/str), xp, xp_current
        xp_raw = None
        experience_val = pc_data.get("experience")
        if isinstance(experience_val, dict):
            # Experience stored as {"current": 2700, ...}
            xp_raw = experience_val.get("current")
        elif experience_val is not None:
            # Experience stored as scalar (int or str like 2700 or "2700")
            xp_raw = experience_val
        elif "xp" in pc_data:
            xp_raw = pc_data.get("xp")
        elif "xp_current" in pc_data:
            xp_raw = pc_data.get("xp_current")

        # Get level value (raw, before coercion)
        provided_level_raw = pc_data.get("level")

        # Coerce XP to int for type safety (handles strings from JSON/LLM)
        if xp_raw is None:
            # If no XP, assume 0 for level 1 character
            xp = 0
            result["assumed_xp"] = 0
        else:
            xp = _coerce_int(xp_raw, 0)

        # Coerce level to int if present (handles strings from JSON/LLM)
        provided_level = None
        if provided_level_raw is not None:
            provided_level = _coerce_int(provided_level_raw, None)

        # Clamp negative XP
        if xp < 0:
            result["clamped_xp"] = 0
            xp = 0
            # Persist clamped XP back to every known XP field to avoid divergence
            if isinstance(experience_val, dict):
                pc_data["experience"]["current"] = 0
            if experience_val is not None and not isinstance(experience_val, dict):
                pc_data["experience"] = 0
            if "xp" in pc_data:
                pc_data["xp"] = 0
            if "xp_current" in pc_data:
                pc_data["xp_current"] = 0
            logging_util.warning("XP validation: Negative XP clamped to 0")

        # Calculate expected level from XP
        expected_level = level_from_xp(xp)
        result["expected_level"] = expected_level

        # Handle missing level - compute from XP and PERSIST to state
        if provided_level is None:
            result["computed_level"] = expected_level
            # Persist computed level to state
            if hasattr(self, "player_character_data") and isinstance(
                self.player_character_data, dict
            ):
                self.player_character_data["level"] = expected_level
            return result

        # Store original level BEFORE clamping (per docstring: "Original level value")
        result["provided_level"] = provided_level

        # Clamp level minimum to 1 (no max - epic levels 21+ allowed)
        if provided_level < 1:
            result["clamped_level"] = 1
            logging_util.warning(f"XP validation: Level {provided_level} clamped to 1")
            provided_level = 1
            if hasattr(self, "player_character_data") and isinstance(
                self.player_character_data, dict
            ):
                self.player_character_data["level"] = provided_level
        elif provided_level > 20:
            # Epic levels (21+) are allowed for epic/mythic campaigns
            # Log as info, not warning - this is intentional for epic play
            result["epic_level"] = True
            logging_util.info(
                f"Epic level detected: Level {provided_level} (beyond standard D&D 5e cap)"
            )

        # Check for mismatch (skip XP validation for epic levels 21+)
        # Epic levels are set by the LLM for epic/mythic campaigns and don't follow XP table
        if provided_level > 20:
            # Epic level - valid by definition, no XP-based validation needed
            result["valid"] = True
            result["epic_level"] = True
            return result

        if provided_level != expected_level:
            result["valid"] = False

            message = (
                f"XP/Level mismatch: XP={xp} should be Level {expected_level}, "
                f"but provided Level {provided_level}"
            )

            if strict:
                raise ValueError(message)

            # For the current structured schema (experience={"current": ...}), level-ups are
            # handled by the rewards_pending flow rather than server-side mutation.
            #
            # For legacy/compat schemas (scalar experience/xp fields), auto-correct to keep
            # state consistent and tests deterministic.
            if expected_level > provided_level:
                if isinstance(experience_val, dict):
                    logging_util.info(
                        f"XP validation: {message} - level-up detected, letting LLM handle via rewards_pending"
                    )
                    result["level_up_pending"] = True
                else:
                    # Do NOT set "corrected" flag when no actual correction happens
                    # Only set level_up_pending to indicate LLM should handle the level-up
                    result["level_up_pending"] = True  # Ensure test detects level up
                    logging_util.warning(
                        f"XP validation: {message} - flagging level up mismatch (legacy XP schema, LLM will handle)"
                    )
                    # Do NOT auto-correct level upwards - let the user/LLM process the level up
                    # if hasattr(self, "player_character_data") and isinstance(
                    #     self.player_character_data, dict
                    # ):
                    #     self.player_character_data["level"] = expected_level
                    #     result["corrected_level"] = expected_level
            else:
                # Level regression/mismatch: stored level is HIGHER than XP indicates
                # This is a data integrity issue - auto-correct it
                result["corrected"] = True
                logging_util.warning(
                    f"XP validation: {message} - auto-correcting level regression"
                )
                if hasattr(self, "player_character_data") and isinstance(
                    self.player_character_data, dict
                ):
                    self.player_character_data["level"] = expected_level
                    result["corrected_level"] = expected_level

        return result

    # =========================================================================
    # Time Monotonicity Validation Methods
    # =========================================================================

    def validate_time_monotonicity(
        self,
        new_time: dict[str, Any],
        strict: bool = False,
        previous_time: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Validate that time progression is monotonic (never goes backwards).

        Args:
            new_time: Dict with time fields (hour, minute, optionally day)
            strict: If True, raise ValueError on backwards time

        Returns:
            Dict with validation results.
        """
        result: dict[str, Any] = {"valid": True}

        # Get reference time: prefer explicitly supplied previous_time (from caller),
        # otherwise fall back to the GameState's current world_data value.
        current_world_time = previous_time or (self.world_data or {}).get("world_time")
        if not current_world_time or not isinstance(current_world_time, dict):
            return result

        if not isinstance(new_time, dict):
            return result

        current_day = None
        current_month = None
        current_year = None
        if isinstance(current_world_time, dict):
            current_day = current_world_time.get("day")
            current_month = current_world_time.get("month")
            current_year = current_world_time.get("year")

        old_total = self._time_to_minutes(current_world_time)
        new_total = self._time_to_minutes(
            new_time,
            default_day=current_day,
            default_month=current_month,
            default_year=current_year,
        )

        if new_total < old_total:
            old_str = self._format_time(current_world_time)
            new_str = self._format_time(new_time)
            message = f"Time regression detected: {new_str} is earlier than {old_str}"

            if strict:
                raise ValueError(f"Time cannot go backwards: {message}")

            result["valid"] = True  # Still valid but with warning
            result["warning"] = True
            result["message"] = message
            logging_util.warning(f"Time monotonicity: {message}")

        return result

    def _time_to_minutes(
        self,
        time_dict: dict[str, Any],
        default_day: int | None = None,
        default_month: int | None = None,
        default_year: int | None = None,
    ) -> int:
        """
        Convert a time dict to total minutes for comparison.

        Assumes: 1 year = 12 months, 1 month = 30 days (game time approximation).
        """
        # Extract year and month (default to 0 if not present for backward compatibility)
        fallback_year = 0 if default_year is None else _coerce_int(default_year, 0)
        fallback_month = 0 if default_month is None else _coerce_int(default_month, 0)
        year = _coerce_int(time_dict.get("year", fallback_year), fallback_year)
        month = _coerce_int(time_dict.get("month", fallback_month), fallback_month)

        fallback_day = 0 if default_day is None else _coerce_int(default_day, 0)
        day = _coerce_int(time_dict.get("day", fallback_day), fallback_day)
        hour = _coerce_int(time_dict.get("hour", 0), 0)
        minute = _coerce_int(time_dict.get("minute", 0), 0)

        # Months are 1-indexed (1-12) in game data; convert to a 0-based offset for math.
        # Preserve backward compatibility: month <= 0 contributes 0 months.
        month_offset = max(month - 1, 0)

        # Calculate total minutes including year and month
        # 1 year = 12 months, 1 month = 30 days
        return (
            (year * 12 * 30 * 24 * 60)
            + (month_offset * 30 * 24 * 60)
            + (day * 24 * 60)
            + (hour * 60)
            + minute
        )

    def _format_time(self, time_dict: dict[str, Any]) -> str:
        """Format a time dict as a human-readable string."""
        year_raw = time_dict.get("year")
        year = _coerce_int(year_raw, None) if year_raw is not None else None
        month_raw = time_dict.get("month")
        month = _coerce_int(month_raw, None) if month_raw is not None else None
        day_raw = time_dict.get("day")
        day = _coerce_int(day_raw, None) if day_raw is not None else None
        hour = _coerce_int(time_dict.get("hour", 0), 0)
        minute = _coerce_int(time_dict.get("minute", 0), 0)

        # Build time string with available components
        parts = []
        if year is not None:
            era = time_dict.get("era")
            if era is not None and str(era).strip():
                parts.append(f"{year} {str(era).strip()}")
            else:
                parts.append(f"{year}")
        if month is not None:
            parts.append(f"Month {month}")
        if day is not None:
            parts.append(f"Day {day}")

        time_part = f"{hour:02d}:{minute:02d}"

        if parts:
            return f"{', '.join(parts)}, {time_part}"
        return time_part

    # =========================================================================
    # Character Identity Methods
    # =========================================================================

    def get_character_identity_block(self) -> str:
        """
        Generate a character identity block for system prompts.

        This ensures the LLM always has access to immutable character facts
        like name, gender, pronouns, and key relationships.

        Returns:
            Formatted string block for system prompts
        """
        pc = self.player_character_data
        if not pc or not isinstance(pc, dict):
            return ""

        lines = ["## Character Identity (IMMUTABLE)"]

        # Name
        name = pc.get("name")
        if name:
            lines.append(f"- **Name**: {name}")

        # Gender and pronouns - handle None values properly
        # Note: .get("gender", "") returns None if key exists with None value
        gender_raw = pc.get("gender")
        gender = str(gender_raw).lower() if gender_raw else ""
        if gender:
            if gender in ("female", "woman", "f"):
                lines.append("- **Gender**: Female (she/her)")
                lines.append(
                    "- **NEVER** refer to this character as 'he', 'him', "
                    "or use male-gendered familial terms for them"
                )
            elif gender in ("male", "man", "m"):
                lines.append("- **Gender**: Male (he/him)")
                lines.append(
                    "- **NEVER** refer to this character as 'she', 'her', "
                    "or use female-gendered familial terms for them"
                )
            else:
                lines.append(f"- **Gender**: {gender}")

        # Race
        race = pc.get("race")
        if race:
            lines.append(f"- **Race**: {race}")

        # Class
        char_class = pc.get("class") or pc.get("character_class")
        if char_class:
            lines.append(f"- **Class**: {char_class}")

        # Key relationships (from backstory or explicit field)
        relationships = pc.get("relationships", {})
        if isinstance(relationships, dict) and relationships:
            lines.append("- **Key Relationships**:")
            for rel_name, rel_type in relationships.items():
                lines.append(f"  - {rel_name}: {rel_type}")

        # Parentage (important for characters like Alexiel)
        parentage = pc.get("parentage") or pc.get("parents")
        if parentage:
            if isinstance(parentage, dict):
                for parent_type, parent_name in parentage.items():
                    lines.append(f"- **{parent_type.title()}**: {parent_name}")
            elif isinstance(parentage, str):
                lines.append(f"- **Parentage**: {parentage}")

        # Active Effects (buffs, conditions, persistent effects)
        # These MUST be applied to all relevant rolls and checks
        active_effects = pc.get("active_effects", [])
        if active_effects and isinstance(active_effects, list):
            lines.append("")
            lines.append("### Active Effects (ALWAYS APPLY)")
            lines.append(
                "The following buffs/effects are ALWAYS active and MUST be applied "
                "to all relevant rolls, checks, saves, and combat calculations:"
            )
            for effect in active_effects:
                if isinstance(effect, str) and effect.strip():
                    lines.append(f"  - {effect}")
                elif isinstance(effect, dict):
                    effect_name = (
                        effect.get("name") or effect.get("effect") or str(effect)
                    )
                    lines.append(f"  - {effect_name}")

        if len(lines) == 1:
            return ""  # Only header, no actual data

        return "\n".join(lines)

    # =========================================================================
    # God Mode Directive Management
    # =========================================================================

    def add_god_mode_directive(self, directive: str) -> None:
        """
        Add a God Mode directive to the campaign rules.

        These directives persist across sessions and are injected into prompts.

        Args:
            directive: The rule to add (e.g., "always award XP after combat")
        """
        if "god_mode_directives" not in self.custom_campaign_state:
            self.custom_campaign_state["god_mode_directives"] = []

        directives = self.custom_campaign_state["god_mode_directives"]

        # Check for duplicates
        existing_texts = [
            d.get("rule") if isinstance(d, dict) else d for d in directives
        ]
        if directive not in existing_texts:
            directives.append(
                {
                    "rule": directive,
                    "added": datetime.datetime.now(datetime.UTC).isoformat(),
                }
            )
            logging_util.info(f"GOD MODE DIRECTIVE ADDED: {directive}")

    def get_god_mode_directives(self) -> list[str]:
        """
        Get all active God Mode directives as a list of strings.

        Returns:
            List of directive rule strings
        """
        directives = self.custom_campaign_state.get("god_mode_directives", [])
        result = []
        for d in directives:
            if isinstance(d, dict):
                result.append(d.get("rule", str(d)))
            else:
                result.append(str(d))
        return result

    def get_god_mode_directives_block(self) -> str:
        """
        Generate a formatted block of God Mode directives for system prompts.

        Returns:
            Formatted string block for system prompts
        """
        directives = self.get_god_mode_directives()
        if not directives:
            return ""

        lines = ["## Active God Mode Directives"]
        lines.append("The following rules were set by the player and MUST be followed:")
        for i, directive in enumerate(directives, 1):
            lines.append(f"{i}. {directive}")

        return "\n".join(lines)

    # =========================================================================
    # Campaign Upgrade Detection (Divine/Multiverse Tiers)
    # =========================================================================
    # Delegated to campaign_divine.py module for maintainability

    def get_campaign_tier(self) -> str:
        """Get the current campaign tier (mortal, divine, or sovereign)."""
        return _get_campaign_tier(self.custom_campaign_state)

    def is_divine_upgrade_available(self) -> bool:
        """
        Check if divine upgrade (mortal → divine) is available.

        Triggers:
        - divine_potential >= 100
        - Level >= 25
        - divine_upgrade_available flag set by narrative milestone
        """
        return _is_divine_upgrade_available(
            self.custom_campaign_state, self.player_character_data
        )

    def is_multiverse_upgrade_available(self) -> bool:
        """
        Check if multiverse upgrade (any tier → sovereign) is available.

        Triggers:
        - universe_control >= 70
        - multiverse_upgrade_available flag set by narrative milestone
        """
        return _is_multiverse_upgrade_available(self.custom_campaign_state)

    def is_campaign_upgrade_available(self) -> bool:
        """Check if any campaign upgrade is currently available."""
        return _is_campaign_upgrade_available(
            self.custom_campaign_state, self.player_character_data
        )

    def get_pending_upgrade_type(self) -> str | None:
        """
        Get the type of upgrade that's currently available.

        Returns:
            "divine" if divine upgrade is available
            "multiverse" if multiverse upgrade is available
            None if no upgrade is available
        """
        return _get_pending_upgrade_type(
            self.custom_campaign_state, self.player_character_data
        )

    def get_highest_stat_modifier(self) -> int:
        """
        Get the highest ability score modifier for GP calculation.

        Used for converting stats to God Power in divine/sovereign tiers.
        """
        return _get_highest_stat_modifier(self.player_character_data)

    # =========================================================================
    # Divine Rank System (Level-Based Progression)
    # =========================================================================

    def get_character_level(self) -> int:
        """
        Get the character's current level.

        Returns:
            Character level (defaults to 1 if not found or invalid)
        """
        # Level may be at top-level (normalized) or in experience dict
        # Guard against non-dict player_character_data (Firestore can persist nulls)
        pc_data = (
            self.player_character_data
            if isinstance(self.player_character_data, dict)
            else {}
        )
        level_raw = pc_data.get("level", None)
        if level_raw is None:
            experience = pc_data.get("experience", {})
            level_raw = (
                experience.get("level", 1) if isinstance(experience, dict) else 1
            )
        try:
            level = int(level_raw) if level_raw else 1
        except (ValueError, TypeError):
            level = 1
        return max(1, level)  # Ensure at least level 1

    def get_divine_rank(self) -> str:
        """
        Get the divine rank name based on character level.

        Uses constants.get_divine_rank_from_level() for calculation.

        Returns:
            Divine rank constant (e.g., "minor_god", "lesser_deity")
        """
        level = self.get_character_level()
        return constants.get_divine_rank_from_level(level)

    def get_divine_rank_display_name(self) -> str:
        """
        Get the display name for the character's divine rank.

        Returns:
            Human-readable rank name (e.g., "Minor God", "Lesser Deity")
        """
        rank = self.get_divine_rank()
        return constants.DIVINE_RANK_DISPLAY_NAMES.get(rank, "Mortal")

    def get_divine_rank_bonus(self) -> int:
        """
        Get the divine rank bonus for the character.

        This bonus is applied to:
        - AC (Divine Defense)
        - Attack rolls (Divine Strike)
        - Saving throws (Divine Resilience)
        - Ability checks (Divine Competence)
        - Spell DCs (Divine Authority)

        Returns:
            Divine rank bonus (0-6+)
        """
        level = self.get_character_level()
        return constants.get_divine_rank_bonus(level)

    def get_divine_safe_limit(self) -> int:
        """
        Get the safe leverage limit for the character.

        Using Divine Leverage beyond this limit generates Dissonance.
        Safe Limit = Divine Rank × 5

        Returns:
            Safe leverage limit (0, 5, 10, 15, 20, 25, 30)
        """
        level = self.get_character_level()
        return constants.get_divine_safe_limit(level)

    def get_xp_for_next_level(self) -> int:
        """
        Get the XP required to reach the next level.

        Returns:
            XP needed for next level
        """
        level = self.get_character_level()
        return constants.get_xp_for_level(level + 1)

    def get_xp_to_next_level(self) -> int:
        """
        Get the XP needed to advance from current level to next.

        Returns:
            XP delta needed for next level
        """
        level = self.get_character_level()
        return constants.get_xp_to_next_level(level)

    def get_divine_immunities(self) -> list[str]:
        """
        Get the list of immunities granted by divine rank.

        Immunities are cumulative as divine rank increases.

        Returns:
            List of immunity names (e.g., ["sleep", "paralysis", "charm"])
        """
        level = self.get_character_level()
        return constants.get_divine_immunities(level)

    def is_epic_level(self) -> bool:
        """
        Check if the character is at epic level (21+).

        Returns:
            True if level 21 or higher
        """
        return constants.is_epic_level(self.get_character_level())

    def is_divine_level(self) -> bool:
        """
        Check if the character has divine rank bonuses (26+).

        Returns:
            True if level 26 or higher (Quasi-Deity+)
        """
        return constants.is_divine_level(self.get_character_level())

    def get_divine_leverage_bonus(self) -> int:
        """
        Calculate the total Divine Leverage bonus.

        Divine Leverage = Highest Ability Modifier + Divine Rank Bonus

        This replaces the separate DPP system with scaled stats.

        Returns:
            Total leverage bonus available
        """
        highest_mod = self.get_highest_stat_modifier()
        rank_bonus = self.get_divine_rank_bonus()
        return highest_mod + rank_bonus

    # =========================================================================
    # Post-Combat Reward Detection
    # =========================================================================

    def detect_post_combat_issues(
        self,
        previous_combat_state: dict[str, Any] | None,
        state_changes: dict[str, Any],
    ) -> list[str]:
        """
        Detect issues after combat ends, such as missing XP awards.

        Args:
            previous_combat_state: Combat state before the update
            state_changes: The state changes being applied

        Returns:
            List of warning messages
        """
        warnings: list[str] = []

        # Normalize inputs - handle None and non-dict types
        if not previous_combat_state or not isinstance(previous_combat_state, dict):
            return warnings
        if not isinstance(state_changes, dict):
            state_changes = {}

        was_in_combat = previous_combat_state.get("in_combat", False)
        is_now_in_combat = self.combat_state.get("in_combat", False)

        # Check if combat just ended
        if was_in_combat and not is_now_in_combat:
            # Check if XP was awarded in the state changes
            # Use `or {}` to handle explicit null values in state_changes
            pc_changes = state_changes.get("player_character_data") or {}
            if not isinstance(pc_changes, dict):
                pc_changes = {}
            xp_awarded = False

            # Check various XP fields
            if "xp" in pc_changes or "xp_current" in pc_changes:
                xp_awarded = True
            elif "experience" in pc_changes:
                exp_changes = pc_changes["experience"]
                if (
                    isinstance(exp_changes, dict)
                    and "current" in exp_changes
                    or isinstance(exp_changes, (int, float, str))
                ):
                    xp_awarded = True

            if not xp_awarded:
                # Count only defeated enemies (hp <= 0, excluding player/allies)
                combatants = previous_combat_state.get("combatants") or {}
                if not isinstance(combatants, dict):
                    combatants = {}
                defeated_count = sum(
                    1
                    for combatant in combatants.values()
                    if isinstance(combatant, dict)
                    and _coerce_int(combatant.get("hp_current", 1), 1) <= 0
                    and not combatant.get("is_player", False)
                    and not combatant.get("is_ally", False)
                )
                if defeated_count == 0:
                    # Fallback to combat_summary if combatants were already cleaned up
                    combat_summary = previous_combat_state.get("combat_summary")
                    if isinstance(combat_summary, dict):
                        enemies_defeated = combat_summary.get("enemies_defeated", 0)
                        enemies_defeated_int = _coerce_int(enemies_defeated, 0)
                        defeated_count = max(defeated_count, enemies_defeated_int)
                if defeated_count > 0:
                    warnings.append(
                        f"Combat ended but no XP was awarded. "
                        f"Consider awarding XP for {defeated_count} defeated enemy/enemies."
                    )

        return warnings


@overload
def validate_and_correct_state(
    state_dict: dict[str, Any],
    previous_world_time: dict[str, Any] | None = None,
    return_corrections: Literal[False] = False,
) -> dict[str, Any]: ...


@overload
def validate_and_correct_state(
    state_dict: dict[str, Any],
    previous_world_time: dict[str, Any] | None = None,
    return_corrections: Literal[True] = ...,
) -> tuple[dict[str, Any], list[str]]: ...


def validate_and_correct_state(
    state_dict: dict[str, Any],
    previous_world_time: dict[str, Any] | None = None,
    return_corrections: bool = False,
) -> dict[str, Any] | tuple[dict[str, Any], list[str]]:
    """
    Validate state dict and apply corrections before persistence.

    Uses GameState's internal validation logic.

    Args:
        state_dict: The state dictionary to validate
        previous_world_time: Previous world time for monotonicity check
        return_corrections: If True, returns tuple of (state, corrections_list)

    Returns:
        If return_corrections=False: corrected state dict
        If return_corrections=True: tuple of (corrected state dict, list of correction messages)

    Note:
        Schema validation failures are non-blocking (warning-only) by design.
        Errors are added to the corrections list for visibility but do not raise.
    """
    corrections: list[str] = []

    # First apply the one-time schema migration marker and normalize obvious legacy shapes.
    # This ensures runtime schema validation can be strict without breaking older persisted
    # payloads (e.g. legacy player_character_data={}).
    normalized_state = state_dict.copy()
    normalized_state, migration_applied = migrate_legacy_state_for_schema(normalized_state)
    if migration_applied:
        corrections.append("Applied one-time schema migration for legacy compatibility")

    # Normalize common legacy/drifted fields into canonical locations before running
    # validations so persistence always writes schema-compliant payloads.
    pc = normalized_state.get("player_character_data")
    custom_state = normalized_state.get("custom_campaign_state")
    if not isinstance(custom_state, dict):
        custom_state = {}
        normalized_state["custom_campaign_state"] = custom_state

    if isinstance(pc, dict):
        pc_copy = copy.deepcopy(pc)
        _canonicalize_player_character_data_in_place(
            pc_copy,
            custom_campaign_state=custom_state,
            corrections_out=corrections,
        )

        # REV-uqjo: Normalize hit_dice format (LLM outputs current/max, schema expects used/total)
        resources = pc_copy.get("resources")
        if isinstance(resources, dict):
            hit_dice = resources.get("hit_dice")
            if isinstance(hit_dice, dict):
                # Check if LLM used current/max format
                if "current" in hit_dice and "max" in hit_dice and "used" not in hit_dice:
                    current = hit_dice.get("current", 0)
                    max_dice = hit_dice.get("max", 0)
                    # Convert: used = total - current, total = max
                    used = max_dice - current
                    resources["hit_dice"] = {"used": used, "total": max_dice}
                    corrections.append(
                        f"Normalized hit_dice from current/max to used/total format: "
                        f"current={current}, max={max_dice} -> used={used}, total={max_dice}"
                    )

        normalized_state["player_character_data"] = pc_copy

    social_hp = normalized_state.get("social_hp_challenge")
    if isinstance(social_hp, dict):
        _canonicalize_social_hp_challenge_in_place(social_hp, corrections_out=corrections)

    _canonicalize_god_mode_directives_in_place(custom_state, corrections_out=corrections)
    _canonicalize_arc_milestones_in_place(custom_state, corrections_out=corrections)

    # Create temporary GameState to run validations
    temp_state = GameState.from_dict(normalized_state)
    if temp_state is None:
        logging_util.warning(
            "VALIDATION: Could not create GameState from dict, skipping validation"
        )
        if return_corrections:
            return state_dict, corrections
        return state_dict

    # 1. XP/Level Validation (non-strict by design)
    # We auto-correct XP/level drift to preserve forward progress.
    # Schema validation failures are warning-only and do not block persistence.
    xp_result = temp_state.validate_xp_level(strict=False)
    if xp_result.get("corrected"):
        provided = xp_result.get("provided_level")
        expected = xp_result.get("expected_level")
        corrections.append(
            f"Level auto-corrected from {provided} to {expected} based on XP"
        )
        logging_util.info(f"XP Validation applied corrections: {xp_result}")
    elif xp_result.get("computed_level"):
        corrections.append(
            f"Level computed as {xp_result.get('computed_level')} from XP"
        )
        logging_util.info(f"XP Validation applied corrections: {xp_result}")
    if xp_result.get("clamped_xp") is not None:
        corrections.append("Negative XP clamped to 0")
    if xp_result.get("clamped_level") is not None:
        corrections.append(
            f"Level clamped to minimum 1: {xp_result.get('clamped_level')}"
        )
    if xp_result.get("epic_level"):
        corrections.append(
            f"Epic level {xp_result.get('provided_level')} accepted (beyond standard D&D 5e)"
        )

    # 2. Time Monotonicity (non-strict by design)
    # Get current time from world_data in state_dict (not temp_state, as we want to check input)
    new_time = (state_dict.get("world_data", {}) or {}).get("world_time")
    if new_time:
        # Note: In strict mode this raises, in default mode it just warns
        time_result = temp_state.validate_time_monotonicity(
            new_time, strict=False, previous_time=previous_world_time
        )
        if time_result.get("warning"):
            corrections.append(
                f"Time warning: {time_result.get('message', 'time regression detected')}"
            )

    result_state = temp_state.to_dict()

    # 3. JSON Schema Validation (REV-0b5)
    # Validate against schema using ISO-serializable copy, but return raw datetimes
    # WARNING ONLY - Schema validation failures generate GCP logs and user warnings but do not crash
    data_for_validation = temp_state._json_serializable(result_state)
    schema_errors = validate_game_state(data_for_validation)
    schema_errors.extend(_validate_post_migration_schema_invariants(result_state))
    if schema_errors:
        error_msg = "GameState schema validation failed:\n" + "\n".join(schema_errors)
        logging_util.warning(f"VALIDATION FAILURE (non-blocking): {error_msg}")
        # Add to corrections list for visibility without crashing
        corrections.extend(f"Schema validation: {err}" for err in schema_errors)

    if return_corrections:
        return result_state, corrections
    return result_state


def migrate_legacy_state_for_schema(
    state_dict: dict[str, Any],
    *,
    migration_seed: str | None = None,
) -> tuple[dict[str, Any], bool]:
    """Apply one-time legacy->schema migration to a campaign state dict.

    Returns a migrated copy plus a boolean indicating whether migration was applied.
    """
    migrated_state = copy.deepcopy(state_dict) if isinstance(state_dict, dict) else {}
    current_version = _coerce_int(
        migrated_state.get(SCHEMA_MIGRATION_VERSION_FIELD), 0
    )
    if current_version >= SCHEMA_MIGRATION_VERSION:
        return migrated_state, False

    # Ensure minimum required schema marker fields (REV-3q63).
    # Only add defaults if this looks like a real game state (has player_character_data or world_data).
    # This prevents garbage data from passing validation just because migration added required fields.
    looks_like_game_state = (
        "player_character_data" in migrated_state
        or "world_data" in migrated_state
        or "narrative" in migrated_state
    )

    if looks_like_game_state:
        if not isinstance(migrated_state.get("game_state_version"), int):
            migrated_state["game_state_version"] = 1

        # REV-noy4: Add session_id and turn_number if missing for backward compatibility
        if "session_id" not in migrated_state:
            migrated_state["session_id"] = _build_migrated_session_id(
                migrated_state, migration_seed=migration_seed
            )

        if "turn_number" not in migrated_state:
            migrated_state["turn_number"] = 0

    # Legacy payloads commonly persisted player_character_data as {}.
    # Normalize to null semantics before enabling strict checks.
    if migrated_state.get("player_character_data") == {}:
        migrated_state["player_character_data"] = None

    migrated_state[SCHEMA_MIGRATION_VERSION_FIELD] = SCHEMA_MIGRATION_VERSION
    migrated_state[SCHEMA_MIGRATED_AT_FIELD] = dt.now(UTC).isoformat()
    return migrated_state, True


def _validate_post_migration_schema_invariants(state_dict: dict[str, Any]) -> list[str]:
    """Enforce strict invariants only after schema migration has completed."""
    version = _coerce_int(state_dict.get(SCHEMA_MIGRATION_VERSION_FIELD), 0)
    if version < SCHEMA_MIGRATION_VERSION:
        return []

    errors: list[str] = []
    if "game_state_version" not in state_dict:
        errors.append("game_state_version: required after schema migration")

    player_character_data = state_dict.get("player_character_data")
    if player_character_data == {}:
        errors.append(
            "player_character_data: empty object is invalid after schema migration "
            "(use null or a full player character object)"
        )
    elif player_character_data is not None and not isinstance(player_character_data, dict):
        errors.append(
            "player_character_data: must be null or object after schema migration"
        )
    elif isinstance(player_character_data, dict):
        has_identity = any(
            player_character_data.get(field)
            for field in ("entity_id", "string_id", "id", "display_name", "name")
        )
        has_creation_progress = any(
            player_character_data.get(field)
            for field in (
                "class",
                "class_name",
                "level",
                "background",
                "race",
                "subclass",
                "stats",
            )
        )

        missing = [] if has_identity else ["entity_id/display_name (or legacy aliases)"]
        if not has_identity and has_creation_progress:
            missing = []
        if missing:
            errors.append(
                "player_character_data: missing required fields after migration: "
                + ", ".join(missing)
            )
    return errors


def roll_dice(notation: str) -> DiceRollResult:
    """Backward-compatible wrapper around dice.roll_dice."""
    return dice_module.roll_dice(notation)


def roll_with_advantage(notation: str) -> tuple[DiceRollResult, DiceRollResult, int]:
    """Backward-compatible wrapper around dice.roll_with_advantage."""
    return dice_module.roll_with_advantage(notation)


def roll_with_disadvantage(notation: str) -> tuple[DiceRollResult, DiceRollResult, int]:
    """Backward-compatible wrapper around dice.roll_with_disadvantage."""
    return dice_module.roll_with_disadvantage(notation)


def calculate_attack_roll(
    attack_modifier: int, advantage: bool = False, disadvantage: bool = False
) -> dict:
    """Backward-compatible wrapper that keeps monkeypatching stable in tests."""
    notation = (
        f"1d20+{attack_modifier}" if attack_modifier >= 0 else f"1d20{attack_modifier}"
    )

    def _safe_natural_roll(roll: DiceRollResult) -> int:
        if roll.individual_rolls:
            return int(roll.individual_rolls[0])
        return max(0, int(roll.total) - int(roll.modifier))

    if advantage and not disadvantage:
        roll1, roll2, total = roll_with_advantage(notation)
        natural_rolls = [_safe_natural_roll(roll1), _safe_natural_roll(roll2)]
        natural = max(natural_rolls)
        return {
            "rolls": natural_rolls,
            "modifier": attack_modifier,
            "total": total,
            "used_roll": "higher",
            "is_critical": natural == 20,
            "is_fumble": natural_rolls[0] == 1 and natural_rolls[1] == 1,
            "notation": notation,
        }
    if disadvantage and not advantage:
        roll1, roll2, total = roll_with_disadvantage(notation)
        natural_rolls = [_safe_natural_roll(roll1), _safe_natural_roll(roll2)]
        natural = min(natural_rolls)
        return {
            "rolls": natural_rolls,
            "modifier": attack_modifier,
            "total": total,
            "used_roll": "lower",
            "is_critical": natural_rolls[0] == 20 and natural_rolls[1] == 20,
            "is_fumble": natural == 1,
            "notation": notation,
        }
    roll = roll_dice(notation)
    return {
        "rolls": roll.individual_rolls,
        "modifier": attack_modifier,
        "total": roll.total,
        "used_roll": "single",
        "is_critical": roll.natural_20,
        "is_fumble": roll.natural_1,
        "notation": notation,
    }


def calculate_damage(damage_notation: str, is_critical: bool = False) -> DiceRollResult:
    """Backward-compatible wrapper around dice.calculate_damage."""
    return dice_module.calculate_damage(damage_notation, is_critical)


def calculate_skill_check(
    attribute_modifier: int,
    proficiency_bonus: int,
    proficient: bool = False,
    expertise: bool = False,
) -> DiceRollResult:
    """Backward-compatible wrapper around dice.calculate_skill_check."""
    return dice_module.calculate_skill_check(
        attribute_modifier, proficiency_bonus, proficient, expertise
    )


def calculate_saving_throw(
    attribute_modifier: int, proficiency_bonus: int, proficient: bool = False
) -> DiceRollResult:
    """Backward-compatible wrapper around dice.calculate_saving_throw."""
    return dice_module.calculate_saving_throw(
        attribute_modifier, proficiency_bonus, proficient
    )


def calculate_modifier(attribute: int) -> int:
    """Calculate ability modifier from attribute score."""
    return (attribute - 10) // 2


def calculate_proficiency_bonus(level: int) -> int:
    """Get proficiency bonus for a given character level."""
    if level < 1:
        return 2
    if level > 20:
        return 6
    return PROFICIENCY_BY_LEVEL.get(level, 2)


def calculate_armor_class(
    dex_modifier: int, armor_bonus: int = 0, shield_bonus: int = 0
) -> int:
    """Calculate Armor Class."""
    return 10 + dex_modifier + armor_bonus + shield_bonus


def calculate_passive_perception(
    wis_modifier: int, proficient: bool, proficiency_bonus: int
) -> int:
    """Calculate passive Perception score."""
    base = 10 + wis_modifier
    if proficient:
        base += proficiency_bonus
    return base


def xp_for_cr(cr: float) -> int:
    """Get XP award for defeating a creature of given Challenge Rating."""
    return XP_BY_CR.get(cr, 0)


def calculate_resource_depletion(
    current_amount: float,
    depletion_rate: float,
    time_elapsed: float,
    _depletion_unit: str = "per_day",
) -> float:
    """Calculate resource depletion over time."""
    depleted = depletion_rate * time_elapsed
    remaining = current_amount - depleted
    return max(0.0, remaining)


def execute_tool_requests(tool_requests: list[dict]) -> list[dict]:
    """
    Execute a list of tool requests with strict type validation.

    Args:
        tool_requests: List of dicts, each containing "tool" (str) and "args" (dict).

    Returns:
        List of results with tool execution details.
    """
    if not isinstance(tool_requests, list):
        logging_util.error(f"tool_requests must be a list, got {type(tool_requests)}")
        return []

    results = []
    last_faction_power: int | None = None
    for request in tool_requests:
        if not isinstance(request, dict):
            logging_util.error(f"Tool request must be dict, got {type(request)}")
            results.append(
                {
                    "tool": "unknown",
                    "args": {},
                    "result": {"error": f"Invalid request type: {type(request)}"},
                }
            )
            continue

        tool_name = request.get("tool")
        args = request.get("args", {})

        # Strict Type Validation
        if not isinstance(tool_name, str) or not tool_name:
            logging_util.error(
                f"Invalid tool name type or empty: {tool_name} ({type(tool_name)})"
            )
            results.append(
                {
                    "tool": str(tool_name),
                    "args": args if isinstance(args, dict) else {},
                    "result": {"error": "Invalid tool name"},
                }
            )
            continue

        if not isinstance(args, dict):
            logging_util.error(f"Tool args must be dict, got {type(args)}")
            args = {}

        try:
            # Route to appropriate tool handler
            if tool_name in FACTION_TOOL_NAMES:
                if (
                    tool_name == "faction_calculate_ranking"
                    and last_faction_power is not None
                ):
                    # Enforce ranking args to match the latest power tool result.
                    args = dict(args)
                    args["player_faction_power"] = last_faction_power
                result = execute_faction_tool(tool_name, args)
            else:
                # Delegate to the dice tool handler
                result = execute_dice_tool(tool_name, args)
        except Exception as e:
            logging_util.error(f"Tool execution error: {tool_name}: {e}")
            result = {"error": str(e)}

        if tool_name == "faction_calculate_power" and isinstance(result, dict):
            fp_value = result.get("faction_power")
            try:
                last_faction_power = int(fp_value) if fp_value is not None else None
            except (TypeError, ValueError):
                last_faction_power = None

        results.append(
            {
                "tool": tool_name,
                "args": args,
                "result": result,
            }
        )

    return results


def update_game_state_with_tool_results(
    game_state_dict: dict[str, Any],
    tool_results: list[dict],
    turn_number: int | None = None,
) -> dict[str, Any]:
    """Update game_state with faction tool results before Phase 2 LLM call.

    This ensures Phase 2 LLM sees both explicit tool results AND updated game_state
    values, providing consistency reinforcement to prevent LLM from ignoring tool results.

    Only updates read-only calculation tools (faction_calculate_power, faction_calculate_ranking).
    State-modifying tools (build, recruit) already update state through their own mechanisms.

    Args:
        game_state_dict: Game state dictionary to update (will be modified in-place)
        tool_results: List of tool execution results from execute_tool_requests()
        turn_number: Current turn number for timestamp tracking (optional)

    Returns:
        Updated game_state_dict (same reference, modified in-place)

    See bead csz: "Update game state with tool results before Phase 2 LLM call"
    """
    if not isinstance(game_state_dict, dict):
        return game_state_dict

    if not isinstance(tool_results, list):
        return game_state_dict

    custom_campaign_state = game_state_dict.get("custom_campaign_state", {})
    if not isinstance(custom_campaign_state, dict):
        return game_state_dict

    faction_minigame = custom_campaign_state.get("faction_minigame", {})
    if not isinstance(faction_minigame, dict):
        return game_state_dict

    timestamp = dt.now(UTC).isoformat() if turn_number is not None else None

    for tool_result in tool_results:
        if not isinstance(tool_result, dict):
            continue

        tool_name = tool_result.get("tool", "")
        result = tool_result.get("result", {})

        if not isinstance(result, dict):
            continue

        # Only update for read-only calculation tools
        if tool_name == "faction_calculate_power":
            faction_power = result.get("faction_power")
            if faction_power is not None:
                try:
                    fp_value = int(faction_power)
                    old_value = faction_minigame.get("faction_power")

                    # Update game_state (this automatically removes PENDING_CALCULATION if present)
                    faction_minigame["faction_power"] = fp_value
                    if timestamp:
                        faction_minigame["faction_power_last_calculated"] = timestamp

                    # Log state update
                    logging_util.info(
                        logging_util.with_campaign(
                            f"🏰 STATE_UPDATE: faction_power updated {old_value} → {fp_value} from tool result"
                        )
                    )
                except (ValueError, TypeError):
                    logging_util.warning(
                        logging_util.with_campaign(
                            f"🏰 STATE_UPDATE_FAILED: Invalid faction_power value: {faction_power}"
                        )
                    )

        elif tool_name == "faction_calculate_ranking":
            ranking = result.get("rank") or result.get("ranking")
            if ranking is not None:
                try:
                    rank_value = int(ranking)
                    old_value = faction_minigame.get("ranking")

                    # Update game_state (this automatically removes PENDING_CALCULATION if present)
                    faction_minigame["ranking"] = rank_value
                    if timestamp:
                        faction_minigame["ranking_last_calculated"] = timestamp

                    # Log state update
                    logging_util.info(
                        logging_util.with_campaign(
                            f"🏰 STATE_UPDATE: ranking updated {old_value} → {rank_value} from tool result"
                        )
                    )
                except (ValueError, TypeError):
                    logging_util.warning(
                        logging_util.with_campaign(
                            f"🏰 STATE_UPDATE_FAILED: Invalid ranking value: {ranking}"
                        )
                    )

    return game_state_dict


def format_tool_results_text(tool_results: Any) -> str:
    """Format tool execution results into a stable, human-readable prompt snippet.

    Providers use this to inject server-executed dice results back into Phase 2.
    """
    if not isinstance(tool_results, list):
        return ""

    lines: list[str] = []
    for item in tool_results:
        if not isinstance(item, dict):
            continue
        tool_name = item.get("tool")
        result = item.get("result", {})
        if not isinstance(tool_name, str) or not tool_name:
            continue
        if (
            isinstance(result, dict)
            and isinstance(result.get("formatted"), str)
            and result["formatted"]
        ):
            # Keep Phase 2 context tight: formatted strings already embed the exact numbers.
            lines.append(f"- {result['formatted']}")
            continue
        if (
            isinstance(result, dict)
            and isinstance(result.get("error"), str)
            and result["error"]
        ):
            lines.append(f"- {tool_name}: ERROR {result['error']}")
            continue
        # Fallback: last-resort JSON (should be rare)
        try:
            result_str = json.dumps(result, sort_keys=True)
        except TypeError:
            result_str = json.dumps(
                {"error": "unserializable tool result"}, sort_keys=True
            )
        lines.append(f"- {tool_name}: {result_str}")

    return "\n".join(lines)
