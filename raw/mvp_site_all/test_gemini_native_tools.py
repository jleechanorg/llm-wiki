from __future__ import annotations

import os
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch


class TestGeminiNativeTools(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["TESTING_AUTH_BYPASS"] = "true"
        os.environ.setdefault("GEMINI_API_KEY", "test")

    @patch("mvp_site.llm_providers.gemini_provider.get_client")
    def test_native_tools_does_not_force_tool_calling(self, mock_get_client: MagicMock):
        """Gemini native-tools path should not force at least one tool call."""
        from mvp_site.llm_providers import gemini_provider

        client = MagicMock()
        mock_get_client.return_value = client

        # Return a response that includes no function calls (narrative-only)
        response1 = SimpleNamespace(
            candidates=[
                SimpleNamespace(
                    content=SimpleNamespace(
                        parts=[SimpleNamespace(text="No dice needed.")]
                    )
                )
            ]
        )
        client.models.generate_content.return_value = response1

        with patch(
            "mvp_site.llm_providers.gemini_provider.generate_json_mode_content"
        ) as mock_json:
            mock_json.return_value = SimpleNamespace(text='{"narrative":"ok"}')

            gemini_provider.generate_content_with_native_tools(
                prompt_contents=["Describe the room."],
                model_name="gemini-2.0-flash",
                system_instruction_text="sys",
                temperature=0.0,
                safety_settings=[],
                json_mode_max_output_tokens=256,
            )

        # Capture config passed to Phase 1 call
        _args, kwargs = client.models.generate_content.call_args
        config = kwargs["config"]
        assert config.tool_config is not None
        assert config.tool_config.function_calling_config is not None
        assert config.tool_config.function_calling_config.mode == "AUTO", (
            "Should not use mode='ANY' (forced tool calling)"
        )

    @patch("mvp_site.llm_providers.gemini_provider.get_client")
    def test_native_tools_no_function_calls_still_returns_json(
        self, mock_get_client: MagicMock
    ):
        """No-roll turns should still produce a valid JSON response via Phase 2."""
        from mvp_site.llm_providers import gemini_provider

        client = MagicMock()
        mock_get_client.return_value = client

        # Phase 1 response: no function calls, but some text
        response1 = SimpleNamespace(
            candidates=[
                SimpleNamespace(
                    content=SimpleNamespace(
                        parts=[SimpleNamespace(text="Some narrative.")]
                    )
                )
            ]
        )
        client.models.generate_content.return_value = response1

        with patch(
            "mvp_site.llm_providers.gemini_provider.generate_json_mode_content"
        ) as mock_json:
            mock_json.return_value = SimpleNamespace(text='{"narrative":"ok"}')

            out = gemini_provider.generate_content_with_native_tools(
                prompt_contents=["Describe the room."],
                model_name="gemini-2.0-flash",
                system_instruction_text="sys",
                temperature=0.0,
                safety_settings=[],
                json_mode_max_output_tokens=256,
            )

        assert out.text == '{"narrative":"ok"}'
        assert mock_json.called, (
            "Phase 2 JSON call should happen when no function_calls"
        )


class TestGeminiNativeToolLoop(unittest.TestCase):
    """Test cases for Gemini native tool loop mismatch handling."""

    def setUp(self) -> None:
        os.environ["TESTING_AUTH_BYPASS"] = "true"
        os.environ.setdefault("GEMINI_API_KEY", "test")

    @patch("mvp_site.llm_providers.gemini_provider.logging_util")
    @patch("mvp_site.llm_providers.gemini_provider.execute_tool_requests")
    @patch("mvp_site.llm_providers.gemini_provider.get_client")
    def test_tool_result_mismatch_logs_warning(
        self, mock_get_client, mock_execute, mock_logging
    ):
        """Verify warning logged when len(tool_results) != len(tool_requests)."""
        from mvp_site.llm_providers import gemini_provider

        client = MagicMock()
        mock_get_client.return_value = client

        # Create tool requests
        tool_requests = [
            {"tool": "tool1", "args": {}},
            {"tool": "tool2", "args": {}},
        ]

        # Mock execute_tool_requests to return fewer results than requests
        mock_execute.return_value = [
            {"result": "data1"}
        ]  # Only 1 result for 2 requests

        # Phase 1 response with function calls
        response1 = SimpleNamespace(
            candidates=[
                SimpleNamespace(
                    content=SimpleNamespace(
                        parts=[
                            SimpleNamespace(
                                function_call=SimpleNamespace(name="tool1", args={})
                            )
                        ]
                    )
                )
            ]
        )
        client.models.generate_content.return_value = response1

        with patch(
            "mvp_site.llm_providers.gemini_provider.generate_json_mode_content"
        ) as mock_json:
            mock_json.return_value = SimpleNamespace(text='{"narrative":"ok"}')

            # Mock the tool extraction
            with patch(
                "mvp_site.llm_providers.gemini_provider._extract_function_calls"
            ) as mock_extract:
                mock_extract.return_value = tool_requests

                gemini_provider.generate_content_with_native_tools(
                    prompt_contents=["Test input"],
                    model_name="gemini-2.0-flash",
                    system_instruction_text="sys",
                    temperature=0.0,
                    safety_settings=[],
                    json_mode_max_output_tokens=256,
                )

        # Verify warning was logged
        warning_calls = [
            call
            for call in mock_logging.warning.call_args_list
            if "mismatch" in str(call).lower() or "tool_results" in str(call).lower()
        ]
        self.assertGreater(
            len(warning_calls), 0, "Warning should be logged for tool result mismatch"
        )

    @patch("mvp_site.llm_providers.gemini_provider.execute_tool_requests")
    @patch("mvp_site.llm_providers.gemini_provider.get_client")
    def test_tool_result_mismatch_builds_from_results_only(
        self, mock_get_client, mock_execute
    ):
        """Verify function responses built from tool_results only when mismatch."""
        from mvp_site.llm_providers import gemini_provider

        client = MagicMock()
        mock_get_client.return_value = client

        tool_requests = [
            {"tool": "tool1", "args": {}},
            {"tool": "tool2", "args": {}},
        ]

        # Return fewer results than requests
        mock_execute.return_value = [{"result": "data1"}]

        response1 = SimpleNamespace(
            candidates=[
                SimpleNamespace(
                    content=SimpleNamespace(
                        parts=[
                            SimpleNamespace(
                                function_call=SimpleNamespace(name="tool1", args={})
                            )
                        ]
                    )
                )
            ]
        )
        client.models.generate_content.return_value = response1

        with patch(
            "mvp_site.llm_providers.gemini_provider.generate_json_mode_content"
        ) as mock_json:
            mock_json.return_value = SimpleNamespace(text='{"narrative":"ok"}')

            with patch(
                "mvp_site.llm_providers.gemini_provider._extract_function_calls"
            ) as mock_extract:
                mock_extract.return_value = tool_requests

                # Should not raise exception - should handle mismatch gracefully
                result = gemini_provider.generate_content_with_native_tools(
                    prompt_contents=["Test input"],
                    model_name="gemini-2.0-flash",
                    system_instruction_text="sys",
                    temperature=0.0,
                    safety_settings=[],
                    json_mode_max_output_tokens=256,
                )

                # Should still return a result
                self.assertIsNotNone(result)
