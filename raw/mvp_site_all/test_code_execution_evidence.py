"""
Unit tests for code execution evidence extraction and RNG verification.

These tests validate the code execution evidence extraction logic
without requiring real LLM calls.
"""

# ruff: noqa: PT009,N802,SIM117

import os
import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from mvp_site.dice_integrity import _is_code_execution_fabrication
from mvp_site.llm_providers import gemini_code_execution, gemini_provider

os.environ["TESTING_AUTH_BYPASS"] = "true"


class TestCodeExecutionFabricationDetection(unittest.TestCase):
    """TDD tests for code_execution fabrication detection edge cases."""

    def test_empty_evidence_dict_flags_fabrication_when_dice_present(self):
        """Empty evidence dict should still evaluate fabrication when dice are present."""
        structured = SimpleNamespace(
            action_resolution={
                "mechanics": {"rolls": [{"notation": "1d20", "total": 12}]}
            }
        )
        evidence = {}
        self.assertTrue(
            _is_code_execution_fabrication(structured, evidence),
            "Empty evidence dict should not bypass fabrication detection",
        )

    def test_string_audit_events_count_as_dice_when_rolls_missing(self):
        """Legacy string audit_events should count as dice evidence when rolls are absent."""
        structured = SimpleNamespace(
            action_resolution={
                "mechanics": {"audit_events": ["1d20 = 17 (perception)"]}
            }
        )
        self.assertTrue(
            _is_code_execution_fabrication(structured, None),
            "String audit_events should trigger fabrication detection when evidence is missing",
        )

    def test_string_audit_events_with_rng_verified_is_not_fabrication(self):
        """Legacy string audit_events should not be flagged when RNG evidence is verified."""
        structured = SimpleNamespace(
            action_resolution={
                "mechanics": {"audit_events": ["1d20 = 17 (perception)"]}
            }
        )
        evidence_with_rng = {
            "code_execution_used": True,
            "rng_verified": True,
        }
        self.assertFalse(
            _is_code_execution_fabrication(structured, evidence_with_rng),
            "RNG-verified evidence should clear fabrication even with string audit_events",
        )


class TestRNGVerification(unittest.TestCase):
    """Tests for RNG verification in code execution dice rolls."""

    @staticmethod
    def _make_mock_response(code: str, output: str = '{"rolls": [15], "total": 15}'):
        mock_response = Mock()
        mock_part = Mock()
        mock_part.executable_code = Mock(language="python", code=code)
        mock_part.code_execution_result = Mock(outcome="OUTCOME_OK", output=output)
        mock_response.candidates = [Mock(content=Mock(parts=[mock_part]))]
        return mock_response

    def test_fabrication_detected_when_code_lacks_rng(self):
        """Code that prints JSON without random.randint() should be FABRICATION."""
        structured = SimpleNamespace(
            action_resolution={
                "mechanics": {"rolls": [{"notation": "1d20", "total": 16}]}
            }
        )
        evidence_no_rng = {
            "code_execution_used": True,
            "executable_code_parts": 1,
            "code_execution_result_parts": 1,
            "stdout": '{"rolls": [16], "total": 21}',
            "stdout_is_valid_json": True,
            "code_contains_rng": False,
            "rng_verified": False,
        }
        self.assertTrue(
            _is_code_execution_fabrication(structured, evidence_no_rng),
            "Code execution WITHOUT random.randint() should be detected as FABRICATION",
        )

    def test_extract_evidence_includes_rng_verified_field(self):
        """extract_code_execution_evidence should return rng_verified field."""
        mock_response = Mock()
        mock_part = Mock()
        mock_part.executable_code = Mock(
            language="python",
            code='import json; print(json.dumps({"rolls": [16], "total": 21}))',
        )
        mock_part.code_execution_result = Mock(
            outcome="OUTCOME_OK", output='{"rolls": [16], "total": 21}'
        )
        mock_response.candidates = [Mock(content=Mock(parts=[mock_part]))]
        evidence = gemini_provider.extract_code_execution_evidence(mock_response)
        self.assertIn("rng_verified", evidence)
        self.assertFalse(
            evidence.get("rng_verified", True),
            "rng_verified should be False when code lacks random.randint()",
        )

    def test_valid_rng_passes_verification(self):
        """Legitimate dice rolls with actual RNG should not be flagged."""
        structured = SimpleNamespace(
            action_resolution={
                "mechanics": {"rolls": [{"notation": "1d20", "total": 15}]}
            }
        )
        evidence_with_rng = {
            "code_execution_used": True,
            "executable_code_parts": 1,
            "code_execution_result_parts": 1,
            "stdout": '{"rolls": [15], "total": 20}',
            "stdout_is_valid_json": True,
            "code_contains_rng": True,
            "rng_verified": True,
        }
        self.assertFalse(
            _is_code_execution_fabrication(structured, evidence_with_rng),
            "Code with random.randint() should NOT be flagged as fabrication",
        )

    def test_extract_evidence_detects_rng_in_code(self):
        """extract_code_execution_evidence should detect RNG in code."""
        mock_response = self._make_mock_response(
            "import random, json; roll = random.randint(1, 20); "
            'print(json.dumps({"rolls": [roll], "total": roll}))'
        )
        evidence = gemini_provider.extract_code_execution_evidence(mock_response)
        self.assertTrue(evidence.get("code_execution_used"))
        self.assertTrue(evidence.get("code_contains_rng"))
        self.assertTrue(evidence.get("rng_verified"))

    def test_extract_evidence_detects_rng_from_imported_randint(self):
        """Should detect RNG for from-import style."""
        mock_response = self._make_mock_response(
            "from random import randint; import json; roll = randint(1, 20); "
            'print(json.dumps({"rolls": [roll], "total": roll}))'
        )
        evidence = gemini_provider.extract_code_execution_evidence(mock_response)
        self.assertTrue(evidence.get("code_contains_rng"))
        self.assertTrue(evidence.get("rng_verified"))

    def test_extract_evidence_detects_rng_for_numpy_alias(self):
        """Should detect RNG for numpy alias."""
        mock_response = self._make_mock_response(
            "import numpy as np, json; roll = np.random.randint(1, 21); "
            'print(json.dumps({"rolls": [int(roll)], "total": int(roll)}))'
        )
        evidence = gemini_provider.extract_code_execution_evidence(mock_response)
        self.assertTrue(evidence.get("code_contains_rng"))
        self.assertTrue(evidence.get("rng_verified"))

    def test_extract_evidence_detects_rng_for_default_rng_generator(self):
        """Should detect RNG for default_rng generator."""
        mock_response = self._make_mock_response(
            "import numpy as np, json; rng = np.random.default_rng(); "
            "roll = rng.integers(1, 21); "
            'print(json.dumps({"rolls": [int(roll)], "total": int(roll)}))'
        )
        evidence = gemini_provider.extract_code_execution_evidence(mock_response)
        self.assertTrue(evidence.get("code_contains_rng"))
        self.assertTrue(evidence.get("rng_verified"))

    def test_extract_evidence_detects_rng_for_system_random_chain(self):
        """Should detect RNG for SystemRandom chain."""
        mock_response = self._make_mock_response(
            "import random, json; roll = random.SystemRandom().randint(1, 20); "
            'print(json.dumps({"rolls": [roll], "total": roll}))'
        )
        evidence = gemini_provider.extract_code_execution_evidence(mock_response)
        self.assertTrue(evidence.get("code_contains_rng"))
        self.assertTrue(evidence.get("rng_verified"))

    def test_extract_evidence_flags_dc_after_rng(self):
        """Should flag DC assignments that occur after RNG calls."""
        mock_response = self._make_mock_response(
            "import random, json; roll = random.randint(1, 20); dc = 12; "
            'print(json.dumps({"rolls": [roll], "total": roll, "dc": dc}))'
        )
        evidence = gemini_provider.extract_code_execution_evidence(mock_response)
        self.assertIs(evidence.get("dc_set_before_rng"), False)

    def test_extract_evidence_accepts_dc_before_rng(self):
        """Should accept DC assignments that occur before RNG calls."""
        mock_response = self._make_mock_response(
            "import random, json; dc = 12; dc_reasoning = 'Test'; "
            "roll = random.randint(1, 20); "
            'print(json.dumps({"rolls": [roll], "total": roll, "dc": dc}))'
        )
        evidence = gemini_provider.extract_code_execution_evidence(mock_response)
        self.assertTrue(evidence.get("dc_set_before_rng"))

    def test_extract_evidence_omits_dc_check_when_no_dc_used(self):
        """Should not flag DC ordering when RNG is used without any DC."""
        mock_response = self._make_mock_response(
            "import random, json; roll = random.randint(1, 20); "
            'print(json.dumps({"rolls": [roll], "total": roll}))'
        )
        evidence = gemini_provider.extract_code_execution_evidence(mock_response)
        self.assertIsNone(evidence.get("dc_set_before_rng"))
        self.assertIsNone(evidence.get("dc_set_before_next_rng"))

    def test_extract_evidence_flags_missing_dc_when_output_includes_dc(self):
        """Should flag dc_reasoning_missing when output includes DC but no reasoning."""
        # Updated: With schema-based validation, we don't set dc_set_before_rng
        # when no `dc =` pattern is found. Instead, we flag dc_reasoning_missing.
        mock_response = self._make_mock_response(
            "import random, json; roll = random.randint(1, 20); "
            'print(json.dumps({"rolls": [roll], "total": roll, "dc": 12}))',
            output='{"rolls": [10], "total": 10, "dc": 12}',
        )
        evidence = gemini_provider.extract_code_execution_evidence(mock_response)
        # dc_set_before_rng should NOT be set (no `dc =` found in code)
        self.assertIsNone(evidence.get("dc_set_before_rng"))
        self.assertIsNone(evidence.get("dc_set_before_next_rng"))
        # Instead, dc_reasoning_missing should be True (DC in output, no reasoning)
        self.assertTrue(evidence.get("dc_reasoning_missing"))

    def test_extract_evidence_dc_before_next_rng_true_with_prior_rng(self):
        """DC set after earlier RNG but before its own roll should pass per-roll check."""
        mock_response = self._make_mock_response(
            "import random, json; roll1 = random.randint(1, 20); "
            "dc = 12; roll2 = random.randint(1, 20); "
            'print(json.dumps({"rolls": [roll1, roll2], "dc": dc}))'
        )
        evidence = gemini_provider.extract_code_execution_evidence(mock_response)
        self.assertIs(evidence.get("dc_set_before_rng"), False)
        self.assertTrue(evidence.get("dc_set_before_next_rng"))

    def test_extract_evidence_dc_before_next_rng_false_when_dc_after_roll(self):
        """DC assigned after its roll with no subsequent RNG should fail per-roll check."""
        mock_response = self._make_mock_response(
            "import random, json; roll = random.randint(1, 20); dc = 12; "
            'print(json.dumps({"rolls": [roll], "dc": dc}))'
        )
        evidence = gemini_provider.extract_code_execution_evidence(mock_response)
        self.assertIs(evidence.get("dc_set_before_rng"), False)
        self.assertIs(evidence.get("dc_set_before_next_rng"), False)

    def test_extract_evidence_dc_before_next_rng_true_when_dc_before_first_rng(self):
        """DC assigned before the first RNG should pass per-roll check."""
        mock_response = self._make_mock_response(
            "import random, json; dc = 12; roll = random.randint(1, 20); "
            'print(json.dumps({"rolls": [roll], "dc": dc}))'
        )
        evidence = gemini_provider.extract_code_execution_evidence(mock_response)
        self.assertTrue(evidence.get("dc_set_before_rng"))
        self.assertTrue(evidence.get("dc_set_before_next_rng"))

    # === NEW SCHEMA-BASED DC VALIDATION TESTS ===

    def test_dc_reasoning_missing_when_dc_present_without_reasoning(self):
        """Should flag when output has DC but no dc_reasoning field."""
        mock_response = self._make_mock_response(
            "import random, json; dc = 15; roll = random.randint(1, 20); "
            'print(json.dumps({"rolls": [roll], "dc": dc, "success": roll >= dc}))',
            output='{"rolls": [12], "dc": 15, "success": false}',
        )
        evidence = gemini_provider.extract_code_execution_evidence(mock_response)
        self.assertTrue(
            evidence.get("dc_reasoning_missing"),
            "Should flag dc_reasoning_missing when DC present but reasoning absent",
        )

    def test_dc_reasoning_present_when_both_dc_and_reasoning_exist(self):
        """Should NOT flag when both DC and dc_reasoning are present."""
        mock_response = self._make_mock_response(
            "import random, json; dc = 15; roll = random.randint(1, 20); "
            'print(json.dumps({"rolls": [roll], "dc": dc, "dc_reasoning": "guard is alert", "success": roll >= dc}))',
            output='{"rolls": [12], "dc": 15, "dc_reasoning": "guard is alert", "success": false}',
        )
        evidence = gemini_provider.extract_code_execution_evidence(mock_response)
        self.assertFalse(
            evidence.get("dc_reasoning_missing", False),
            "Should NOT flag when dc_reasoning is present",
        )

    def test_no_dc_reasoning_flag_when_no_dc_in_output(self):
        """Should NOT flag dc_reasoning when there's no DC at all (e.g., attack vs AC)."""
        mock_response = self._make_mock_response(
            "import random, json; roll = random.randint(1, 20); ac = 15; "
            'print(json.dumps({"rolls": [roll], "ac": ac, "hit": roll >= ac}))',
            output='{"rolls": [18], "ac": 15, "hit": true}',
        )
        evidence = gemini_provider.extract_code_execution_evidence(mock_response)
        self.assertFalse(
            evidence.get("dc_reasoning_missing", False),
            "Should NOT flag when no DC is present (attack rolls use AC, not DC)",
        )

    def test_descriptive_dc_variable_names_not_flagged(self):
        """Using plan_dc, stealth_dc etc should NOT trigger false positives."""
        # This is the real-world case that was causing false positives
        mock_response = self._make_mock_response(
            "import random, json; plan_dc = 15; plan_roll = random.randint(1, 20); "
            'print(json.dumps({"dc": plan_dc, "dc_reasoning": "complex plan", "rolls": [plan_roll]}))',
            output='{"dc": 15, "dc_reasoning": "complex plan", "rolls": [12]}',
        )
        evidence = gemini_provider.extract_code_execution_evidence(mock_response)
        # Should NOT have dc_set_before_rng = False (the old false positive)
        # The dc_set_before_rng check should either be True or not present
        if "dc_set_before_rng" in evidence:
            self.assertIsNot(
                evidence.get("dc_set_before_rng"),
                False,
                "Descriptive DC variable names should NOT trigger ordering false positive",
            )
        # And should NOT flag dc_reasoning_missing since reasoning is present
        self.assertFalse(
            evidence.get("dc_reasoning_missing", False),
            "Should NOT flag when dc_reasoning is present",
        )


class TestCodeExecutionIntegrity(unittest.TestCase):
    """Test cases for code execution integrity and safety."""

    def test_extract_code_execution_evidence_finds_usage(self):
        """Should detect when code execution was used in response."""
        mock_response = Mock()
        mock_part = Mock()
        mock_part.executable_code = Mock(language="python", code="print('world')")
        mock_part.code_execution_result = Mock(outcome="OUTCOME_OK", output="world")
        mock_response.candidates = [Mock(content=Mock(parts=[mock_part]))]
        evidence = gemini_code_execution.extract_code_execution_evidence(mock_response)
        self.assertTrue(evidence["code_execution_used"])
        self.assertEqual(evidence["executable_code_parts"], 1)
        self.assertEqual(evidence["code_execution_result_parts"], 1)
        self.assertEqual(evidence["stdout"], "hello")

    def test_extract_code_execution_evidence_no_usage(self):
        """Should handle responses without code execution."""
        mock_response = Mock()
        mock_part = Mock()
        del mock_part.executable_code
        del mock_part.code_execution_result
        mock_part.text = "Just text"
        mock_response.candidates = [Mock(content=Mock(parts=[mock_part]))]
        evidence = gemini_code_execution.extract_code_execution_evidence(mock_response)
        self.assertFalse(evidence["code_execution_used"])
        self.assertEqual(evidence["executable_code_parts"], 0)
        self.assertEqual(evidence["code_execution_result_parts"], 0)

    def test_extract_code_execution_evidence_aggregates_stdout_parts(self):
        """Should preserve multiple stdout parts and flag JSON if any part is valid."""
        mock_response = Mock()
        mock_part1 = SimpleNamespace(
            executable_code=SimpleNamespace(language="python", code="print('world')"),
            code_execution_result=SimpleNamespace(
                outcome="OUTCOME_OK", output="not json"
            ),
        )
        mock_part2 = SimpleNamespace(
            executable_code=None,
            code_execution_result=SimpleNamespace(
                outcome="OUTCOME_OK", output='{"rolls": [4], "total": 9}'
            ),
        )
        mock_response.candidates = [Mock(content=Mock(parts=[mock_part1, mock_part2]))]

        evidence = gemini_code_execution.extract_code_execution_evidence(mock_response)

        self.assertEqual(
            evidence.get("stdout_parts"),
            ["not json", '{"rolls": [4], "total": 9}'],
        )
        self.assertEqual(
            evidence.get("stdout"),
            'not json\n{"rolls": [4], "total": 9}',
        )
        self.assertTrue(evidence.get("stdout_is_valid_json"))

    def test_extract_code_execution_parts_summary(self):
        """Should generate readable summary of code execution."""
        mock_response = Mock()
        mock_part1 = Mock()
        mock_part1.executable_code = Mock(language="python", code="x = 1")
        mock_part2 = Mock()
        mock_part2.code_execution_result = Mock(outcome="OUTCOME_OK", output="")
        mock_response.candidates = [Mock(content=Mock(parts=[mock_part1, mock_part2]))]
        summary = gemini_code_execution.extract_code_execution_parts_summary(
            mock_response
        )
        self.assertTrue(summary["code_execution_used"])
        self.assertEqual(summary["parts"], 2)
        self.assertEqual(len(summary["executable_code_samples"]), 1)
        self.assertEqual(len(summary["code_execution_result_samples"]), 1)


class TestToolRequestsFallbackNotFabrication(unittest.TestCase):
    """Tests for bead worktree_dice2-4f5: tool_requests fallback is NOT fabrication.

    When the model emits tool_requests for dice instead of using code_execution,
    the fallback at gemini_provider.py:1494-1515 executes them server-side with
    real RNG. This should NOT be flagged as fabrication.
    """

    # Dice tool results for fallback tests
    DICE_TOOL_RESULTS = [
        {
            "tool": "roll_attack",
            "result": {"roll": 13, "total": 18, "notation": "1d20+5", "formatted": "1d20+5 = 18"},
        }
    ]

    def test_fallback_tool_requests_executed_is_not_fabrication(self):
        """Dice executed via tool_requests fallback should NOT be flagged as fabrication."""
        structured = SimpleNamespace(
            action_resolution={
                "mechanics": {"rolls": [{"notation": "1d20+5", "total": 18}]}
            }
        )
        evidence = {
            "code_execution_used": False,
            "rng_verified": False,
            "executable_code_parts": 0,
            "code_execution_result_parts": 0,
        }
        result = _is_code_execution_fabrication(
            structured, evidence,
            tool_requests_executed=True,
            tool_results=self.DICE_TOOL_RESULTS,
        )
        self.assertFalse(
            result,
            "Fallback dice execution via tool_requests should NOT be fabrication",
        )

    def test_fallback_non_dice_tools_still_fabrication(self):
        """Fallback with only non-dice tools (e.g. faction) should still flag fabrication."""
        structured = SimpleNamespace(
            action_resolution={
                "mechanics": {"rolls": [{"notation": "1d20+5", "total": 18}]}
            }
        )
        evidence = {
            "code_execution_used": False,
            "rng_verified": False,
        }
        non_dice_results = [
            {"tool": "faction_action", "result": {"status": "ok"}},
        ]
        result = _is_code_execution_fabrication(
            structured, evidence,
            tool_requests_executed=True,
            tool_results=non_dice_results,
        )
        self.assertTrue(
            result,
            "Fallback with only non-dice tools should still flag fabrication",
        )

    def test_no_code_exec_no_fallback_is_fabrication(self):
        """Dice without code_execution AND without fallback IS fabrication."""
        structured = SimpleNamespace(
            action_resolution={
                "mechanics": {"rolls": [{"notation": "1d20+5", "total": 18}]}
            }
        )
        evidence = {
            "code_execution_used": False,
            "rng_verified": False,
            "executable_code_parts": 0,
            "code_execution_result_parts": 0,
        }
        result = _is_code_execution_fabrication(
            structured, evidence, tool_requests_executed=False
        )
        self.assertTrue(
            result,
            "Dice without code_execution or fallback IS fabrication",
        )

    def test_fallback_with_audit_events_is_not_fabrication(self):
        """Audit events from fallback tool_requests should NOT be fabrication."""
        structured = SimpleNamespace(
            action_resolution={
                "mechanics": {
                    "audit_events": [
                        {"purpose": "Attack", "rolls": [15], "total": 20}
                    ]
                }
            }
        )
        evidence = {
            "code_execution_used": False,
            "rng_verified": False,
        }
        result = _is_code_execution_fabrication(
            structured, evidence,
            tool_requests_executed=True,
            tool_results=self.DICE_TOOL_RESULTS,
        )
        self.assertFalse(
            result,
            "Audit events from fallback should NOT be fabrication",
        )

    def test_backward_compat_no_kwarg_defaults_to_fabrication(self):
        """Existing callers without tool_requests_executed should still detect fabrication."""
        structured = SimpleNamespace(
            action_resolution={
                "mechanics": {"rolls": [{"notation": "1d20", "total": 12}]}
            }
        )
        evidence = {
            "code_execution_used": False,
            "rng_verified": False,
        }
        # Call WITHOUT tool_requests_executed kwarg (backward compat)
        result = _is_code_execution_fabrication(structured, evidence)
        self.assertTrue(
            result,
            "Default (no tool_requests_executed) should still flag fabrication",
        )


if __name__ == "__main__":
    unittest.main()
