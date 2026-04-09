"""AI Faction Generator for WorldAI Faction Management.

Generates 200 deterministic AI factions for the ranking system using
seeded random generation to ensure consistency across sessions.
"""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

from mvp_site.constants import AI_FACTION_COUNT, AI_FACTION_SEED

if TYPE_CHECKING:
    from mvp_site.faction.rankings import AIFaction


# =============================================================================
# Name Generation Components
# =============================================================================

ADJECTIVES = [
    "Ancient",
    "Azure",
    "Blazing",
    "Broken",
    "Celestial",
    "Crimson",
    "Crystal",
    "Dark",
    "Dawn",
    "Divine",
    "Dusk",
    "Emerald",
    "Eternal",
    "Fallen",
    "Frozen",
    "Golden",
    "Grim",
    "Hidden",
    "Holy",
    "Iron",
    "Ivory",
    "Jade",
    "Marble",
    "Mystic",
    "Noble",
    "Obsidian",
    "Platinum",
    "Radiant",
    "Ruby",
    "Sacred",
    "Scarlet",
    "Shadow",
    "Silent",
    "Silver",
    "Smoke",
    "Storm",
    "Tempest",
    "Thunder",
    "Twilight",
    "Verdant",
    "Violet",
    "Void",
    "Whispered",
    "Wicked",
    "Wild",
    "Ashen",
    "Black",
    "Blood",
    "Bronze",
    "Copper",
    "Dread",
    "Ebon",
    "Fading",
    "Ghostly",
    "Glorious",
    "Gray",
    "Haunted",
    "Hollow",
    "Lustrous",
    "Midnight",
    "Moonlit",
    "Obsidian",
    "Pearl",
    "Phantom",
    "Prismatic",
    "Raging",
    "Raven",
    "Rusted",
    "Sable",
    "Sapphire",
    "Serpent",
    "Shattered",
    "Shining",
    "Spectral",
    "Starlit",
    "Sunlit",
    "Tarnished",
    "Topaz",
    "Umbral",
    "Vengeful",
]

NOUNS = [
    "Alliance",
    "Armada",
    "Arsenal",
    "Bastion",
    "Battalion",
    "Blade",
    "Brotherhood",
    "Bulwark",
    "Circle",
    "Citadel",
    "Clan",
    "Coalition",
    "Conclave",
    "Covenant",
    "Crown",
    "Crusade",
    "Dawn",
    "Dominion",
    "Dynasty",
    "Empire",
    "Enclave",
    "Fellowship",
    "Flame",
    "Force",
    "Fortress",
    "Guard",
    "Guild",
    "Hammer",
    "Hand",
    "Horde",
    "Host",
    "Keep",
    "Kingdom",
    "Knights",
    "Legion",
    "Lords",
    "Order",
    "Pact",
    "Phalanx",
    "Realm",
    "Regiment",
    "Republic",
    "Sanctum",
    "Sect",
    "Senate",
    "Shield",
    "Spear",
    "Stronghold",
    "Syndicate",
    "Throne",
    "Tribunal",
    "Union",
    "Vanguard",
    "Wardens",
    "Watch",
    "Assembly",
    "Banner",
    "Bastion",
    "Brigade",
    "Cadre",
    "Cabal",
    "Collective",
    "Company",
    "Congregation",
    "Council",
    "Court",
    "Federation",
    "Fleet",
    "Forge",
    "Garrison",
    "Hegemony",
    "Hierarchy",
    "Imperium",
    "League",
    "Network",
]

BEHAVIORS = [
    "defensive",
    "isolationist",
    "trader",
    "raider",
    "expansionist",
    "balanced",
    "aggressive",
    "arcane",
    "diplomatic",
    "shadowy",
    "nature",
    "imperial",
    "mysterious",
    "dominating",
    "crusading",
    "ancient",
]


# =============================================================================
# AI Faction Generation
# =============================================================================


def generate_ai_factions(
    seed: int = AI_FACTION_SEED,
    count: int = AI_FACTION_COUNT,
) -> list[AIFaction]:
    """Generate deterministic AI factions for ranking system.

    Creates a fixed roster of AI factions with consistent names, difficulties,
    base FP values, behaviors, and aggression levels. Uses seeded random
    generation to ensure the same factions are generated across sessions.

    Distribution:
        - Easy (30%): 5K-50K base FP, lower aggression
        - Medium (40%): 75K-300K base FP, moderate aggression
        - Hard (30%): 400K-1.5M base FP, higher aggression

    Args:
        seed: Random seed for deterministic generation (default: AI_FACTION_SEED)
        count: Number of factions to generate (default: AI_FACTION_COUNT = 200)

    Returns:
        List of AIFaction dicts sorted by base_fp ascending

    Example:
        >>> factions = generate_ai_factions(seed=42, count=200)
        >>> len(factions)
        200
        >>> factions[0]["difficulty"]
        'easy'
        >>> factions[-1]["difficulty"]
        'hard'
    """
    rng = random.Random(seed)

    # Calculate counts for each difficulty
    easy_count = int(count * 0.30)  # 30%
    medium_count = int(count * 0.40)  # 40%
    hard_count = count - easy_count - medium_count  # Remaining (~30%)

    factions: list[AIFaction] = []
    used_names: set[str] = set()

    # Generate easy factions (5K-50K FP)
    for _ in range(easy_count):
        name = _generate_unique_name(rng, used_names)
        base_fp = rng.randint(5_000, 50_000)
        behavior = rng.choice(BEHAVIORS)
        aggression = round(rng.uniform(0.1, 0.4), 2)

        factions.append(
            {
                "name": name,
                "difficulty": "easy",
                "base_fp": base_fp,
                "behavior": behavior,
                "aggression": aggression,
            }
        )

    # Generate medium factions (75K-300K FP)
    for _ in range(medium_count):
        name = _generate_unique_name(rng, used_names)
        base_fp = rng.randint(75_000, 300_000)
        behavior = rng.choice(BEHAVIORS)
        aggression = round(rng.uniform(0.3, 0.6), 2)

        factions.append(
            {
                "name": name,
                "difficulty": "medium",
                "base_fp": base_fp,
                "behavior": behavior,
                "aggression": aggression,
            }
        )

    # Generate hard factions (400K-1.5M FP)
    for _ in range(hard_count):
        name = _generate_unique_name(rng, used_names)
        base_fp = rng.randint(400_000, 1_500_000)
        behavior = rng.choice(BEHAVIORS)
        aggression = round(rng.uniform(0.5, 0.8), 2)

        factions.append(
            {
                "name": name,
                "difficulty": "hard",
                "base_fp": base_fp,
                "behavior": behavior,
                "aggression": aggression,
            }
        )

    # Sort by base_fp ascending (weakest to strongest)
    factions.sort(key=lambda f: f["base_fp"])

    return factions


def _generate_unique_name(rng: random.Random, used_names: set[str]) -> str:
    """Generate a unique faction name using adjective + noun.

    Args:
        rng: Random number generator (seeded for determinism)
        used_names: Set of already used names to avoid duplicates

    Returns:
        Unique faction name in format "Adjective Noun"
    """
    max_attempts = 1000
    for _ in range(max_attempts):
        adjective = rng.choice(ADJECTIVES)
        noun = rng.choice(NOUNS)
        name = f"{adjective} {noun}"

        if name not in used_names:
            used_names.add(name)
            return name

    # Fallback: add numeric suffix if we somehow exhaust combinations
    base_name = f"{rng.choice(ADJECTIVES)} {rng.choice(NOUNS)}"
    suffix = 1
    while f"{base_name} {suffix}" in used_names:
        suffix += 1
    name = f"{base_name} {suffix}"
    used_names.add(name)
    return name
