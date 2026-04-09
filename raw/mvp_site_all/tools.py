"""Faction tool definitions for LLM function calling.

Exposes faction Python code as Gemini function tools so the backend executes
calculations instead of the LLM manually applying formulas from prompts.

Pattern follows dice.py: FACTION_TOOLS list + execute_faction_tool() handler.
"""

from __future__ import annotations

from typing import Any

from mvp_site import logging_util
from mvp_site.faction.battle_sim import simulate_battle
from mvp_site.faction.combat import calculate_faction_power
from mvp_site.faction.intel import execute_intel_operation
from mvp_site.faction.rankings import calculate_ranking, get_fp_to_next_rank
from mvp_site.faction.srd_units import create_unit_group
from mvp_site.numeric_converters import coerce_int_safe as _coerce_int

# =============================================================================
# FACTION TOOL DEFINITIONS (for tool use / function calling)
# =============================================================================

# Canonical list of faction tool names (used by dice.py and game_state.py for routing)
FACTION_TOOL_NAMES = {
    "faction_simulate_battle",
    "faction_intel_operation",
    "faction_calculate_ranking",
    "faction_fp_to_next_rank",
    "faction_calculate_power",
}

FACTION_TOOLS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "faction_simulate_battle",
            "description": (
                "Simulate a tactical battle between attacker and defender forces. "
                "Returns casualties, victor, rounds fought, and battle log. "
                "Use this when the player attacks another faction or is attacked. "
                "The LLM should narrate the setup BEFORE calling this tool, then "
                "narrate the outcome AFTER receiving results."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "attacker_soldiers": {
                        "type": "integer",
                        "description": "Number of attacker soldiers",
                    },
                    "attacker_elites": {
                        "type": "integer",
                        "description": "Number of attacker elite units (default 0)",
                    },
                    "attacker_elite_type": {
                        "type": "string",
                        "description": "Type of attacker elites: elite_6, veteran, assassin (default elite_6)",
                    },
                    "defender_soldiers": {
                        "type": "integer",
                        "description": "Number of defender soldiers",
                    },
                    "defender_elites": {
                        "type": "integer",
                        "description": "Number of defender elite units (default 0)",
                    },
                    "defender_elite_type": {
                        "type": "string",
                        "description": "Type of defender elites: elite_6, veteran, assassin (default elite_6)",
                    },
                    "defender_fortifications": {
                        "type": "integer",
                        "description": "Defender fortification level 0-3 (adds defense bonus)",
                    },
                    "battle_seed": {
                        "type": "integer",
                        "description": "Random seed for reproducible results (optional)",
                    },
                },
                "required": ["attacker_soldiers", "defender_soldiers"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "faction_intel_operation",
            "description": (
                "Execute an intel/spy operation against a target faction. "
                "Returns success tier (FAILURE/PARTIAL/SUCCESS/CRITICAL), "
                "detection status, intel gathered, and combat buffs. "
                "Use this when the player sends spies to gather intelligence."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "spies_deployed": {
                        "type": "integer",
                        "description": "Number of spies assigned to this operation",
                    },
                    "target_shadow_networks": {
                        "type": "integer",
                        "description": "Target faction's shadow network count (counter-intel)",
                    },
                    "target_wards": {
                        "type": "integer",
                        "description": "Target faction's magical ward count",
                    },
                    "spymaster_modifier": {
                        "type": "integer",
                        "description": "Spymaster council member ability modifier (0 if none)",
                    },
                    "lineage_intrigue": {
                        "type": "integer",
                        "description": "Player's intrigue lineage level (0-5)",
                    },
                    "target_difficulty": {
                        "type": "string",
                        "description": "Target faction difficulty: easy, medium, hard, legendary",
                    },
                },
                "required": [
                    "spies_deployed",
                    "target_shadow_networks",
                    "target_wards",
                ],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "faction_calculate_ranking",
            "description": (
                "Calculate player's ranking among all 200 AI factions. "
                "Returns current rank (1-201 or None if unranked), and nearby factions. "
                "Use this to show the player their standing in the world."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "player_faction_power": {
                        "type": "integer",
                        "description": "Player's total Faction Power (FP)",
                    },
                    "turn_number": {
                        "type": "integer",
                        "description": "Current game turn (AI factions grow over time)",
                    },
                },
                "required": ["player_faction_power", "turn_number"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "faction_fp_to_next_rank",
            "description": (
                "Calculate Faction Power needed to reach the next higher rank. "
                "Returns FP gap to beat the faction above, or None if already #1."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "player_faction_power": {
                        "type": "integer",
                        "description": "Player's current Faction Power",
                    },
                    "turn_number": {
                        "type": "integer",
                        "description": "Current game turn",
                    },
                },
                "required": ["player_faction_power", "turn_number"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "faction_calculate_power",
            "description": (
                "Calculate total Faction Power (FP) from faction assets. "
                "Use this to compute FP after state changes (recruitment, conquest, etc)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "soldiers": {
                        "type": "integer",
                        "description": "Number of soldiers",
                    },
                    "spies": {
                        "type": "integer",
                        "description": "Number of spies",
                    },
                    "elites": {
                        "type": "integer",
                        "description": "Number of elite units",
                    },
                    "elite_avg_level": {
                        "type": "integer",
                        "description": "Average level of elites (6-20, default 6)",
                    },
                    "territory": {
                        "type": "integer",
                        "description": "Territory in acres",
                    },
                    "fortifications": {
                        "type": "integer",
                        "description": "Number of fortification buildings",
                    },
                },
                "required": ["soldiers", "spies", "elites"],
            },
        },
    },
]


# =============================================================================
# Tool Execution Handler
# =============================================================================


def _coerce_str(value: Any, default: str = "") -> str:
    """Safely coerce value to string."""
    if value is None:
        return default
    return str(value)


def execute_faction_tool(tool_name: str, arguments: dict) -> dict:
    """Execute a faction tool call and return the result.

    Args:
        tool_name: Name of the faction tool to execute
        arguments: Tool arguments from LLM

    Returns:
        Dict with tool results and "formatted" string for LLM consumption
    """
    logging_util.info(
        logging_util.with_campaign(
            f"FACTION_TOOL_EXEC: tool={tool_name} | args={arguments}"
        )
    )

    if tool_name == "faction_simulate_battle":
        # Validate required fields
        if "attacker_soldiers" not in arguments:
            return {
                "error": "Missing required field: attacker_soldiers",
                "formatted": "ERROR: attacker_soldiers is required for battle simulation",
            }
        if "defender_soldiers" not in arguments:
            return {
                "error": "Missing required field: defender_soldiers",
                "formatted": "ERROR: defender_soldiers is required for battle simulation",
            }

        # Parse attacker forces
        attacker_soldiers = _coerce_int(arguments.get("attacker_soldiers"), 0)
        attacker_elites = _coerce_int(arguments.get("attacker_elites"), 0)
        attacker_elite_type = _coerce_str(
            arguments.get("attacker_elite_type"), "elite_6"
        )

        # Parse defender forces
        defender_soldiers = _coerce_int(arguments.get("defender_soldiers"), 0)
        defender_elites = _coerce_int(arguments.get("defender_elites"), 0)
        defender_elite_type = _coerce_str(
            arguments.get("defender_elite_type"), "elite_6"
        )
        defender_forts = _coerce_int(arguments.get("defender_fortifications"), 0)

        # Validate non-negative values
        if attacker_soldiers < 0:
            logging_util.warning(
                logging_util.with_campaign(
                    f"FACTION_TOOL_NEGATIVE_VALUE: attacker_soldiers={attacker_soldiers}, clamping to 0"
                )
            )
            attacker_soldiers = 0
        if attacker_elites < 0:
            logging_util.warning(
                logging_util.with_campaign(
                    f"FACTION_TOOL_NEGATIVE_VALUE: attacker_elites={attacker_elites}, clamping to 0"
                )
            )
            attacker_elites = 0
        if defender_soldiers < 0:
            logging_util.warning(
                logging_util.with_campaign(
                    f"FACTION_TOOL_NEGATIVE_VALUE: defender_soldiers={defender_soldiers}, clamping to 0"
                )
            )
            defender_soldiers = 0
        if defender_elites < 0:
            logging_util.warning(
                logging_util.with_campaign(
                    f"FACTION_TOOL_NEGATIVE_VALUE: defender_elites={defender_elites}, clamping to 0"
                )
            )
            defender_elites = 0
        if defender_forts < 0:
            logging_util.warning(
                logging_util.with_campaign(
                    f"FACTION_TOOL_NEGATIVE_VALUE: defender_fortifications={defender_forts}, clamping to 0"
                )
            )
            defender_forts = 0

        # Optional seed
        seed = arguments.get("battle_seed")
        if seed is not None:
            seed = _coerce_int(seed)

        # Validate non-empty armies
        if attacker_soldiers == 0 and attacker_elites == 0:
            return {
                "error": "Attacker army is empty (no soldiers or elites)",
                "formatted": "ERROR: Cannot simulate battle with empty attacker army",
            }
        if defender_soldiers == 0 and defender_elites == 0:
            return {
                "error": "Defender army is empty (no soldiers or elites)",
                "formatted": "ERROR: Cannot simulate battle with empty defender army",
            }

        # Build unit groups
        try:
            attacker_units = []
            if attacker_soldiers > 0:
                attacker_units.append(create_unit_group("soldier", attacker_soldiers))
            if attacker_elites > 0:
                attacker_units.append(
                    create_unit_group(attacker_elite_type, attacker_elites)
                )

            defender_units = []
            if defender_soldiers > 0:
                defender_units.append(create_unit_group("soldier", defender_soldiers))
            if defender_elites > 0:
                defender_units.append(
                    create_unit_group(defender_elite_type, defender_elites)
                )
        except KeyError as exc:
            message = exc.args[0] if exc.args else str(exc)
            logging_util.warning(
                logging_util.with_campaign(
                    f"FACTION_TOOL_INVALID_UNIT_TYPE: tool={tool_name} | error={message}"
                )
            )
            return {
                "error": message,
                "formatted": (
                    f"ERROR: {message}. "
                    "Try an allowed elite type like 'elite_6', 'veteran', or 'assassin'."
                ),
            }

        # Apply fortification bonus to defender stats
        if defender_forts > 0 and defender_units:
            fort_ac_bonus = defender_forts * 2  # +2 AC per fort level
            for unit in defender_units:
                unit["stats"]["ac"] += fort_ac_bonus

        # Run battle simulation
        result = simulate_battle(
            attacker_units=attacker_units,
            defender_units=defender_units,
            seed=seed,
            mode="fast",
        )

        # Format for LLM
        formatted = (
            f"BATTLE RESULT: {result['victor'].upper()} VICTORY | "
            f"Rounds: {result['rounds']} | "
            f"Attacker casualties: {result['attacker_casualties']} "
            f"(remaining: {result['attacker_remaining']}) | "
            f"Defender casualties: {result['defender_casualties']} "
            f"(remaining: {result['defender_remaining']})"
        )

        tool_result = {
            "victor": result["victor"],
            "rounds": result["rounds"],
            "attacker_casualties": result["attacker_casualties"],
            "attacker_remaining": result["attacker_remaining"],
            "defender_casualties": result["defender_casualties"],
            "defender_remaining": result["defender_remaining"],
            "battle_log": result["detailed_log"][:10],  # First 10 log entries
            "formatted": formatted,
        }

        logging_util.info(
            logging_util.with_campaign(
                f"FACTION_TOOL_RESULT: tool=faction_simulate_battle | "
                f"victor={result['victor']} | rounds={result['rounds']} | "
                f"atk_casualties={result['attacker_casualties']} | "
                f"def_casualties={result['defender_casualties']}"
            )
        )
        return tool_result

    if tool_name == "faction_intel_operation":
        spies = _coerce_int(arguments.get("spies_deployed"), 1)
        shadow_networks = _coerce_int(arguments.get("target_shadow_networks"), 0)
        wards = _coerce_int(arguments.get("target_wards"), 0)
        spymaster_mod = _coerce_int(arguments.get("spymaster_modifier"), 0)
        intrigue = _coerce_int(arguments.get("lineage_intrigue"), 0)
        difficulty = _coerce_str(arguments.get("target_difficulty"), "medium")

        result = execute_intel_operation(
            spies_deployed=spies,
            target_shadow_networks=shadow_networks,
            target_wards=wards,
            spymaster_mod=spymaster_mod,
            lineage_intrigue=intrigue,
            target_difficulty=difficulty,
        )

        formatted = (
            f"INTEL RESULT: {result['tier']} | "
            f"Detected: {'YES' if result['detected'] else 'NO'} | "
            f"Intel gathered: {result['intel_gathered']} points | "
            f"{result['message']}"
        )

        tool_result = {
            "tier": result["tier"],
            "detected": result["detected"],
            "intel_gathered": result["intel_gathered"],
            "message": result["message"],
            "formatted": formatted,
        }

        logging_util.info(
            logging_util.with_campaign(
                f"FACTION_TOOL_RESULT: tool=faction_intel_operation | "
                f"tier={result['tier']} | detected={result['detected']} | "
                f"intel={result['intel_gathered']}"
            )
        )
        return tool_result

    if tool_name == "faction_calculate_ranking":
        # Accept both player_faction_power and faction_power for flexibility
        # Use explicit None check to preserve valid 0 values
        raw_fp = arguments.get("player_faction_power")
        if raw_fp is None:
            raw_fp = arguments.get("faction_power")
        player_fp = _coerce_int(raw_fp, 0)
        turn = _coerce_int(arguments.get("turn_number"), 1)

        ranking, factions = calculate_ranking(player_fp, turn)

        # Get nearby factions for context
        if ranking is not None:
            player_idx = ranking - 1
            above = factions[max(0, player_idx - 2) : player_idx]
            below = factions[player_idx + 1 : player_idx + 3]
        else:
            above = []
            below = []

        if ranking is None:
            formatted = (
                f"RANKING: UNRANKED (FP {player_fp} below threshold) | "
                f"Total factions: {len(factions)}"
            )
        else:
            formatted = (
                f"RANKING: #{ranking} of {len(factions)} | Player FP: {player_fp}"
            )
            if above:
                formatted += f" | Above: {[f['name'] + ' (' + str(f['faction_power']) + ' FP)' for f in above]}"
            if below:
                formatted += f" | Below: {[f['name'] + ' (' + str(f['faction_power']) + ' FP)' for f in below]}"

        tool_result = {
            "ranking": ranking,
            "total_factions": len(factions),
            "player_fp": player_fp,
            "factions_above": [
                {"name": f["name"], "fp": f["faction_power"]} for f in above
            ],
            "factions_below": [
                {"name": f["name"], "fp": f["faction_power"]} for f in below
            ],
            "formatted": formatted,
        }

        logging_util.info(
            logging_util.with_campaign(
                f"FACTION_TOOL_RESULT: tool=faction_calculate_ranking | "
                f"ranking={ranking} | player_fp={player_fp} | turn={turn}"
            )
        )
        return tool_result

    if tool_name == "faction_fp_to_next_rank":
        # Accept both player_faction_power and faction_power for flexibility
        # (matches faction_calculate_ranking behavior)
        raw_fp = arguments.get("player_faction_power")
        if raw_fp is None:
            raw_fp = arguments.get("faction_power")
        player_fp = _coerce_int(raw_fp, 0)
        turn = _coerce_int(arguments.get("turn_number"), 1)

        fp_needed = get_fp_to_next_rank(player_fp, turn)

        if fp_needed is None:
            formatted = "FP TO NEXT RANK: Already #1! No higher rank to achieve."
        else:
            formatted = f"FP TO NEXT RANK: Need {fp_needed} more FP to advance"

        tool_result = {
            "fp_needed": fp_needed,
            "current_fp": player_fp,
            "formatted": formatted,
        }

        logging_util.info(
            logging_util.with_campaign(
                f"FACTION_TOOL_RESULT: tool=faction_fp_to_next_rank | "
                f"fp_needed={fp_needed} | current_fp={player_fp}"
            )
        )
        return tool_result

    if tool_name == "faction_calculate_power":
        soldiers = _coerce_int(arguments.get("soldiers"), 0)
        spies = _coerce_int(arguments.get("spies"), 0)
        elites = _coerce_int(arguments.get("elites"), 0)
        elite_level = _coerce_int(arguments.get("elite_avg_level"), 6)
        territory = _coerce_int(arguments.get("territory"), 0)
        forts = _coerce_int(arguments.get("fortifications"), 0)

        fp = calculate_faction_power(
            soldiers=soldiers,
            spies=spies,
            elites=elites,
            elite_avg_level=elite_level,
            territory=territory,
            fortifications=forts,
        )

        formatted = (
            f"FACTION POWER: {fp} FP | "
            f"Army: {soldiers} soldiers, {spies} spies, {elites} elites (lvl {elite_level}) | "
            f"Territory: {territory} acres | Forts: {forts}"
        )

        tool_result = {
            "faction_power": fp,
            "breakdown": {
                "soldiers": soldiers,
                "spies": spies,
                "elites": elites,
                "elite_avg_level": elite_level,
                "territory": territory,
                "fortifications": forts,
            },
            "formatted": formatted,
        }

        logging_util.info(
            logging_util.with_campaign(
                f"FACTION_TOOL_RESULT: tool=faction_calculate_power | fp={fp}"
            )
        )
        return tool_result

    # Unknown tool
    logging_util.warning(
        logging_util.with_campaign(f"FACTION_TOOL_UNKNOWN: tool={tool_name}")
    )
    return {
        "error": f"Unknown faction tool: {tool_name}",
        "formatted": f"ERROR: Unknown faction tool '{tool_name}'",
    }
