"""
Unit tests for LLM provider tool request handling.

These tests validate the tool request flow for Cerebras and OpenRouter providers
using mocks.
"""

# ruff: noqa: PT009,N802,SIM117

import inspect
import json
import os
import unittest
from unittest.mock import Mock, patch

import requests

from mvp_site import constants, llm_service
from mvp_site.agent_prompts import load_dice_instructions
from mvp_site.dice_strategy import DICE_STRATEGY_CODE_EXECUTION
from mvp_site.llm_providers import (
    cerebras_provider,
    gemini_provider,
    openrouter_provider,
)
from mvp_site.llm_providers.cerebras_provider import (
    CerebrasResponse,
    execute_tool_requests,
)
from mvp_site.llm_providers.openrouter_provider import OpenRouterResponse
from mvp_site.tests.fake_llm import FakeLLMResponse

os.environ["TESTING_AUTH_BYPASS"] = "true"


class TestCerebrasToolUseIntegration(unittest.TestCase):
    """Test Cerebras provider tool use for dice rolling (two-stage inference)."""

    def test_cerebras_provider_accepts_tools_parameter(self):
        """Verify Cerebras provider can accept tools parameter."""
        sig = inspect.signature(cerebras_provider.generate_content)
        param_names = list(sig.parameters.keys())
        self.assertIn(
            "tools",
            param_names,
            "FAIL: cerebras_provider.generate_content should accept 'tools' parameter",
        )

    def test_cerebras_response_handles_tool_calls(self):
        """Verify CerebrasResponse can extract tool_calls from response."""
        mock_response = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": "call_123",
                                "type": "function",
                                "function": {
                                    "name": "roll_dice",
                                    "arguments": '{"notation": "1d20+5"}',
                                },
                            }
                        ],
                    },
                    "finish_reason": "tool_calls",
                }
            ]
        }
        response = CerebrasResponse("", mock_response)
        self.assertTrue(
            hasattr(response, "tool_calls") or hasattr(response, "get_tool_calls"),
            "FAIL: CerebrasResponse should expose tool_calls",
        )


class TestLLMServiceToolIntegration(unittest.TestCase):
    """Test llm_service integration with tool use providers."""

    def test_call_llm_api_routes_to_tool_requests_for_cerebras(self):
        """Verify _call_llm_api routes to JSON-first tool_requests flow for Cerebras."""
        with patch(
            "mvp_site.llm_providers.cerebras_provider.generate_content_with_tool_requests"
        ) as mock_tool_requests:
            mock_tool_requests.return_value = Mock(
                text='{"narrative": "test", "entities_mentioned": [], "dice_rolls": []}'
            )
            with patch.dict(os.environ, {"MOCK_SERVICES_MODE": "false"}):
                llm_service._call_llm_api(
                    ["test prompt"],
                    "qwen-3-235b-a22b-instruct-2507",
                    "test logging",
                    provider_name=constants.LLM_PROVIDER_CEREBRAS,
                )
            self.assertTrue(
                mock_tool_requests.called,
                "generate_content_with_tool_requests should be called for Cerebras",
            )

    def test_call_llm_api_routes_to_tool_requests_for_openrouter(self):
        """Verify _call_llm_api routes to JSON-first tool_requests flow for OpenRouter."""
        with patch(
            "mvp_site.llm_providers.openrouter_provider.generate_content_with_tool_requests"
        ) as mock_tool_requests:
            mock_tool_requests.return_value = Mock(
                text='{"narrative": "test", "entities_mentioned": [], "dice_rolls": []}'
            )
            with patch.dict(os.environ, {"MOCK_SERVICES_MODE": "false"}):
                llm_service._call_llm_api(
                    ["test prompt"],
                    "meta-llama/llama-3.1-70b-instruct",
                    "test logging",
                    provider_name=constants.LLM_PROVIDER_OPENROUTER,
                )
            self.assertTrue(
                mock_tool_requests.called,
                "generate_content_with_tool_requests should be called for OpenRouter",
            )

    def test_call_llm_api_uses_tool_requests_for_all_cerebras_models(self):
        """Verify _call_llm_api uses JSON-first tool_requests for ALL Cerebras models."""
        with patch(
            "mvp_site.llm_providers.cerebras_provider.generate_content_with_tool_requests"
        ) as mock_tool_requests:
            mock_tool_requests.return_value = Mock(
                text='{"narrative": "test", "entities_mentioned": [], "dice_rolls": []}'
            )
            with patch.dict(os.environ, {"MOCK_SERVICES_MODE": "false"}):
                llm_service._call_llm_api(
                    ["test prompt"],
                    "llama-3.3-70b",
                    "test logging",
                    provider_name=constants.LLM_PROVIDER_CEREBRAS,
                )
            self.assertTrue(
                mock_tool_requests.called,
                "generate_content_with_tool_requests should be called for all Cerebras models",
            )

    def test_call_llm_api_owns_gemini_code_execution_orchestration(self):
        """Verify llm_service orchestrates Gemini code_execution tool requests."""
        prompt_contents = [
            json.dumps(
                {
                    "game_state": {
                        "custom_campaign_state": {
                            "faction_minigame": {"enabled": True, "turn_number": 5}
                        }
                    }
                }
            )
        ]
        phase1_response = FakeLLMResponse(
            json.dumps(
                {
                    "tool_requests": [
                        {
                            "tool": "faction_calculate_power",
                            "args": {"soldiers": 10, "spies": 0, "elites": 0},
                        }
                    ]
                }
            )
        )
        phase2_response = FakeLLMResponse('{"narrative":"ok"}')

        with (
            patch(
                "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution",
                return_value=phase1_response,
            ) as mock_phase1,
            patch(
                "mvp_site.dice_strategy.get_dice_roll_strategy",
                return_value=DICE_STRATEGY_CODE_EXECUTION,
            ),
            patch(
                "mvp_site.llm_service.execute_gemini_code_execution_tool_orchestration",
                return_value=[
                    {
                        "tool": "faction_calculate_power",
                        "args": {"soldiers": 10, "spies": 0, "elites": 0},
                        "result": {"faction_power": 10},
                    }
                ],
            ),
            patch(
                "mvp_site.llm_providers.gemini_provider.generate_json_mode_content",
                return_value=phase2_response,
            ) as mock_phase2,
        ):
            with patch.dict(os.environ, {"MOCK_SERVICES_MODE": "false"}):
                response = llm_service._call_llm_api(
                    prompt_contents=prompt_contents,
                    model_name="gemini-3-flash-preview",
                    current_prompt_text_for_logging="faction test",
                    provider_name=constants.LLM_PROVIDER_GEMINI,
                )

        self.assertIs(response, phase2_response)
        self.assertTrue(mock_phase1.called)
        self.assertTrue(mock_phase2.called)
        self.assertTrue(getattr(response, "_tool_requests_executed", False))
        self.assertEqual(len(getattr(response, "_tool_results", [])), 1)

    def test_code_execution_phase2_reapplies_code_execution_instruction(self):
        """Phase 2 in llm_service orchestration should use code_execution override."""
        phase1_response = FakeLLMResponse(
            '{"tool_requests":[{"tool":"faction_calculate_power","args":{"soldiers":10}}]}'
        )
        phase2_response = FakeLLMResponse('{"narrative":"ok"}')

        with (
            patch(
                "mvp_site.llm_service.execute_gemini_code_execution_tool_orchestration",
                return_value=[
                    {
                        "tool": "faction_calculate_power",
                        "args": {"soldiers": 10},
                        "result": {"faction_power": 10},
                    }
                ],
            ),
            patch(
                "mvp_site.llm_providers.gemini_provider.generate_json_mode_content",
                return_value=phase2_response,
            ) as mock_phase2,
        ):
            llm_service._orchestrate_gemini_code_execution_tool_requests(
                prompt_contents=[
                    json.dumps(
                        {
                            "user_action": "enable_faction_minigame",
                            "game_state": {
                                "custom_campaign_state": {
                                    "faction_minigame": {
                                        "enabled": True,
                                        "turn_number": 1,
                                    }
                                }
                            },
                        }
                    )
                ],
                response_1=phase1_response,
                model_name="gemini-3-flash-preview",
                system_instruction_text="base system instruction",
                temperature=0.0,
                safety_settings=[],
                json_mode_max_output_tokens=2048,
            )

        phase2_system_instruction = mock_phase2.call_args.kwargs.get(
            "system_instruction_text"
        )
        self.assertIsInstance(phase2_system_instruction, str)
        self.assertIn("DICE VALUES ARE UNKNOWABLE", phase2_system_instruction)

    def test_code_execution_phase2_retries_on_retriable_error(self):
        """Phase 2 should retry retriable Gemini errors during orchestration."""

        class RetriableGeminiError(Exception):
            def __init__(self, message: str):
                super().__init__(message)
                self.status = "FAILED_PRECONDITION"

        phase1_response = FakeLLMResponse(
            '{"tool_requests":[{"tool":"faction_calculate_power","args":{"soldiers":10}}]}'
        )
        phase2_response = FakeLLMResponse('{"narrative":"ok"}')

        with (
            patch(
                "mvp_site.llm_service.execute_gemini_code_execution_tool_orchestration",
                return_value=[
                    {
                        "tool": "faction_calculate_power",
                        "args": {"soldiers": 10},
                        "result": {"faction_power": 10},
                    }
                ],
            ),
            patch(
                "mvp_site.llm_service.time.sleep"
            ) as mock_sleep,
            patch(
                "mvp_site.llm_providers.gemini_provider.generate_json_mode_content",
                side_effect=[
                    RetriableGeminiError("temporary phase2 failure"),
                    phase2_response,
                ],
            ) as mock_phase2,
        ):
            response = llm_service._orchestrate_gemini_code_execution_tool_requests(
                prompt_contents=[
                    json.dumps(
                        {
                            "game_state": {
                                "custom_campaign_state": {
                                    "faction_minigame": {
                                        "enabled": True,
                                        "turn_number": 1,
                                    }
                                }
                            },
                        }
                    )
                ],
                response_1=phase1_response,
                model_name="gemini-2.0-flash-exp",
                system_instruction_text="base system instruction",
                temperature=0.0,
                safety_settings=[],
                json_mode_max_output_tokens=2048,
            )

        self.assertIs(response, phase2_response)
        self.assertEqual(mock_phase2.call_count, 2)
        self.assertTrue(mock_sleep.called)

    def test_code_execution_phase2_stops_after_two_attempts_for_non_gemini_3(self):
        """Non-Gemini 3 tool flows should stop after 2 attempts on retriable errors."""

        class RetriableGeminiError(Exception):
            def __init__(self, message: str):
                super().__init__(message)
                self.status = "FAILED_PRECONDITION"

        phase1_response = FakeLLMResponse(
            '{"tool_requests":[{"tool":"faction_calculate_power","args":{"soldiers":10}}]}'
        )

        with (
            patch(
                "mvp_site.llm_service.execute_gemini_code_execution_tool_orchestration",
                return_value=[
                    {
                        "tool": "faction_calculate_power",
                        "args": {"soldiers": 10},
                        "result": {"faction_power": 10},
                    }
                ],
            ),
            patch(
                "mvp_site.llm_service.time.sleep"
            ) as mock_sleep,
            patch(
                "mvp_site.llm_providers.gemini_provider.generate_json_mode_content",
                side_effect=RetriableGeminiError("temporary phase2 failure"),
            ) as mock_phase2,
        ):
            with self.assertRaises(RetriableGeminiError):
                llm_service._orchestrate_gemini_code_execution_tool_requests(
                    prompt_contents=[
                        json.dumps(
                            {
                                "game_state": {
                                    "custom_campaign_state": {
                                        "faction_minigame": {
                                            "enabled": True,
                                            "turn_number": 1,
                                        }
                                    }
                                },
                            }
                        )
                    ],
                    response_1=phase1_response,
                    model_name="gemini-2.0-flash-exp",
                    system_instruction_text="base system instruction",
                    temperature=0.0,
                    safety_settings=[],
                    json_mode_max_output_tokens=2048,
                )

        self.assertEqual(mock_phase2.call_count, 2)
        self.assertEqual(mock_sleep.call_count, 1)

    def test_code_execution_phase2_gemini_3_does_not_retry_on_retriable_error(self):
        """Gemini 3 code_execution should remain single-pass even on retriable errors."""

        class RetriableGeminiError(Exception):
            def __init__(self, message: str):
                super().__init__(message)
                self.status = "FAILED_PRECONDITION"

        phase1_response = FakeLLMResponse(
            '{"tool_requests":[{"tool":"faction_calculate_power","args":{"soldiers":10}}]}'
        )

        with (
            patch(
                "mvp_site.llm_service.execute_gemini_code_execution_tool_orchestration",
                return_value=[
                    {
                        "tool": "faction_calculate_power",
                        "args": {"soldiers": 10},
                        "result": {"faction_power": 10},
                    }
                ],
            ),
            patch(
                "mvp_site.llm_service.time.sleep"
            ) as mock_sleep,
            patch(
                "mvp_site.llm_providers.gemini_provider.generate_json_mode_content",
                side_effect=RetriableGeminiError("temporary phase2 failure"),
            ) as mock_phase2,
        ):
            with self.assertRaises(RetriableGeminiError):
                llm_service._orchestrate_gemini_code_execution_tool_requests(
                    prompt_contents=[
                        json.dumps(
                            {
                                "game_state": {
                                    "custom_campaign_state": {
                                        "faction_minigame": {
                                            "enabled": True,
                                            "turn_number": 1,
                                        }
                                    }
                                },
                            }
                        )
                    ],
                    response_1=phase1_response,
                    model_name="gemini-3-flash-preview",
                    system_instruction_text="base system instruction",
                    temperature=0.0,
                    safety_settings=[],
                    json_mode_max_output_tokens=2048,
                )

        self.assertEqual(mock_phase2.call_count, 1)
        self.assertFalse(mock_sleep.called)

    def test_call_llm_api_uses_code_execution_when_not_explicit_think_mode(self):
        """Do not auto-enable think mode from a phrase in system instructions."""
        with (
            patch(
                "mvp_site.dice_strategy.get_dice_roll_strategy",
                return_value=DICE_STRATEGY_CODE_EXECUTION,
            ),
            patch(
                "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
            ) as mock_code_exec,
            patch(
                "mvp_site.llm_providers.gemini_provider.generate_content_with_native_tools"
            ) as mock_native_tools,
        ):
            mock_code_exec.return_value = FakeLLMResponse('{"narrative":"ok"}')
            with patch.dict(os.environ, {"MOCK_SERVICES_MODE": "false"}):
                llm_service._call_llm_api(
                    ["test prompt"],
                    "gemini-2.0-flash",
                    "Think Mode System Instruction: do not use this for routing",
                    provider_name=constants.LLM_PROVIDER_GEMINI,
                    is_think_mode=False,
                )

            self.assertTrue(mock_code_exec.called)
            self.assertFalse(mock_native_tools.called)


class TestToolRequestsE2EFlow(unittest.TestCase):
    """E2E tests for generate_content_with_tool_requests() internal logic."""

    def test_path1_no_tool_requests_returns_phase1(self):
        """Path 1: Response without tool_requests returns Phase 1 directly."""
        phase1_json = json.dumps(
            {
                "narrative": "You look around the room.",
                "planning_block": {"thinking": "Observing surroundings"},
            }
        )
        with patch.object(cerebras_provider, "generate_content") as mock_gen:
            mock_gen.return_value = CerebrasResponse(
                text=phase1_json, raw_response=None
            )
            result = cerebras_provider.generate_content_with_tool_requests(
                prompt_contents=["Look around"],
                model_name="test-model",
                system_instruction_text="You are a GM",
                temperature=0.7,
                max_output_tokens=1000,
            )
            self.assertEqual(mock_gen.call_count, 1)
            self.assertEqual(result.text, phase1_json)

    def test_path2_tool_requests_triggers_phase2(self):
        """Path 2: Response with tool_requests executes tools and makes Phase 2 call."""
        phase1_json = json.dumps(
            {
                "narrative": "You attack the goblin!",
                "tool_requests": [
                    {"tool": "roll_dice", "args": {"notation": "1d20+5"}}
                ],
            }
        )
        phase2_json = json.dumps(
            {
                "narrative": "You rolled a 17! The goblin is hit.",
                "planning_block": {"thinking": "Attack successful"},
                "action_resolution": {
                    "mechanics": {
                        "rolls": [
                            {"purpose": "Attack", "notation": "1d20+5", "total": 17}
                        ]
                    }
                },
            }
        )
        with patch.object(cerebras_provider, "generate_content") as mock_gen:
            mock_gen.side_effect = [
                CerebrasResponse(text=phase1_json, raw_response=None),
                CerebrasResponse(text=phase2_json, raw_response=None),
            ]
            result = cerebras_provider.generate_content_with_tool_requests(
                prompt_contents=["I attack the goblin"],
                model_name="test-model",
                system_instruction_text="You are a GM",
                temperature=0.7,
                max_output_tokens=1000,
            )
            self.assertEqual(mock_gen.call_count, 2)
            self.assertEqual(result.text, phase2_json)
            phase2_call_args = mock_gen.call_args_list[1]
            messages = phase2_call_args.kwargs.get("messages", [])
            self.assertTrue(len(messages) >= 3)
            tool_results_msg = messages[-1]["content"]
            self.assertIn("Tool results", tool_results_msg)
            self.assertIn("1d20+5", tool_results_msg)

    def test_path3_invalid_json_returns_as_is(self):
        """Path 3: Non-JSON response returns as-is without Phase 2."""
        invalid_response = "This is not valid JSON"
        with patch.object(cerebras_provider, "generate_content") as mock_gen:
            mock_gen.return_value = CerebrasResponse(
                text=invalid_response, raw_response=None
            )
            result = cerebras_provider.generate_content_with_tool_requests(
                prompt_contents=["Test"],
                model_name="test-model",
                system_instruction_text=None,
                temperature=0.7,
                max_output_tokens=1000,
            )
            self.assertEqual(mock_gen.call_count, 1)
            self.assertEqual(result.text, invalid_response)

    def test_path4_tool_execution_errors_captured(self):
        """Path 4: Tool execution errors are captured in results."""
        tool_requests = [
            {"tool": "invalid_tool", "args": {}},
            {"tool": "roll_dice", "args": {"notation": "1d20"}},
        ]
        results = execute_tool_requests(tool_requests)
        self.assertEqual(len(results), 2)
        self.assertIn("error", results[0]["result"])
        self.assertIn("total", results[1]["result"])

    def test_path5_execute_tool_requests_helper(self):
        """Path 5: Test execute_tool_requests helper function directly."""
        tool_requests = [
            {"tool": "roll_dice", "args": {"notation": "2d6+3", "purpose": "damage"}},
            {"tool": "roll_attack", "args": {"attack_modifier": 5, "target_ac": 15}},
            {
                "tool": "roll_skill_check",
                "args": {
                    "skill_name": "Perception",
                    "attribute_modifier": 2,
                    "proficiency_bonus": 2,
                    "proficient": True,
                    "dc": 12,
                    "dc_reasoning": "Normal perception check in dim light",
                },
            },
        ]
        results = execute_tool_requests(tool_requests)
        self.assertEqual(len(results), 3)
        for i, result in enumerate(results):
            self.assertIn("tool", result)
            self.assertIn("args", result)
            self.assertIn("result", result)
            self.assertEqual(result["tool"], tool_requests[i]["tool"])
        self.assertIn("total", results[0]["result"])
        self.assertIn("rolls", results[0]["result"])
        self.assertNotIn("error", results[2]["result"])
        self.assertIn("success", results[2]["result"])

    def test_openrouter_path1_no_tool_requests(self):
        """Test OpenRouter provider Path 1: No tool_requests."""
        phase1_json = json.dumps(
            {
                "narrative": "The forest is peaceful.",
                "planning_block": {"thinking": "Peaceful scene"},
            }
        )
        with patch.object(openrouter_provider, "generate_content") as mock_gen:
            mock_gen.return_value = OpenRouterResponse(text=phase1_json)
            result = openrouter_provider.generate_content_with_tool_requests(
                prompt_contents=["Describe the forest"],
                model_name="test-model",
                system_instruction_text="You are a GM",
                temperature=0.7,
                max_output_tokens=1000,
            )
            self.assertEqual(mock_gen.call_count, 1)
            self.assertEqual(result.text, phase1_json)

    def test_openrouter_path2_with_tool_requests(self):
        """Test OpenRouter provider Path 2: With tool_requests."""
        phase1_json = json.dumps(
            {
                "narrative": "You attempt a skill check.",
                "tool_requests": [
                    {
                        "tool": "roll_skill_check",
                        "args": {
                            "skill_name": "Stealth",
                            "attribute_modifier": 4,
                            "proficiency_bonus": 2,
                            "proficient": True,
                            "dc": 12,
                            "dc_reasoning": "Guard is distracted",
                        },
                    }
                ],
            }
        )
        phase2_json = json.dumps(
            {
                "narrative": "You rolled a 16! You move silently.",
                "planning_block": {"thinking": "Stealth success"},
                "action_resolution": {
                    "mechanics": {
                        "rolls": [
                            {
                                "purpose": "Stealth",
                                "notation": "1d20+6",
                                "total": 16,
                                "dc": 12,
                                "success": True,
                            }
                        ]
                    }
                },
            }
        )
        with patch.object(openrouter_provider, "generate_content") as mock_gen:
            mock_gen.side_effect = [
                OpenRouterResponse(text=phase1_json),
                OpenRouterResponse(text=phase2_json),
            ]
            result = openrouter_provider.generate_content_with_tool_requests(
                prompt_contents=["I try to sneak past"],
                model_name="test-model",
                system_instruction_text="You are a GM",
                temperature=0.7,
                max_output_tokens=1000,
            )
            self.assertEqual(mock_gen.call_count, 2)
            self.assertEqual(result.text, phase2_json)


class TestThinkingConfigEnforcement(unittest.TestCase):
    """TDD tests for thinkingConfig + code_execution incompatibility (PR #4534)."""

    def test_gemini_3_disables_thinking_config_for_code_execution(self):
        """Verify ThinkingConfig is NOT used with code_execution (prevents FAILED_PRECONDITION).

        Context: PR #4534 - ThinkingConfig + code_execution triggers Gemini API
        FAILED_PRECONDITION errors (~60% failure rate). ThinkingConfig removed
        from code_execution calls to restore 100% pass rate.

        Evidence: docs/evidence/pr_4534_schema_validation/EVIDENCE_SUMMARY.md
        """
        mock_client = Mock()
        mock_response = Mock(text='{"narrative": "test", "dice_rolls": []}')
        mock_client.models.generate_content.return_value = mock_response
        # Must disable test stub to exercise real code path
        # Set TESTING_AUTH_BYPASS=false or use non-test API key
        with patch.dict(os.environ, {"TESTING_AUTH_BYPASS": "false"}):
            with patch.object(gemini_provider, "get_client", return_value=mock_client):
                gemini_provider.generate_content_with_code_execution(
                    prompt_contents=["test prompt"],
                    model_name="gemini-3-flash-preview",
                    system_instruction_text="test system",
                    temperature=0.7,
                    safety_settings=[],
                    json_mode_max_output_tokens=256,
                )
        self.assertTrue(mock_client.models.generate_content.called)
        call_args = mock_client.models.generate_content.call_args
        self.assertIsNotNone(call_args)
        config = call_args.kwargs.get("config")
        self.assertIsNotNone(config)
        # CRITICAL: thinking_config must be None/absent to prevent FAILED_PRECONDITION
        self.assertIsNone(getattr(config, "thinking_config", None))


class TestNativeToolsSystemInstruction(unittest.TestCase):
    """TDD tests for native two-phase system instruction retention."""

    def test_native_phase2_keeps_system_instruction_when_phase1_text_exists(self):
        """Verify Phase 2 call retains system instruction."""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.text = "Phase 1 narrative response."
        mock_part.function_call = None
        mock_response.candidates = [Mock(content=Mock(parts=[mock_part]))]
        mock_client.models.generate_content.return_value = mock_response
        with patch.object(gemini_provider, "get_client", return_value=mock_client):
            with patch.object(
                gemini_provider, "generate_json_mode_content"
            ) as mock_json:
                gemini_provider.generate_content_with_native_tools(
                    prompt_contents=["prompt"],
                    model_name="gemini-2.5-flash",
                    system_instruction_text="SYSTEM_INSTRUCTION",
                    temperature=0.7,
                    safety_settings=[],
                    json_mode_max_output_tokens=256,
                )
                _, kwargs = mock_json.call_args
                assert kwargs.get("system_instruction_text") == "SYSTEM_INSTRUCTION"


class TestSystemPromptEnforcementWarning(unittest.TestCase):
    """TDD tests for system prompt enforcement warning in code_execution mode.

    DICE-s8u Architecture Note:
    As of DICE-s8u, dice instructions are loaded from separate prompt files
    (dice_system_instruction_code_execution.md) via load_dice_instructions()
    at prompt-build time in agent_prompts.py, NOT injected inline in
    generate_content_with_code_execution(). These tests verify the source
    of truth (the prompt file) contains the expected enforcement content.
    """

    def test_enforcement_warning_is_in_dice_instruction_file(self):
        """Verify dice code_execution instruction file includes enforcement warning."""
        dice_instructions = load_dice_instructions(DICE_STRATEGY_CODE_EXECUTION)

        self.assertIsNotNone(dice_instructions)
        self.assertIn("ENFORCEMENT WARNING", dice_instructions)
        self.assertIn("IS INSPECTED", dice_instructions)
        self.assertIn("WILL BE REJECTED", dice_instructions)

    def test_fabrication_example_is_documented(self):
        """Verify dice instruction file documents the specific fabrication pattern."""
        dice_instructions = load_dice_instructions(DICE_STRATEGY_CODE_EXECUTION)

        self.assertIn("hardcoded", dice_instructions.lower())
        self.assertIn("without RNG", dice_instructions)


if __name__ == "__main__":
    # Standard unittest invocation
    unittest.main()

class TestOpenClawProviderIntegration(unittest.TestCase):
    """Test OpenClaw provider implementation using mocks."""

    def setUp(self):
        self.monkeypatch = patch("requests.post")
        self.mock_post = self.monkeypatch.start()

    def tearDown(self):
        self.monkeypatch.stop()

    def test_non_stream_response(self):
        from mvp_site.llm_providers import openclaw_provider
        self.mock_post.return_value = Mock()
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.json.return_value = {"choices": [{"message": {"content": "Hello world"}}]}
        self.mock_post.return_value.raise_for_status = lambda: None

        response = openclaw_provider.generate_content(
            prompt_contents=["test"],
            model_name="openclaw/gemini-3-pro",
            system_instruction_text="system",
            temperature=0.8,
            max_output_tokens=4096,
        )

        self.assertIsInstance(response, openclaw_provider.OpenClawResponse)
        self.assertEqual(response.text, "Hello world")

    def test_streaming_yields_chunks(self):
        from mvp_site.llm_providers import openclaw_provider
        
        class FakeStream:
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def raise_for_status(self): pass
            def iter_lines(self):
                yield b'data: {"choices":[{"delta":{"content":"A"}}]}'
                yield b'data: {"choices":[{"delta":{"content":"B"}}]}'
                yield b"data: [DONE]"

        self.mock_post.return_value = FakeStream()

        chunks = list(
            openclaw_provider.generate_content_stream_sync(
                prompt_contents=["payload"],
                model_name="openclaw/gemini-3-pro",
                system_instruction_text="system",
                temperature=0.8,
                max_output_tokens=1024,
            )
        )

        self.assertEqual(chunks, ["A", "B"])

    def test_gateway_unavailable_raises_actionable_error(self):
        from mvp_site.llm_providers import openclaw_provider
        self.mock_post.side_effect = requests.ConnectionError("connection refused")

        with self.assertRaises(RuntimeError) as cm:
            openclaw_provider.generate_content(
                prompt_contents=["test"],
                model_name="openclaw/gemini-3-pro",
                system_instruction_text="system",
                temperature=0.8,
                max_output_tokens=256,
            )
        self.assertIn("OpenClaw", str(cm.exception))

    def test_gateway_port_overrides_default(self):
        from mvp_site.llm_providers import openclaw_provider
        self.mock_post.return_value = Mock()
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.json.return_value = {"choices": [{"message": {"content": "ok"}}]}
        self.mock_post.return_value.raise_for_status = lambda: None

        openclaw_provider.generate_content(
            prompt_contents=["payload"],
            model_name="openclaw/gemini-3-pro",
            system_instruction_text="system",
            temperature=0.8,
            max_output_tokens=256,
            gateway_port=28999,
        )

        args, kwargs = self.mock_post.call_args
        url = args[0]
        self.assertIn("28999", url)

    def test_model_name_strips_prefix(self):
        from mvp_site.llm_providers import openclaw_provider
        self.mock_post.return_value = Mock()
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.json.return_value = {"choices": [{"message": {"content": "test"}}]}
        self.mock_post.return_value.raise_for_status = lambda: None

        openclaw_provider.generate_content(
            prompt_contents=["test"],
            model_name="openclaw/MiniMax-M2.5",
            system_instruction_text="system",
            temperature=0.8,
            max_output_tokens=256,
        )

        _, kwargs = self.mock_post.call_args
        self.assertEqual(kwargs["json"]["model"], "MiniMax-M2.5")

    def test_invoke_error_raises(self):
        from mvp_site.llm_providers import openclaw_provider
        self.mock_post.return_value = Mock()
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.json.return_value = {"error": {"message": "bad"}}
        self.mock_post.return_value.raise_for_status = lambda: None

        with self.assertRaises(RuntimeError) as cm:
            openclaw_provider.generate_content(
                prompt_contents=["test"],
                model_name="openclaw/gemini-3-pro",
                system_instruction_text="system",
                temperature=0.8,
                max_output_tokens=256,
            )
        self.assertIn("OpenClaw invoke failed", str(cm.exception))
