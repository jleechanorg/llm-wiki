"""SRD 5.1 stat block mapping for faction units.

Maps faction unit archetypes to D&D 5.1 SRD creature stat blocks.
This mapping is intentionally generic: unit names can come from any genre or era,
but they must resolve to a small set of SRD archetypes for simulation.
Provides scaling functions for elite units based on D&D character levels.

All creatures and stats are from the D&D 5.1 System Reference Document (open license).
"""

from __future__ import annotations

import math
from typing import TypedDict


class SRDStatBlock(TypedDict):
    """D&D 5.1 SRD creature stat block."""

    name: str
    ac: int
    hp: int
    attack_bonus: int
    damage_dice: str
    cr: float
    traits: list[str]


# =============================================================================
# Unit Archetype to SRD Creature Mapping
# =============================================================================

UNIT_TO_SRD_MAP: dict[str, str] = {
    "soldier": "guard",
    "veteran": "veteran",
    "spy": "spy",
    "scout": "scout",
    "assassin": "assassin",
    "elite_6": "knight",
    "elite_10": "gladiator",  # High-level elites (SRD-compliant)
    "gladiator": "gladiator",
}

# Generic aliases so units from any genre map into the same SRD archetypes.
# Keep these as non-IP, role-based labels only.
UNIT_ARCHETYPE_ALIASES: dict[str, str] = {
    # Soldier/infantry
    "infantry": "soldier",
    "trooper": "soldier",
    "rifleman": "soldier",
    "militia": "soldier",
    "garrison": "soldier",
    "guard": "soldier",
    "footman": "soldier",
    "sentinel": "soldier",
    "marine": "soldier",
    # Scout/recon
    "recon": "scout",
    "pathfinder": "scout",
    "ranger": "scout",
    "spotter": "scout",
    # Spy/infiltration
    "agent": "spy",
    "operative": "spy",
    "infiltrator": "spy",
    "saboteur": "spy",
    # Veteran/elite soldiers
    "veteran": "veteran",
    "specialist": "veteran",
    "commando": "veteran",
    "sergeant": "veteran",
    # Assassins
    "assassin": "assassin",
    "sniper": "assassin",
    "hitman": "assassin",
    # Elite archetypes
    "champion": "elite_6",
    "honor_guard": "elite_6",
    "brute": "elite_10",
    "warlord": "elite_10",
}

# Substring keyword mapping for flexible naming.
UNIT_KEYWORD_MAP: dict[str, str] = {
    "elite": "elite_6",
    "assassin": "assassin",
    "sniper": "assassin",
    "spy": "spy",
    "infil": "spy",
    "recon": "scout",
    "scout": "scout",
    "ranger": "scout",
    "veteran": "veteran",
    "commando": "veteran",
    "trooper": "soldier",
    "infantry": "soldier",
    "guard": "soldier",
    "soldier": "soldier",
}


# =============================================================================
# SRD Stat Blocks (D&D 5.1 SRD)
# =============================================================================

SRD_STAT_BLOCKS: dict[str, SRDStatBlock] = {
    "guard": {
        "name": "Guard",
        "ac": 16,
        "hp": 11,
        "attack_bonus": 3,
        "damage_dice": "1d6+1",
        "cr": 0.125,
        "traits": [],
    },
    "veteran": {
        "name": "Veteran",
        "ac": 17,
        "hp": 58,
        "attack_bonus": 5,
        "damage_dice": "1d8+3",
        "cr": 3.0,
        "traits": [],
    },
    "spy": {
        "name": "Spy",
        "ac": 12,
        "hp": 27,
        "attack_bonus": 4,
        "damage_dice": "1d6+2",
        "cr": 1.0,
        "traits": ["sneak_attack"],
    },
    "scout": {
        "name": "Scout",
        "ac": 13,
        "hp": 16,
        "attack_bonus": 4,
        "damage_dice": "1d6+2",
        "cr": 0.5,
        "traits": ["keen_hearing_sight"],
    },
    "knight": {
        "name": "Knight",
        "ac": 18,
        "hp": 52,
        "attack_bonus": 5,
        "damage_dice": "1d8+3",
        "cr": 3.0,
        "traits": ["brave"],
    },
    "assassin": {
        "name": "Assassin",
        "ac": 15,
        "hp": 78,
        "attack_bonus": 6,
        "damage_dice": "1d6+4",
        "cr": 8.0,
        "traits": ["assassinate", "sneak_attack", "evasion"],
    },
    "gladiator": {
        "name": "Gladiator",
        "ac": 16,
        "hp": 112,
        "attack_bonus": 7,
        "damage_dice": "1d12+5",
        "cr": 5.0,
        "traits": ["brave", "brute", "parry"],
    },
}


# =============================================================================
# Public API
# =============================================================================


def _normalize_unit_key(unit_type: str) -> str:
    """Normalize unit labels for consistent alias matching."""
    return unit_type.strip().lower().replace("-", "_").replace(" ", "_")


def resolve_unit_type(unit_type: str) -> str:
    """Resolve a unit label into a canonical archetype.

    Accepts genre-agnostic unit labels (e.g., modern or sci-fi) and maps them
    into a small set of SRD-backed archetypes.
    """
    normalized = _normalize_unit_key(unit_type)

    if normalized in UNIT_TO_SRD_MAP:
        return normalized

    alias_match = UNIT_ARCHETYPE_ALIASES.get(normalized)
    if alias_match is not None:
        return alias_match

    for keyword, mapped in UNIT_KEYWORD_MAP.items():
        if keyword in normalized:
            return mapped

    raise KeyError(f"Unknown unit type: {unit_type}")


def get_srd_stats(unit_type: str) -> SRDStatBlock:
    """Get SRD stat block for a faction unit type.

    Args:
        unit_type: Faction unit type (soldier, spy, elite_6) or a generic alias
            from any genre (infantry, recon, operative, sniper, etc.)

    Returns:
        SRD stat block for the unit

    Raises:
        KeyError: If unit_type is not recognized
    """
    resolved_type = resolve_unit_type(unit_type)
    srd_name = UNIT_TO_SRD_MAP.get(resolved_type)
    if srd_name is None:
        raise KeyError(f"SRD stat block not found for: {resolved_type}")

    stat_block = SRD_STAT_BLOCKS.get(srd_name)
    if stat_block is None:
        raise KeyError(f"SRD stat block not found for: {srd_name}")

    # Return a copy to prevent mutation
    return {
        "name": stat_block["name"],
        "ac": stat_block["ac"],
        "hp": stat_block["hp"],
        "attack_bonus": stat_block["attack_bonus"],
        "damage_dice": stat_block["damage_dice"],
        "cr": stat_block["cr"],
        "traits": stat_block["traits"].copy(),
    }


def scale_srd_unit(base: SRDStatBlock, level: int) -> SRDStatBlock:
    """Scale an SRD stat block based on D&D character level.

    Scaling rules:
    - HP: +10% per level above base (level 6 for elites)
    - Attack bonus: +1 every 4 levels
    - Damage: +1 every 4 levels
    - AC: Constant (no scaling)

    Args:
        base: Base SRD stat block
        level: D&D character level (6-20)

    Returns:
        Scaled stat block
    """
    # Elite base level is 6
    base_level = 6
    levels_above_base = max(0, level - base_level)

    # HP scaling: +10% per level above base
    hp_multiplier = 1.0 + (levels_above_base * 0.1)
    scaled_hp = int(math.ceil(base["hp"] * hp_multiplier))

    # Attack bonus scaling: +1 every 4 levels
    attack_bonus_increase = levels_above_base // 4
    scaled_attack_bonus = base["attack_bonus"] + attack_bonus_increase

    # Damage scaling: +1 every 4 levels
    damage_increase = levels_above_base // 4
    scaled_damage_dice = _scale_damage_dice(base["damage_dice"], damage_increase)

    # CR approximation (rough estimate based on scaling)
    # CR doubles roughly every 3 levels
    cr_multiplier = 2 ** (levels_above_base / 3)
    scaled_cr = base["cr"] * cr_multiplier

    return {
        "name": f"{base['name']} (Level {level})",
        "ac": base["ac"],  # AC constant
        "hp": scaled_hp,
        "attack_bonus": scaled_attack_bonus,
        "damage_dice": scaled_damage_dice,
        "cr": scaled_cr,
        "traits": base["traits"].copy(),
    }


def _scale_damage_dice(damage_dice: str, increase: int) -> str:
    """Scale damage dice by increasing the flat modifier.

    Args:
        damage_dice: Original damage dice (e.g., "1d8+3")
        increase: Amount to add to the flat modifier

    Returns:
        Scaled damage dice string
    """
    if increase == 0:
        return damage_dice

    # Parse damage dice (e.g., "1d8+3")
    if "+" in damage_dice:
        dice_part, modifier_part = damage_dice.split("+")
        modifier = int(modifier_part)
        new_modifier = modifier + increase
        return f"{dice_part}+{new_modifier}"
    if "-" in damage_dice:
        dice_part, modifier_part = damage_dice.split("-")
        modifier = int(modifier_part)
        # Original modifier is negative, so add increase: -modifier + increase
        # Or equivalently: increase - modifier
        new_modifier = increase - modifier
        if new_modifier < 0:
            return f"{dice_part}{new_modifier}"
        return f"{dice_part}+{new_modifier}"
    # No modifier, add one
    return f"{damage_dice}+{increase}"


# =============================================================================
# Battle Simulation Integration
# =============================================================================


def create_unit_group(unit_type: str, count: int, level: int = 6) -> dict:
    """Create a unit group for battle simulation.

    Args:
        unit_type: Faction unit type (soldier, spy, elite_6, etc.)
        count: Number of units in this group
        level: Character level for scaling (default: 6)

    Returns:
        Dict with unit stats and count for battle simulation

    Example:
        >>> group = create_unit_group("soldier", 100)
        >>> group["count"]
        100
        >>> group["stats"]["ac"]
        16
    """
    base_stats = get_srd_stats(unit_type)

    # Scale if level > 6 (for elites)
    if level > 6 and unit_type.startswith("elite"):
        stats = scale_srd_unit(base_stats, level)
    else:
        stats = base_stats

    return {
        "unit_type": unit_type,
        "stats": stats,
        "count": count,
        "remaining": count,  # For tracking casualties in battle
    }


def map_faction_troops(
    soldiers: int = 0,
    spies: int = 0,
    elites: int = 0,
    elite_avg_level: int = 6,
) -> list[dict]:
    """Map faction troop counts to SRD unit groups for battle.

    Args:
        soldiers: Number of soldiers
        spies: Number of spies
        elites: Number of elite units
        elite_avg_level: Average level of elite units (6-20)

    Returns:
        List of unit groups ready for battle simulation

    Example:
        >>> groups = map_faction_troops(soldiers=100, elites=5, elite_avg_level=8)
        >>> len(groups)
        2
        >>> groups[0]["unit_type"]
        'soldier'
    """
    groups = []

    if soldiers > 0:
        groups.append(create_unit_group("soldier", soldiers))

    if spies > 0:
        groups.append(create_unit_group("spy", spies))

    if elites > 0:
        # Map to appropriate elite tier based on level
        if elite_avg_level >= 10:
            unit_type = "elite_10"  # Gladiator (SRD-compliant high-tier)
        else:
            unit_type = "elite_6"  # Knight
        groups.append(create_unit_group(unit_type, elites, elite_avg_level))

    return groups


def calculate_total_cr(groups: list[dict]) -> float:
    """Calculate total Challenge Rating for a force.

    Args:
        groups: List of unit groups (from create_unit_group)

    Returns:
        Total CR (sum of individual unit CRs)

    Example:
        >>> soldiers = create_unit_group("soldier", 100)
        >>> elites = create_unit_group("elite_6", 5)
        >>> calculate_total_cr([soldiers, elites])
        27.5
    """
    total_cr = 0.0
    for group in groups:
        unit_cr = group["stats"]["cr"]
        count = group["count"]
        total_cr += unit_cr * count
    return total_cr
