"""SRD-based battle simulation for WorldAI Faction Management.

Implements D&D 5.1 SRD combat mechanics for tactical battle resolution between
faction forces. Supports three simulation modes:
- Fast: Expected damage calculation (no dice, deterministic)
- Detailed: Full roll-by-roll simulation with combat log
- Deterministic: Seeded RNG for reproducible test results

All mechanics follow D&D 5.1 SRD rules (attack rolls, damage rolls, initiative).
"""

from __future__ import annotations

import random
import re
from typing import TypedDict

from mvp_site.constants import (
    AI_FACTION_SEED,  # Deterministic seed for battle simulation
    BATTLE_MAX_ROUNDS,  # Maximum rounds before draw
    MORALE_ROUT_THRESHOLD,  # HP threshold for unit retreat
)

# =============================================================================
# Type Definitions
# =============================================================================


class BattleResult(TypedDict):
    """Result of a battle simulation."""

    attacker_casualties: int
    defender_casualties: int
    rounds: int
    victor: str  # "attacker", "defender", or "draw"
    detailed_log: list[str]  # Combat log (if mode='detailed')
    attacker_remaining: int
    defender_remaining: int


# =============================================================================
# Constants
# =============================================================================

# =============================================================================
# Dice Rolling
# =============================================================================


def parse_damage_dice(damage_dice: str) -> tuple[int, int, int]:
    """Parse damage dice string into components.

    Args:
        damage_dice: Damage string (e.g., "1d8+3", "2d6", "1d4-1")

    Returns:
        Tuple of (num_dice, die_size, modifier)

    Example:
        >>> parse_damage_dice("2d8+3")
        (2, 8, 3)
    """
    match = re.match(r"(\d+)d(\d+)(([+-])(\d+))?", damage_dice)
    if not match:
        raise ValueError(f"Invalid damage dice format: {damage_dice}")

    num_dice = int(match.group(1))
    die_size = int(match.group(2))
    modifier = 0

    if match.group(3):
        sign = match.group(4)
        mod_value = int(match.group(5))
        modifier = mod_value if sign == "+" else -mod_value

    return num_dice, die_size, modifier


def roll_dice(num_dice: int, die_size: int, rng: random.Random) -> int:
    """Roll dice using provided RNG."""
    return sum(rng.randint(1, die_size) for _ in range(num_dice))


def calculate_expected_damage_value(damage_dice: str) -> float:
    """Calculate expected damage without rolling (for fast mode)."""
    num_dice, die_size, modifier = parse_damage_dice(damage_dice)
    expected_per_die = (die_size + 1) / 2.0
    return (num_dice * expected_per_die) + modifier


# =============================================================================
# Attack Resolution
# =============================================================================


def roll_attack(attack_bonus: int, target_ac: int, rng: random.Random) -> bool:
    """Resolve an attack roll against target AC."""
    d20 = rng.randint(1, 20)
    if d20 == 1:
        return False
    if d20 == 20:
        return True
    return (d20 + attack_bonus) >= target_ac


def calculate_hit_chance(attack_bonus: int, target_ac: int) -> float:
    """Calculate probability of hitting target (for fast mode)."""
    needed = target_ac - attack_bonus
    if needed <= 2:
        return 0.95
    if needed >= 20:
        return 0.05
    return (21 - needed) / 20.0


# =============================================================================
# Battle Simulation
# =============================================================================


def simulate_battle(
    attacker_units: list[dict],
    defender_units: list[dict],
    seed: int | None = None,
    mode: str = "fast",
    max_rounds: int | None = None,
) -> BattleResult:
    """Simulate a tactical battle between two forces.

    Args:
        attacker_units: List of unit groups (from create_unit_group)
        defender_units: List of unit groups (from create_unit_group)
        seed: Random seed for deterministic mode
        mode: Simulation mode ("fast", "detailed", or "deterministic")
        max_rounds: Maximum combat rounds

    Returns:
        BattleResult with casualties, victor, and combat log
    """
    if seed is None:
        seed = AI_FACTION_SEED
    if max_rounds is None:
        max_rounds = BATTLE_MAX_ROUNDS

    rng = random.Random(seed)

    if mode == "fast":
        return _simulate_fast(attacker_units, defender_units, max_rounds)
    if mode in ("detailed", "deterministic"):
        return _simulate_detailed(attacker_units, defender_units, rng, max_rounds)
    raise ValueError(f"Unknown simulation mode: {mode}")


def _check_morale_rout(units: list[dict]) -> bool:
    """Check if a force has suffered enough casualties to trigger morale rout.

    Args:
        units: Unit groups to check

    Returns:
        True if force should rout (HP remaining <= MORALE_ROUT_THRESHOLD)
    """
    total_count = sum(g["count"] for g in units)
    total_remaining = sum(g["remaining"] for g in units)

    if total_count == 0:
        return False

    # MORALE_ROUT_THRESHOLD is "percentage of HP remaining before units rout"
    # So rout when remaining_rate <= threshold (e.g., <= 25% remaining)
    remaining_rate = total_remaining / total_count
    return remaining_rate <= MORALE_ROUT_THRESHOLD


def _distribute_casualties(groups: list[dict], total_casualties: int) -> None:
    """Distribute casualties across unit groups proportionally by size.

    Modifies group["remaining"] in-place. Larger groups take proportionally
    more casualties since they present bigger targets.

    Args:
        groups: Unit groups to distribute casualties across
        total_casualties: Total casualties to distribute

    Example:
        Group A: 100 units, Group B: 50 units
        Total casualties: 15
        Group A takes: 15 * (100/150) = 10 casualties
        Group B takes: 15 * (50/150) = 5 casualties
    """
    if total_casualties <= 0:
        return

    # Get list of alive groups (with remaining > 0)
    alive_groups = [g for g in groups if g["remaining"] > 0]

    if not alive_groups:
        return

    # Calculate total alive units
    total_alive = sum(g["remaining"] for g in alive_groups)

    # Distribute casualties proportionally by group size
    casualties_allocated = 0
    for i, group in enumerate(alive_groups):
        # Calculate this group's proportion of total force
        proportion = group["remaining"] / total_alive

        # Last ALIVE group gets remaining casualties (handles rounding)
        if i == len(alive_groups) - 1:
            group_casualties = total_casualties - casualties_allocated
        else:
            group_casualties = int(proportion * total_casualties)

        # Apply casualties (can't go below 0)
        group["remaining"] = max(0, group["remaining"] - group_casualties)
        casualties_allocated += group_casualties


def _simulate_fast(
    attacker_units: list[dict],
    defender_units: list[dict],
    max_rounds: int,
) -> BattleResult:
    """Fast simulation using expected damage (no dice rolls)."""
    attackers = [u.copy() for u in attacker_units]
    defenders = [u.copy() for u in defender_units]

    for group in attackers:
        group["remaining"] = group["count"]
    for group in defenders:
        group["remaining"] = group["count"]

    rounds = 0
    log = ["=== Fast Battle Simulation ==="]
    routed_side = None

    while rounds < max_rounds:
        rounds += 1

        attacker_alive = sum(g["remaining"] for g in attackers)
        defender_alive = sum(g["remaining"] for g in defenders)

        if attacker_alive == 0 or defender_alive == 0:
            break

        defender_casualties = _calculate_round_casualties_fast(attackers, defenders)
        _distribute_casualties(defenders, defender_casualties)

        # Check defender morale
        if _check_morale_rout(defenders):
            routed_side = "defender"
            log.append(
                f"Round {rounds}: Defenders routed (remaining <= {MORALE_ROUT_THRESHOLD:.0%})"
            )
            break

        attacker_casualties = _calculate_round_casualties_fast(defenders, attackers)
        _distribute_casualties(attackers, attacker_casualties)

        # Check attacker morale
        if _check_morale_rout(attackers):
            routed_side = "attacker"
            log.append(
                f"Round {rounds}: Attackers routed (remaining <= {MORALE_ROUT_THRESHOLD:.0%})"
            )
            break

    final_attacker = sum(g["remaining"] for g in attackers)
    final_defender = sum(g["remaining"] for g in defenders)

    # Determine victor (routing counts as defeat)
    if routed_side == "defender" or (final_attacker > 0 and final_defender == 0):
        victor = "attacker"
    elif routed_side == "attacker" or (final_defender > 0 and final_attacker == 0):
        victor = "defender"
    elif final_attacker > final_defender:
        victor = "attacker"
    elif final_defender > final_attacker:
        victor = "defender"
    else:
        victor = "draw"

    attacker_casualties_total = sum(g["count"] - g["remaining"] for g in attackers)
    defender_casualties_total = sum(g["count"] - g["remaining"] for g in defenders)

    if routed_side:
        log.append(f"Battle ended by rout after {rounds} rounds - Victor: {victor}")
    else:
        log.append(f"Battle concluded after {rounds} rounds - Victor: {victor}")

    return {
        "attacker_casualties": attacker_casualties_total,
        "defender_casualties": defender_casualties_total,
        "rounds": rounds,
        "victor": victor,
        "detailed_log": log,
        "attacker_remaining": final_attacker,
        "defender_remaining": final_defender,
    }


def _calculate_round_casualties_fast(
    attackers: list[dict],
    defenders: list[dict],
) -> int:
    """Calculate expected casualties in one round (fast mode)."""
    total_damage = 0.0

    # Calculate total damage from all attackers
    # Each attacker attacks once per round, not once per defender group
    for atk_group in attackers:
        if atk_group["remaining"] <= 0:
            continue

        atk_stats = atk_group["stats"]
        atk_count = atk_group["remaining"]

        # Use average defender AC for hit chance calculation
        # (attackers don't target specific groups, they attack the force as a whole)
        if defenders:
            alive_defenders = [g for g in defenders if g["remaining"] > 0]
            if alive_defenders:
                avg_defender_ac = sum(g["stats"]["ac"] for g in alive_defenders) / len(
                    alive_defenders
                )
                hit_chance = calculate_hit_chance(
                    atk_stats["attack_bonus"], int(avg_defender_ac)
                )
                expected_dmg = calculate_expected_damage_value(atk_stats["damage_dice"])
                damage_per_unit = hit_chance * expected_dmg
                total_damage += damage_per_unit * atk_count

    if defenders:
        # Weight average HP by unit count (not just group count)
        total_defender_units = sum(g["remaining"] for g in defenders)
        if total_defender_units > 0:
            weighted_avg_defender_hp = (
                sum(g["stats"]["hp"] * g["remaining"] for g in defenders)
                / total_defender_units
            )
            # Guard division by zero: all defenders can have hp=0 (malformed/custom data)
            if weighted_avg_defender_hp <= 0:
                return 0
            return int(total_damage / weighted_avg_defender_hp)

    return 0


def _simulate_detailed(
    attacker_units: list[dict],
    defender_units: list[dict],
    rng: random.Random,
    max_rounds: int,
) -> BattleResult:
    """Detailed simulation with full dice rolls and combat log."""
    attackers = [u.copy() for u in attacker_units]
    defenders = [u.copy() for u in defender_units]

    for group in attackers:
        group["remaining"] = group["count"]
    for group in defenders:
        group["remaining"] = group["count"]

    rounds = 0
    log = ["=== Detailed Battle Simulation ==="]
    routed_side = None

    while rounds < max_rounds:
        rounds += 1
        log.append(f"\n--- Round {rounds} ---")

        attacker_alive = sum(g["remaining"] for g in attackers)
        defender_alive = sum(g["remaining"] for g in defenders)

        if attacker_alive == 0 or defender_alive == 0:
            break

        log.append(f"Attackers: {attacker_alive} | Defenders: {defender_alive}")

        defender_casualties = _simulate_round_detailed(
            attackers, defenders, rng, log, "Attacker"
        )
        _distribute_casualties(defenders, defender_casualties)

        # Check defender morale
        if _check_morale_rout(defenders):
            routed_side = "defender"
            log.append(
                f"Round {rounds}: Defenders routed (remaining <= {MORALE_ROUT_THRESHOLD:.0%})!"
            )
            break

        attacker_casualties = _simulate_round_detailed(
            defenders, attackers, rng, log, "Defender"
        )
        _distribute_casualties(attackers, attacker_casualties)

        # Check attacker morale
        if _check_morale_rout(attackers):
            routed_side = "attacker"
            log.append(
                f"Round {rounds}: Attackers routed (remaining <= {MORALE_ROUT_THRESHOLD:.0%})!"
            )
            break

    final_attacker = sum(g["remaining"] for g in attackers)
    final_defender = sum(g["remaining"] for g in defenders)

    # Determine victor (routing counts as defeat)
    if routed_side == "defender" or (final_attacker > 0 and final_defender == 0):
        victor = "attacker"
    elif routed_side == "attacker" or (final_defender > 0 and final_attacker == 0):
        victor = "defender"
    elif final_attacker > final_defender:
        victor = "attacker"
    elif final_defender > final_attacker:
        victor = "defender"
    else:
        victor = "draw"

    attacker_casualties_total = sum(g["count"] - g["remaining"] for g in attackers)
    defender_casualties_total = sum(g["count"] - g["remaining"] for g in defenders)

    log.append("\n=== Battle Result ===")
    if routed_side:
        log.append(f"Battle ended by rout after {rounds} rounds - Victor: {victor}")
    else:
        log.append(f"Battle concluded after {rounds} rounds - Victor: {victor}")
    log.append(f"Attacker casualties: {attacker_casualties_total}")
    log.append(f"Defender casualties: {defender_casualties_total}")

    return {
        "attacker_casualties": attacker_casualties_total,
        "defender_casualties": defender_casualties_total,
        "rounds": rounds,
        "victor": victor,
        "detailed_log": log,
        "attacker_remaining": final_attacker,
        "defender_remaining": final_defender,
    }


def _simulate_round_detailed(
    attackers: list[dict],
    defenders: list[dict],
    rng: random.Random,
    log: list[str],
    side_name: str,
) -> int:
    """Simulate one round with detailed combat log."""
    total_damage = 0
    total_hits = 0
    total_attacks = 0

    # Calculate average defender AC for hit chance (attackers attack force as a whole)
    if defenders:
        alive_defenders = [g for g in defenders if g["remaining"] > 0]
        if alive_defenders:
            total_defender_units = sum(g["remaining"] for g in alive_defenders)
            if total_defender_units > 0:
                weighted_avg_defender_ac = (
                    sum(g["stats"]["ac"] * g["remaining"] for g in alive_defenders)
                    / total_defender_units
                )
            else:
                weighted_avg_defender_ac = sum(
                    g["stats"]["ac"] for g in alive_defenders
                ) / len(alive_defenders)
        else:
            weighted_avg_defender_ac = 10  # Default AC
    else:
        weighted_avg_defender_ac = 10

    # Each attacker attacks once per round (not once per defender group)
    for atk_group in attackers:
        if atk_group["remaining"] <= 0:
            continue

        atk_stats = atk_group["stats"]
        remaining = atk_group["remaining"]
        atk_count = min(remaining, 10)

        # Scale factor if we're capping attacks (e.g., 100 units -> 10 attacks * 10.0 scale)
        scale = remaining / atk_count if atk_count > 0 else 0.0
        group_damage = 0

        # Attack against average defender AC
        for _ in range(atk_count):
            total_attacks += 1
            hit = roll_attack(
                atk_stats["attack_bonus"], int(weighted_avg_defender_ac), rng
            )

            if hit:
                total_hits += 1
                num_dice, die_size, modifier = parse_damage_dice(
                    atk_stats["damage_dice"]
                )
                damage = roll_dice(num_dice, die_size, rng) + modifier
                group_damage += damage

        # Add scaled damage to total
        total_damage += int(group_damage * scale)

    casualties = 0
    if defenders and total_damage > 0:
        # Weight average HP by unit count (not just group count)
        total_defender_units = sum(g["remaining"] for g in defenders)
        if total_defender_units > 0:
            weighted_avg_defender_hp = (
                sum(g["stats"]["hp"] * g["remaining"] for g in defenders)
                / total_defender_units
            )
            if weighted_avg_defender_hp > 0:
                casualties = max(1, int(total_damage / weighted_avg_defender_hp))
            else:
                casualties = 0
        else:
            casualties = 0

    log.append(
        f"{side_name}: {total_attacks} attacks, {total_hits} hits, "
        f"{total_damage} damage, {casualties} casualties"
    )

    return casualties


# =============================================================================
# Additional Helper Functions (for __init__.py exports)
# =============================================================================


class BattleConfig(TypedDict):
    """Configuration for battle simulation."""

    mode: str  # "fast", "detailed", or "deterministic"
    seed: int
    max_rounds: int


def expected_damage_per_round(
    attacker_units: list[dict],
    defender_units: list[dict],
) -> float:
    """Calculate expected damage per round (fast mode calculation).

    Args:
        attacker_units: Attacking unit groups
        defender_units: Defending unit groups

    Returns:
        Expected damage per round

    Example:
        >>> attackers = [create_unit_group("soldier", 100)]
        >>> defenders = [create_unit_group("soldier", 80)]
        >>> dmg = expected_damage_per_round(attackers, defenders)
        >>> dmg > 0
        True
    """
    if not defender_units:
        return 0.0

    # Calculate weighted average defender AC (same approach as _calculate_round_casualties_fast)
    total_defender_count = sum(
        g.get("remaining", g.get("count", 0))
        for g in defender_units
        if g.get("remaining", g.get("count", 0)) > 0
    )
    if total_defender_count == 0:
        return 0.0

    weighted_ac = (
        sum(
            g["stats"]["ac"] * g.get("remaining", g.get("count", 0))
            for g in defender_units
            if g.get("remaining", g.get("count", 0)) > 0
        )
        / total_defender_count
    )

    total_damage = 0.0

    # Each attacker attacks once per round, not once per defender group
    for atk_group in attacker_units:
        if atk_group.get("remaining", atk_group.get("count", 0)) <= 0:
            continue

        atk_stats = atk_group["stats"]
        atk_count = atk_group.get("remaining", atk_group["count"])

        hit_chance = calculate_hit_chance(atk_stats["attack_bonus"], weighted_ac)
        expected_dmg = calculate_expected_damage_value(atk_stats["damage_dice"])
        damage_per_unit = hit_chance * expected_dmg
        total_damage += damage_per_unit * atk_count

    return total_damage


def calculate_army_hp(unit_groups: list[dict]) -> int:
    """Calculate total HP for an army (all unit groups).

    Args:
        unit_groups: List of unit groups

    Returns:
        Total HP across all units

    Example:
        >>> soldiers = create_unit_group("soldier", 100)
        >>> hp = calculate_army_hp([soldiers])
        >>> hp == 100 * 11  # 100 guards * 11 HP each
        True
    """
    total_hp = 0
    for group in unit_groups:
        unit_hp = group["stats"]["hp"]
        count = group.get("remaining", group["count"])
        total_hp += unit_hp * count
    return total_hp
