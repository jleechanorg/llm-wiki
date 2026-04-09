"""Resource calculation formulas for WorldAI Faction Management.

Implements exact formulas for:
- Citizens growth per turn
- Gold pieces income per turn
- Arcana yield per turn
- Building construction rates
- Unit recruitment rates

All formulas are reverse-engineered from the WorldAI Faction Management ruleset.
"""

from __future__ import annotations

import math
from typing import TypedDict


class BuildingCounts(TypedDict, total=False):
    """Building counts in a faction."""

    farms: int
    training_grounds: int
    artisans_guilds: int
    arcane_libraries: int
    mana_fonts: int
    fortifications: int
    wards: int
    shadow_networks: int


# =============================================================================  # noqa: ERA001
# Citizens (Population)  # noqa: ERA001
# =============================================================================  # noqa: ERA001


def calculate_citizen_growth(current_citizens: int, territory: int) -> int:
    """Calculate citizen growth per turn.

    Formula: 50 + 0.015 * current_citizens
    - Tapers at 90-100% of max capacity
    - Goes negative if over max (exodus)

    Args:
        current_citizens: Current citizen count
        territory: Territory in acres (max = territory * 50)

    Returns:
        Growth amount (can be negative if over capacity)
    """
    max_citizens = territory * 50
    base_growth = 50 + int(0.015 * current_citizens)

    # Taper growth as we approach max
    capacity_ratio = current_citizens / max_citizens if max_citizens > 0 else 1.0

    if capacity_ratio >= 1.0:
        # Over capacity - citizens leave
        excess = current_citizens - max_citizens
        return -int(excess * 0.1)  # 10% of excess leaves

    if capacity_ratio >= 0.9:
        # 90-100% capacity - reduced growth
        taper = 1.0 - ((capacity_ratio - 0.9) / 0.1)
        return int(base_growth * taper)

    return base_growth


def get_max_citizens(territory: int) -> int:
    """Get maximum citizen capacity.

    Formula: territory * 50

    Args:
        territory: Territory in acres

    Returns:
        Maximum citizen capacity
    """
    return territory * 50


# =============================================================================
# Gold Pieces (Income)
# =============================================================================


def calculate_gold_income(
    citizens: int,
    farms: int = 0,
    artisans_guilds: int = 0,
    prosperity_active: bool = False,
) -> int:
    """Calculate gold pieces income per turn.

    Formula:
    - Tax Revenue: citizens × 0.5gp per citizen per week
    - Farm Surplus: farms × 100gp per farm per week
    - Trade Routes: artisans_guilds × 200gp per workshop per week
    - Prosperity Ritual: Doubles income for 1 turn

    Args:
        citizens: Current citizen count (end of turn)
        farms: Number of farms built
        artisans_guilds: Number of artisan workshops built
        prosperity_active: Whether Prosperity Ritual is active

    Returns:
        Gold income for the turn
    """
    # Base tax revenue: 0.5gp per citizen per week
    tax_revenue = int(citizens * 0.5)
    
    # Farm surplus: 100gp per farm per week
    farm_income = farms * 100
    
    # Trade routes: 200gp per artisan workshop per week
    trade_income = artisans_guilds * 200
    
    base_income = tax_revenue + farm_income + trade_income

    if prosperity_active:
        return base_income * 2

    return base_income


# =============================================================================  # noqa: ERA001
# Arcana (Mana)  # noqa: ERA001
# =============================================================================  # noqa: ERA001


def calculate_arcana_yield(territory: int, mana_fonts: int) -> int:
    """Calculate arcana yield per turn.

    Formula:
        X = floor(100 * fonts / territory)
        Yield = (territory/1000 * X)/100 + fonts * (100 - X)/10

    Full formula (for reference):
        Yield = (territory/1000 * X * (110 - X))/1000

    Optimal ratio: 55-55.99% fonts (diminishing returns above 56%)

    Args:
        territory: Territory in acres
        mana_fonts: Number of mana font buildings

    Returns:
        Arcana yield for the turn
    """
    if territory == 0:
        return 0

    # Calculate X (font percentage) and clamp to avoid negative yields when fonts
    # massively exceed territory.
    x = math.floor(100 * mana_fonts / territory)
    x = max(0, min(x, 110))

    # Simplified yield formula
    l_factor = territory / 1000
    yield_part1 = (l_factor * x) / 100
    yield_part2 = mana_fonts * max(0, 100 - x) / 10

    return max(0, int(yield_part1 + yield_part2))


def calculate_arcana_yield_full(territory: int, mana_fonts: int) -> int:
    """Calculate arcana yield using full formula.

    Full formula: (territory/1000 * X * (110 - X))/1000

    Args:
        territory: Territory in acres
        mana_fonts: Number of mana font buildings

    Returns:
        Arcana yield for the turn
    """
    if territory == 0:
        return 0

    x = math.floor(100 * mana_fonts / territory)
    x = max(0, min(x, 110))
    l_factor = territory / 1000

    return max(0, int((l_factor * x * (110 - x)) / 1000))


def get_max_arcana(mana_fonts: int) -> int:
    """Get maximum arcana storage capacity.

    Formula: 1000 * fonts

    Args:
        mana_fonts: Number of mana font buildings

    Returns:
        Maximum arcana storage
    """
    return mana_fonts * 1000


def get_optimal_font_ratio() -> tuple[float, float]:
    """Get optimal font-to-territory ratio.

    Returns:
        Tuple of (min_optimal, max_optimal) as percentages
    """
    return (55.0, 55.99)


# =============================================================================
# Building Construction
# =============================================================================


def get_artisans_percentage(artisans_guilds: int, territory: int) -> float:
    """Calculate artisans percentage (W).

    Formula: W = artisans / territory * 100

    Args:
        artisans_guilds: Number of artisan guild buildings
        territory: Territory in acres

    Returns:
        Artisans percentage (W)
    """
    if territory == 0:
        return 0.0
    return (artisans_guilds / territory) * 100


def get_build_rate(building_type: str, artisans_guilds: int, territory: int) -> float:
    """Calculate build rate for a building type.

    Formulas (W = artisans percentage):
        farms/training_grounds: (W/10 + 0.1) * 2
        artisans_guilds: W/10 + 0.1
        arcane_libraries: (W/10 + 0.1) / 2
        mana_fonts: (W/10 + 0.1) / 3
        fortifications: (W/10 + 0.1) / 30
        wards: 1 (fixed)
        shadow_networks: (W/10 + 0.1) / 4

    Args:
        building_type: Type of building
        artisans_guilds: Number of artisan guild buildings
        territory: Territory in acres

    Returns:
        Build rate (buildings per turn)
    """
    w = get_artisans_percentage(artisans_guilds, territory)
    base_rate = w / 10 + 0.1

    rates = {
        "farms": base_rate * 2,
        "training_grounds": base_rate * 2,
        "artisans_guilds": base_rate,
        "arcane_libraries": base_rate / 2,
        "mana_fonts": base_rate / 3,
        "fortifications": base_rate / 30,
        "wards": 1.0,  # Fixed rate
        "shadow_networks": base_rate / 4,
    }

    return rates.get(building_type, 0.0)


# =============================================================================
# Unit Recruitment
# =============================================================================


def get_recruit_rate(
    unit_type: str,
    gold_cost: int,
    buildings: int,
    modifier: float = 0.0,
) -> int:
    """Calculate recruitment rate for a unit type.

    Formulas:
        Soldiers: floor((100 / gold_cost) * training_grounds * (1 + mod))
        Spies: floor((200 / gold_cost) * shadow_networks * (1 + mod))

    Args:
        unit_type: Type of unit ("soldiers" or "spies")
        gold_cost: Gold cost per unit
        buildings: Number of relevant buildings (training_grounds or shadow_networks)
        modifier: Recruitment modifier (e.g., -0.1 for -10%)

    Returns:
        Units recruited per turn
    """
    if gold_cost == 0:
        return 0

    if unit_type == "soldiers":
        base_multiplier = 100
    elif unit_type == "spies":
        base_multiplier = 200  # Spies use 200 as base (2x cost means slower recruit)
    else:
        return 0

    rate = (base_multiplier / gold_cost) * buildings * (1 + modifier)
    return int(rate)


# =============================================================================
# Research
# =============================================================================


def get_research_rate(arcane_libraries: int, territory: int) -> float:
    """Calculate research (lore) generation rate.

    Formula: ~1.8/library % territory (log scale, dedicate 2x)
    Advanced max: ~400-500 per school

    Args:
        arcane_libraries: Number of arcane library buildings
        territory: Territory in acres

    Returns:
        Research points per turn (approximate)
    """
    if territory == 0:
        return 0.0

    library_pct = (arcane_libraries / territory) * 100
    # Approximately 1.8 RP per library percentage point
    return library_pct * 1.8


# =============================================================================
# Prestige
# =============================================================================


def calculate_prestige_income(territory: int, vassals: int) -> float:
    """Calculate prestige income per turn.

    Formula: 0.05 * territory/1000 + 0.5 * vassals

    Args:
        territory: Territory in acres
        vassals: Number of vassal factions

    Returns:
        Prestige income per turn
    """
    return 0.05 * (territory / 1000) + 0.5 * vassals
