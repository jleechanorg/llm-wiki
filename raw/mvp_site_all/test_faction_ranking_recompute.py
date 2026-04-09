"""Tests for faction ranking recompute logic in gemini_provider.

Validates that ranking is correctly recomputed when:
1. LLM emits ranking without power tool (ranking dropped, auto-attached after power)
2. LLM emits ranking with stale FP (mismatch detected, ranking recomputed)
3. Phase 2 response includes tool_requests mirroring server-executed args/results

These tests cover the HIGH priority fix for FP/ranking divergence.
"""

from __future__ import annotations

# ruff: noqa: PT009
import json
import os
import unittest
from unittest.mock import MagicMock, patch

from mvp_site import faction_state_util, llm_service
from mvp_site.llm_providers import (
    cerebras_provider,
    gemini_provider,
    openrouter_provider,
)

# Set testing environment
os.environ["TESTING_AUTH_BYPASS"] = "true"
os.environ.setdefault("GEMINI_API_KEY", "test")


def _orchestrate_code_execution(
    *,
    prompt_contents: list[str],
    response_1: MagicMock,
    model_name: str = "gemini-2.0-flash",
    system_instruction_text: str = "sys",
) -> MagicMock:
    return llm_service._orchestrate_gemini_code_execution_tool_requests(
        prompt_contents=prompt_contents,
        response_1=response_1,
        model_name=model_name,
        system_instruction_text=system_instruction_text,
        temperature=0.0,
        safety_settings=[],
        json_mode_max_output_tokens=4096,
    )


class TestFactionRankingRecompute(unittest.TestCase):
    """Test ranking recompute logic for FP/ranking consistency."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.provider = gemini_provider

    def _create_mock_response(self, text: str) -> MagicMock:
        """Create a mock Gemini response with given text."""
        mock_response = MagicMock()
        mock_response.text = text
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].content = MagicMock()
        mock_response.candidates[0].content.parts = []
        return mock_response

    def test_ranking_without_power_is_dropped_and_recomputed(self):
        """Ranking tool without power should be dropped and auto-attached with correct FP.

        Scenario: LLM emits faction_calculate_ranking but NOT faction_calculate_power.
        Expected:
        1. Ranking tool request is DROPPED (not executed with placeholder FP)
        2. Power is auto-invoked from state_updates data
        3. Ranking is auto-attached using the FP from auto-invoked power
        """
        # Phase 1 response with ranking tool but NO power tool
        phase1_json = """{
            "narrative": "Faction enabled!",
            "state_updates": {
                "custom_campaign_state": {
                    "faction_minigame": {
                        "enabled": true,
                        "units": {"soldiers": 15000, "spies": 10, "elites": 2, "elite_avg_level": 6},
                        "resources": {"territory": 500},
                        "buildings": {"fortifications": 3}
                    }
                }
            },
            "tool_requests": [
                {"tool": "faction_calculate_ranking", "args": {"player_faction_power": 0, "turn_number": 1}}
            ]
        }"""

        phase2_json = '{"narrative": "Your faction rises!"}'

        mock_phase1 = self._create_mock_response(phase1_json)
        mock_phase2 = self._create_mock_response(phase2_json)

        tool_call_log: list[tuple[str, dict]] = []

        def mock_execute_tool(tool_name: str, args: dict) -> dict:
            tool_call_log.append((tool_name, dict(args)))
            if tool_name == "faction_calculate_power":
                # Auto-invoked power calculation
                return {"faction_power": 20500, "army_power": 15000}
            if tool_name == "faction_calculate_ranking":
                fp = args.get("player_faction_power", 0)
                # Return ranking based on FP - this verifies the FP value used
                if fp >= 20000:
                    return {"ranking": 150, "total_factions": 201}
                return {"ranking": 201, "total_factions": 201}  # Wrong ranking if FP=0
            return {}

        with (
            patch.object(
                self.provider, "generate_json_mode_content", return_value=mock_phase2
            ),
            patch(
                "mvp_site.llm_providers.provider_utils.execute_faction_tool",
                side_effect=mock_execute_tool,
            ),
            patch.object(
                faction_state_util, "is_faction_enable_action", return_value=True
            ),
        ):
            result = _orchestrate_code_execution(
                prompt_contents=['{"game_state": {}}'],
                response_1=mock_phase1,
            )

            assert result is not None

            # KEY ASSERTION: Verify the original ranking with FP=0 was NOT executed
            # Instead, ranking should only be called with the correct FP (20500)
            ranking_calls = [
                (name, args)
                for name, args in tool_call_log
                if name == "faction_calculate_ranking"
            ]

            # There should be ranking call(s)
            assert len(ranking_calls) >= 1, (
                f"Expected ranking calls, got: {tool_call_log}"
            )

            # The ranking call should use FP=20500 (from auto-invoked power), NOT FP=0
            # If the guard works, the original ranking with FP=0 should have been dropped
            for _name, args in ranking_calls:
                fp_used = args.get("player_faction_power", 0)
                assert fp_used == 20500, (
                    f"Ranking was called with FP={fp_used}, expected 20500. "
                    f"The ranking-without-power guard should have dropped the original FP=0 call."
                )

            # Verify power was auto-invoked
            power_calls = [
                name for name, _ in tool_call_log if name == "faction_calculate_power"
            ]
            assert len(power_calls) >= 1, "Power should have been auto-invoked"

    def test_ranking_with_stale_fp_is_recomputed(self):
        """Ranking with stale FP should be detected and recomputed.

        Scenario: LLM emits both power and ranking tools, but ranking uses stale FP (0)
        while power returns FP=33000.
        Expected: Ranking is recomputed with the correct FP from power tool.
        """
        # Phase 1 response with BOTH tools but ranking has stale FP
        phase1_json = """{
            "narrative": "Faction enabled!",
            "state_updates": {
                "custom_campaign_state": {
                    "faction_minigame": {
                        "enabled": true,
                        "units": {"soldiers": 15000, "spies": 10, "elites": 2, "elite_avg_level": 6},
                        "resources": {"territory": 3000},
                        "buildings": {"fortifications": 3}
                    }
                }
            },
            "tool_requests": [
                {"tool": "faction_calculate_power", "args": {"soldiers": 15000, "territory": 3000, "fortifications": 3}},
                {"tool": "faction_calculate_ranking", "args": {"player_faction_power": 0, "turn_number": 1}}
            ]
        }"""

        phase2_json = '{"narrative": "Your faction rises!"}'

        mock_phase1 = self._create_mock_response(phase1_json)
        mock_phase2 = self._create_mock_response(phase2_json)

        tool_call_log: list[tuple[str, dict]] = []

        def mock_execute_tool(tool_name: str, args: dict) -> dict:
            tool_call_log.append((tool_name, dict(args)))
            if tool_name == "faction_calculate_power":
                # Power returns FP=33000
                return {"faction_power": 33000, "army_power": 15000}
            if tool_name == "faction_calculate_ranking":
                fp = args.get("player_faction_power", 0)
                # Return ranking based on actual FP passed
                if fp >= 30000:
                    return {"ranking": 165, "total_factions": 201}
                return {
                    "ranking": 201,
                    "total_factions": 201,
                }  # Weak ranking if FP is 0
            return {}

        with (
            patch.object(
                self.provider, "generate_json_mode_content", return_value=mock_phase2
            ),
            patch(
                "mvp_site.llm_providers.provider_utils.execute_faction_tool",
                side_effect=mock_execute_tool,
            ),
            patch.object(
                faction_state_util, "is_faction_enable_action", return_value=True
            ),
        ):
            result = _orchestrate_code_execution(
                prompt_contents=['{"game_state": {}}'],
                response_1=mock_phase1,
            )

            assert result is not None

            # Verify ranking was called with corrected FP (33000), not stale FP (0)
            ranking_calls = [
                (name, args)
                for name, args in tool_call_log
                if name == "faction_calculate_ranking"
            ]

            # Should have at least one ranking call with correct FP
            # The final ranking call should use FP=33000 (from power result)
            assert len(ranking_calls) >= 1, (
                f"Expected ranking calls, got: {tool_call_log}"
            )

            # Check that the LAST ranking call used the correct FP
            last_ranking_call = ranking_calls[-1]
            last_fp = last_ranking_call[1].get("player_faction_power")
            assert last_fp == 33000, f"Expected ranking with FP=33000, got FP={last_fp}"

    def test_power_error_does_not_mask_later_power_result(self):
        """Error power tool results should not block later valid power results.

        Scenario: LLM emits two power tool calls (first errors, second succeeds).
        Expected: Ranking recompute uses the valid power result, not fallback FP.
        """
        phase1_json = """{
            "narrative": "Faction enabled!",
            "state_updates": {
                "custom_campaign_state": {
                    "faction_minigame": {
                        "enabled": true,
                        "faction_power": 12345
                    }
                }
            },
            "tool_requests": [
                {"tool": "faction_calculate_power", "args": {"soldiers": 0, "territory": 0, "fortifications": 0}},
                {"tool": "faction_calculate_power", "args": {"soldiers": 45000, "territory": 0, "fortifications": 0}},
                {"tool": "faction_calculate_ranking", "args": {"player_faction_power": 0, "turn_number": 1}}
            ]
        }"""

        phase2_json = '{"narrative": "Your faction rises!"}'

        mock_phase1 = self._create_mock_response(phase1_json)
        mock_phase2 = self._create_mock_response(phase2_json)

        tool_call_log: list[tuple[str, dict]] = []
        power_call_count = {"count": 0}

        def mock_execute_tool(tool_name: str, args: dict) -> dict:
            tool_call_log.append((tool_name, dict(args)))
            if tool_name == "faction_calculate_power":
                power_call_count["count"] += 1
                if power_call_count["count"] == 1:
                    return {"error": "boom"}
                return {"faction_power": 45000, "army_power": 45000}
            if tool_name == "faction_calculate_ranking":
                fp = args.get("player_faction_power", 0)
                return {"ranking": 100 if fp >= 45000 else 201, "total_factions": 201}
            return {}

        with (
            patch.object(
                self.provider, "generate_json_mode_content", return_value=mock_phase2
            ),
            patch(
                "mvp_site.llm_providers.provider_utils.execute_faction_tool",
                side_effect=mock_execute_tool,
            ),
            patch.object(
                faction_state_util, "is_faction_enable_action", return_value=True
            ),
        ):
            result = _orchestrate_code_execution(
                prompt_contents=['{"game_state": {}}'],
                response_1=mock_phase1,
            )

            assert result is not None

            ranking_calls = [
                (name, args)
                for name, args in tool_call_log
                if name == "faction_calculate_ranking"
            ]
            assert ranking_calls, f"Expected ranking calls, got: {tool_call_log}"
            last_fp = ranking_calls[-1][1].get("player_faction_power")
            assert last_fp == 45000, f"Expected ranking with FP=45000, got FP={last_fp}"

    def test_explicit_fp_without_unit_data_skips_auto_invoke(self):
        """When LLM provides explicit FP but no unit data, auto-invoke should be skipped.

        Scenario: LLM sets faction_power=50000 in state_updates but provides no
        units/resources/buildings data (required fields missing).
        Expected: Auto-invoke is skipped because _has_required_faction_init_data returns False.
        """
        # Phase 1 response with explicit FP but no unit data
        phase1_json = """{
            "narrative": "Faction enabled!",
            "state_updates": {
                "custom_campaign_state": {
                    "faction_minigame": {
                        "enabled": true,
                        "faction_power": 50000,
                        "ranking": 100
                    }
                }
            }
        }"""

        phase2_json = '{"narrative": "Your faction rises!"}'

        mock_phase1 = self._create_mock_response(phase1_json)
        mock_phase2 = self._create_mock_response(phase2_json)

        tool_call_log: list[tuple[str, dict]] = []

        def mock_execute_tool(tool_name: str, args: dict) -> dict:
            tool_call_log.append((tool_name, dict(args)))
            if tool_name == "faction_calculate_power":
                # This should NOT be called when required init data is missing
                return {"faction_power": 0, "army_power": 0}
            if tool_name == "faction_calculate_ranking":
                fp = args.get("player_faction_power", 0)
                if fp >= 50000:
                    return {"ranking": 100, "total_factions": 201}
                return {"ranking": 201, "total_factions": 201}
            return {}

        with (
            patch.object(
                self.provider,
                "generate_json_mode_content",
                side_effect=[mock_phase1, mock_phase2],
            ),
            patch(
                "mvp_site.llm_providers.provider_utils.execute_faction_tool",
                side_effect=mock_execute_tool,
            ),
            patch.object(
                faction_state_util, "is_faction_enable_action", return_value=True
            ),
        ):
            result = _orchestrate_code_execution(
                prompt_contents=['{"game_state": {}}'],
                response_1=mock_phase1,
            )

            assert result is not None

            # The key assertion: power tool should NOT be called when required init data is missing
            # The _has_required_faction_init_data function should prevent auto-invoke
            power_calls = [
                name for name, _ in tool_call_log if name == "faction_calculate_power"
            ]

            # With the fix, power should NOT be auto-invoked when unit data is missing
            # (because _has_required_faction_init_data returns False)
            assert len(power_calls) == 0, (
                f"Power tool should NOT be called when required init data is missing. "
                f"Got {len(power_calls)} power calls: {tool_call_log}"
            )

    def test_phase2_response_has_tool_results_attached(self):
        """Phase 2 response should have _tool_results attached for downstream processing.

        This verifies that server-executed tool results are properly attached to the
        response object, which is used by dice_integrity.py and debug_info.
        """
        phase1_json = """{
            "narrative": "Faction enabled!",
            "state_updates": {
                "custom_campaign_state": {
                    "faction_minigame": {
                        "enabled": true,
                        "units": {"soldiers": 10000, "spies": 5, "elites": 1, "elite_avg_level": 6},
                        "resources": {"territory": 200},
                        "buildings": {"fortifications": 1}
                    }
                }
            },
            "tool_requests": [
                {"tool": "faction_calculate_power", "args": {"soldiers": 10000, "territory": 200, "fortifications": 1}}
            ]
        }"""

        phase2_json = '{"narrative": "Your faction rises!"}'

        mock_phase1 = self._create_mock_response(phase1_json)
        mock_phase2 = self._create_mock_response(phase2_json)

        def mock_execute_tool(tool_name: str, args: dict) -> dict:
            if tool_name == "faction_calculate_power":
                return {"faction_power": 12000, "army_power": 10000}
            if tool_name == "faction_calculate_ranking":
                return {"ranking": 180, "total_factions": 201}
            return {}

        with (
            patch.object(
                self.provider, "generate_json_mode_content", return_value=mock_phase2
            ),
            patch(
                "mvp_site.llm_providers.provider_utils.execute_faction_tool",
                side_effect=mock_execute_tool,
            ),
            patch.object(
                faction_state_util, "is_faction_enable_action", return_value=True
            ),
        ):
            result = _orchestrate_code_execution(
                prompt_contents=['{"game_state": {}}'],
                response_1=mock_phase1,
            )

            assert result is not None

            # KEY ASSERTION: Response should have _tool_results attached
            assert hasattr(result, "_tool_results"), (
                "Response should have _tool_results attribute"
            )
            assert result._tool_results is not None, "_tool_results should not be None"
            assert len(result._tool_results) >= 1, (
                "_tool_results should have at least one entry"
            )

            # Verify tool_results contain the expected tools
            tool_names = [
                tr.get("tool") for tr in result._tool_results if isinstance(tr, dict)
            ]
            assert "faction_calculate_power" in tool_names, (
                "Power tool should be in results"
            )
            assert "faction_calculate_ranking" in tool_names, (
                "Ranking tool should be auto-attached"
            )

            # Verify the ranking result uses the correct FP (12000 from power)
            for tr in result._tool_results:
                if (
                    isinstance(tr, dict)
                    and tr.get("tool") == "faction_calculate_ranking"
                ):
                    ranking_args = tr.get("args", {})
                    ranking_fp = ranking_args.get("player_faction_power")
                    assert ranking_fp == 12000, (
                        f"Ranking should use FP=12000 from power result, got {ranking_fp}"
                    )

            # Verify _tool_requests_executed flag is set
            assert hasattr(result, "_tool_requests_executed"), (
                "Should have _tool_requests_executed"
            )
            assert result._tool_requests_executed is True, (
                "_tool_requests_executed should be True"
            )

    def test_malformed_faction_data_handles_attributeerror(self):
        """Malformed LLM response with non-dict units/resources should not crash.

        Scenario: LLM returns units as a string instead of dict (malformed JSON).
        Expected: Exception is caught gracefully, no AttributeError raised.
        """
        # Phase 1 JSON with malformed faction data (units is string, not dict)
        phase1_json = """{
            "narrative": "Faction enabled!",
            "state_updates": {
                "custom_campaign_state": {
                    "faction_minigame": {
                        "enabled": true,
                        "units": "invalid_string_not_dict",
                        "resources": null,
                        "buildings": 12345
                    }
                }
            }
        }"""

        phase2_json = '{"narrative": "Your faction rises!"}'

        def mock_generate(*args, **kwargs):
            return self._create_mock_response(phase1_json)

        def mock_generate_phase2(*args, **kwargs):
            return self._create_mock_response(phase2_json)

        call_count = [0]

        def side_effect_generate(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return mock_generate(*args, **kwargs)
            return mock_generate_phase2(*args, **kwargs)

        with (
            patch.object(
                self.provider,
                "generate_json_mode_content",
                side_effect=side_effect_generate,
            ),
            patch.object(
                faction_state_util, "is_faction_enable_action", return_value=True
            ),
        ):
            # This should NOT raise AttributeError
            try:
                result = _orchestrate_code_execution(
                    prompt_contents=['{"game_state": {}}'],
                    response_1=self._create_mock_response(phase1_json),
                )
                # If we get here without exception, test passes
                assert result is not None
            except AttributeError as e:
                self.fail(f"AttributeError should be caught: {e}")


class TestBuildExpectedFactionToolRequests(unittest.TestCase):
    """Tests for build_expected_faction_tool_requests helper function.

    Validates that the function correctly handles edge cases and returns
    empty array when FP cannot be determined (null FP propagation bug fix).
    """

    def test_returns_empty_when_power_result_has_error(self):
        """Should return empty array when power tool result contains an error.

        Regression test: Prevents null FP propagation when power tool errors.
        """
        tool_results = [
            {
                "tool": "faction_calculate_power",
                "args": {"soldiers": 100},
                "result": {"error": "Missing required field: territory"},
            }
        ]

        result = faction_state_util.build_expected_faction_tool_requests(
            tool_results, turn_number=1
        )

        # Should return empty array, NOT an array with player_faction_power=None
        self.assertEqual(result, [])

    def test_returns_empty_when_power_result_missing_faction_power(self):
        """Should return empty array when power result lacks faction_power field.

        Regression test: Prevents null FP propagation when faction_power is missing.
        """
        tool_results = [
            {
                "tool": "faction_calculate_power",
                "args": {"soldiers": 100},
                "result": {"army_power": 100},  # Missing faction_power
            }
        ]

        result = faction_state_util.build_expected_faction_tool_requests(
            tool_results, turn_number=1
        )

        # Should return empty array, NOT an array with player_faction_power=None
        self.assertEqual(result, [])

    def test_returns_tool_requests_when_valid_fp(self):
        """Should return proper tool_requests array when FP is valid."""
        tool_results = [
            {
                "tool": "faction_calculate_power",
                "args": {"soldiers": 1000, "territory": 200},
                "result": {"faction_power": 2000, "army_power": 1000},
            }
        ]

        result = faction_state_util.build_expected_faction_tool_requests(
            tool_results, turn_number=1
        )

        # Should return both tool requests with valid FP
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["tool"], "faction_calculate_power")
        self.assertEqual(result[1]["tool"], "faction_calculate_ranking")
        self.assertEqual(result[1]["args"]["player_faction_power"], 2000)
        self.assertEqual(result[1]["args"]["turn_number"], 1)


class TestProviderBoundary(unittest.TestCase):
    """Provider boundary tests for faction orchestration helpers."""

    def test_gemini_provider_does_not_define_build_expected_helper(self):
        """Gemini provider should not own faction tool_request synthesis helper."""
        self.assertFalse(
            hasattr(gemini_provider, "_build_expected_faction_tool_requests")
        )

    def test_openrouter_provider_has_no_faction_tool_gating_logic(self):
        """OpenRouter provider should not implement faction gating/business logic."""
        self.assertFalse(hasattr(openrouter_provider, "FACTION_TOOLS"))
        self.assertFalse(
            hasattr(
                openrouter_provider,
                "extract_faction_minigame_state_from_prompt_contents",
            )
        )

    def test_cerebras_provider_has_no_faction_tool_gating_logic(self):
        """Cerebras provider should not implement faction gating/business logic."""
        self.assertFalse(hasattr(cerebras_provider, "FACTION_TOOLS"))
        self.assertFalse(
            hasattr(
                cerebras_provider, "extract_faction_minigame_state_from_prompt_contents"
            )
        )


class TestIsFactionEnableAction(unittest.TestCase):
    """Tests for is_faction_enable_action helper function (faction_state_util).

    Validates that the function correctly handles both string and dict formats
    and that pattern lists are consistent with agent routing.
    """

    def test_handles_dict_format_prompt_contents(self):
        """Should handle dict format for prompt_contents[0].

        Regression test: worktree_faction-di0
        Bug: Function returns False for dict format, but other code paths handle it.
        """
        # Dict format with user_action
        prompt_contents = [{"user_action": "enable_faction_minigame", "game_state": {}}]

        result = faction_state_util.is_faction_enable_action(prompt_contents)

        # Should return True for dict format containing enable action
        self.assertTrue(result)

    def test_handles_dict_format_with_non_enable_action(self):
        """Should return False for dict format with non-enable action."""
        prompt_contents = [{"user_action": "check faction status", "game_state": {}}]

        result = faction_state_util.is_faction_enable_action(prompt_contents)

        self.assertFalse(result)

    def test_non_command_phrases_return_false(self):
        """Free-form phrases should not be treated as enable commands."""
        prompt_contents = [json.dumps({"user_action": "enable faction mode"})]

        result = faction_state_util.is_faction_enable_action(prompt_contents)

        self.assertFalse(result)

        prompt_contents = [json.dumps({"user_action": "faction minigame"})]

        result = faction_state_util.is_faction_enable_action(prompt_contents)

        self.assertFalse(result)

    def test_accepts_enforcement_suffix_for_enable_action(self):
        """Enable action should still match when system enforcement suffix is appended."""
        prompt_contents = [
            json.dumps(
                {
                    "user_action": (
                        "enable_faction_minigame\n\n"
                        "[SYSTEM ENFORCEMENT: For ANY dice roll, you MUST use the "
                        "code_execution tool with random.randint(). Your code will be inspected.]"
                    )
                }
            )
        ]

        result = faction_state_util.is_faction_enable_action(prompt_contents)

        self.assertTrue(result)


class TestRankingErrorHandling(unittest.TestCase):
    """Tests for ranking tool error handling in code execution flow.

    Validates that ranking is properly dropped when power tool returns an error.
    """

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.provider = gemini_provider

    def _create_mock_response(self, text: str) -> MagicMock:
        """Create a mock Gemini response with given text."""
        mock_response = MagicMock()
        mock_response.text = text
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].content = MagicMock()
        mock_response.candidates[0].content.parts = []
        return mock_response

    def test_ranking_dropped_when_power_has_error(self):
        """Ranking tool should be dropped when power tool returns error.

        Regression test: worktree_faction-lxe
        Bug: Guard at line 1266 only checks `if power_result is None` but doesn't
        check for error in power_result. If power returns {"error": "..."},
        power_result is not None, so ranking proceeds with stale FP.
        """
        # Phase 1 response with both tools, but power will return error
        phase1_json = """{
            "narrative": "Faction enabled!",
            "state_updates": {
                "custom_campaign_state": {
                    "faction_minigame": {"enabled": true}
                }
            },
            "tool_requests": [
                {"tool": "faction_calculate_power", "args": {"soldiers": 100}},
                {"tool": "faction_calculate_ranking", "args": {"player_faction_power": 999, "turn_number": 1}}
            ]
        }"""

        phase2_json = '{"narrative": "Your faction rises!"}'

        mock_phase1 = self._create_mock_response(phase1_json)
        mock_phase2 = self._create_mock_response(phase2_json)

        tool_call_log: list[tuple[str, dict]] = []

        def mock_execute_tool(tool_name: str, args: dict) -> dict:
            tool_call_log.append((tool_name, dict(args)))
            if tool_name == "faction_calculate_power":
                # Power tool returns ERROR
                return {"error": "Missing required field: territory"}
            if tool_name == "faction_calculate_ranking":
                # If ranking is called with stale FP=999, that's the bug
                return {"ranking": 50, "total_factions": 201}
            return {}

        with (
            patch.object(
                self.provider, "generate_json_mode_content", return_value=mock_phase2
            ),
            patch(
                "mvp_site.llm_providers.provider_utils.execute_faction_tool",
                side_effect=mock_execute_tool,
            ),
            patch.object(
                faction_state_util, "is_faction_enable_action", return_value=True
            ),
        ):
            result = _orchestrate_code_execution(
                prompt_contents=['{"game_state": {}}'],
                response_1=mock_phase1,
            )

            assert result is not None

            # KEY ASSERTION: Ranking should NOT be executed with stale FP=999
            # when power tool returned an error
            ranking_calls = [
                (name, args)
                for name, args in tool_call_log
                if name == "faction_calculate_ranking"
            ]

            # Ranking should either:
            # 1. Not be called at all (dropped due to power error), OR
            # 2. Be called later with correct FP from auto-invoke (not stale 999)
            for _name, args in ranking_calls:
                fp_used = args.get("player_faction_power", 0)
                self.assertNotEqual(
                    fp_used,
                    999,
                    f"Ranking was called with stale FP={fp_used}. "
                    f"Should have been dropped because power tool returned error.",
                )


if __name__ == "__main__":
    unittest.main()
