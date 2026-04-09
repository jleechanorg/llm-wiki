"""Unit upkeep calculation for WorldAI Faction Management.

Implements upkeep costs for military units based on D&D 5e hireling wages.
"""

from __future__ import annotations


def calculate_unit_upkeep(
    soldiers: int,
    spies: int = 0,
    elites: int = 0,
) -> int:
    """Calculate weekly upkeep cost for all units.

    Formula (based on D&D 5e hireling wages):
    - Soldiers: 0.5gp per soldier per week (conscript/regular pay)
    - Spies: 1gp per spy per week (specialist pay)
    - Elites: 5gp per elite per week (elite unit pay)

    Args:
        soldiers: Number of soldiers
        spies: Number of spies
        elites: Number of elite units

    Returns:
        Total weekly upkeep cost in gold pieces
    """
    soldier_upkeep = int(soldiers * 0.5)
    spy_upkeep = spies * 1
    elite_upkeep = elites * 5
    
    return soldier_upkeep + spy_upkeep + elite_upkeep
