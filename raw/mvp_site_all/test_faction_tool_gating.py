"""Tests for faction tool gating when faction_minigame_enabled=False.

Verifies that faction tools are NOT available to the LLM when the minigame is disabled.
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from mvp_site import faction_state_util
from mvp_site.dice import DICE_ROLL_TOOLS
from mvp_site.faction.tools import FACTION_TOOLS, FACTION_TOOL_NAMES
from mvp_site.llm_providers import cerebras_provider, gemini_provider, openrouter_provider


class TestFactionToolGating:
    """Test that faction tools are gated based on faction_minigame.enabled."""

    def _create_prompt_contents_with_faction_state(self, enabled: bool) -> list[str]:
        """Create prompt_contents JSON with faction_minigame.enabled set."""
        payload = {
            "game_state": {
                "custom_campaign_state": {
                    "faction_minigame": {
                        "enabled": enabled,
                        "turn_number": 1,
                    }
                }
            }
        }
        return [json.dumps(payload)]

    def _create_prompt_contents_without_faction_state(self) -> list[str]:
        """Create prompt_contents JSON without faction_minigame."""
        payload = {
            "game_state": {
                "custom_campaign_state": {}
            }
        }
        return [json.dumps(payload)]

    def _create_prompt_contents_enable_action(self) -> list[str]:
        """Create prompt_contents JSON with explicit enable action."""
        payload = {
            "user_action": "enable_faction_minigame",
            "game_state": {
                "custom_campaign_state": {
                    "faction_minigame": {
                        "enabled": False,
                        "turn_number": 1,
                    }
                }
            },
        }
        return [json.dumps(payload)]

    @patch("mvp_site.llm_providers.gemini_provider.get_client")
    @patch("mvp_site.llm_providers.gemini_provider._build_gemini_tools")
    def test_gemini_native_tools_excludes_faction_when_disabled(
        self, mock_build_tools, mock_get_client
    ):
        """Verify Gemini native tools excludes faction tools when enabled=False."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_build_tools.return_value = []

        # Mock the response
        mock_response = MagicMock()
        mock_response.text = '{"narrative": "test"}'
        mock_client.models.generate_content.return_value = mock_response

        prompt_contents = self._create_prompt_contents_with_faction_state(enabled=False)

        gemini_provider.generate_content_with_native_tools(
            prompt_contents=prompt_contents,
            model_name="gemini-2.0-flash-exp",
            system_instruction_text="test",
            temperature=0.9,
            safety_settings=[],
            json_mode_max_output_tokens=4096,
        )

        # Verify _build_gemini_tools was called
        assert mock_build_tools.called
        call_args = mock_build_tools.call_args[0][0]

        # Extract tool names from the call
        tool_names = [
            tool["function"]["name"]
            for tool in call_args
            if "function" in tool and "name" in tool["function"]
        ]

        # Verify dice tools are present
        dice_tool_names = [
            tool["function"]["name"]
            for tool in DICE_ROLL_TOOLS
            if "function" in tool and "name" in tool["function"]
        ]
        for dice_tool in dice_tool_names:
            assert dice_tool in tool_names, f"Dice tool {dice_tool} should be present"

        # Verify faction tools are NOT present
        faction_tool_names = [
            tool["function"]["name"]
            for tool in FACTION_TOOLS
            if "function" in tool and "name" in tool["function"]
        ]
        for faction_tool in faction_tool_names:
            assert (
                faction_tool not in tool_names
            ), f"Faction tool {faction_tool} should NOT be present when enabled=False"

    @patch("mvp_site.llm_providers.gemini_provider.get_client")
    @patch("mvp_site.llm_providers.gemini_provider._build_gemini_tools")
    def test_gemini_native_tools_includes_faction_when_enabled(
        self, mock_build_tools, mock_get_client
    ):
        """Verify Gemini native tools includes faction tools when enabled=True."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_build_tools.return_value = []

        # Mock the response
        mock_response = MagicMock()
        mock_response.text = '{"narrative": "test"}'
        mock_client.models.generate_content.return_value = mock_response

        prompt_contents = self._create_prompt_contents_with_faction_state(enabled=True)

        gemini_provider.generate_content_with_native_tools(
            prompt_contents=prompt_contents,
            model_name="gemini-2.0-flash-exp",
            system_instruction_text="test",
            temperature=0.9,
            safety_settings=[],
            json_mode_max_output_tokens=4096,
        )

        # Verify _build_gemini_tools was called
        assert mock_build_tools.called
        call_args = mock_build_tools.call_args[0][0]

        # Extract tool names from the call
        tool_names = [
            tool["function"]["name"]
            for tool in call_args
            if "function" in tool and "name" in tool["function"]
        ]

        # Verify faction tools ARE present
        faction_tool_names = [
            tool["function"]["name"]
            for tool in FACTION_TOOLS
            if "function" in tool and "name" in tool["function"]
        ]
        for faction_tool in faction_tool_names:
            assert (
                faction_tool in tool_names
            ), f"Faction tool {faction_tool} should be present when enabled=True"

    @patch("mvp_site.llm_providers.gemini_provider.get_client")
    @patch("mvp_site.llm_providers.gemini_provider._build_gemini_tools")
    def test_gemini_native_tools_excludes_faction_when_missing(
        self, mock_build_tools, mock_get_client
    ):
        """Verify Gemini native tools excludes faction tools when faction_minigame is missing."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_build_tools.return_value = []

        # Mock the response
        mock_response = MagicMock()
        mock_response.text = '{"narrative": "test"}'
        mock_client.models.generate_content.return_value = mock_response

        prompt_contents = self._create_prompt_contents_without_faction_state()

        gemini_provider.generate_content_with_native_tools(
            prompt_contents=prompt_contents,
            model_name="gemini-2.0-flash-exp",
            system_instruction_text="test",
            temperature=0.9,
            safety_settings=[],
            json_mode_max_output_tokens=4096,
        )

        # Verify _build_gemini_tools was called
        assert mock_build_tools.called
        call_args = mock_build_tools.call_args[0][0]

        # Extract tool names from the call
        tool_names = [
            tool["function"]["name"]
            for tool in call_args
            if "function" in tool and "name" in tool["function"]
        ]

        # Verify faction tools are NOT present (defaults to disabled)
        faction_tool_names = [
            tool["function"]["name"]
            for tool in FACTION_TOOLS
            if "function" in tool and "name" in tool["function"]
        ]
        for faction_tool in faction_tool_names:
            assert (
                faction_tool not in tool_names
            ), f"Faction tool {faction_tool} should NOT be present when faction_minigame is missing"

    @patch("mvp_site.llm_providers.gemini_provider.get_client")
    @patch("mvp_site.llm_providers.gemini_provider._build_gemini_tools")
    def test_gemini_native_tools_include_faction_on_enable_action(
        self, mock_build_tools, mock_get_client
    ):
        """Verify explicit enable action includes faction tools even when currently disabled."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_build_tools.return_value = []
        mock_response = MagicMock()
        mock_response.text = '{"narrative": "test"}'
        mock_client.models.generate_content.return_value = mock_response

        prompt_contents = self._create_prompt_contents_enable_action()

        gemini_provider.generate_content_with_native_tools(
            prompt_contents=prompt_contents,
            model_name="gemini-2.0-flash-exp",
            system_instruction_text="test",
            temperature=0.9,
            safety_settings=[],
            json_mode_max_output_tokens=4096,
        )

        assert mock_build_tools.called
        call_args = mock_build_tools.call_args[0][0]
        tool_names = [
            tool["function"]["name"]
            for tool in call_args
            if "function" in tool and "name" in tool["function"]
        ]
        for faction_tool in FACTION_TOOL_NAMES:
            assert faction_tool in tool_names

    @patch("mvp_site.llm_providers.openrouter_provider.run_openai_native_two_phase_flow")
    def test_openrouter_excludes_faction_when_disabled(self, mock_flow):
        """Verify OpenRouter excludes faction tools when enabled=False."""
        prompt_contents = self._create_prompt_contents_with_faction_state(enabled=False)
        native_tools = faction_state_util.build_native_tools_for_prompt_contents(
            prompt_contents
        )

        openrouter_provider.generate_content_with_native_tools(
            prompt_contents=prompt_contents,
            model_name="gpt-4o",
            system_instruction_text="test",
            temperature=0.9,
            max_output_tokens=4096,
            native_tools=native_tools,
        )

        # Verify run_openai_native_two_phase_flow was called
        assert mock_flow.called
        call_kwargs = mock_flow.call_args[1]

        # Check dice_roll_tools parameter
        dice_roll_tools = call_kwargs.get("dice_roll_tools", [])

        # Extract tool names
        tool_names = [
            tool["function"]["name"]
            for tool in dice_roll_tools
            if "function" in tool and "name" in tool["function"]
        ]

        # Verify faction tools are NOT present
        faction_tool_names = [
            tool["function"]["name"]
            for tool in FACTION_TOOLS
            if "function" in tool and "name" in tool["function"]
        ]
        for faction_tool in faction_tool_names:
            assert (
                faction_tool not in tool_names
            ), f"Faction tool {faction_tool} should NOT be present when enabled=False"

    @patch("mvp_site.llm_providers.openrouter_provider.run_openai_native_two_phase_flow")
    def test_openrouter_includes_faction_when_enabled(self, mock_flow):
        """Verify OpenRouter includes faction tools when enabled=True."""
        prompt_contents = self._create_prompt_contents_with_faction_state(enabled=True)
        native_tools = faction_state_util.build_native_tools_for_prompt_contents(
            prompt_contents
        )

        openrouter_provider.generate_content_with_native_tools(
            prompt_contents=prompt_contents,
            model_name="gpt-4o",
            system_instruction_text="test",
            temperature=0.9,
            max_output_tokens=4096,
            native_tools=native_tools,
        )

        assert mock_flow.called
        call_kwargs = mock_flow.call_args[1]
        dice_roll_tools = call_kwargs.get("dice_roll_tools", [])
        tool_names = [
            tool["function"]["name"]
            for tool in dice_roll_tools
            if "function" in tool and "name" in tool["function"]
        ]

        faction_tool_names = [
            tool["function"]["name"]
            for tool in FACTION_TOOLS
            if "function" in tool and "name" in tool["function"]
        ]
        for faction_tool in faction_tool_names:
            assert (
                faction_tool in tool_names
            ), f"Faction tool {faction_tool} should be present when enabled=True"

    @patch("mvp_site.llm_providers.cerebras_provider.run_openai_native_two_phase_flow")
    def test_cerebras_excludes_faction_when_disabled(self, mock_flow):
        """Verify Cerebras excludes faction tools when enabled=False."""
        prompt_contents = self._create_prompt_contents_with_faction_state(enabled=False)
        native_tools = faction_state_util.build_native_tools_for_prompt_contents(
            prompt_contents
        )

        cerebras_provider.generate_content_with_native_tools(
            prompt_contents=prompt_contents,
            model_name="qwen-3-235b-a22b-instruct-2507",
            system_instruction_text="test",
            temperature=0.7,
            max_output_tokens=4096,
            native_tools=native_tools,
        )

        # Verify run_openai_native_two_phase_flow was called
        assert mock_flow.called
        call_kwargs = mock_flow.call_args[1]

        # Check dice_roll_tools parameter
        dice_roll_tools = call_kwargs.get("dice_roll_tools", [])

        # Extract tool names
        tool_names = [
            tool["function"]["name"]
            for tool in dice_roll_tools
            if "function" in tool and "name" in tool["function"]
        ]

        # Verify faction tools are NOT present
        faction_tool_names = [
            tool["function"]["name"]
            for tool in FACTION_TOOLS
            if "function" in tool and "name" in tool["function"]
        ]
        for faction_tool in faction_tool_names:
            assert (
                faction_tool not in tool_names
            ), f"Faction tool {faction_tool} should NOT be present when enabled=False"

    @patch("mvp_site.llm_providers.cerebras_provider.run_openai_native_two_phase_flow")
    def test_cerebras_includes_faction_when_enabled(self, mock_flow):
        """Verify Cerebras includes faction tools when enabled=True."""
        prompt_contents = self._create_prompt_contents_with_faction_state(enabled=True)
        native_tools = faction_state_util.build_native_tools_for_prompt_contents(
            prompt_contents
        )

        cerebras_provider.generate_content_with_native_tools(
            prompt_contents=prompt_contents,
            model_name="qwen-3-235b-a22b-instruct-2507",
            system_instruction_text="test",
            temperature=0.7,
            max_output_tokens=4096,
            native_tools=native_tools,
        )

        assert mock_flow.called
        call_kwargs = mock_flow.call_args[1]
        dice_roll_tools = call_kwargs.get("dice_roll_tools", [])
        tool_names = [
            tool["function"]["name"]
            for tool in dice_roll_tools
            if "function" in tool and "name" in tool["function"]
        ]

        faction_tool_names = [
            tool["function"]["name"]
            for tool in FACTION_TOOLS
            if "function" in tool and "name" in tool["function"]
        ]
        for faction_tool in faction_tool_names:
            assert (
                faction_tool in tool_names
            ), f"Faction tool {faction_tool} should be present when enabled=True"
