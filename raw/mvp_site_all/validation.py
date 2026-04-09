"""
JSON Schema validation infrastructure for GameState (ADR-0003 Phase 2).

This module provides schema loading, caching, and validation utilities
for runtime game state validation against the canonical schema.
"""

import datetime
import difflib
import json
import os
import re
import time
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from mvp_site import logging_util

# Create format checker with custom date-time support
_FORMAT_CHECKER = FormatChecker()
_RFC3339_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})$"
)


@_FORMAT_CHECKER.checks("date-time", raises=ValueError)
def check_datetime(instance):
    """Check RFC 3339 date-time format (ISO 8601 with Z or offset)."""
    if not isinstance(instance, str):
        return True
    if not _RFC3339_PATTERN.match(instance):
        raise ValueError(f"Invalid date-time: {instance}")
    try:
        datetime.datetime.fromisoformat(instance.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        raise ValueError(f"Invalid date-time: {instance}") from None
    return True


# Cache for loaded schemas
_SCHEMA_CACHE: dict[str, dict[str, Any]] = {}
_VALIDATOR_CACHE: dict[str, Draft202012Validator] = {}
_SCHEMA_WARN_THRESHOLD_MS = 50.0
_CANONICAL_EQUIPMENT_SLOTS_CACHE: set[str] | None = None
_GAME_STATE_TOP_LEVEL_PROPERTIES_CACHE: set[str] | None = None
_SOCIAL_HP_REQUEST_SEVERITY_CACHE: set[str] | None = None
_SOCIAL_HP_SKILLS_CACHE: set[str] | None = None
_TIME_OF_DAY_VALUES_CACHE: set[str] | None = None
_STRICT_OVERLAY_NESTED_KEYS_CACHE: dict[str, set[str]] | None = None
_STORY_ENTRY_VALIDATOR_CACHE: Draft202012Validator | None = None
_PLAYER_CHARACTER_SCHEMA_KEYS_CACHE: set[str] | None = None

# Legacy player-character field names accepted by runtime readers but absent from schema.
_LEGACY_CHARACTER_FIELD_ALIASES: frozenset[str] = frozenset(
    {
        "class_name",
        "spell_slots",
        "conditions",
        "status_effects",
        "personality",
        "backstory",
        "alignment",
        "proficiencies",
        "subclass",
        "player_name",
        "hero_points",
        "inspiration",
    }
)

# Backward-compatible slot aliases accepted by runtime readers.
# Canonical writes should use target values.
_LEGACY_EQUIPMENT_SLOT_ALIASES: dict[str, str] = {
    "weapon_main": "main_hand",
    "weapon_secondary": "off_hand",
    "mainhand": "main_hand",
    "offhand": "off_hand",
    "boots": "feet",
    "gloves": "hands",
    "amulet": "neck",
    "necklace": "neck",
}

# Legacy-but-readable slot names preserved for backward compatibility.
_LEGACY_EQUIPMENT_SLOT_NAMES: set[str] = {
    "weapon",
    "weapons",
    "ring",
    "ring1",
    "ring2",
    "bracers",
    *_LEGACY_EQUIPMENT_SLOT_ALIASES.keys(),
}

_STRICT_RESOURCE_KEYS: set[str] = {
    "gold",
    "hit_dice",
    "spell_slots",
    "class_features",
    "consumables",
}

# Compatibility keys that are valid in state_updates but not yet represented as
# canonical top-level game_state schema properties.
_LEGACY_STATE_UPDATE_TOP_LEVEL_KEYS: set[str] = {
    "frozen_plans",
}

_STRICT_OVERLAY_NESTED_SCHEMA_DEFS: dict[str, str] = {
    "combat_state": "CombatState",
    "encounter_state": "EncounterState",
    "rewards_pending": "RewardsPending",
    "custom_campaign_state": "CustomCampaignState",
}


def _enrich_validation_message(path: str, message: str, validator_name: str) -> str:
    """Add user-actionable hints for common schema failures."""
    if (
        path == "player_character_data"
        and validator_name in {"oneOf", "anyOf"}
        and "not valid under any of the given schemas" in message
    ):
        return (
            f"{message}. For GOD_MODE_UPDATE_STATE, set "
            "'player_character_data' to null or provide a full player character object "
            "with identity fields (for example 'entity_id' and 'display_name')."
        )
    return message


def load_schema(schema_name: str) -> dict[str, Any]:
    """
    Load a JSON Schema from the schemas directory.

    Args:
        schema_name: Name of the schema file (without .schema.json extension)

    Returns:
        Parsed JSON schema as a dictionary

    Raises:
        FileNotFoundError: If schema file doesn't exist
        json.JSONDecodeError: If schema file is invalid JSON
    """
    if schema_name in _SCHEMA_CACHE:
        return _SCHEMA_CACHE[schema_name]

    # Locate schema file
    schema_dir = Path(__file__).parent
    schema_path = schema_dir / f"{schema_name}.schema.json"

    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    # Load and cache
    with open(schema_path, encoding="utf-8") as f:
        schema = json.load(f)

    _SCHEMA_CACHE[schema_name] = schema
    return schema


def get_validator(schema_name: str) -> Draft202012Validator:
    """
    Get a cached JSON Schema validator for the specified schema.

    Args:
        schema_name: Name of the schema (e.g., "game_state")

    Returns:
        Cached Draft202012Validator instance
    """
    if schema_name in _VALIDATOR_CACHE:
        return _VALIDATOR_CACHE[schema_name]

    schema = load_schema(schema_name)
    validator = Draft202012Validator(schema, format_checker=_FORMAT_CHECKER)

    _VALIDATOR_CACHE[schema_name] = validator
    return validator


def validate_game_state(state: dict[str, Any]) -> list[str]:
    """
    Validate a game state dictionary against the canonical schema.

    Args:
        state: Game state dictionary to validate

    Returns:
        List of validation error messages (empty if valid)
    """
    start = time.perf_counter()
    validator = get_validator("game_state")

    errors = []
    for error in validator.iter_errors(state):
        # Format error messages for readability
        path = ".".join(str(p) for p in error.path) if error.path else "root"
        message = _enrich_validation_message(path, error.message, error.validator)
        errors.append(f"{path}: {message}")

    elapsed_ms = (time.perf_counter() - start) * 1000.0
    warn_threshold = float(
        os.getenv("SCHEMA_VALIDATION_WARN_MS", str(_SCHEMA_WARN_THRESHOLD_MS))
    )
    if elapsed_ms > warn_threshold:
        logging_util.warning(
            "Schema validation took %.1fms (threshold %.1fms, errors=%d)",
            elapsed_ms,
            warn_threshold,
            len(errors),
        )

    return errors


def get_story_entry_validator() -> Draft202012Validator:
    """Return validator for the canonical StoryEntry contract."""
    global _STORY_ENTRY_VALIDATOR_CACHE  # noqa: PLW0603
    if _STORY_ENTRY_VALIDATOR_CACHE is not None:
        return _STORY_ENTRY_VALIDATOR_CACHE

    game_state_schema = load_schema("game_state")
    story_entry_schema = {
        "$schema": game_state_schema.get(
            "$schema", "https://json-schema.org/draft/2020-12/schema"
        ),
        "$ref": "#/$defs/StoryEntry",
        "$defs": game_state_schema.get("$defs", {}),
    }
    _STORY_ENTRY_VALIDATOR_CACHE = Draft202012Validator(
        story_entry_schema, format_checker=_FORMAT_CHECKER
    )
    return _STORY_ENTRY_VALIDATOR_CACHE


def validate_story_entry(entry: Any) -> list[str]:
    """Validate a Firestore story entry against the canonical StoryEntry contract."""
    if not isinstance(entry, dict):
        return ["story_entry: must be a dict"]

    validator = get_story_entry_validator()
    errors: list[str] = []
    for error in validator.iter_errors(entry):
        path = ".".join(str(p) for p in error.path) if error.path else "story_entry"
        errors.append(f"{path}: {error.message}")
    return errors


def get_canonical_equipment_slots() -> set[str]:
    """Return canonical equipment slot names derived from game_state schema."""
    global _CANONICAL_EQUIPMENT_SLOTS_CACHE  # noqa: PLW0603
    if _CANONICAL_EQUIPMENT_SLOTS_CACHE is not None:
        return set(_CANONICAL_EQUIPMENT_SLOTS_CACHE)

    schema = load_schema("game_state")
    defs = schema.get("$defs", {})
    character = defs.get("Character", {})
    character_props = character.get("properties", {})

    slots: set[str] = set()

    equipped_items = character_props.get("equipped_items", {})
    for slot_name in equipped_items.get("properties", {}):
        slots.add(slot_name)

    # Runtime alias object includes backpack and may evolve.
    equipment = character_props.get("equipment", {})
    for slot_name in equipment.get("properties", {}):
        slots.add(slot_name)

    _CANONICAL_EQUIPMENT_SLOTS_CACHE = set(slots)
    return set(slots)


def _merge_schema_properties(
    target: dict[str, Any],
    source_def: dict[str, Any],
    definitions: dict[str, Any],
) -> None:
    """Merge properties from a schema fragment, resolving refs/allOf inheritance."""
    if not isinstance(source_def, dict):
        return

    target.update(source_def.get("properties", {}))

    ref_path = source_def.get("$ref")
    if isinstance(ref_path, str) and ref_path.startswith("#/$defs/"):
        ref_name = ref_path.split("/")[-1]
        _merge_schema_properties(target, definitions.get(ref_name, {}), definitions)

    for sub_schema in source_def.get("allOf", []):
        _merge_schema_properties(target, sub_schema, definitions)


def get_player_character_schema_keys() -> set[str]:
    """Return allowed player_character_data keys derived from canonical schema."""
    global _PLAYER_CHARACTER_SCHEMA_KEYS_CACHE  # noqa: PLW0603
    if _PLAYER_CHARACTER_SCHEMA_KEYS_CACHE is not None:
        return set(_PLAYER_CHARACTER_SCHEMA_KEYS_CACHE)

    schema = load_schema("game_state")
    definitions = schema.get("$defs", {})
    pc_def = definitions.get("PlayerCharacter", {})
    pc_props: dict[str, Any] = {}
    _merge_schema_properties(pc_props, pc_def, definitions)

    if not pc_props:
        _merge_schema_properties(pc_props, definitions.get("Character", {}), definitions)

    _PLAYER_CHARACTER_SCHEMA_KEYS_CACHE = set(pc_props) | _LEGACY_CHARACTER_FIELD_ALIASES
    return set(_PLAYER_CHARACTER_SCHEMA_KEYS_CACHE)


def get_legacy_equipment_slot_aliases() -> dict[str, str]:
    """Return legacy->canonical equipment slot alias mapping."""
    return dict(_LEGACY_EQUIPMENT_SLOT_ALIASES)


def get_known_equipment_slots(*, include_legacy: bool = True) -> set[str]:
    """Return known equipment slots for runtime reads (canonical + optional legacy)."""
    slots = get_canonical_equipment_slots()
    if include_legacy:
        slots.update(_LEGACY_EQUIPMENT_SLOT_NAMES)
    return slots


def get_game_state_top_level_properties() -> set[str]:
    """Return canonical top-level game state keys from schema."""
    global _GAME_STATE_TOP_LEVEL_PROPERTIES_CACHE  # noqa: PLW0603
    if _GAME_STATE_TOP_LEVEL_PROPERTIES_CACHE is not None:
        return set(_GAME_STATE_TOP_LEVEL_PROPERTIES_CACHE)

    schema = load_schema("game_state")
    properties = schema.get("properties", {})
    keys = {key for key in properties if isinstance(key, str) and key.strip()}
    _GAME_STATE_TOP_LEVEL_PROPERTIES_CACHE = set(keys)
    return set(keys)


def get_strict_overlay_nested_allowed_keys() -> dict[str, set[str]]:
    """Return strict nested key allowlists for high-risk overlay regions."""
    global _STRICT_OVERLAY_NESTED_KEYS_CACHE  # noqa: PLW0603
    if _STRICT_OVERLAY_NESTED_KEYS_CACHE is not None:
        return {
            key: set(values)
            for key, values in _STRICT_OVERLAY_NESTED_KEYS_CACHE.items()
        }

    schema = load_schema("game_state")
    defs = schema.get("$defs", {})
    allowed: dict[str, set[str]] = {}
    for top_level_key, def_name in _STRICT_OVERLAY_NESTED_SCHEMA_DEFS.items():
        def_schema = defs.get(def_name, {})
        properties = def_schema.get("properties", {})
        keys = {key for key in properties if isinstance(key, str) and key.strip()}
        allowed[top_level_key] = keys

    _STRICT_OVERLAY_NESTED_KEYS_CACHE = {
        key: set(values) for key, values in allowed.items()
    }
    return {key: set(values) for key, values in allowed.items()}


def _get_social_hp_enum_values(property_name: str) -> set[str]:
    """Return enum values for a SocialHPChallenge property from canonical schema."""
    schema = load_schema("game_state")
    social_hp_props = (
        schema.get("$defs", {}).get("SocialHPChallenge", {}).get("properties", {})
    )
    prop_schema = social_hp_props.get(property_name, {})
    raw_values = prop_schema.get("enum", [])
    if not isinstance(raw_values, list):
        return set()
    return {value for value in raw_values if isinstance(value, str) and value.strip()}


def get_social_hp_request_severity_values() -> set[str]:
    """Return canonical request_severity enum values from schema."""
    global _SOCIAL_HP_REQUEST_SEVERITY_CACHE  # noqa: PLW0603
    if _SOCIAL_HP_REQUEST_SEVERITY_CACHE is not None:
        return set(_SOCIAL_HP_REQUEST_SEVERITY_CACHE)

    values = _get_social_hp_enum_values("request_severity")
    _SOCIAL_HP_REQUEST_SEVERITY_CACHE = set(values)
    return set(values)


def get_social_hp_skill_values() -> set[str]:
    """Return canonical skill_used enum values from schema."""
    global _SOCIAL_HP_SKILLS_CACHE  # noqa: PLW0603
    if _SOCIAL_HP_SKILLS_CACHE is not None:
        return set(_SOCIAL_HP_SKILLS_CACHE)

    values = _get_social_hp_enum_values("skill_used")
    _SOCIAL_HP_SKILLS_CACHE = set(values)
    return set(values)


def _get_time_of_day_values() -> set[str]:
    """Return lowercase time_of_day enum values from schema (canonical form)."""
    global _TIME_OF_DAY_VALUES_CACHE  # noqa: PLW0603
    if _TIME_OF_DAY_VALUES_CACHE is not None:
        return set(_TIME_OF_DAY_VALUES_CACHE)

    schema = load_schema("game_state")
    # Get WorldTime definition
    world_time_props = (
        schema.get("$defs", {}).get("WorldTime", {}).get("properties", {})
    )
    time_of_day_schema = world_time_props.get("time_of_day", {})
    raw_values = time_of_day_schema.get("enum", [])

    # Return only lowercase canonical values
    lowercase_values = {
        value.lower() for value in raw_values if isinstance(value, str) and value.strip()
    }
    _TIME_OF_DAY_VALUES_CACHE = set(lowercase_values)
    return set(lowercase_values)


def get_time_of_day_values() -> set[str]:
    """Return lowercase time_of_day enum values from schema."""
    return _get_time_of_day_values()


# Cache for common field paths
_COMMON_FIELD_PATHS_CACHE: dict[str, str] | None = None


def get_common_field_paths() -> dict[str, str]:  # noqa: PLR0912, PLR0915
    """Return commonly-used field paths extracted from schema.

    This provides a schema-driven source of truth for high-traffic nested paths,
    reducing hardcoded string literals in game_state.py.

    Returns a dict mapping semantic names to JSON path strings:
        {
            "pc.resources": "player_character_data.resources",
            "pc.equipment": "player_character_data.equipment",
            "pc.stats": "player_character_data.stats",
            "resource.gold": "player_character_data.resources.gold",
            "resource.hit_dice": "player_character_data.resources.hit_dice",
            "equipment.backpack": "player_character_data.equipment.backpack",
            "world.time": "world_data.world_time",
            "combat.in_combat": "combat_state.in_combat",
            ...
        }

    These can be used to access nested fields safely with schema-derived constants.
    """
    global _COMMON_FIELD_PATHS_CACHE  # noqa: PLW0603
    if _COMMON_FIELD_PATHS_CACHE is not None:
        return dict(_COMMON_FIELD_PATHS_CACHE)

    schema = load_schema("game_state")

    # Extract commonly-used paths from schema (focus on hot paths)
    paths: dict[str, str] = {}

    # Player character data paths
    definitions = schema.get("$defs", {})
    pc_def = definitions.get("PlayerCharacter", {})
    pc_props: dict[str, Any] = {}
    _merge_schema_properties(pc_props, pc_def, definitions)

    # Fallback to Character if PlayerCharacter has no properties
    if not pc_props:
        _merge_schema_properties(pc_props, definitions.get("Character", {}), definitions)

    if pc_props:
        # Resources
        resources_def = pc_props.get("resources", {})
        resources_props: dict[str, Any] = {}
        _merge_schema_properties(resources_props, resources_def, definitions)

        if resources_props:
            for key in resources_props:
                paths[f"pc.resources.{key}"] = f"player_character_data.resources.{key}"
            paths["pc.resources"] = "player_character_data.resources"

        # Equipment
        equipment_def = pc_props.get("equipment", {})
        equipment_props: dict[str, Any] = {}
        _merge_schema_properties(equipment_props, equipment_def, definitions)

        if equipment_props:
            for key in equipment_props:
                paths[f"pc.equipment.{key}"] = f"player_character_data.equipment.{key}"
            paths["pc.equipment"] = "player_character_data.equipment"

        # Stats
        if "stats" in pc_props:
            paths["pc.stats"] = "player_character_data.stats"

        # Experience
        if "experience" in pc_props:
            paths["pc.experience"] = "player_character_data.experience"

        # Health
        if "health" in pc_props:
            paths["pc.health"] = "player_character_data.health"

        # Level
        if "level" in pc_props:
            paths["pc.level"] = "player_character_data.level"

    # World data paths
    world_props = schema.get("$defs", {}).get("WorldData", {}).get("properties", {})
    if world_props:
        if "world_time" in world_props:
            paths["world.time"] = "world_data.world_time"
        if "locations" in world_props:
            paths["world.locations"] = "world_data.locations"
        if "current_location" in world_props:
            paths["world.current_location"] = "world_data.current_location"

    # Combat state paths
    combat_props = schema.get("$defs", {}).get("CombatState", {}).get("properties", {})
    if combat_props:
        for key in combat_props:
            paths[f"combat.{key}"] = f"combat_state.{key}"
        paths["combat.state"] = "combat_state"

    # Custom campaign state paths
    custom_props = (
        schema.get("$defs", {}).get("CustomCampaignState", {}).get("properties", {})
    )
    for key in [
        "arc_milestones",
        "companion_arcs",
        "god_mode_directives",
        "faction_minigame",
    ]:
        if key in custom_props:
            paths[f"custom.{key}"] = f"custom_campaign_state.{key}"

    # Top-level paths
    for top_key in schema.get("properties", {}):
        paths[f"top.{top_key}"] = top_key

    _COMMON_FIELD_PATHS_CACHE = dict(paths)
    return dict(paths)


def validate_state_updates_overlay(
    state_updates: Any,
) -> tuple[list[str], list[str]]:  # noqa: PLR0912, PLR0915
    """Validate strict overlay policy for high-risk state_update regions.

    This is intentionally stricter than canonical schema `additionalProperties` behavior.
    It protects write paths from one-off field drift while preserving backward-compatible
    read behavior in full-state validation.

    Returns:
        Tuple of (warnings, errors). Warnings are non-blocking suggestions,
        errors are actual validation failures that should fail tests.
    """
    if not isinstance(state_updates, dict):
        return [], ["state_updates must be a dict"]

    normalized = dict(state_updates)
    _normalize_dotted_state_update_keys(normalized, corrections=[])
    _canonicalize_frozen_plans_placement(normalized, corrections=[])

    errors: list[str] = []
    warnings: list[str] = []

    allowed_top_level = get_game_state_top_level_properties()
    allowed_top_level.update(_LEGACY_STATE_UPDATE_TOP_LEVEL_KEYS)
    for key in normalized:
        if key not in allowed_top_level:
            suggestions = _get_near_match_suggestions(key, allowed_top_level)
            suggestion_suffix = (
                f" (did you mean: {', '.join(suggestions)})" if suggestions else ""
            )
            errors.append(
                "state_updates."
                f"{key}: unknown top-level key (not in canonical schema)"
                f"{suggestion_suffix}"
            )

    player_data = normalized.get("player_character_data")
    if isinstance(player_data, dict):
        equipment = player_data.get("equipment")
        if isinstance(equipment, dict):
            allowed_equipment_slots = get_known_equipment_slots(include_legacy=True)
            allowed_equipment_slots.add("backpack")
            for slot_name in equipment:
                if slot_name not in allowed_equipment_slots:
                    suggestions = _get_near_match_suggestions(
                        slot_name, allowed_equipment_slots
                    )
                    suggestion_suffix = (
                        f" (did you mean: {', '.join(suggestions)})"
                        if suggestions
                        else ""
                    )
                    # Unknown equipment slots are warnings, not errors
                    warnings.append(
                        "player_character_data.equipment."
                        f"{slot_name}: unknown equipment slot for strict overlay policy"
                        f"{suggestion_suffix}"
                    )

        resources = player_data.get("resources")
        if isinstance(resources, dict):
            for resource_key in resources:
                if resource_key not in _STRICT_RESOURCE_KEYS:
                    suggestions = _get_near_match_suggestions(
                        resource_key, _STRICT_RESOURCE_KEYS
                    )
                    suggestion_suffix = (
                        f" (did you mean: {', '.join(suggestions)})"
                        if suggestions
                        else ""
                    )
                    # Unknown resource keys are warnings, not errors (per "warnings not asserts" philosophy)
                    warnings.append(
                        "player_character_data.resources."
                        f"{resource_key}: unknown resource key for strict overlay policy"
                        f"{suggestion_suffix}"
                    )

    strict_nested_keys = get_strict_overlay_nested_allowed_keys()
    for top_level_key, allowed_nested_keys in strict_nested_keys.items():
        nested = normalized.get(top_level_key)
        if not isinstance(nested, dict):
            continue
        for nested_key in nested:
            if nested_key not in allowed_nested_keys:
                suggestions = _get_near_match_suggestions(
                    nested_key, allowed_nested_keys
                )
                suggestion_suffix = (
                    f" (did you mean: {', '.join(suggestions)})" if suggestions else ""
                )
                # Unknown nested keys are warnings, not errors
                warnings.append(
                    f"{top_level_key}.{nested_key}: unknown key for strict overlay policy"
                    f"{suggestion_suffix}"
                )

    social_hp_challenge = normalized.get("social_hp_challenge")
    if isinstance(social_hp_challenge, dict):
        request_severity = social_hp_challenge.get("request_severity")
        if request_severity is not None:
            if not isinstance(request_severity, str):
                errors.append(
                    "social_hp_challenge.request_severity: must be a string when provided"
                )
            else:
                severity_normalized = request_severity.strip().lower()
                if (
                    severity_normalized
                    and severity_normalized
                    not in get_social_hp_request_severity_values()
                ):
                    errors.append(
                        "social_hp_challenge.request_severity: "
                        f"'{request_severity}' not in canonical enum"
                    )

        skill_used = social_hp_challenge.get("skill_used")
        if skill_used is not None:
            if not isinstance(skill_used, str):
                errors.append(
                    "social_hp_challenge.skill_used: must be a string when provided"
                )
            else:
                normalized_skill = skill_used.strip()
                if (
                    normalized_skill
                    and normalized_skill not in get_social_hp_skill_values()
                    and normalized_skill.title() not in get_social_hp_skill_values()
                ):
                    errors.append(
                        f"social_hp_challenge.skill_used: '{skill_used}' not in canonical enum"
    )

    # Validate time_of_day in world_time with case-insensitive matching
    world_data = normalized.get("world_data")
    if isinstance(world_data, dict):
        world_time = world_data.get("world_time")
        if isinstance(world_time, dict):
            time_of_day = world_time.get("time_of_day")
            if time_of_day is not None:
                if not isinstance(time_of_day, str):
                    errors.append(
                        "world_data.world_time.time_of_day: must be a string when provided"
                    )
                else:
                    normalized_tod = time_of_day.strip().lower()
                    if normalized_tod and normalized_tod not in get_time_of_day_values():
                        errors.append(
                            "world_data.world_time.time_of_day: "
                            f"'{time_of_day}' not in canonical enum (use lowercase: "
                            f"{', '.join(sorted(get_time_of_day_values()))})"
                        )

    # Return warnings and errors separately (warnings are non-blocking)
    return warnings, errors


def sanitize_state_updates_overlay(  # noqa: PLR0912
    state_updates: Any,
) -> tuple[dict[str, Any], list[str]]:
    """Map typo-like keys when possible; otherwise keep unknown keys and report corrections."""
    if not isinstance(state_updates, dict):
        return {}, ["state_updates must be a dict"]

    sanitized: dict[str, Any] = dict(state_updates)
    corrections: list[str] = []

    _normalize_dotted_state_update_keys(sanitized, corrections)
    _canonicalize_frozen_plans_placement(sanitized, corrections)

    def _map_or_keep_unknown_key(
        container: dict[str, Any],
        unknown_key: str,
        allowed_keys: set[str],
        *,
        path_prefix: str,
        reason: str,
    ) -> None:
        suggestions = _get_near_match_suggestions(unknown_key, allowed_keys)
        if suggestions:
            target_key = suggestions[0]
            if target_key not in container:
                container[target_key] = container.pop(unknown_key)
                corrections.append(
                    f"Mapped {path_prefix}.{unknown_key} -> {path_prefix}.{target_key}: "
                    f"{reason} (did you mean: {', '.join(suggestions)})"
                )
                return
            corrections.append(
                f"Kept {path_prefix}.{unknown_key}: {reason} "
                f"(did you mean: {', '.join(suggestions)}; target already present)"
            )
            return

        corrections.append(
            f"Kept {path_prefix}.{unknown_key}: {reason} (no close match)"
        )

    allowed_top_level = get_game_state_top_level_properties()
    allowed_top_level.update(_LEGACY_STATE_UPDATE_TOP_LEVEL_KEYS)
    for key in list(sanitized.keys()):
        if key not in allowed_top_level:
            _map_or_keep_unknown_key(
                sanitized,
                key,
                allowed_top_level,
                path_prefix="state_updates",
                reason="unknown top-level key in strict overlay policy",
            )

    player_data = sanitized.get("player_character_data")
    if isinstance(player_data, dict):
        equipment = player_data.get("equipment")
        if isinstance(equipment, dict):
            allowed_equipment_slots = get_known_equipment_slots(include_legacy=True)
            allowed_equipment_slots.add("backpack")
            for slot_name in list(equipment.keys()):
                if slot_name not in allowed_equipment_slots:
                    _map_or_keep_unknown_key(
                        equipment,
                        slot_name,
                        allowed_equipment_slots,
                        path_prefix="player_character_data.equipment",
                        reason="unknown equipment slot in strict overlay policy",
                    )

        resources = player_data.get("resources")
        if isinstance(resources, dict):
            for resource_key in list(resources.keys()):
                if resource_key not in _STRICT_RESOURCE_KEYS:
                    _map_or_keep_unknown_key(
                        resources,
                        resource_key,
                        _STRICT_RESOURCE_KEYS,
                        path_prefix="player_character_data.resources",
                        reason="unknown resource key in strict overlay policy",
                    )

    strict_nested_keys = get_strict_overlay_nested_allowed_keys()
    for top_level_key, allowed_nested_keys in strict_nested_keys.items():
        nested = sanitized.get(top_level_key)
        if not isinstance(nested, dict):
            continue
        for nested_key in list(nested.keys()):
            if nested_key not in allowed_nested_keys:
                _map_or_keep_unknown_key(
                    nested,
                    nested_key,
                    allowed_nested_keys,
                    path_prefix=f"state_updates.{top_level_key}",
                    reason="unknown key in strict overlay policy",
                )

    # Normalize time_of_day to lowercase in world_time
    world_data = sanitized.get("world_data")
    if isinstance(world_data, dict):
        world_time = world_data.get("world_time")
        if isinstance(world_time, dict):
            time_of_day = world_time.get("time_of_day")
            if time_of_day is not None and isinstance(time_of_day, str):
                normalized_tod = time_of_day.strip().lower()
                if normalized_tod in get_time_of_day_values():
                    if normalized_tod != time_of_day:
                        world_time["time_of_day"] = normalized_tod
                        corrections.append(
                            f"Normalized world_data.world_time.time_of_day: "
                            f"'{time_of_day}' -> '{normalized_tod}'"
                        )

    return sanitized, corrections


def _canonicalize_frozen_plans_placement(
    state_updates: dict[str, Any], corrections: list[str]
) -> None:
    """Canonicalize nested custom_campaign_state.frozen_plans to top-level frozen_plans.

    Historical prompts sometimes emit frozen_plans under custom_campaign_state.
    Overlay policy treats frozen_plans as a legacy top-level key, so we normalize
    placement here to avoid warning noise while preserving payload content.
    """
    custom_state = state_updates.get("custom_campaign_state")
    if not isinstance(custom_state, dict) or "frozen_plans" not in custom_state:
        return

    nested_value = custom_state.get("frozen_plans")
    if "frozen_plans" not in state_updates:
        state_updates["frozen_plans"] = nested_value
        corrections.append(
            "Mapped state_updates.custom_campaign_state.frozen_plans -> "
            "state_updates.frozen_plans: canonicalized legacy frozen plan placement"
        )
    else:
        corrections.append(
            "Kept state_updates.custom_campaign_state.frozen_plans: "
            "state_updates.frozen_plans already present"
        )

    # Remove nested key to avoid strict-overlay unknown-key warning.
    custom_state.pop("frozen_plans", None)


def _normalize_dotted_state_update_keys(
    state_updates: Any, corrections: list[str]
) -> None:
    """Expand dotted top-level keys into nested dict structure in-place.

    Example:
      {"player_character_data.experience.current": 123}
      -> {"player_character_data": {"experience": {"current": 123}}}
    """
    if not isinstance(state_updates, dict):
        return

    dotted_keys = [
        key for key in list(state_updates.keys()) if isinstance(key, str) and "." in key
    ]

    for dotted_key in dotted_keys:
        value = state_updates.get(dotted_key)
        if value is None and dotted_key not in state_updates:
            continue

        path_parts = [part for part in dotted_key.split(".") if part]
        if path_parts and path_parts[0] == "state_updates":
            path_parts = path_parts[1:]
        if len(path_parts) < 2:
            continue
        display_key = ".".join(path_parts)

        current: dict[str, Any] = state_updates
        conflict = False
        for part in path_parts[:-1]:
            existing = current.get(part)
            if existing is None:
                current[part] = {}
                existing = current[part]
            if not isinstance(existing, dict):
                conflict = True
                corrections.append(
                    "Kept state_updates."
                    f"{display_key}: dotted-key normalization conflict at '{part}' "
                    "(existing value is not a dict)"
                )
                break
            current = existing

        if conflict:
            continue

        leaf = path_parts[-1]
        if leaf in current:
            corrections.append(
                "Kept state_updates."
                f"{display_key}: dotted-key target already present"
            )
            continue

        current[leaf] = value
        del state_updates[dotted_key]
        corrections.append(
            "Expanded state_updates." f"{display_key} into nested structure"
        )


def is_valid_game_state(state: dict[str, Any]) -> bool:
    """
    Quick boolean check for game state validity.

    Args:
        state: Game state dictionary to validate

    Returns:
        True if valid, False otherwise
    """
    validator = get_validator("game_state")
    return validator.is_valid(state)


def _normalize_for_similarity(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def _get_near_match_suggestions(
    unknown_key: str, allowed_keys: set[str], max_results: int = 3
) -> list[str]:
    if not unknown_key or not allowed_keys:
        return []

    normalized_to_original: dict[str, str] = {}
    for key in sorted(allowed_keys):
        normalized_to_original.setdefault(_normalize_for_similarity(key), key)

    normalized_unknown = _normalize_for_similarity(unknown_key)
    normalized_candidates = list(normalized_to_original.keys())
    matches = difflib.get_close_matches(
        normalized_unknown, normalized_candidates, n=max_results, cutoff=0.72
    )

    suggestions = [
        normalized_to_original[match]
        for match in matches
        if match in normalized_to_original
    ]
    return list(dict.fromkeys(suggestions))
