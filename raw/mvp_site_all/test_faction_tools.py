"""
Unit tests for faction tool definitions and execution.

Tests verify tool schemas and that tools call correct functions.
"""

import os
import sys
import unittest
from unittest.mock import patch

# Add project root to path
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.insert(0, project_root)

from mvp_site import constants
from mvp_site.faction.tools import (
    FACTION_TOOL_NAMES,
    FACTION_TOOLS,
    execute_faction_tool,
)


class TestFactionToolsSchema(unittest.TestCase):
    """Test cases for faction tool schema definitions."""

    def test_faction_calculate_power_tool_schema(self):
        """Verify faction_calculate_power tool schema is correct."""
        # Find the tool in FACTION_TOOLS
        power_tool = None
        for tool in FACTION_TOOLS:
            if tool["function"]["name"] == "faction_calculate_power":
                power_tool = tool
                break

        self.assertIsNotNone(power_tool, "faction_calculate_power tool not found")

        # Verify schema structure
        self.assertEqual(power_tool["type"], "function")
        self.assertIn("parameters", power_tool["function"])
        self.assertIn("properties", power_tool["function"]["parameters"])

        # Verify required fields
        required = power_tool["function"]["parameters"].get("required", [])
        self.assertIn("soldiers", required)
        self.assertIn("spies", required)
        self.assertIn("elites", required)

    def test_faction_calculate_ranking_tool_schema(self):
        """Verify faction_calculate_ranking tool schema is correct."""
        # Find the tool in FACTION_TOOLS
        ranking_tool = None
        for tool in FACTION_TOOLS:
            if tool["function"]["name"] == "faction_calculate_ranking":
                ranking_tool = tool
                break

        self.assertIsNotNone(ranking_tool, "faction_calculate_ranking tool not found")

        # Verify schema structure
        self.assertEqual(ranking_tool["type"], "function")
        self.assertIn("parameters", ranking_tool["function"])
        self.assertIn("properties", ranking_tool["function"]["parameters"])

        # Verify required fields
        required = ranking_tool["function"]["parameters"].get("required", [])
        self.assertIn("player_faction_power", required)

    def test_faction_tools_are_in_faction_tools_list(self):
        """Verify tools are exported correctly."""
        tool_names = {tool["function"]["name"] for tool in FACTION_TOOLS}

        # Verify all expected tools are present
        self.assertIn("faction_calculate_power", tool_names)
        self.assertIn("faction_calculate_ranking", tool_names)
        self.assertIn("faction_simulate_battle", tool_names)
        self.assertIn("faction_intel_operation", tool_names)
        self.assertIn("faction_fp_to_next_rank", tool_names)

        # Verify FACTION_TOOL_NAMES matches
        self.assertEqual(tool_names, FACTION_TOOL_NAMES)

    def test_faction_tools_call_correct_functions(self):
        """Verify tool calls map to correct functions."""
        # Test faction_calculate_power
        with patch("mvp_site.faction.tools.calculate_faction_power") as mock_calc:
            mock_calc.return_value = 5000
            result = execute_faction_tool(
                "faction_calculate_power", {"soldiers": 100, "spies": 50, "elites": 10}
            )

            mock_calc.assert_called_once()
            self.assertIn("faction_power", result)
            self.assertEqual(result["faction_power"], 5000)

        # Test faction_calculate_ranking
        with patch("mvp_site.faction.tools.calculate_ranking") as mock_rank:
            mock_rank.return_value = (
                3,
                [{"name": "Player", "faction_power": 5000, "rank": 3}],
            )
            result = execute_faction_tool(
                "faction_calculate_ranking",
                {"player_faction_power": 5000, "turn_number": 1},
            )

            mock_rank.assert_called_once()
            self.assertIn("ranking", result)
            self.assertEqual(result["ranking"], 3)

    def test_faction_calculate_power_tool_execution(self):
        """Verify faction_calculate_power tool executes correctly."""
        result = execute_faction_tool(
            "faction_calculate_power",
            {
                "soldiers": 100,
                "spies": 50,
                "elites": 10,
                "elite_avg_level": 6,
                "territory": 200,
                "fortifications": 2,
            },
        )

        self.assertIn("faction_power", result)
        self.assertIsInstance(result["faction_power"], int)
        self.assertGreater(result["faction_power"], 0)
        self.assertIn("formatted", result)

    @patch("mvp_site.faction.rankings.get_all_ai_factions")
    def test_faction_calculate_ranking_tool_execution(self, mock_get_ai):
        """Verify faction_calculate_ranking tool executes correctly."""
        mock_get_ai.return_value = [
            {"name": "AI1", "base_fp": 10000, "difficulty": "hard"},
            {"name": "AI2", "base_fp": 5000, "difficulty": "medium"},
        ]

        # Use FP above MIN_RANK_FP to ensure ranking
        player_fp = max(6000, constants.MIN_RANK_FP + 1000)
        result = execute_faction_tool(
            "faction_calculate_ranking",
            {"player_faction_power": player_fp, "turn_number": 1},
        )

        self.assertIn("ranking", result)
        # ranking can be int or None
        if result["ranking"] is not None:
            self.assertIsInstance(result["ranking"], int)
            self.assertGreater(result["ranking"], 0)
        self.assertIn("formatted", result)

    def test_faction_tool_handles_missing_required_fields(self):
        """Verify tools handle missing required fields gracefully (by using defaults)."""
        result = execute_faction_tool(
            "faction_calculate_power",
            {"soldiers": 100},  # Missing spies and elites
        )

        # Should NOT return error, but calculate with defaults (0)
        self.assertIn("faction_power", result)
        self.assertIn("formatted", result)

    def test_faction_tool_handles_invalid_tool_name(self):
        """Verify handles invalid tool name gracefully."""
        result = execute_faction_tool("invalid_tool_name", {})

        # Should return error
        self.assertIn("error", result)
        self.assertIn("unknown faction tool", result.get("error", "").lower())

    def test_faction_fp_to_next_rank_accepts_faction_power_alias(self):
        """Verify faction_fp_to_next_rank accepts faction_power as parameter alias.

        Since faction_calculate_power returns 'faction_power' in its output,
        the LLM may naturally use this key. Both tools should accept it.
        """
        # Test with faction_power (alias)
        result_alias = execute_faction_tool(
            "faction_fp_to_next_rank", {"faction_power": 50000, "turn_number": 5}
        )

        # Test with player_faction_power (canonical)
        result_canonical = execute_faction_tool(
            "faction_fp_to_next_rank", {"player_faction_power": 50000, "turn_number": 5}
        )

        # Both should work and return the same fp_needed
        self.assertEqual(result_alias.get("current_fp"), 50000)
        self.assertEqual(result_canonical.get("current_fp"), 50000)
        self.assertEqual(
            result_alias.get("fp_needed"), result_canonical.get("fp_needed")
        )


if __name__ == "__main__":
    unittest.main()
