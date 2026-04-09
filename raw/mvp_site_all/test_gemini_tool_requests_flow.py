"""Tests for Gemini native function calling flow.

Tests generate_content_with_native_tools which uses Gemini's native
function_call API (not JSON-first tool_requests parsing).
"""

from __future__ import annotations

import os
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from mvp_site.llm_providers import gemini_provider


class TestGeminiNativeToolsFlow(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["TESTING_AUTH_BYPASS"] = "true"
        os.environ.setdefault("GEMINI_API_KEY", "test")

    def test_native_tools_runs_phase2_when_function_calls_present(self):
        """Phase 2 runs when model returns function calls."""
        # Mock Phase 1 response with function calls
        mock_function_call = MagicMock()
        mock_function_call.name = "roll_dice"
        mock_function_call.args = {"notation": "1d20"}

        mock_part = MagicMock()
        mock_part.function_call = mock_function_call

        mock_content = MagicMock()
        mock_content.parts = [mock_part]

        mock_candidate = MagicMock()
        mock_candidate.content = mock_content

        phase1_response = MagicMock()
        phase1_response.candidates = [mock_candidate]

        phase2_response = SimpleNamespace(text='{"narrative":"Rolled a 15!"}')

        with (
            patch.object(gemini_provider, "get_client") as mock_get_client,
            patch.object(gemini_provider, "execute_tool_requests") as mock_exec,
            patch.object(gemini_provider, "generate_json_mode_content") as mock_json,
        ):
            mock_client = MagicMock()
            mock_client.models.generate_content.return_value = phase1_response
            mock_get_client.return_value = mock_client

            mock_exec.return_value = [
                {"tool": "roll_dice", "args": {"notation": "1d20"}, "result": 15}
            ]
            mock_json.return_value = phase2_response

            out = gemini_provider.generate_content_with_native_tools(
                prompt_contents=["Roll for initiative"],
                model_name="gemini-2.0-flash",
                system_instruction_text="sys",
                temperature=0.0,
                safety_settings=[],
                json_mode_max_output_tokens=256,
            )

        assert out.text == '{"narrative":"Rolled a 15!"}'
        assert mock_exec.called
        assert mock_json.called

    def test_native_tools_skips_phase2_when_no_function_calls(self):
        """No Phase 2 when model doesn't call functions."""
        # Mock Phase 1 response without function calls (just text)
        mock_part = MagicMock()
        mock_part.function_call = None

        mock_content = MagicMock()
        mock_content.parts = [mock_part]

        mock_candidate = MagicMock()
        mock_candidate.content = mock_content

        phase1_response = MagicMock()
        phase1_response.candidates = [mock_candidate]

        phase2_response = SimpleNamespace(text='{"narrative":"No dice needed"}')

        with (
            patch.object(gemini_provider, "get_client") as mock_get_client,
            patch.object(gemini_provider, "execute_tool_requests") as mock_exec,
            patch.object(gemini_provider, "generate_json_mode_content") as mock_json,
        ):
            mock_client = MagicMock()
            mock_client.models.generate_content.return_value = phase1_response
            mock_get_client.return_value = mock_client

            mock_json.return_value = phase2_response

            out = gemini_provider.generate_content_with_native_tools(
                prompt_contents=["Hello"],
                model_name="gemini-2.0-flash",
                system_instruction_text="sys",
                temperature=0.0,
                safety_settings=[],
                json_mode_max_output_tokens=256,
            )

        assert out.text == '{"narrative":"No dice needed"}'
        # execute_tool_requests should NOT be called when no function calls
        assert not mock_exec.called
        # Phase 2 still runs to get final JSON output
        assert mock_json.called

    def test_extract_function_calls_ignores_secondary_candidates(self):
        """Verify we only extract function calls from the first candidate.

        If we extract calls from all candidates but only put the first candidate's
        content in history, we get a mismatch error from the API.
        """
        # Mock a response with 2 candidates
        # Candidate 1: Calls "tool_one"
        mock_call_1 = MagicMock()
        mock_call_1.name = "tool_one"
        mock_call_1.args = {"arg": 1}

        part_1 = MagicMock()
        part_1.function_call = mock_call_1

        content_1 = MagicMock()
        content_1.parts = [part_1]

        candidate_1 = MagicMock()
        candidate_1.content = content_1

        # Candidate 2: Calls "tool_two" (Should be ignored)
        mock_call_2 = MagicMock()
        mock_call_2.name = "tool_two"
        mock_call_2.args = {"arg": 2}

        part_2 = MagicMock()
        part_2.function_call = mock_call_2

        content_2 = MagicMock()
        content_2.parts = [part_2]

        candidate_2 = MagicMock()
        candidate_2.content = content_2

        # Response object
        mock_response = MagicMock()
        mock_response.candidates = [candidate_1, candidate_2]

        # Execute
        # Access protected member for unit testing the logic directly
        tool_requests = gemini_provider._extract_function_calls(mock_response)

        # Verify
        self.assertEqual(
            len(tool_requests), 1, "Should only have 1 tool request from 2 candidates"
        )
        self.assertEqual(
            tool_requests[0]["tool"], "tool_one", "Should match first candidate's tool"
        )

        # Explicitly ensure candidate 2 was NOT processed
        tools_found = [r["tool"] for r in tool_requests]
        self.assertNotIn(
            "tool_two", tools_found, "Secondary candidate tool calls must be ignored"
        )


class TestGeminiProviderTestStub(unittest.TestCase):
    def setUp(self) -> None:
        self.original_env = os.environ.copy()
        gemini_provider.clear_cached_client()

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self.original_env)
        gemini_provider.clear_cached_client()

    def test_stub_client_used_for_test_api_key(self):
        os.environ["TESTING_AUTH_BYPASS"] = "true"
        os.environ["GEMINI_API_KEY"] = "test-ci-key-only"

        client = gemini_provider.get_client()
        self.assertEqual(type(client).__name__, "_TestClient")

    def test_stub_short_circuits_json_mode_generation(self):
        os.environ["TESTING_AUTH_BYPASS"] = "true"
        os.environ["GEMINI_API_KEY"] = "test-ci-key-only"

        with patch.object(gemini_provider, "get_client") as mock_get_client:
            response = gemini_provider.generate_json_mode_content(
                prompt_contents=["hello"],
                model_name="gemini-2.5-flash",
                system_instruction_text="sys",
                temperature=0.7,
                safety_settings=[],
                json_mode_max_output_tokens=128,
            )
            self.assertIn("test-mode Gemini response", response.text)
            mock_get_client.assert_not_called()

    def test_stub_count_tokens_returns_approximate(self):
        os.environ["TESTING_AUTH_BYPASS"] = "true"
        os.environ["GEMINI_API_KEY"] = "test-ci-key-only"

        with patch.object(gemini_provider, "get_client") as mock_get_client:
            total_tokens = gemini_provider.count_tokens(
                model_name="gemini-2.5-flash", contents=["hello world"]
            )
            self.assertGreaterEqual(total_tokens, 1)
            mock_get_client.assert_not_called()
