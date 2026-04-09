"""
Session Header Utilities - Standardizing and normalizing the game state display.

This module provides functions for formatting, normalizing, and generating
session headers from game state data.
"""

import json
import re
from typing import Any

from mvp_site import constants
from mvp_site.numeric_converters import coerce_int_safe as _coerce_int


def _get_player_character_data(game_state: Any) -> dict[str, Any]:
    """Safely extract player character data from game state objects or dicts."""
    if isinstance(game_state, dict):
        pc_data = game_state.get("player_character_data", {}) or {}
        # Guard against non-dict player_character_data (e.g., list)
        return pc_data if isinstance(pc_data, dict) else {}
    if hasattr(game_state, "player_character_data"):
        pc_data = game_state.player_character_data or {}
        # Guard against non-dict attribute
        return pc_data if isinstance(pc_data, dict) else {}
    return {}


def _get_world_data(game_state: Any) -> dict[str, Any]:
    """Safely extract world data from game state objects or dicts."""
    if isinstance(game_state, dict):
        world_data = game_state.get("world_data", {}) or {}
        return world_data if isinstance(world_data, dict) else {}
    if hasattr(game_state, "world_data"):
        world_data = game_state.world_data or {}
        return world_data if isinstance(world_data, dict) else {}
    return {}


def normalize_session_header(session_header: str | None) -> str:
    """
    Normalize session_header format to ensure consistent structure.

    Handles:
    1. Dict-as-string format: Converts JSON dict to proper string format
    2. Missing [SESSION_HEADER] prefix: Adds prefix if content exists but prefix missing
    3. Empty/None: Returns empty string (fallback generation handled separately)
    4. Non-string types: Converts dict to string format, drops unsupported types
    """
    # Handle non-string inputs (dict, list, etc.)
    if isinstance(session_header, dict):
        # Direct dict input - convert to string format
        lines = []
        if "Timestamp" in session_header:
            lines.append(f"Timestamp: {session_header['Timestamp']}")
        if "Location" in session_header:
            lines.append(f"Location: {session_header['Location']}")
        if "Status" in session_header:
            lines.append(f"Status: {session_header['Status']}")
        if "Conditions" in session_header:
            lines.append(f"Conditions: {session_header['Conditions']}")
        if "Resources" in session_header:
            lines.append(f"Resources: {session_header['Resources']}")
        session_header = "\n".join(lines) if lines else ""
    elif not isinstance(session_header, str):
        # Unsupported types (list, int, etc.) - return empty
        return ""

    if not session_header:
        return ""

    # Handle dict-as-string format (LLM sometimes returns JSON object as string)
    if isinstance(session_header, str) and session_header.strip().startswith("{"):
        try:
            header_dict = json.loads(session_header)
            if isinstance(header_dict, dict):
                # Convert dict to proper session header format
                lines = []
                if "Timestamp" in header_dict:
                    lines.append(f"Timestamp: {header_dict['Timestamp']}")
                if "Location" in header_dict:
                    lines.append(f"Location: {header_dict['Location']}")
                if "Status" in header_dict:
                    lines.append(f"Status: {header_dict['Status']}")
                if "Conditions" in header_dict:
                    lines.append(f"Conditions: {header_dict['Conditions']}")
                if "Resources" in header_dict:
                    lines.append(f"Resources: {header_dict['Resources']}")

                session_header = "\n".join(lines)
        except (json.JSONDecodeError, TypeError):
            pass

    # Ensure [SESSION_HEADER] prefix exists if there's content
    if session_header and "[SESSION_HEADER]" not in session_header:
        session_header = "[SESSION_HEADER]\n" + session_header

    return session_header


def generate_session_header_fallback(game_state: Any) -> str:
    """
    Generate session_header from game_state when LLM omits it.
    """
    pc = _get_player_character_data(game_state)
    world = _get_world_data(game_state)

    lines = []

    # Timestamp
    current_time = world.get("current_time", "Unknown")
    if current_time == "Unknown" and "world_time" in world:
        wt = world["world_time"]
        if isinstance(wt, dict):
            year = wt.get("year", "")
            month = wt.get("month", "")
            day = wt.get("day", "")
            # Ensure hour/minute/second are ints for formatting
            hour = _coerce_int(wt.get("hour"), 0)
            minute = _coerce_int(wt.get("minute"), 0)
            second = _coerce_int(wt.get("second"), 0)
            # Use dynamic era if available, default to DR for backward compatibility
            era = wt.get("era", "DR")
            current_time = (
                f"{year} {era}, {month} {day}, {hour:02d}:{minute:02d}:{second:02d}"
            )
    lines.append(f"Timestamp: {current_time}")

    # Location
    location = world.get("current_location", "Unknown")
    lines.append(f"Location: {location}")

    # Status line
    status_parts = []
    level = pc.get("level")
    if level:
        class_name = pc.get("class", "Adventurer")
        status_parts.append(f"Lvl {level} {class_name}")

    hp_current = pc.get("hp_current")
    # Check canonical hp_max first, then fallback to legacy hp_maximum
    hp_maximum = pc.get("hp_max")
    if hp_maximum is None:
        hp_maximum = pc.get("hp_maximum")

    if hp_current is not None and hp_maximum is not None:
        status_parts.append(f"HP: {hp_current}/{hp_maximum}")

    if status_parts:
        lines.append(f"Status: {' | '.join(status_parts)}")

    # Resources (format from game_state)
    resources = pc.get("resources", {})
    if not isinstance(resources, dict):
        resources = {}

    if resources:
        resource_parts = []

        # Hit dice
        hit_dice = resources.get("hit_dice", {})
        if isinstance(hit_dice, dict):
            # Check canonical max, fallback to total (coerce both)
            max_val = _coerce_int(hit_dice.get("max"), None)
            if max_val is None:
                max_val = _coerce_int(hit_dice.get("total"), None)

            if max_val is not None:
                used = _coerce_int(hit_dice.get("used"), 0)
                current = max(0, max_val - used)
                resource_parts.append(f"HD: {current}/{max_val}")

        # Spell slots
        spell_slots = resources.get("spell_slots", {})
        if isinstance(spell_slots, dict):
            spell_parts = []
            for level_key in sorted(
                spell_slots.keys(),
                key=lambda x: int(x.split("_")[-1])
                if x.split("_")[-1].isdigit()
                else 999,
            ):
                slot_data = spell_slots[level_key]
                if isinstance(slot_data, dict) and "max" in slot_data:
                    used = _coerce_int(slot_data.get("used"), 0)
                    max_val = _coerce_int(slot_data.get("max"), 0)
                    current = max(0, max_val - used)
                    level_num = (
                        level_key.split("_")[-1] if "_" in level_key else level_key
                    )
                    spell_parts.append(f"L{level_num} {current}/{max_val}")
            if spell_parts:
                resource_parts.append(f"Spells: {', '.join(spell_parts)}")

        # Class features (bardic inspiration, etc.)
        class_features = resources.get("class_features", {})
        if isinstance(class_features, dict):
            for feature_name, feature_data in class_features.items():
                if isinstance(feature_data, dict) and "max" in feature_data:
                    used = _coerce_int(feature_data.get("used"), 0)
                    max_val = _coerce_int(feature_data.get("max"), 0)
                    current = max(0, max_val - used)
                    feature_display = feature_name.replace("_", " ").title()
                    resource_parts.append(f"{feature_display}: {current}/{max_val}")

        if resource_parts:
            lines.append(f"Resources: {' | '.join(resource_parts)}")
        else:
            lines.append("Resources: None")
    else:
        lines.append("Resources: None")

    return "[SESSION_HEADER]\n" + "\n".join(lines)


def transform_resources_format(session_header: str) -> str:
    """
    Normalize the resources format in the session header.
    (No-op since prompts updated to CURRENT/MAX).
    """
    if not session_header:
        return session_header
    return session_header


def enrich_session_header_with_progress(
    session_header: str | None, game_state: Any
) -> str:
    """Ensure XP and gold are present in the session header for the UI."""

    session_header = session_header or ""

    player_data = _get_player_character_data(game_state)
    xp_current = player_data.get("xp_current")
    xp_next_level = player_data.get("xp_next_level")
    gold_amount = player_data.get("gold")

    contains_xp = re.search(r"\b(XP|experience)\b", session_header, flags=re.IGNORECASE)
    contains_gold = re.search(r"\b(Gold|gp)\b", session_header, flags=re.IGNORECASE)

    remove_prefixes: tuple[str, ...] = ()
    additions: list[str] = []
    if xp_current is not None and not contains_xp:
        xp_text = (
            f"XP: {xp_current}/{xp_next_level}"
            if xp_next_level is not None and xp_next_level != ""
            else f"XP: {xp_current}"
        )
        additions.append(xp_text)
        remove_prefixes += ("xp:", "experience:")

    if gold_amount is not None and not contains_gold:
        additions.append(f"Gold: {gold_amount}gp")
        remove_prefixes += ("gold:", "gp:")

    if not additions:
        return session_header

    def _remove_resource_tokens(tokens: list[str]) -> list[str]:
        if not remove_prefixes:
            return tokens

        return [
            token
            for token in tokens
            if token and not token.lower().strip().startswith(remove_prefixes)
        ]

    lines = session_header.splitlines()
    for idx, line in enumerate(lines):
        if line.strip().startswith("Status:"):
            prefix, _, remainder = line.partition("Status:")
            status_tokens = [part.strip() for part in remainder.split("|")]
            status_tokens = _remove_resource_tokens(status_tokens)
            merged_tokens = [token for token in status_tokens if token]
            merged_tokens.extend(additions)
            lines[idx] = f"{prefix}Status: {' | '.join(merged_tokens)}"
            return "\n".join(lines)

    if lines:
        separator = " | " if lines[-1].strip() else ""
        lines[-1] = f"{lines[-1]}{separator}{' | '.join(additions)}"
    else:
        lines.append(" | ".join(additions))

    return "\n".join(lines)


def ensure_session_header_resources(
    structured_fields: dict[str, Any], game_state: Any
) -> dict[str, Any]:
    """
    Ensures session header is properly formatted and enriched.
    """
    if not structured_fields:
        return structured_fields

    session_header = structured_fields.get(constants.FIELD_SESSION_HEADER, "")

    # Step 1: Normalize format (dict-as-string, missing prefix)
    normalized_header = normalize_session_header(session_header)

    # Step 2: Generate fallback if still empty after normalization
    if not normalized_header or normalized_header.strip() == "[SESSION_HEADER]":
        normalized_header = generate_session_header_fallback(game_state)

    # Step 3: Transform resources format (USED/MAX -> CURRENT/MAX)
    transformed_header = transform_resources_format(normalized_header)

    # Step 4: Enrich with XP and gold
    enriched_header = enrich_session_header_with_progress(
        transformed_header, game_state
    )

    if enriched_header == session_header:
        return structured_fields

    updated_fields = structured_fields.copy()
    updated_fields[constants.FIELD_SESSION_HEADER] = enriched_header
    return updated_fields
