"""Combat formulas for WorldAI Faction Management.

Implements exact formulas for:
- Faction Power (FP) calculation
- Damage calculation
- Position multipliers
- School counter bonuses

All formulas are reverse-engineered from the WorldAI Faction Management ruleset.
"""

from __future__ import annotations

import random
from typing import TypedDict


class UnitStats(TypedDict, total=False):
    """Unit statistics for combat calculations."""

    count: int
    attack: float
    defense: float
    fp_mult: float
    avg_level: int  # For elites


# =============================================================================
# Position Multipliers
# =============================================================================

POSITION_MULTIPLIERS = {
    "ranged": 1.0,
    "melee": 1.5,
    "flying": 2.25,
}


def get_position_multiplier(position: str) -> float:
    """Get combat multiplier for unit position.

    Multipliers:
        ranged: 1.0x (base)
        melee: 1.5x
        flying: 2.25x

    Args:
        position: Unit position (ranged, melee, flying)

    Returns:
        Position multiplier (defaults to 1.0 for invalid inputs)
    """
    if not isinstance(position, str):
        return 1.0  # Default safe value for non-string inputs
    return POSITION_MULTIPLIERS.get(position.lower(), 1.0)


# =============================================================================
# School Counter System
# =============================================================================

# Counter cycle: Radiant > Shadow > Illusion > Evocation > Conjuration > Radiant
SCHOOL_COUNTERS = {
    "radiant": "shadow",
    "shadow": "illusion",
    "illusion": "evocation",
    "evocation": "conjuration",
    "conjuration": "radiant",
}


def get_school_counter_bonus(attacker_school: str, defender_school: str) -> float:
    """Get damage bonus for school counter matchup.

    Counter cycle:
        Radiant > Shadow > Illusion > Evocation > Conjuration > Radiant

    Args:
        attacker_school: Attacker's primary school
        defender_school: Defender's primary school

    Returns:
        Bonus multiplier (1.0 if no counter, 1.25 if counter)
    """
    if not isinstance(attacker_school, str) or not isinstance(defender_school, str):
        return 1.0  # Default safe value for non-string inputs
    
    attacker = attacker_school.lower()
    defender = defender_school.lower()

    if SCHOOL_COUNTERS.get(attacker) == defender:
        return 1.25  # 25% bonus for counter

    return 1.0


# =============================================================================
# Faction Power (FP) Calculation
# =============================================================================


def calculate_faction_power(
    soldiers: int,
    spies: int,
    elites: int,
    elite_avg_level: int = 6,
    territory: int = 0,
    fortifications: int = 0,
    base_stats: dict | None = None,
) -> int:
    """Calculate total Faction Power (FP).

    Formula:
        Soldiers FP = soldiers * 1.0 * attack * defense
        Spies FP = spies * 0.5 * attack * defense
        Elites FP = elites * 3.0 * attack * defense * level_bonus
        Territory FP = territory * 5
        Fort FP = fortifications * 1000

    Args:
        soldiers: Number of soldiers
        spies: Number of spies
        elites: Number of elites
        elite_avg_level: Average level of elite units (6-20)
        territory: Territory in acres
        fortifications: Number of fortification buildings
        base_stats: Optional dict with 'attack' and 'defense' base values

    Returns:
        Total Faction Power
    """
    # Default base stats
    attack = 1.0
    defense = 1.0
    if base_stats:
        attack = base_stats.get("attack", 1.0)
        defense = base_stats.get("defense", 1.0)

    # Unit FP contributions
    soldiers_fp = soldiers * 1.0 * attack * defense
    spies_fp = spies * 0.5 * attack * defense

    # Elites get level bonus (scaled from level 6 base)
    level_bonus = 1.0 + ((elite_avg_level - 6) * 0.1) if elite_avg_level > 6 else 1.0
    elites_fp = elites * 3.0 * attack * defense * level_bonus

    # Territory and fortification bonuses
    territory_fp = territory * 5
    fort_fp = fortifications * 1000

    return int(soldiers_fp + spies_fp + elites_fp + territory_fp + fort_fp)


# =============================================================================
# Damage Calculation
# =============================================================================


def calculate_damage(
    attackers: int,
    attack_stat: float,
    efficiency: float,
    accuracy: float,
    avg_resistance: float,
    position: str = "ranged",
    school_bonus: float = 1.0,
    other_multipliers: float = 1.0,
    random_range: tuple[float, float] = (0.2, 0.8),
) -> int:
    """Calculate combat damage.

    Formula:
        Damage = #attackers * Attack * Efficiency * Accuracy * Rand(0.2-0.8)
                 * (1 - avg_res) * Position * School * Other

    Args:
        attackers: Number of attacking units
        attack_stat: Attack value of units
        efficiency: Efficiency multiplier (0.0-1.0)
        accuracy: Accuracy multiplier (0.0-1.0)
        avg_resistance: Average resistance of defenders (0.0-1.0)
        position: Unit position (ranged, melee, flying)
        school_bonus: School counter bonus (1.0 or 1.25)
        other_multipliers: Additional multipliers
        random_range: Random factor range (default 0.2-0.8)

    Returns:
        Damage dealt
    """
    # Validate random_range (a <= b)
    if random_range[0] > random_range[1]:
        random_range = (0.2, 0.8)  # Safe default
    
    # Clamp values to [0, 1] to prevent damage amplification bugs
    efficiency = max(0.0, min(1.0, efficiency))
    accuracy = max(0.0, min(1.0, accuracy))
    avg_resistance = max(0.0, min(1.0, avg_resistance))
    
    # Random factor
    rand_factor = random.uniform(random_range[0], random_range[1])

    # Position multiplier
    position_mult = get_position_multiplier(position)

    # Full damage formula
    damage = (
        attackers
        * attack_stat
        * efficiency
        * accuracy
        * rand_factor
        * (1 - avg_resistance)
        * position_mult
        * school_bonus
        * other_multipliers
    )

    return max(0, int(damage))


def calculate_damage_deterministic(
    attackers: int,
    attack_stat: float,
    efficiency: float,
    accuracy: float,
    avg_resistance: float,
    position: str = "ranged",
    school_bonus: float = 1.0,
    other_multipliers: float = 1.0,
    random_factor: float = 0.5,
) -> int:
    """Calculate combat damage with deterministic random factor.

    Same as calculate_damage but with fixed random factor for testing.

    Args:
        attackers: Number of attacking units
        attack_stat: Attack value of units
        efficiency: Efficiency multiplier (0.0-1.0)
        accuracy: Accuracy multiplier (0.0-1.0)
        avg_resistance: Average resistance of defenders (0.0-1.0)
        position: Unit position (ranged, melee, flying)
        school_bonus: School counter bonus (1.0 or 1.25)
        other_multipliers: Additional multipliers
        random_factor: Fixed random factor (default 0.5)

    Returns:
        Damage dealt
    """
    position_mult = get_position_multiplier(position)

    damage = (
        attackers
        * attack_stat
        * efficiency
        * accuracy
        * random_factor
        * (1 - avg_resistance)
        * position_mult
        * school_bonus
        * other_multipliers
    )

    return max(0, int(damage))


# =============================================================================
# Army Stats
# =============================================================================


def calculate_army_stats(
    soldiers: int,
    spies: int,
    elites: int,
    elite_avg_level: int = 6,
) -> dict:
    """Calculate aggregate army statistics.

    Args:
        soldiers: Number of soldiers
        spies: Number of spies
        elites: Number of elites
        elite_avg_level: Average level of elite units

    Returns:
        Dict with total_units, effective_strength, composition breakdown
    """
    total_units = soldiers + spies + elites

    # Effective strength (weighted by FP multipliers)
    effective_strength = (
        soldiers * 1.0
        + spies * 0.5
        + elites * 3.0 * (1.0 + (max(0, elite_avg_level - 6) * 0.1))
    )

    return {
        "total_units": total_units,
        "effective_strength": int(effective_strength),
        "composition": {
            "soldiers": soldiers,
            "soldiers_pct": (soldiers / total_units * 100) if total_units else 0,
            "spies": spies,
            "spies_pct": (spies / total_units * 100) if total_units else 0,
            "elites": elites,
            "elites_pct": (elites / total_units * 100) if total_units else 0,
        },
    }
