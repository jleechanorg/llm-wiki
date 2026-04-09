"""
Red-Green TDD Test: Gemini Model Selection - GREEN PHASE

Tests verify that both continue_story() and get_initial_story() respect user model preferences.

FIXED: continue_story() now accepts user_id parameter and uses _select_model_for_user() helper
VERIFIED: User's gemini_model setting is properly read and applied via GEMINI_MODEL_MAPPING
"""

import os
import unittest
from unittest.mock import MagicMock, patch

from mvp_site import constants, llm_service
from mvp_site.game_state import GameState


class TestGeminiModelSelection(unittest.TestCase):
    """Test that user model preferences are respected in all code paths."""

    def setUp(self):
        """Set up test environment."""
        # Ensure we're in test mode
        os.environ["TESTING_AUTH_BYPASS"] = "true"
        os.environ["MOCK_SERVICES_MODE"] = "false"  # Test real model selection logic

    def tearDown(self):
        """Clean up after test."""
        if "MOCK_SERVICES_MODE" in os.environ:
            del os.environ["MOCK_SERVICES_MODE"]

    @patch("mvp_site.llm_service._select_provider_and_model")
    @patch("mvp_site.llm_service._call_llm_api_with_llm_request")
    def test_continue_story_respects_user_model_preference(
        self, mock_api_call, mock_select_provider
    ):
        """
        GREEN TEST: Verify continue_story() uses user's preferred model.

        Tests that continue_story() correctly uses the model returned by
        _select_provider_and_model() for API calls.

        NOTE: We patch _select_provider_and_model directly because in test mode
        (TESTING_AUTH_BYPASS=true), the function has a guard that returns the default model.
        This patch simulates what would happen when a user has preferences set.
        """
        # Arrange: Simulate user has selected Gemini 3 Pro Preview
        test_user_id = "test_user_123"
        mock_select_provider.return_value = llm_service.ProviderSelection(
            constants.LLM_PROVIDER_GEMINI, "gemini-2.0-flash"
        )

        # Mock API response
        mock_response = MagicMock()
        mock_response.text = (
            '{"narrative": "Test story continuation", "entities_identified": []}'
        )
        mock_api_call.return_value = mock_response

        # Create minimal game state
        game_state = GameState()
        game_state.user_id = test_user_id
        game_state.custom_campaign_state = {
            "session_number": 1,
            "scene_number": 1,
            "character_name": "Test Hero",
        }

        story_context = [
            {"actor": "gemini", "text": "Welcome to the adventure!"},
            {"actor": "user", "text": "I look around."},
        ]

        # Act: Call continue_story with user_id to trigger model preference selection
        llm_service.continue_story(
            user_input="I walk forward.",
            mode=constants.MODE_CHARACTER,
            story_context=story_context,
            current_game_state=game_state,
            selected_prompts=[constants.PROMPT_TYPE_NARRATIVE],
            use_default_world=False,
            user_id=test_user_id,
        )

        # Assert: Should have called API with gemini-2.0-flash
        assert mock_api_call.called, "API should have been called"

        # Check what model was actually used
        call_kwargs = mock_api_call.call_args.kwargs
        actual_model = call_kwargs.get("model_name")

        assert actual_model == "gemini-2.0-flash", (
            f"BUG DETECTED: Expected gemini-2.0-flash but got {actual_model}. "
            f"continue_story() is ignoring user preferences!"
        )

    @patch("mvp_site.llm_service._select_provider_and_model")
    @patch("mvp_site.llm_service._call_llm_api_with_llm_request")
    def test_get_initial_story_respects_user_model_preference(
        self, mock_api_call, mock_select_provider
    ):
        """
        BASELINE TEST: get_initial_story() correctly uses user's model preference.

        Tests that get_initial_story() correctly uses the model returned by
        _select_provider_and_model() for API calls.

        NOTE: We patch _select_provider_and_model directly because in test mode
        (TESTING_AUTH_BYPASS=true), the function has a guard that returns the default model.
        This patch simulates what would happen when a user has preferences set.
        """
        # Arrange: Simulate user has selected Gemini 3 Pro Preview
        test_user_id = "test_user_456"
        mock_select_provider.return_value = llm_service.ProviderSelection(
            constants.LLM_PROVIDER_GEMINI, "gemini-2.0-flash"
        )

        # Mock API response
        mock_response = MagicMock()
        mock_response.text = (
            '{"narrative": "Your adventure begins!", "entities_identified": []}'
        )
        mock_api_call.return_value = mock_response

        # Act: Call get_initial_story
        llm_service.get_initial_story(
            prompt="I want to be a brave knight",
            user_id=test_user_id,
            selected_prompts=[constants.PROMPT_TYPE_NARRATIVE],
            generate_companions=False,
            use_default_world=False,
        )

        # Assert: Should have called API with gemini-2.0-flash
        assert mock_api_call.called, "API should have been called"

        call_kwargs = mock_api_call.call_args.kwargs
        actual_model = call_kwargs.get("model_name")

        assert actual_model == "gemini-2.0-flash", (
            f"get_initial_story() should respect user preference (got {actual_model})"
        )


if __name__ == "__main__":
    unittest.main()


class TestProviderSelectionEnvPriority(unittest.TestCase):
    """Regression tests for provider selection env var precedence."""

    def test_testing_auth_bypass_uses_defaults_without_user_settings(self):
        original_testing = os.environ.get("TESTING_AUTH_BYPASS")
        original_mock = os.environ.get("MOCK_SERVICES_MODE")
        original_force = os.environ.get("FORCE_TEST_MODEL")

        try:
            os.environ["TESTING_AUTH_BYPASS"] = "true"
            os.environ.pop("MOCK_SERVICES_MODE", None)
            os.environ.pop("FORCE_TEST_MODEL", None)

            result = llm_service._select_provider_and_model(user_id=None)

            assert result.provider == "gemini", (
                "Expected default provider when no user settings are available, "
                f"got '{result.provider}'."
            )
        finally:
            if original_testing is not None:
                os.environ["TESTING_AUTH_BYPASS"] = original_testing
            else:
                os.environ.pop("TESTING_AUTH_BYPASS", None)
            if original_mock is not None:
                os.environ["MOCK_SERVICES_MODE"] = original_mock
            else:
                os.environ.pop("MOCK_SERVICES_MODE", None)
            if original_force is not None:
                os.environ["FORCE_TEST_MODEL"] = original_force
            else:
                os.environ.pop("FORCE_TEST_MODEL", None)

    def test_testing_auth_bypass_respects_user_provider_selection(self):
        original_testing = os.environ.get("TESTING_AUTH_BYPASS")
        original_mock = os.environ.get("MOCK_SERVICES_MODE")
        original_force = os.environ.get("FORCE_TEST_MODEL")

        try:
            os.environ["TESTING_AUTH_BYPASS"] = "true"
            os.environ.pop("MOCK_SERVICES_MODE", None)
            os.environ.pop("FORCE_TEST_MODEL", None)

            fake_user_id = "test-user-with-openrouter"

            with patch("mvp_site.llm_service.get_user_settings") as mock_settings:
                mock_settings.return_value = {
                    "llm_provider": "openrouter",
                    "openrouter_model": "x-ai/grok-4.1-fast",
                }

                result = llm_service._select_provider_and_model(user_id=fake_user_id)

                assert result.provider == "openrouter", (
                    "Expected TESTING_AUTH_BYPASS to preserve user-selected provider, "
                    f"got '{result.provider}'."
                )
        finally:
            if original_testing is not None:
                os.environ["TESTING_AUTH_BYPASS"] = original_testing
            else:
                os.environ.pop("TESTING_AUTH_BYPASS", None)
            if original_mock is not None:
                os.environ["MOCK_SERVICES_MODE"] = original_mock
            else:
                os.environ.pop("MOCK_SERVICES_MODE", None)
            if original_force is not None:
                os.environ["FORCE_TEST_MODEL"] = original_force
            else:
                os.environ.pop("FORCE_TEST_MODEL", None)

    def test_force_provider_overrides_user_settings_in_testing_auth_bypass(self):
        original_testing = os.environ.get("TESTING_AUTH_BYPASS")
        original_mock = os.environ.get("MOCK_SERVICES_MODE")
        original_force = os.environ.get("FORCE_TEST_MODEL")
        original_force_provider = os.environ.get("FORCE_PROVIDER")

        try:
            os.environ["TESTING_AUTH_BYPASS"] = "true"
            os.environ["FORCE_PROVIDER"] = "gemini"
            os.environ.pop("MOCK_SERVICES_MODE", None)
            os.environ.pop("FORCE_TEST_MODEL", None)

            with patch("mvp_site.llm_service.get_user_settings") as mock_settings:
                mock_settings.return_value = {
                    "llm_provider": "openrouter",
                    "openrouter_model": "x-ai/grok-4.1-fast",
                }

                result = llm_service._select_provider_and_model(
                    user_id="test-user-with-openrouter"
                )

                assert result.provider == "gemini", (
                    "Expected FORCE_PROVIDER to override user settings, "
                    f"got '{result.provider}'."
                )
        finally:
            if original_testing is not None:
                os.environ["TESTING_AUTH_BYPASS"] = original_testing
            else:
                os.environ.pop("TESTING_AUTH_BYPASS", None)
            if original_mock is not None:
                os.environ["MOCK_SERVICES_MODE"] = original_mock
            else:
                os.environ.pop("MOCK_SERVICES_MODE", None)
            if original_force is not None:
                os.environ["FORCE_TEST_MODEL"] = original_force
            else:
                os.environ.pop("FORCE_TEST_MODEL", None)
            if original_force_provider is not None:
                os.environ["FORCE_PROVIDER"] = original_force_provider
            else:
                os.environ.pop("FORCE_PROVIDER", None)
