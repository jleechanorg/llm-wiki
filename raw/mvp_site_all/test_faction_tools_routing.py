#!/usr/bin/env python3
"""Test that faction tools work in Cerebras/OpenRouter providers."""

from __future__ import annotations

import json
import os
import unittest
from unittest.mock import patch

from mvp_site import constants, llm_service
from mvp_site.dice_strategy import DICE_STRATEGY_CODE_EXECUTION
from mvp_site.game_state import execute_tool_requests


# Import the unified executor from dice.py
from mvp_site.dice import execute_unified_tool as unified_tool_executor
from mvp_site.llm_providers import gemini_provider


class TestFactionToolsRouting(unittest.TestCase):
    """Test that faction tools are routed correctly."""

    def test_unified_executor_routes_faction_tools(self):
        """Unified executor should route faction tools to execute_faction_tool."""
        result = unified_tool_executor("faction_calculate_power", {
            "soldiers": 100,
            "spies": 0,
            "elites": 0,
        })

        self.assertIn("faction_power", result, "Should return faction_power")
        self.assertEqual(result["faction_power"], 100, "100 soldiers = 100 FP")

    def test_unified_executor_routes_dice_tools(self):
        """Unified executor should route dice tools to execute_dice_tool."""
        result = unified_tool_executor("roll_dice", {
            "notation": "1d20",
        })

        self.assertIn("total", result, "Should return dice total")
        self.assertGreaterEqual(result["total"], 1)
        self.assertLessEqual(result["total"], 20)

    def test_execute_tool_requests_handles_faction_tools(self):
        """execute_tool_requests should handle faction tools."""
        results = execute_tool_requests([
            {"tool": "faction_calculate_power", "args": {"soldiers": 50, "spies": 0, "elites": 0}},
        ])

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["tool"], "faction_calculate_power")
        self.assertIn("faction_power", results[0]["result"])

    def test_llm_service_code_execution_faction_tool_requests_are_executed(self):
        """llm_service should own Gemini code_execution faction orchestration."""

        class _StubResponse:
            def __init__(self, text: str):
                self.text = text
                self.candidates = []

        prompt_contents = [
            json.dumps(
                {
                    "game_state": {
                        "custom_campaign_state": {
                            "faction_minigame": {"enabled": True, "turn_number": 7}
                        }
                    }
                }
            )
        ]

        phase1 = _StubResponse(
            json.dumps(
                {
                    "tool_requests": [
                        {
                            "tool": "faction_calculate_power",
                            "args": {"soldiers": 100, "spies": 0, "elites": 0},
                        },
                    ]
                }
            )
        )
        phase2 = _StubResponse(json.dumps({"ok": True}))

        with patch.object(
            gemini_provider, "generate_content_with_code_execution", return_value=phase1
        ), patch(
            "mvp_site.dice_strategy.get_dice_roll_strategy",
            return_value=DICE_STRATEGY_CODE_EXECUTION,
        ), patch.object(
            llm_service,
            "execute_gemini_code_execution_tool_orchestration",
            return_value=[
                {
                    "tool": "faction_calculate_power",
                    "args": {"soldiers": 100, "spies": 0, "elites": 0},
                    "result": {"faction_power": 100},
                },
                {
                    "tool": "faction_calculate_ranking",
                    "args": {"player_faction_power": 100, "turn_number": 7},
                    "result": {"rank_name": "C"},
                },
            ],
        ), patch.object(
            gemini_provider, "generate_json_mode_content", return_value=phase2
        ):
            with patch.dict(os.environ, {"MOCK_SERVICES_MODE": "false"}):
                response = llm_service._call_llm_api(
                    prompt_contents=prompt_contents,
                    model_name="gemini-3-flash-preview",
                    current_prompt_text_for_logging="faction",
                    provider_name=constants.LLM_PROVIDER_GEMINI,
                )

        tool_results = getattr(response, "_tool_results", []) or []
        tool_names = [tr.get("tool") for tr in tool_results if isinstance(tr, dict)]

        self.assertIn("faction_calculate_power", tool_names)
        self.assertIn("faction_calculate_ranking", tool_names)


if __name__ == "__main__":
    unittest.main()
