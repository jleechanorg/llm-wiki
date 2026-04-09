"""
TDD tests for cache + provably fair compatibility (REV-wvh, REV-lfl).

Verifies that:
1. generate_content_with_code_execution passes cache_name through to API (not None)
2. Provably fair seed is injected as a content part, not in system_instruction
3. generate_content_with_tool_requests passes cache_name even when tool_requests exist

Layer 1 unit test — no server required.
"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from google.genai import types


class TestCacheProvablyFairCompatibility(unittest.TestCase):
    """Cache must remain active when provably fair seed is injected."""

    @patch("mvp_site.llm_providers.gemini_provider.generate_json_mode_content")
    def test_code_execution_passes_cache_name_through(self, mock_gen):
        """generate_content_with_code_execution must pass cache_name to API, not None."""
        from mvp_site.llm_providers import gemini_provider

        mock_response = MagicMock()
        mock_gen.return_value = mock_response

        gemini_provider.generate_content_with_code_execution(
            prompt_contents=["test prompt"],
            model_name="gemini-3-flash-preview",
            system_instruction_text="You are a DM.",
            temperature=1.0,
            safety_settings=[],
            json_mode_max_output_tokens=8192,
            cache_name="cachedContents/test-cache-abc",
        )

        mock_gen.assert_called_once()
        call_kwargs = mock_gen.call_args
        self.assertEqual(
            call_kwargs.kwargs.get("cache_name") or call_kwargs[1].get("cache_name"),
            "cachedContents/test-cache-abc",
            "cache_name must flow through to generate_json_mode_content, not be set to None",
        )

    @patch("mvp_site.llm_providers.gemini_provider.generate_json_mode_content")
    def test_seed_injected_as_content_part_not_system_instruction(self, mock_gen):
        """Provably fair seed must appear in prompt_contents, not system_instruction."""
        from mvp_site.llm_providers import gemini_provider

        mock_response = MagicMock()
        mock_gen.return_value = mock_response

        gemini_provider.generate_content_with_code_execution(
            prompt_contents=["test prompt"],
            model_name="gemini-3-flash-preview",
            system_instruction_text="You are a DM.",
            temperature=1.0,
            safety_settings=[],
            json_mode_max_output_tokens=8192,
            cache_name="cachedContents/test-cache-abc",
        )

        call_kwargs = mock_gen.call_args
        # Get the actual keyword arguments
        kwargs = call_kwargs.kwargs if call_kwargs.kwargs else {}
        if not kwargs:
            # Positional call — use call_args[1]
            kwargs = call_kwargs[1] if len(call_kwargs) > 1 else {}

        # With cache enabled, system_instruction is carried by cached content
        # and must be omitted from the request payload.
        sys_inst = kwargs.get("system_instruction_text")
        self.assertIsNone(
            sys_inst,
            "system_instruction must be omitted when using cached_content",
        )

        # Prompt contents must contain the seed override as first item
        prompt_contents = kwargs.get("prompt_contents", [])
        self.assertTrue(len(prompt_contents) >= 2, "seed part should be prepended")
        first_content = prompt_contents[0]
        self.assertIsInstance(first_content, types.Content)
        seed_text = first_content.parts[0].text
        self.assertIn(
            "PROVABLY_FAIR_SEED_OVERRIDE",
            seed_text,
            "First content part must be the provably fair seed override",
        )
        self.assertIn(
            "random.seed('",
            seed_text,
            "Seed override must contain the actual hex seed",
        )

    @patch("mvp_site.llm_providers.gemini_provider.generate_json_mode_content")
    @patch("mvp_site.llm_providers.gemini_provider.get_client")
    def test_native_tools_does_not_disable_cache(self, mock_client, mock_gen):
        """Native-tools cache path keeps cache and suppresses phase1 system_instruction."""
        from mvp_site.llm_providers import gemini_provider

        # Phase 1: model returns a function call (triggers tool execution)
        phase1_response = MagicMock()
        phase1_candidate = MagicMock()
        phase1_part = MagicMock()
        phase1_part.function_call = MagicMock()
        phase1_part.function_call.name = "roll_dice"
        phase1_part.function_call.args = {"notation": "1d20"}
        phase1_candidate.content = MagicMock()
        phase1_candidate.content.parts = [phase1_part]
        phase1_response.candidates = [phase1_candidate]
        mock_client.return_value.models.generate_content.return_value = phase1_response

        # Phase 2: generate_json_mode_content returns final response
        phase2_response = MagicMock()
        mock_gen.return_value = phase2_response

        gemini_provider.generate_content_with_native_tools(
            prompt_contents=["test prompt"],
            model_name="gemini-2.0-flash",
            system_instruction_text="You are a DM.",
            temperature=1.0,
            safety_settings=[],
            json_mode_max_output_tokens=8192,
            cache_name="cachedContents/test-cache-xyz",
            native_tools=[{
                "function": {
                    "name": "roll_dice",
                    "description": "Roll dice",
                    "parameters": {"type": "object", "properties": {}},
                }
            }],
        )

        # Phase 2 should have been called with cache_name preserved
        mock_gen.assert_called_once()
        call_kwargs = mock_gen.call_args
        kwargs = call_kwargs.kwargs if call_kwargs.kwargs else call_kwargs[1]
        self.assertEqual(
            kwargs.get("cache_name"),
            "cachedContents/test-cache-xyz",
            "cache_name must NOT be disabled when tool_requests exist",
        )
        self.assertIsNone(
            kwargs.get("system_instruction_text"),
            "phase2 system_instruction must be suppressed when cache_name is set",
        )
        phase1_call = mock_client.return_value.models.generate_content.call_args
        phase1_config = phase1_call.kwargs["config"]
        self.assertIsNone(
            getattr(phase1_config, "system_instruction", None),
            "phase1 system_instruction must be suppressed when cache_name is set",
        )


if __name__ == "__main__":
    unittest.main()
