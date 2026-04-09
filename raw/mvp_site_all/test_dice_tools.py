"""
Unit tests for dice tools and execution.

These tests validate the dice tool definitions and execution logic
without requiring real LLM calls.
"""

# ruff: noqa: PT009,N802,SIM117

import os
import pathlib
import unittest
from unittest.mock import patch

from mvp_site.dice import DICE_ROLL_TOOLS, execute_dice_tool
from mvp_site.dice_integrity import (
    _extract_dice_audit_events_from_tool_results,
)
from mvp_site.llm_providers.gemini_provider import _DICE_TOOL_NAMES

os.environ["TESTING_AUTH_BYPASS"] = "true"


class TestDiceRollTools(unittest.TestCase):
    """Test the dice roll tool definitions."""

    def test_dice_roll_tools_exist(self):
        """Verify DICE_ROLL_TOOLS array contains all required tools."""
        tool_names = [t["function"]["name"] for t in DICE_ROLL_TOOLS]
        self.assertIn("roll_dice", tool_names)
        self.assertIn("roll_attack", tool_names)
        self.assertIn("roll_skill_check", tool_names)
        self.assertIn("roll_saving_throw", tool_names)

    def test_execute_dice_tool_roll_dice(self):
        """Verify execute_dice_tool handles roll_dice correctly."""
        result = execute_dice_tool(
            "roll_dice", {"notation": "2d6+3", "purpose": "damage"}
        )
        self.assertIn("notation", result)
        self.assertIn("total", result)
        self.assertIn("rolls", result)
        self.assertEqual(result["notation"], "2d6+3")
        self.assertEqual(result["purpose"], "damage")

    def test_execute_dice_tool_roll_attack(self):
        """Verify execute_dice_tool handles roll_attack correctly."""
        result = execute_dice_tool(
            "roll_attack",
            {"attack_modifier": 5, "damage_notation": "1d8+3", "target_ac": 15},
        )
        self.assertIn("attack_roll", result)
        self.assertIn("target_ac", result)
        self.assertIn("hit", result)
        self.assertEqual(result["target_ac"], 15)

    def test_execute_dice_tool_roll_skill_check(self):
        """Verify execute_dice_tool handles roll_skill_check correctly."""
        result = execute_dice_tool(
            "roll_skill_check",
            {
                "attribute_modifier": 3,
                "proficiency_bonus": 2,
                "proficient": True,
                "dc": 15,
                "dc_reasoning": "guard is distracted",
                "skill_name": "Stealth",
            },
        )
        self.assertIn("skill", result)
        self.assertIn("total", result)
        self.assertIn("success", result)
        self.assertEqual(result["skill"], "Stealth")

    def test_execute_dice_tool_skill_check_with_dc_reasoning(self):
        """Verify roll_skill_check includes dc_reasoning in the result."""
        dc_reasoning = "FBI agent, professionally trained to resist manipulation"
        result = execute_dice_tool(
            "roll_skill_check",
            {
                "attribute_modifier": 4,
                "proficiency_bonus": 2,
                "proficient": True,
                "dc": 18,
                "dc_reasoning": dc_reasoning,
                "skill_name": "Persuasion",
            },
        )
        self.assertIn("dc_reasoning", result)
        self.assertEqual(result["dc_reasoning"], dc_reasoning)
        self.assertEqual(result["dc"], 18)
        self.assertIn("formatted", result)
        self.assertIn("vs DC 18", result["formatted"])
        self.assertIn("FBI agent", result["formatted"])

    def test_execute_dice_tool_saving_throw_with_dc_reasoning(self):
        """Verify roll_saving_throw includes dc_reasoning in the result."""
        dc_reasoning = "Fireball from 5th-level caster (8+3+3)"
        result = execute_dice_tool(
            "roll_saving_throw",
            {
                "attribute_modifier": 2,
                "proficiency_bonus": 2,
                "proficient": False,
                "dc": 14,
                "dc_reasoning": dc_reasoning,
                "save_type": "DEX",
            },
        )
        self.assertIn("dc_reasoning", result)
        self.assertEqual(result["dc_reasoning"], dc_reasoning)
        self.assertEqual(result["dc"], 14)
        self.assertIn("formatted", result)
        self.assertIn("vs DC 14", result["formatted"])
        self.assertIn("Fireball", result["formatted"])

    def test_skill_check_auto_fills_dc_reasoning_when_missing(self):
        """Verify roll_skill_check auto-fills dc_reasoning when missing."""
        result = execute_dice_tool(
            "roll_skill_check",
            {
                "attribute_modifier": 3,
                "proficiency_bonus": 2,
                "dc": 15,
                "skill_name": "Stealth",
            },
        )
        self.assertNotIn("error", result)
        self.assertIn("roll", result)
        self.assertIn("total", result)
        self.assertIn("success", result)
        self.assertIn("formatted", result)
        self.assertIn("DC 15", result["formatted"])

    def test_saving_throw_auto_fills_dc_reasoning_when_missing(self):
        """Verify roll_saving_throw auto-fills dc_reasoning when missing."""
        result = execute_dice_tool(
            "roll_saving_throw",
            {
                "attribute_modifier": 2,
                "proficiency_bonus": 2,
                "dc": 14,
                "save_type": "DEX",
            },
        )
        self.assertNotIn("error", result)
        self.assertIn("roll", result)
        self.assertIn("total", result)
        self.assertIn("success", result)
        self.assertIn("formatted", result)
        self.assertIn("DC 14", result["formatted"])

    def test_execute_dice_tool_unknown(self):
        """Unknown tool should return error."""
        result = execute_dice_tool("unknown_tool", {})
        self.assertIn("error", result)


class TestDiceToolExecution(unittest.TestCase):
    """Test cases for server-side dice tool execution."""

    def test_execute_dice_tool_roll_dice_with_mock(self):
        """roll_dice tool should return correct structure."""
        with patch("mvp_site.dice.roll_dice_notation") as mock_roll:
            mock_roll.return_value = {
                "notation": "1d20",
                "total": 15,
                "rolls": [15],
                "type": "d20",
            }
            result = execute_dice_tool("roll_dice", {"notation": "1d20"})
            self.assertEqual(result["total"], 15)
            self.assertEqual(result["notation"], "1d20")
            self.assertIn("rolls", result)

    def test_execute_dice_tool_roll_attack_with_mock(self):
        """roll_attack tool should return correct structure."""
        with patch("mvp_site.dice.roll_dice_notation") as mock_roll:
            mock_roll.return_value = {"total": 15, "rolls": [15]}
            result = execute_dice_tool("roll_attack", {"attack_modifier": 5})
            self.assertIn("attack_roll", result)
            self.assertIn("total", result["attack_roll"])


class TestDCAuditTrail(unittest.TestCase):
    """Test that DC and dc_reasoning are properly captured in audit events."""

    def test_dice_audit_events_include_dc_for_skill_check(self):
        """Verify dice_audit_events extraction includes DC and dc_reasoning."""
        tool_results = [
            {
                "tool": "roll_skill_check",
                "args": {
                    "skill_name": "Persuasion",
                    "dc": 18,
                    "dc_reasoning": "FBI agent, trained to resist",
                },
                "result": {
                    "skill": "Persuasion",
                    "roll": 14,
                    "modifier": 6,
                    "total": 20,
                    "dc": 18,
                    "dc_reasoning": "FBI agent, trained to resist",
                    "success": True,
                },
            }
        ]
        events = _extract_dice_audit_events_from_tool_results(tool_results)
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event["label"], "Persuasion")
        self.assertEqual(event["total"], 20)
        self.assertEqual(event["dc"], 18)
        self.assertEqual(event["dc_reasoning"], "FBI agent, trained to resist")
        self.assertTrue(event["success"])

    def test_dice_audit_events_include_dc_for_saving_throw(self):
        """Verify dice_audit_events extraction includes DC for saves."""
        tool_results = [
            {
                "tool": "roll_saving_throw",
                "args": {
                    "save_type": "DEX",
                    "dc": 14,
                    "dc_reasoning": "Fireball DC 14",
                },
                "result": {
                    "save_type": "DEX",
                    "roll": 8,
                    "modifier": 2,
                    "total": 10,
                    "dc": 14,
                    "dc_reasoning": "Fireball DC 14",
                    "success": False,
                },
            }
        ]
        events = _extract_dice_audit_events_from_tool_results(tool_results)
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event["label"], "DEX Save")
        self.assertEqual(event["total"], 10)
        self.assertEqual(event["dc"], 14)
        self.assertEqual(event["dc_reasoning"], "Fireball DC 14")
        self.assertFalse(event["success"])


class TestCodeExecutionDiceToolExposure(unittest.TestCase):
    """Test that dice tools are NOT exposed in Gemini code_execution mode.

    REV-3wj: In code_execution mode, we want ZERO dice tool exposure to prevent
    the model from emitting tool_requests for dice. Dice should only be computed
    via code_execution (Python code with random.randint).
    """

    def test_code_execution_override_does_not_name_dice_tools(self):
        """CODE_EXECUTION_DICE_OVERRIDE must NOT contain dice tool names.

        If we name the tools (even to say "don't use them"), we teach the model
        the vocabulary and it may still emit tool_requests for them.
        """
        from mvp_site.llm_providers.gemini_provider import CODE_EXECUTION_DICE_OVERRIDE

        dice_tool_names = [
            "roll_dice",
            "roll_attack",
            "roll_skill_check",
            "roll_saving_throw",
        ]

        for tool_name in dice_tool_names:
            self.assertNotIn(
                tool_name,
                CODE_EXECUTION_DICE_OVERRIDE,
                f"CODE_EXECUTION_DICE_OVERRIDE must NOT contain '{tool_name}' - "
                f"naming tools teaches the model vocabulary even when saying 'don't use'",
            )

    def test_apply_code_execution_system_instruction_strips_marked_dice_tools(self):
        """System instruction with marked dice sections gets those sections stripped."""
        from mvp_site.llm_providers.gemini_provider import (
            apply_code_execution_system_instruction,
        )

        # Sample system instruction with properly marked dice tool sections
        original_instruction = """
        General game instructions here.

        <!-- BEGIN_TOOL_REQUESTS_DICE: Dice guidance stripped for code_execution -->
        Use roll_dice for damage. Use roll_attack for attacks.
        roll_skill_check and roll_saving_throw are also available.
        <!-- END_TOOL_REQUESTS_DICE -->

        Other instructions continue here.
        """

        result = apply_code_execution_system_instruction(
            original_instruction, "gemini-3.0-flash"
        )

        # Marked sections should be stripped
        dice_tool_names = [
            "roll_dice",
            "roll_attack",
            "roll_skill_check",
            "roll_saving_throw",
        ]
        for tool_name in dice_tool_names:
            self.assertNotIn(
                tool_name,
                result,
                f"Marked dice section should be stripped - '{tool_name}' still present",
            )

        # Unmarked content should remain
        self.assertIn("General game instructions", result)
        self.assertIn("Other instructions continue", result)

    def test_non_code_execution_models_retain_dice_tools(self):
        """Gemini 2.x models should still have dice tool references (regression test)."""
        from mvp_site.llm_providers.gemini_provider import (
            apply_code_execution_system_instruction,
        )

        original_instruction = "Use roll_dice for damage. Use roll_attack for attacks."

        # Gemini 2.x should NOT strip dice tools
        result = apply_code_execution_system_instruction(
            original_instruction, "gemini-2.0-flash"
        )

        self.assertIn("roll_dice", result)
        self.assertIn("roll_attack", result)

    def test_dice_tool_names_constant_matches_dice_roll_tools(self):
        """REV-65v: _DICE_TOOL_NAMES must match actual dice rolling tools.

        Note: DICE_ROLL_TOOLS includes declare_no_roll_needed which is a meta-tool
        (declares no roll needed), not an actual dice roll. It should NOT be
        filtered in code_execution mode since the model should be able to skip
        dice rolling for trivial actions.
        """
        from mvp_site.dice import DICE_ROLL_TOOLS
        from mvp_site.llm_providers.gemini_provider import _DICE_TOOL_NAMES

        # Meta-tools that don't perform actual dice rolls
        meta_tools = {"declare_no_roll_needed"}

        # Extract actual dice rolling tool names (exclude meta-tools)
        dice_tool_names_from_source = {
            t["function"]["name"]
            for t in DICE_ROLL_TOOLS
            if t["function"]["name"] not in meta_tools
        }

        # Verify _DICE_TOOL_NAMES matches actual dice rolling tools
        self.assertEqual(
            _DICE_TOOL_NAMES,
            dice_tool_names_from_source,
            "_DICE_TOOL_NAMES must match actual dice rolling tools in DICE_ROLL_TOOLS",
        )


    def test_code_execution_variant_prompts_do_not_name_dice_tools(self):
        """code_execution variant prompts must NOT name dice tools.

        The prompts dice_system_instruction_code_execution.md and
        mechanics_system_instruction_code_execution.md should say
        "Do NOT use tool_requests for dice" WITHOUT naming specific tools
        like roll_dice, roll_attack, etc. Naming them teaches the model
        the vocabulary and it may still emit tool_requests for them.
        """
        prompts_dir = pathlib.Path(__file__).parent.parent / "prompts"

        variant_files = [
            "dice_system_instruction_code_execution.md",
            "mechanics_system_instruction_code_execution.md",
        ]

        for filename in variant_files:
            filepath = prompts_dir / filename
            self.assertTrue(
                filepath.exists(),
                f"Missing prompt file: {filename}",
            )
            content = filepath.read_text()
            for tool_name in _DICE_TOOL_NAMES:
                self.assertNotIn(
                    tool_name,
                    content,
                    f"{filename} must NOT contain '{tool_name}' - "
                    f"naming dice tools teaches the model vocabulary even in prohibition"
                )


if __name__ == "__main__":
    unittest.main()
