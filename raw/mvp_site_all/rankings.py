"""Rankings system for WorldAI Faction Management.

Implements exact formulas for:
- Total Faction Power (FP) calculation
- Army FP calculation
- AI faction behavior and competition
- Ranking position calculation

All formulas are reverse-engineered from the WorldAI Faction Management ruleset.
"""

from __future__ import annotations

from typing import TypedDict

from mvp_site.constants import AI_FACTION_COUNT, AI_FACTION_SEED, MIN_RANK_FP
from mvp_site.faction.ai_factions import generate_ai_factions


class FactionStats(TypedDict, total=False):
    """Faction statistics for ranking calculation."""

    soldiers: int
    spies: int
    elites: int
    elite_avg_level: int
    territory: int
    fortifications: int
    citizens: int
    gold_pieces: int
    arcana: int
    prestige: float


class AIFaction(TypedDict):
    """AI faction data structure."""

    name: str
    difficulty: str
    base_fp: int  # Base faction power (internal representation)
    behavior: str
    aggression: float


# =============================================================================
# AI Factions (200 competitors - dynamically generated)
# =============================================================================

# AI factions are now generated dynamically using generate_ai_factions()
# from mvp_site.faction.ai_factions. This ensures deterministic generation
# of 200 factions with consistent names, stats, and behaviors across sessions.
#
# Use get_all_ai_factions() to retrieve the generated faction list.


# =============================================================================
# Faction Power Calculation
# =============================================================================


def calculate_army_fp(
    soldiers: int,
    spies: int,
    elites: int,
    elite_avg_level: int = 6,
) -> int:
    """Calculate army component of Faction Power.

    Formula:
        Soldiers FP = soldiers * 1.0
        Spies FP = spies * 0.5 (combat penalty)
        Elites FP = elites * 3.0 * level_bonus

    Level bonus = 1.0 + (avg_level - 6) * 0.1 for levels > 6

    Args:
        soldiers: Number of soldiers
        spies: Number of spies
        elites: Number of elites
        elite_avg_level: Average level of elite units (6-20)

    Returns:
        Army Faction Power
    """
    soldiers_fp = soldiers * 1.0
    spies_fp = spies * 0.5

    # Elites scale with level (level 6 = base, each level above = +10%)
    level_bonus = 1.0 + max(0, (elite_avg_level - 6)) * 0.1
    elites_fp = elites * 3.0 * level_bonus

    return int(soldiers_fp + spies_fp + elites_fp)


def calculate_total_fp(stats: FactionStats) -> int:
    """Calculate total Faction Power from all sources.

    Components:
        Army FP: calculate_army_fp()
        Territory FP: territory * 5
        Fortification FP: fortifications * 1000
        Citizen FP: citizens * 0.1
        Gold FP: gold_pieces * 0.001
        Arcana FP: arcana * 0.01
        Prestige FP: prestige * 100

    Args:
        stats: FactionStats with all faction statistics

    Returns:
        Total Faction Power
    """
    # Army component
    army_fp = calculate_army_fp(
        stats.get("soldiers", 0),
        stats.get("spies", 0),
        stats.get("elites", 0),
        stats.get("elite_avg_level", 6),
    )

    # Territory and fortifications (rebalanced: territory reduced from 10 to 5 FP per acre)
    territory_fp = stats.get("territory", 0) * 5
    fort_fp = stats.get("fortifications", 0) * 1000

    # Economic components (smaller contributions)
    citizen_fp = stats.get("citizens", 0) * 0.1
    gold_fp = stats.get("gold_pieces", 0) * 0.001
    arcana_fp = stats.get("arcana", 0) * 0.01

    # Prestige (diplomatic power)
    prestige_fp = stats.get("prestige", 0) * 100

    return int(
        army_fp
        + territory_fp
        + fort_fp
        + citizen_fp
        + gold_fp
        + arcana_fp
        + prestige_fp
    )


# =============================================================================
# AI Faction Behavior
# =============================================================================

BEHAVIOR_DESCRIPTIONS = {
    "defensive": "Focuses on fortifications and territory defense",
    "isolationist": "Avoids conflict, builds internally",
    "trader": "Prioritizes gold income and diplomatic relations",
    "raider": "Opportunistic attacks on weaker neighbors",
    "expansionist": "Constantly seeks to grow territory",
    "balanced": "Well-rounded approach to all aspects",
    "aggressive": "Prioritizes military buildup and attacks",
    "arcane": "Focuses on arcana and magical research",
    "diplomatic": "Seeks alliances and avoids direct conflict",
    "shadowy": "Heavy spy network, sabotage operations",
    "nature": "Defensive, prefers guerilla tactics",
    "imperial": "Structured expansion, tribute demands",
    "mysterious": "Unpredictable actions, unknown motives",
    "dominating": "Seeks absolute regional control",
    "crusading": "Attacks based on ideological reasons",
    "ancient": "Slow but powerful, long-term planning",
}


def get_ai_faction_behavior(faction_name: str) -> dict:
    """Get AI faction behavior profile.

    Args:
        faction_name: Name of the AI faction

    Returns:
        Dict with behavior, description, aggression level
    """
    ai_factions = get_all_ai_factions()
    for faction in ai_factions:
        if faction["name"] == faction_name:
            behavior = faction["behavior"]
            return {
                "name": faction_name,
                "difficulty": faction["difficulty"],
                "behavior": behavior,
                "description": BEHAVIOR_DESCRIPTIONS.get(behavior, "Unknown"),
                "aggression": faction["aggression"],
                "base_fp": faction["base_fp"],
            }

    return {
        "name": faction_name,
        "difficulty": "unknown",
        "behavior": "unknown",
        "description": "Unknown faction",
        "aggression": 0.5,
        "base_fp": 0,
    }


def get_all_ai_factions() -> list[AIFaction]:
    """Get all AI faction data.

    Returns deterministically generated AI factions using the configured
    seed and count from constants.

    Returns:
        List of AIFaction dicts sorted by base FP (already sorted by generator)
    """
    return generate_ai_factions(seed=AI_FACTION_SEED, count=AI_FACTION_COUNT)


# =============================================================================
# Ranking Calculation
# =============================================================================


def calculate_ranking(
    player_fp: int, turn_number: int = 1
) -> tuple[int | None, list[dict]]:
    """Calculate player ranking among all factions.

    AI factions grow over time:
        Turn growth = base_fp * (1 + turn_number * growth_rate)
        Growth rates: easy=0.01, medium=0.015, hard=0.02

    Unranked state:
        If player_fp < MIN_RANK_FP, player is unranked (returns None)

    Args:
        player_fp: Player's total Faction Power
        turn_number: Current game turn (for AI scaling)

    Returns:
        Tuple of (ranking 1-201 or None if unranked, list of all factions sorted by FP)
    """
    # Check if player is below ranking threshold
    if player_fp < MIN_RANK_FP:
        # Player is unranked - still generate faction list for context
        growth_rates = {"easy": 0.01, "medium": 0.015, "hard": 0.02}
        ai_factions = get_all_ai_factions()

        factions = []
        for ai in ai_factions:
            growth = growth_rates.get(ai["difficulty"], 0.01)
            current_fp = int(ai["base_fp"] * (1 + turn_number * growth))
            factions.append(
                {
                    "name": ai["name"],
                    "faction_power": current_fp,
                    "difficulty": ai["difficulty"],
                    "is_player": False,
                }
            )

        # Add player but mark as unranked
        factions.append(
            {
                "name": "Player Faction",
                "faction_power": player_fp,
                "difficulty": "player",
                "is_player": True,
            }
        )

        # Sort by FP descending
        factions.sort(key=lambda f: f["faction_power"], reverse=True)

        return None, factions

    # Player is ranked - calculate normal ranking
    growth_rates = {"easy": 0.01, "medium": 0.015, "hard": 0.02}
    ai_factions = get_all_ai_factions()

    # Calculate current AI FP with turn scaling
    factions = []
    for ai in ai_factions:
        growth = growth_rates.get(ai["difficulty"], 0.01)
        current_fp = int(ai["base_fp"] * (1 + turn_number * growth))
        factions.append(
            {
                "name": ai["name"],
                "faction_power": current_fp,
                "difficulty": ai["difficulty"],
                "is_player": False,
            }
        )

    # Add player
    factions.append(
        {
            "name": "Player Faction",
            "faction_power": player_fp,
            "difficulty": "player",
            "is_player": True,
        }
    )

    # Sort by FP descending
    factions.sort(key=lambda f: f["faction_power"], reverse=True)

    # Find player ranking
    ranking = 1
    for i, faction in enumerate(factions):
        if faction["is_player"]:
            ranking = i + 1
            break

    return ranking, factions


def get_nearby_factions(
    player_fp: int, turn_number: int = 1, range_count: int = 3
) -> dict:
    """Get factions near player's ranking for rivalry/alliance opportunities.

    For unranked players (FP < MIN_RANK_FP), returns empty above/below lists
    since there are no nearby rivals at that level.

    Args:
        player_fp: Player's Faction Power
        turn_number: Current turn
        range_count: Number of factions above/below to include

    Returns:
        Dict with above, at_rank, below faction lists
        If unranked, ranking is None and above/below are empty lists
    """
    ranking, factions = calculate_ranking(player_fp, turn_number)

    # Handle unranked player (FP < MIN_RANK_FP)
    if ranking is None:
        # Find player faction in list for at_rank
        player_faction = [f for f in factions if f.get("is_player", False)]
        return {
            "ranking": None,
            "total_factions": len(factions),
            "above": [],
            "at_rank": player_faction,
            "below": [],
        }

    # Ranked player - normal nearby faction calculation
    player_idx = ranking - 1  # Convert to 0-indexed

    above = factions[max(0, player_idx - range_count) : player_idx]
    at_rank = [factions[player_idx]]
    below = factions[player_idx + 1 : player_idx + 1 + range_count]

    return {
        "ranking": ranking,
        "total_factions": len(factions),
        "above": [f for f in above if not f["is_player"]],
        "at_rank": at_rank,
        "below": [f for f in below if not f["is_player"]],
    }


# =============================================================================
# Win Condition Checks
# =============================================================================


def check_ranking_victory(player_fp: int, turn_number: int = 1) -> bool:
    """Check if player has achieved ranking #1 victory.

    Args:
        player_fp: Player's Faction Power
        turn_number: Current turn

    Returns:
        True if player is ranked #1 (False if unranked or not #1)
    """
    ranking, _ = calculate_ranking(player_fp, turn_number)
    return ranking == 1 if ranking is not None else False


def get_fp_to_next_rank(player_fp: int, turn_number: int = 1) -> int | None:
    """Get FP needed to reach next higher rank.

    For unranked players (FP < MIN_RANK_FP), returns FP needed to become ranked.
    For ranked players, returns FP needed to beat the faction above them.

    Args:
        player_fp: Player's current FP
        turn_number: Current turn

    Returns:
        FP needed, or None if already #1
    """
    ranking, factions = calculate_ranking(player_fp, turn_number)

    # Unranked - need to reach minimum ranking threshold
    if ranking is None:
        return MIN_RANK_FP - player_fp

    # Already #1
    if ranking == 1:
        return None

    # Find faction above player
    player_idx = ranking - 1
    faction_above = factions[player_idx - 1]

    return faction_above["faction_power"] - player_fp + 1
