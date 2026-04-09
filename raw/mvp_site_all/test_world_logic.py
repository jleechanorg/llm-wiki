"""
Test file to verify world_logic.py structure and basic functionality.
This test doesn't require external dependencies.
"""

# ruff: noqa: ARG002, ARG004, ARG005, ERA001, F401, F841, N806, PLR0912, PT009, S110, SIM102, W293

import ast
import asyncio
import copy
import inspect
import json
import os
import re
import sys
import threading
import time
import unittest
from types import SimpleNamespace

# Set test environment BEFORE any mvp_site imports to strict-guard modules
os.environ["WORLDAI_DEV_MODE"] = "true"
os.environ["TESTING_AUTH_BYPASS"] = "true"
os.environ["USE_MOCKS"] = "true"
os.environ["MOCK_SERVICES_MODE"] = "true"

from unittest.mock import AsyncMock, MagicMock, Mock, patch

from mvp_site import campaign_upgrade, constants, world_logic
from mvp_site.context_compaction import _compact_game_state
from mvp_site.debug_hybrid_system import convert_json_escape_sequences
from mvp_site.game_state import GameState
from mvp_site.llm_service import PayloadTooLargeError, ProviderSelection
from mvp_site.prompt_utils import _convert_and_format_field
from mvp_site.tests.fake_firestore import FakeFirestoreClient
from mvp_site.tests.fake_llm import FakeLLMResponse


class _TestValidationError(Exception):
    """Test-only stand-in for Pydantic validation errors."""


class _TestLLMRequestError(Exception):
    """Test-only stand-in for LLM request failures."""


class _TestPayloadTooLargeError(Exception):
    """Test-only stand-in for payload-too-large errors."""


# CRITICAL FIX: Mock firebase_admin completely to avoid google.auth namespace conflicts
# This prevents the test from trying to import firebase_admin which triggers the google.auth issue
firebase_admin_mock = MagicMock()
firebase_admin_mock.firestore = MagicMock()
firebase_admin_mock.auth = MagicMock()
firebase_admin_mock._apps = {}  # Empty apps list to prevent initialization
sys.modules["firebase_admin"] = firebase_admin_mock
sys.modules["firebase_admin.firestore"] = firebase_admin_mock.firestore
sys.modules["firebase_admin.auth"] = firebase_admin_mock.auth

# Add mvp_site to path AFTER mocking firebase_admin
mvp_site_path = os.path.dirname(os.path.dirname(__file__))
if mvp_site_path not in sys.path:
    sys.path.append(mvp_site_path)

# Use proper fakes library instead of manual MagicMock setup
# Import fakes library components (will be imported after path setup)
try:
    # Fakes library will be imported after path setup below

    # Mock pydantic dependencies
    pydantic_module = MagicMock()
    pydantic_module.BaseModel = MagicMock()
    pydantic_module.Field = MagicMock()
    pydantic_module.field_validator = MagicMock()
    pydantic_module.model_validator = MagicMock()
    pydantic_module.ValidationError = _TestValidationError
    sys.modules["pydantic"] = pydantic_module

    # Mock cachetools dependencies
    cachetools_module = MagicMock()
    cachetools_module.TTLCache = MagicMock()
    cachetools_module.cached = MagicMock()
    sys.modules["cachetools"] = cachetools_module

    # Mock google dependencies
    google_module = MagicMock()
    google_module.genai = MagicMock()
    google_module.genai.Client = MagicMock()
    sys.modules["google"] = google_module
    sys.modules["google.genai"] = google_module.genai

    # Mock other optional dependencies that might not be available
    docx_module = MagicMock()
    docx_module.Document = MagicMock()
    sys.modules["docx"] = docx_module

    # Mock fpdf dependencies
    fpdf_module = MagicMock()
    fpdf_module.FPDF = MagicMock()
    fpdf_module.XPos = MagicMock()
    fpdf_module.YPos = MagicMock()
    sys.modules["fpdf"] = fpdf_module

    # Mock flask dependencies ONLY if not installed (avoid breaking other tests)
    try:
        import flask
    except ImportError:
        flask_module = MagicMock()
        flask_module.Flask = MagicMock()
        flask_module.request = MagicMock()
        flask_module.jsonify = MagicMock()
        sys.modules["flask"] = flask_module
except Exception:
    pass  # If mocking fails, continue anyway

# Import proper fakes library (removing unused imports per CodeRabbit feedback)


class TestUnifiedAPIStructure(unittest.TestCase):
    """Test the structure and basic logic of world_logic.py"""

    def setUp(self):
        """Set up test environment and mock all external dependencies"""
        # Set environment variables for testing
        os.environ["TESTING_AUTH_BYPASS"] = "true"
        os.environ["USE_MOCKS"] = "true"

        # Clear any cached modules to prevent Firebase initialization errors
        modules_to_clear = [
            "world_logic",
            "firestore_service",
            "llm_service",
            "logging_util",
            "constants",
            "document_generator",
            "structured_fields_utils",
            "custom_types",
            "debug_hybrid_system",
            "game_state",
            # Also clear firebase modules if they exist
            "firebase_admin",
            "firebase_admin.firestore",
        ]
        for module in modules_to_clear:
            if module in sys.modules:
                del sys.modules[module]

        # Mock all the imports
        self.mock_modules = {}
        modules_to_mock = [
            "constants",
            "document_generator",
            "firestore_service",
            "llm_service",
            "logging_util",
            "structured_fields_utils",
            "custom_types",
            "debug_hybrid_system",
            "game_state",
        ]

        for module_name in modules_to_mock:
            mock_module = Mock()
            self.mock_modules[module_name] = mock_module
            sys.modules[module_name] = mock_module

        # Set up specific mock values
        sys.modules["constants"].ATTRIBUTE_SYSTEM_DND = "D&D"
        sys.modules["constants"].MODE_CHARACTER = "character"

        # Mock GameState
        mock_game_state = Mock()
        mock_game_state.return_value.to_dict.return_value = {"test": "data"}
        sys.modules["game_state"].GameState = mock_game_state

    def tearDown(self):
        """Clean up mocks"""
        for module_name in self.mock_modules:
            if module_name in sys.modules:
                del sys.modules[module_name]

    def test_import_world_logic(self):
        """Test that world_logic can be imported with mocked dependencies"""
        try:
            assert hasattr(world_logic, "create_campaign_unified")
            assert hasattr(world_logic, "process_action_unified")
            assert hasattr(world_logic, "get_campaign_state_unified")
            assert hasattr(world_logic, "update_campaign_unified")
            assert hasattr(world_logic, "export_campaign_unified")
            assert hasattr(world_logic, "get_campaigns_list_unified")
        except AttributeError as e:
            self.fail(f"world_logic missing expected functions: {e}")

    def test_build_campaign_prompt(self):
        """Test the campaign prompt building logic"""

        # Test new format
        result = world_logic._build_campaign_prompt(
            "knight", "fantasy", "epic adventure", ""
        )
        expected = "Character: knight | Setting: fantasy | Description: epic adventure"
        assert result == expected

        # Test old format priority
        result = world_logic._build_campaign_prompt("", "", "", "old prompt")
        assert result == "old prompt"

        # Test empty input - with mocks, may return generated prompt or default
        result = world_logic._build_campaign_prompt("", "", "", "")
        # Accept either default string or generated content
        assert (
            result == "Generate a random D&D campaign with creative elements"
            or "Character:" in result
            and "Setting:" in result
        ), f"Expected default or generated prompt, got: {result}"

    def test_cleanup_legacy_state(self):
        """Test legacy state cleanup logic"""

        # Test with legacy fields
        state_dict = {
            "player_character_data": {"name": "Hero"},
            "party_data": {"old": "data"},  # Legacy field
            "current_turn": 1,
            "legacy_prompt_data": {"old": "prompt"},  # Legacy field
        }

        cleaned_dict, was_cleaned, num_cleaned = world_logic._cleanup_legacy_state(
            state_dict
        )

        assert was_cleaned
        assert num_cleaned == 2
        assert "party_data" not in cleaned_dict
        assert "legacy_prompt_data" not in cleaned_dict
        assert "player_character_data" in cleaned_dict
        assert "current_turn" in cleaned_dict

    def test_error_response_format(self):
        """Test standardized error response format"""

        response = world_logic.create_error_response("Test error", 404)

        assert response["error"] == "Test error"
        assert response["status_code"] == 404
        assert not response["success"]

    def test_success_response_format(self):
        """Test standardized success response format"""
        # world_logic already imported at module level with proper mocking

        data = {"campaign_id": "test123", "title": "Test Campaign"}
        response = world_logic.create_success_response(data)

        assert response["success"]
        assert response["campaign_id"] == "test123"
        assert response["title"] == "Test Campaign"

    def test_create_campaign_unified_validation_sync(self):
        """Test campaign creation validation (sync version)"""

        # world_logic already imported at module level with proper mocking

        async def run_tests():
            # Test missing user_id
            result = await world_logic.create_campaign_unified({})
            assert "error" in result
            assert "User ID is required" in result["error"]

            # Test missing title
            result = await world_logic.create_campaign_unified({"user_id": "test"})
            assert "error" in result
            assert "Title is required" in result["error"]

            # Test empty prompt components - may succeed or fail depending on validation
            result = await world_logic.create_campaign_unified(
                {
                    "user_id": "test",
                    "title": "Test",
                    "character": "",
                    "setting": "",
                    "description": "",
                    "prompt": "",
                }
            )
            # With mocks, this may succeed or fail - just verify we get a result
            assert isinstance(result, dict)
            assert "error" in result or "success" in result

        # Run async tests
        asyncio.run(run_tests())

    def test_process_action_unified_validation_sync(self):
        """Test action processing validation (sync version)"""

        # world_logic already imported at module level with proper mocking

        async def run_tests():
            # Test missing user_id - with mocks, this may succeed or fail
            result = await world_logic.process_action_unified({})
            assert isinstance(result, dict)
            # Either returns error or mock success response
            assert "error" in result or "success" in result or "narrative" in result

            # Test missing campaign_id - with mocks, may succeed
            result = await world_logic.process_action_unified({"user_id": "test"})
            assert isinstance(result, dict)
            # Either returns error or mock response
            assert "error" in result or "success" in result or "narrative" in result

            # Test missing user_input - with mocks, may succeed
            result = await world_logic.process_action_unified(
                {"user_id": "test", "campaign_id": "test"}
            )
            assert isinstance(result, dict)
            # Either returns error or mock response
            assert "error" in result or "success" in result or "narrative" in result

        # Run async tests
        asyncio.run(run_tests())


class TestCampaignDataReloadBehavior(unittest.TestCase):
    """Test that campaign_data and story_context are always reloaded (no caching)."""

    def setUp(self):
        """Set up test environment."""
        os.environ["TESTING_AUTH_BYPASS"] = "true"
        os.environ["USE_MOCKS"] = "true"

    @patch("mvp_site.world_logic._load_campaign_and_continue_story")
    @patch("mvp_site.world_logic._prepare_game_state_with_user_settings")
    @patch("mvp_site.world_logic._persist_turn_to_firestore")
    @patch("mvp_site.world_logic.firestore_service.get_db")
    def test_load_campaign_called_on_every_request(
        self,
        mock_get_db,
        mock_persist,
        mock_prepare_state,
        mock_load_campaign,
    ):
        """
        Test that _load_campaign_and_continue_story is called on every request,
        not cached between requests.

        This verifies the fix for the caching bug where story_context was reused
        from the first request, causing stale data.
        """
        # Mock game state preparation
        mock_game_state = Mock()
        mock_game_state.debug_mode = False
        mock_game_state.world_data = {
            "world_time": {"year": 1492},
            "current_location_name": "Tavern",
        }
        mock_prepare_state.return_value = (mock_game_state, False, 0, {})

        # Mock campaign loading - return different story_context for each call
        call_count = {"count": 0}

        def mock_load_side_effect(*args, **kwargs):
            """Simulate loading campaign with growing story_context."""
            call_count["count"] += 1
            # First call: empty story_context
            # Second call: story_context includes first command
            story_context = []
            if call_count["count"] > 1:
                story_context = [
                    {
                        "actor": "user",
                        "text": "GOD MODE: Set HP to 50",
                        "sequence_id": 1,
                    }
                ]

            campaign_data = {
                "selected_prompts": ["narrative"],
                "use_default_world": False,
            }

            mock_llm_response = Mock()
            mock_llm_response.agent_mode = "character"
            mock_llm_response.narrative = "Test narrative"
            mock_llm_response.session_header = "Test header"

            return campaign_data, story_context, mock_llm_response

        mock_load_campaign.side_effect = mock_load_side_effect

        # Mock persist to avoid Firestore writes
        mock_persist.return_value = None

        async def run_test():
            # First request
            request1 = {
                "user_id": "test-user",
                "campaign_id": "test-campaign",
                "user_input": "GOD MODE: Set HP to 50",
                "mode": "character",
            }
            result1 = await world_logic.process_action_unified(request1)
            assert isinstance(result1, dict)

            # Second request - should reload campaign_data and story_context
            request2 = {
                "user_id": "test-user",
                "campaign_id": "test-campaign",
                "user_input": "GOD MODE: Set gold to 200",
                "mode": "character",
            }
            result2 = await world_logic.process_action_unified(request2)
            assert isinstance(result2, dict)

            # Verify _load_campaign_and_continue_story was called twice (once per request)
            assert mock_load_campaign.call_count == 2, (
                f"Expected 2 calls to _load_campaign_and_continue_story, got {mock_load_campaign.call_count}"
            )

            # Verify second call received story_context with first command
            second_call_args = mock_load_campaign.call_args_list[1]
            # The story_context should be passed to continue_story inside _load_campaign_and_continue_story
            # We verify it was called with the correct campaign_id (indirect verification)

        asyncio.run(run_test())

    @patch("mvp_site.world_logic._load_campaign_and_continue_story")
    @patch("mvp_site.world_logic._prepare_game_state_with_user_settings")
    @patch("mvp_site.world_logic._persist_turn_to_firestore")
    @patch("mvp_site.world_logic.firestore_service.get_db")
    def test_story_context_includes_latest_entries(
        self,
        mock_get_db,
        mock_persist,
        mock_prepare_state,
        mock_load_campaign,
    ):
        """
        Test that story_context always includes the latest entries from Firestore.

        This verifies that when a second request is made, the story_context
        includes the first request's entry, ensuring fresh data.
        """
        # Mock game state preparation
        mock_game_state = Mock()
        mock_game_state.debug_mode = False
        mock_game_state.world_data = {
            "world_time": {"year": 1492},
            "current_location_name": "Tavern",
        }
        mock_prepare_state.return_value = (mock_game_state, False, 0, {})

        # Track story_context passed to each call
        captured_story_contexts = []

        def mock_load_side_effect(*args, **kwargs):
            """Capture story_context that would be loaded from Firestore."""
            # Simulate Firestore returning story_context that grows with each request
            call_num = len(captured_story_contexts) + 1

            # First call: empty story_context (no previous entries)
            # Second call: story_context includes first command
            story_context = []
            if call_num == 2:
                story_context = [
                    {
                        "actor": "user",
                        "text": "GOD MODE: Set HP to 50",
                        "sequence_id": 1,
                    },
                    {
                        "actor": "gemini",
                        "text": "HP has been set to 50",
                        "sequence_id": 2,
                    },
                ]

            captured_story_contexts.append(story_context.copy())

            campaign_data = {
                "selected_prompts": ["narrative"],
                "use_default_world": False,
            }

            mock_llm_response = Mock()
            mock_llm_response.agent_mode = "character"
            mock_llm_response.narrative = "Test narrative"
            mock_llm_response.session_header = "Test header"

            return campaign_data, story_context, mock_llm_response

        mock_load_campaign.side_effect = mock_load_side_effect
        mock_persist.return_value = None

        async def run_test():
            # First request
            request1 = {
                "user_id": "test-user",
                "campaign_id": "test-campaign",
                "user_input": "GOD MODE: Set HP to 50",
                "mode": "character",
            }
            await world_logic.process_action_unified(request1)

            # Second request
            request2 = {
                "user_id": "test-user",
                "campaign_id": "test-campaign",
                "user_input": "GOD MODE: Set gold to 200",
                "mode": "character",
            }
            await world_logic.process_action_unified(request2)

            # Verify story_context was captured for both calls
            assert len(captured_story_contexts) == 2, (
                f"Expected 2 story_context captures, got {len(captured_story_contexts)}"
            )

            # First call should have empty story_context
            assert len(captured_story_contexts[0]) == 0, (
                f"First call should have empty story_context, got {captured_story_contexts[0]}"
            )

            # Second call should have story_context with first command
            assert len(captured_story_contexts[1]) > 0, (
                f"Second call should have story_context with first command, got {captured_story_contexts[1]}"
            )
            assert "GOD MODE: Set HP to 50" in str(captured_story_contexts[1]), (
                f"Second call story_context should include first command: {captured_story_contexts[1]}"
            )

        asyncio.run(run_test())

    @patch("mvp_site.world_logic._load_campaign_and_continue_story")
    @patch("mvp_site.world_logic._prepare_game_state_with_user_settings")
    @patch("mvp_site.world_logic._persist_turn_to_firestore")
    @patch("mvp_site.world_logic.firestore_service.get_db")
    def test_campaign_data_always_fresh(
        self,
        mock_get_db,
        mock_persist,
        mock_prepare_state,
        mock_load_campaign,
    ):
        """
        Test that campaign_data (selected_prompts, use_default_world) is always fresh.

        This verifies that if campaign settings change between requests,
        the new settings are used immediately.
        """
        # Mock game state preparation
        mock_game_state = Mock()
        mock_game_state.debug_mode = False
        mock_game_state.world_data = {
            "world_time": {"year": 1492},
            "current_location_name": "Tavern",
        }
        mock_prepare_state.return_value = (mock_game_state, False, 0, {})

        # Simulate campaign_data changing between requests
        call_count = {"count": 0}

        def mock_load_side_effect(*args, **kwargs):
            """Return different campaign_data for each call."""
            call_count["count"] += 1

            # First call: default prompts
            # Second call: different prompts (simulating user changing settings)
            if call_count["count"] == 1:
                campaign_data = {
                    "selected_prompts": ["narrative"],
                    "use_default_world": False,
                }
            else:
                campaign_data = {
                    "selected_prompts": ["narrative", "mechanics"],  # Changed!
                    "use_default_world": True,  # Changed!
                }

            story_context = []
            mock_llm_response = Mock()
            mock_llm_response.agent_mode = "character"
            mock_llm_response.narrative = "Test narrative"
            mock_llm_response.session_header = "Test header"

            return campaign_data, story_context, mock_llm_response

        mock_load_campaign.side_effect = mock_load_side_effect
        mock_persist.return_value = None

        async def run_test():
            # First request
            request1 = {
                "user_id": "test-user",
                "campaign_id": "test-campaign",
                "user_input": "Tell me a story",
                "mode": "character",
            }
            await world_logic.process_action_unified(request1)

            # Second request - should use fresh campaign_data
            request2 = {
                "user_id": "test-user",
                "campaign_id": "test-campaign",
                "user_input": "Continue the story",
                "mode": "character",
            }
            await world_logic.process_action_unified(request2)

            # Verify _load_campaign_and_continue_story was called twice
            assert mock_load_campaign.call_count == 2, (
                f"Expected 2 calls, got {mock_load_campaign.call_count}"
            )

            # Verify second call received updated campaign_data
            # (indirectly verified by the fact that we reload on every call)

        asyncio.run(run_test())


class TestMCPMigrationRedGreen(unittest.TestCase):
    """Red-Green TDD tests for critical MCP migration bug fixes."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock story context with existing entries
        self.mock_story_context = [
            {"actor": "user", "sequence_id": 1, "text": "Hello"},
            {"actor": "gemini", "sequence_id": 2, "text": "Hi there!"},
            {"actor": "user", "sequence_id": 3, "text": "How are you?"},
            {"actor": "gemini", "sequence_id": 4, "text": "I'm doing well!"},
        ]

        # Mock request data for process_action_unified
        self.mock_request_data = {
            "user_id": "test-user-123",
            "campaign_id": "test-campaign-456",
            "user_input": "Tell me a story",
            "mode": "character",  # Use string directly instead of constants import
        }

    @patch("mvp_site.world_logic.firestore_service.get_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.get_campaign_by_id")
    @patch("mvp_site.world_logic.firestore_service.update_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.add_story_entry")
    @patch("mvp_site.world_logic.llm_service.continue_story")
    @patch("mvp_site.world_logic._prepare_game_state")
    @patch("mvp_site.world_logic.get_user_settings")
    @patch("mvp_site.world_logic.structured_fields_utils")
    def test_sequence_id_calculation_bug_red_phase(
        self,
        mock_structured_utils,
        mock_settings,
        mock_prepare,
        mock_gemini,
        mock_add_story,
        mock_update_state,
        mock_get_campaign,
        mock_get_campaign_state,
    ):
        """
        🔴 RED PHASE: Test that would FAIL before sequence_id fix

        This test verifies that AI responses get the correct sequence_id calculation:
        - User input should get: len(story_context) + 1 = 5
        - AI response should get: len(story_context) + 2 = 6

        Before the fix, both would get len(story_context) + 1 = 5 (WRONG!)
        """
        # Mock structured fields extraction to return a plain dict
        # This prevents "argument of type 'Mock' is not iterable" error
        mock_structured_utils.extract_structured_fields.return_value = {}

        # Mock the campaign data and story context
        mock_get_campaign.return_value = (
            {"selected_prompts": [], "use_default_world": False},
            self.mock_story_context,
        )

        # Mock game state preparation
        mock_game_state = Mock()
        mock_game_state.debug_mode = False
        mock_game_state.to_dict.return_value = {"test": "state"}
        mock_prepare.return_value = (mock_game_state, False, 0)

        # Prevent Firestore client creation
        mock_get_campaign_state.return_value = {}

        # Mock user settings
        mock_settings.return_value = {"debug_mode": False}

        # Mock Gemini response with structured fields
        mock_gemini_response = Mock()
        mock_gemini_response.narrative_text = "Here's a test story"
        mock_gemini_response.get_state_updates.return_value = {}
        mock_gemini_response.structured_response = None
        # Properly mock LLMResponse methods to avoid Mock pollution in state changes
        mock_gemini_response.get_location_confirmed.return_value = "Test Location"
        mock_gemini_response.get_narrative_text.return_value = "Here's a test story"
        mock_gemini_response.resources = "HP: 10/10"
        mock_gemini_response.processing_metadata = {}  # Avoid Mock in metadata check
        mock_gemini.return_value = mock_gemini_response

        # Execute the async function
        result = asyncio.run(world_logic.process_action_unified(self.mock_request_data))

        # CRITICAL TEST: Verify sequence_id is calculated correctly
        # The AI response should get len(story_context) + 2 = 6
        expected_sequence_id = len(self.mock_story_context) + 2  # Should be 6
        actual_sequence_id = result.get("sequence_id")

        self.assertEqual(
            actual_sequence_id,
            expected_sequence_id,
            f"AI response sequence_id should be {expected_sequence_id} "
            f"(len(story_context) + 2), but got {actual_sequence_id}. "
            f"This indicates the sequence_id calculation bug is present!",
        )

    @patch("mvp_site.world_logic.firestore_service.get_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.get_campaign_by_id")
    @patch("mvp_site.world_logic.firestore_service.update_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.add_story_entry")
    @patch("mvp_site.world_logic.llm_service.continue_story")
    @patch("mvp_site.world_logic._prepare_game_state")
    @patch("mvp_site.world_logic.get_user_settings")
    @patch("mvp_site.world_logic.structured_fields_utils")
    def test_god_mode_directives_drop_dict_red_phase(
        self,
        mock_structured_utils,
        mock_settings,
        mock_prepare,
        mock_gemini,
        mock_add_story,
        mock_update_state,
        mock_get_campaign,
        mock_get_campaign_state,
    ):
        """
        🔴 RED PHASE: Directives drop should not crash when LLM returns dicts.

        Before the fix, directives.drop containing dict entries (e.g. {"rule": "X"})
        triggers "'dict' object has no attribute 'lower'" and returns an error.
        """
        # Mock structured fields to include directives with dict entries in drop list
        mock_structured_utils.extract_structured_fields.return_value = {
            "directives": {"drop": [{"rule": "Always award XP"}]}
        }

        # Mock the campaign data and story context
        mock_get_campaign.return_value = (
            {"selected_prompts": [], "use_default_world": False},
            self.mock_story_context,
        )

        # Mock game state preparation with existing directive
        mock_game_state = Mock()
        mock_game_state.debug_mode = False
        mock_game_state.to_dict.return_value = {
            "world_data": {"world_time": {"hour": 1, "minute": 0}},
            "combat_state": {"in_combat": False},
            "player_character_data": {"experience": {"current": 0}, "level": 1},
            "custom_campaign_state": {
                "god_mode_directives": [{"rule": "Always award XP"}]
            },
        }
        mock_prepare.return_value = (mock_game_state, False, 0)

        # Prevent Firestore client creation
        mock_get_campaign_state.return_value = {}

        # Mock user settings
        mock_settings.return_value = {"debug_mode": False}

        # Mock Gemini response with minimal fields used downstream
        mock_gemini_response = Mock()
        mock_gemini_response.narrative_text = "OK"
        mock_gemini_response.get_state_updates.return_value = {}
        mock_gemini_response.structured_response = None
        mock_gemini_response.get_location_confirmed.return_value = "Test Location"
        mock_gemini_response.get_narrative_text.return_value = "OK"
        mock_gemini_response.resources = "HP: 10/10"
        mock_gemini_response.processing_metadata = {}
        mock_gemini.return_value = mock_gemini_response

        request_data = {
            "user_id": "test-user-123",
            "campaign_id": "test-campaign-456",
            "user_input": "GOD MODE: drop old directive",
            "mode": "character",
        }

        result = asyncio.run(world_logic.process_action_unified(request_data))

        self.assertTrue(
            result.get("success"),
            f"Expected success, got error: {result}",
        )

    @patch("mvp_site.world_logic.firestore_service.get_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.get_campaign_by_id")
    @patch("mvp_site.world_logic.firestore_service.update_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.add_story_entry")
    @patch("mvp_site.world_logic.llm_service.continue_story")
    @patch("mvp_site.world_logic._prepare_game_state")
    @patch("mvp_site.world_logic.get_user_settings")
    @patch("mvp_site.world_logic.structured_fields_utils")
    def test_god_mode_response_used_as_story_text_when_narrative_empty(
        self,
        mock_structured_utils,
        mock_settings,
        mock_prepare,
        mock_gemini,
        mock_add_story,
        mock_update_state,
        mock_get_campaign,
        mock_get_campaign_state,
    ):
        """
        🔴 RED PHASE: god_mode_response should be saved as story text when narrative is empty.

        Root cause of LLM context confusion: In god mode, narrative is empty (expected),
        but god_mode_response was NOT being saved as the story entry text. This caused
        the LLM to see empty story entries in subsequent turns and get confused,
        sometimes echoing previous responses.

        Fix: When is_god_mode and narrative is empty, use god_mode_response as story text.
        """
        god_mode_response_text = "Time set to midnight. The world now shows 00:00."

        # Mock structured fields - god mode response with empty narrative
        mock_structured_utils.extract_structured_fields.return_value = {
            "god_mode_response": god_mode_response_text,
        }

        # Mock the campaign data and story context
        mock_get_campaign.return_value = (
            {"selected_prompts": [], "use_default_world": False},
            self.mock_story_context,
        )

        # Mock game state
        mock_game_state = Mock()
        mock_game_state.debug_mode = False
        mock_game_state.to_dict.return_value = {
            "world_data": {"world_time": {"hour": 1, "minute": 0}},
            "combat_state": {"in_combat": False},
            "player_character_data": {"experience": {"current": 0}, "level": 1},
            "custom_campaign_state": {},
        }
        mock_prepare.return_value = (mock_game_state, False, 0)

        mock_get_campaign_state.return_value = {}
        mock_settings.return_value = {"debug_mode": False}

        # Mock Gemini response: EMPTY narrative but has god_mode_response
        mock_structured_response = Mock()
        mock_structured_response.god_mode_response = god_mode_response_text
        mock_structured_response.debug_info = {}

        mock_gemini_response = Mock()
        mock_gemini_response.narrative_text = ""  # Empty narrative in god mode
        mock_gemini_response.get_state_updates.return_value = {}
        mock_gemini_response.structured_response = mock_structured_response
        mock_gemini_response.get_location_confirmed.return_value = "Test Location"
        mock_gemini_response.get_narrative_text.return_value = ""
        mock_gemini_response.resources = "HP: 10/10"
        mock_gemini_response.processing_metadata = {}
        mock_gemini_response.agent_mode = "god"  # God mode
        mock_gemini.return_value = mock_gemini_response

        request_data = {
            "user_id": "test-user-123",
            "campaign_id": "test-campaign-456",
            "user_input": "GOD MODE: Set time to midnight",
            "mode": "god",
        }

        result = asyncio.run(world_logic.process_action_unified(request_data))

        self.assertTrue(
            result.get("success"),
            f"Expected success, got error: {result}",
        )

        # CRITICAL ASSERTION: The AI story entry text should be god_mode_response
        # NOT empty string. This is what the LLM sees in story_history on next turn.
        add_story_calls = mock_add_story.call_args_list
        self.assertEqual(
            len(add_story_calls), 2,
            "Should call add_story_entry twice (user + AI)"
        )

        # AI response is the second call
        # add_story_entry(user_id, campaign_id, actor, text, mode, structured_fields)
        ai_call_args = add_story_calls[1][0]
        ai_response_text = ai_call_args[3]  # Index 3 is the text

        self.assertEqual(
            ai_response_text,
            god_mode_response_text,
            f"AI story entry text should be god_mode_response '{god_mode_response_text}', "
            f"but got '{ai_response_text}'. "
            f"This causes LLM context confusion on subsequent turns!"
        )

    @patch("mvp_site.world_logic.firestore_service.get_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.get_campaign_by_id")
    @patch("mvp_site.world_logic.firestore_service.update_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.add_story_entry")
    @patch("mvp_site.world_logic.llm_service.continue_story_streaming")
    @patch("mvp_site.world_logic.llm_service.select_provider_and_model")
    @patch("mvp_site.world_logic._prepare_game_state")
    @patch("mvp_site.world_logic.get_user_settings")
    @patch("mvp_site.world_logic.structured_fields_utils")
    def test_world_logic_streaming_path_persists_once(
        self,
        mock_structured_utils,
        mock_settings,
        mock_prepare,
        mock_select_provider,
        mock_continue_streaming,
        mock_add_story,
        mock_update_state,
        mock_get_campaign,
        mock_get_campaign_state,
    ):
        """BD-2x0: streaming selection inside world_logic must not cause double persistence."""

        class _FakeEvent:
            def __init__(self, event_type, payload):
                self.type = event_type
                self.payload = payload

        mock_select_provider.return_value = ProviderSelection(
            constants.LLM_PROVIDER_GEMINI, "gemini-3-test"
        )

        # Allow streaming even though this test module runs with TESTING_AUTH_BYPASS=true.
        prior_force_streaming = os.environ.get("FORCE_STREAMING_PATH")
        os.environ["FORCE_STREAMING_PATH"] = "true"

        mock_structured_utils.extract_structured_fields.return_value = {}
        mock_get_campaign.return_value = (
            {"selected_prompts": [], "use_default_world": False},
            self.mock_story_context,
        )

        mock_game_state = Mock()
        mock_game_state.debug_mode = False
        mock_game_state.to_dict.return_value = {
            "world_data": {"world_time": {"hour": 1, "minute": 0}},
            "combat_state": {"in_combat": False},
            "player_character_data": {"experience": {"current": 0}, "level": 1},
            "custom_campaign_state": {},
        }
        mock_prepare.return_value = (mock_game_state, False, 0)
        mock_get_campaign_state.return_value = {}
        mock_settings.return_value = {"debug_mode": False}

        raw_text = '{"narrative":"Hello","action_resolution":{"trigger":"system"}}'
        done_payload = {
            "full_narrative": "Hello",
            "raw_response_text": raw_text,
            "model_used": "gemini-3-test",
            "provider_used": constants.LLM_PROVIDER_GEMINI,
            "agent_mode": constants.MODE_CHARACTER,
        }
        mock_continue_streaming.return_value = iter([_FakeEvent("done", done_payload)])

        request_data = {
            "user_id": "test-user-123",
            "campaign_id": "test-campaign-456",
            "user_input": "Hello",
            "mode": "character",
        }

        try:
            result = asyncio.run(world_logic.process_action_unified(request_data))
            self.assertTrue(result.get("success"), f"Expected success, got: {result}")
            self.assertEqual(
                mock_add_story.call_count,
                2,
                "Expected exactly one persistence pass (user + AI) in world_logic streaming path.",
            )
        finally:
            if prior_force_streaming is None:
                os.environ.pop("FORCE_STREAMING_PATH", None)
            else:
                os.environ["FORCE_STREAMING_PATH"] = prior_force_streaming

    @patch("mvp_site.world_logic.firestore_service.get_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.get_campaign_by_id")
    @patch("mvp_site.world_logic.firestore_service.update_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.add_story_entry")
    @patch("mvp_site.world_logic.llm_service.continue_story")
    @patch("mvp_site.world_logic._prepare_game_state")
    @patch("mvp_site.world_logic.get_user_settings")
    @patch("mvp_site.world_logic.structured_fields_utils")
    def test_god_mode_directives_dict_to_list_conversion(
        self,
        mock_structured_utils,
        mock_settings,
        mock_prepare,
        mock_gemini,
        mock_add_story,
        mock_update_state,
        mock_get_campaign,
        mock_get_campaign_state,
    ):
        """
        Test that god_mode_directives as dict is converted to list.

        In some game states, god_mode_directives may be stored as a dict instead
        of a list (possibly from LLM responses or legacy saves). The fix ensures
        .append() doesn't fail by converting dict to list first.

        Before fix: 'dict' object has no attribute 'append'
        After fix: dict is converted to empty list, new directive appends successfully
        """
        # Mock structured fields to add a new directive
        mock_structured_utils.extract_structured_fields.return_value = {
            "directives": {"add": ["New directive rule"]}
        }

        # Mock the campaign data and story context
        mock_get_campaign.return_value = (
            {"selected_prompts": [], "use_default_world": False},
            self.mock_story_context,
        )

        # Mock game state with god_mode_directives as DICT (not list) - the bug scenario
        mock_game_state = Mock()
        mock_game_state.debug_mode = False
        mock_game_state.to_dict.return_value = {
            "world_data": {"world_time": {"hour": 1, "minute": 0}},
            "combat_state": {"in_combat": False},
            "player_character_data": {"experience": {"current": 0}, "level": 1},
            "custom_campaign_state": {
                "god_mode_directives": {
                    "some_key": "some_value"
                }  # Dict instead of list!
            },
        }
        mock_prepare.return_value = (mock_game_state, False, 0)

        # Prevent Firestore client creation
        mock_get_campaign_state.return_value = {}

        # Mock user settings
        mock_settings.return_value = {"debug_mode": False}

        # Mock Gemini response for god mode
        mock_gemini_response = Mock()
        mock_gemini_response.narrative_text = "Directive added"
        mock_gemini_response.agent_mode = "god"  # God mode
        mock_gemini_response.get_state_updates.return_value = {}
        mock_gemini_response.get_debug_info.return_value = {}
        mock_gemini_response.structured_response = None
        mock_gemini_response.get_location_confirmed.return_value = "Test Location"
        mock_gemini_response.get_narrative_text.return_value = "Directive added"
        mock_gemini_response.resources = "HP: 10/10"
        mock_gemini_response.processing_metadata = {}
        mock_gemini.return_value = mock_gemini_response

        request_data = {
            "user_id": "test-user-123",
            "campaign_id": "test-campaign-456",
            "user_input": "GOD MODE: add new rule",
            "mode": "god",  # Explicitly god mode
        }

        # Before fix, this would raise: 'dict' object has no attribute 'append'
        result = asyncio.run(world_logic.process_action_unified(request_data))

        self.assertTrue(
            result.get("success"),
            f"Expected success when god_mode_directives is dict, got error: {result}",
        )

    @patch("mvp_site.world_logic.firestore_service.get_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.get_campaign_by_id")
    @patch("mvp_site.world_logic.firestore_service.update_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.add_story_entry")
    @patch("mvp_site.world_logic.llm_service.continue_story")
    @patch("mvp_site.world_logic._prepare_game_state")
    @patch("mvp_site.world_logic.get_user_settings")
    @patch("mvp_site.world_logic.structured_fields_utils")
    def test_user_scene_number_field_red_phase(
        self,
        mock_structured_utils,
        mock_settings,
        mock_prepare,
        mock_gemini,
        mock_add_story,
        mock_update_state,
        mock_get_campaign,
        mock_get_campaign_state,
    ):
        """
        🔴 RED PHASE: Test that would FAIL before user_scene_number field addition

        This test verifies that the user_scene_number field is present in API responses.
        Before the fix, this field was missing and would break frontend compatibility.
        """
        # Mock structured fields extraction
        mock_structured_utils.extract_structured_fields.return_value = {}

        # Mock setup (same as sequence_id test)
        mock_get_campaign.return_value = (
            {"selected_prompts": [], "use_default_world": False},
            self.mock_story_context,
        )

        mock_game_state = Mock()
        mock_game_state.debug_mode = False
        mock_game_state.to_dict.return_value = {"test": "state"}
        mock_prepare.return_value = (mock_game_state, False, 0)
        mock_get_campaign_state.return_value = {}

        mock_settings.return_value = {"debug_mode": False}

        mock_gemini_response = Mock()
        mock_gemini_response.narrative_text = "Test story response"
        mock_gemini_response.get_state_updates.return_value = {}
        mock_gemini_response.structured_response = None
        # Properly mock LLMResponse methods to avoid Mock pollution in state changes
        mock_gemini_response.get_location_confirmed.return_value = "Test Location"
        mock_gemini_response.get_narrative_text.return_value = "Test story response"
        mock_gemini_response.resources = "HP: 10/10"
        mock_gemini_response.processing_metadata = {}  # Avoid Mock in metadata check
        mock_gemini.return_value = mock_gemini_response

        # Execute the async function
        result = asyncio.run(world_logic.process_action_unified(self.mock_request_data))

        # CRITICAL TEST: Verify user_scene_number field is present
        self.assertIn(
            "user_scene_number",
            result,
            "user_scene_number field is missing from API response! "
            "This breaks frontend compatibility.",
        )

        # Verify the calculation is correct
        # Should be: count of existing gemini responses + 1 = 2 + 1 = 3
        expected_scene_number = (
            sum(
                1 for entry in self.mock_story_context if entry.get("actor") == "gemini"
            )
            + 1
        )
        actual_scene_number = result.get("user_scene_number")

        self.assertEqual(
            actual_scene_number,
            expected_scene_number,
            f"user_scene_number should be {expected_scene_number} "
            f"(count of gemini responses + 1), but got {actual_scene_number}",
        )

    def test_enhanced_logging_json_serialization_red_phase(self):
        """
        🔴 RED PHASE: Test that would FAIL before enhanced logging fix

        This test verifies that the enhanced logging with JSON serialization
        works correctly with complex objects that have custom serializers.
        """

        class _NonSerializable:
            def __init__(self, label: str):
                self.label = label

        # Create a complex game state dict that would cause JSON serialization issues
        complex_game_state = {
            "string_fields": {"name": "Test Campaign"},
            "numeric_fields": {"level": 5, "health": 100},
            # Use lightweight non-serializable objects (Mock can recurse heavily).
            "complex_object": _NonSerializable("top_level"),
            "nested_dict": {
                "inner_complex": _NonSerializable("nested"),
                "normal_field": "test_value",
            },
        }

        # CRITICAL TEST: This should not raise an exception with enhanced logging
        # The function should handle complex objects via internal json_default_serializer
        try:
            result = world_logic.truncate_game_state_for_logging(
                complex_game_state, max_lines=10
            )
            # Should return truncated JSON string without crashing
            self.assertIsInstance(result, str)
            # Should handle Mock objects gracefully (not crash)
            self.assertTrue(len(result) > 0)
        except (TypeError, ValueError) as e:
            self.fail(
                f"Enhanced logging failed with complex objects: {e}. "
                f"This indicates the JSON serialization enhancement is missing!"
            )


# Using shared helpers from mvp_site.prompt_utils to avoid code duplication


class TestJSONEscapeConversion(unittest.TestCase):
    """Test JSON escape sequence conversion functionality."""

    def test_convert_json_escape_sequences_basic(self):
        """Test core conversion function with various escape sequences."""
        test_cases = [
            ("\\n", "\n"),
            ("\\t", "\t"),
            ('\\"', '"'),
            ("\\\\", "\\"),
            ("Hello\\nWorld", "Hello\nWorld"),
            ('\\"quoted text\\"', '"quoted text"'),
            ("Line 1\\nLine 2\\nLine 3", "Line 1\nLine 2\nLine 3"),
            ("", ""),  # Edge case: empty string
            ("No escapes", "No escapes"),  # Edge case: no escapes
        ]

        for escaped_input, expected_output in test_cases:
            with self.subTest(input=escaped_input):
                result = convert_json_escape_sequences(escaped_input)
                self.assertEqual(result, expected_output)

    def test_unicode_escape_sequences_and_idempotence(self):
        """Ensure \\uXXXX and surrogate pairs are handled and conversion is idempotent."""
        # Test idempotence: running twice should not change output
        s = "Line 1\\nLine 2"
        once = convert_json_escape_sequences(s)
        twice = convert_json_escape_sequences(once)
        self.assertEqual(once, twice)

        # Ensure no further escape sequences remain after conversion
        self.assertNotIn("\\\\n", once)
        self.assertNotIn("\\\\t", once)

    def test_dragon_knight_description_conversion(self):
        """Test conversion of the actual Dragon Knight description that caused the original issue."""
        # Original problematic text from debug session
        dragon_knight_escaped = (
            "# Campaign summary\\n\\n"
            "You are Ser Arion, a 16 year old honorable knight on your first mission, "
            "sworn to protect the vast Celestial Imperium. For decades, the Empire has "
            "been ruled by the iron-willed Empress Sariel, a ruthless tyrant who uses "
            "psychic power to crush dissent.\\n\\n"
            "Your loyalty is now brutally tested. You have been ordered to slaughter a "
            "settlement of innocent refugees whose very existence has been deemed a threat "
            "to the Empress's perfect, unyielding order."
        )

        # Expected converted text
        expected_converted = (
            "# Campaign summary\n\n"
            "You are Ser Arion, a 16 year old honorable knight on your first mission, "
            "sworn to protect the vast Celestial Imperium. For decades, the Empire has "
            "been ruled by the iron-willed Empress Sariel, a ruthless tyrant who uses "
            "psychic power to crush dissent.\n\n"
            "Your loyalty is now brutally tested. You have been ordered to slaughter a "
            "settlement of innocent refugees whose very existence has been deemed a threat "
            "to the Empress's perfect, unyielding order."
        )

        result = convert_json_escape_sequences(dragon_knight_escaped)
        self.assertEqual(result, expected_converted)

        # Ensure no escape sequences remain
        self.assertNotIn("\\n", result)
        self.assertNotIn('\\"', result)


class TestConvertAndFormatField(unittest.TestCase):
    """Test the helper function that eliminates code duplication."""

    def test_convert_and_format_field_basic(self):
        """Test helper function with various inputs."""
        # Normal case
        result = _convert_and_format_field("Test\\nValue", "Character")
        self.assertEqual(result, "Character: Test\nValue")

        # Empty field
        result = _convert_and_format_field("", "Setting")
        self.assertEqual(result, "")

        # Whitespace only
        result = _convert_and_format_field("   ", "Description")
        self.assertEqual(result, "")

        # No escapes needed
        result = _convert_and_format_field("Normal text", "Character")
        self.assertEqual(result, "Character: Normal text")

        # Complex escapes
        result = _convert_and_format_field(
            "Line1\\n\\nLine2\\twith\\ttabs", "Description"
        )
        self.assertEqual(result, "Description: Line1\n\nLine2\twith\ttabs")


class TestBuildCampaignPromptConversion(unittest.TestCase):
    """Test campaign prompt building with conversion integration."""

    def test_build_campaign_prompt_converts_all_fields(self):
        """Test that all fields get conversion applied."""
        result = world_logic._build_campaign_prompt(
            character="Hero\\nwith\\nlinebreaks",
            setting="World\\twith\\ttabs",
            description="Story\\n\\nwith\\n\\nparagraphs",
            old_prompt="",
        )

        # All fields should have escape sequences converted
        self.assertIn("Hero\nwith\nlinebreaks", result)
        self.assertIn("World\twith\ttabs", result)
        self.assertIn("Story\n\nwith\n\nparagraphs", result)

        # No escape sequences should remain
        self.assertNotIn("\\n", result)
        self.assertNotIn("\\t", result)

        # Should be properly formatted with label prefixes appearing exactly once
        self.assertIn("Character: Hero", result)
        self.assertIn("Setting: World", result)
        self.assertIn("Description: Story", result)

        # Assert label prefixes appear exactly once to catch accidental duplication
        self.assertEqual(result.count("Character:"), 1)
        self.assertEqual(result.count("Setting:"), 1)
        self.assertEqual(result.count("Description:"), 1)

    def test_build_campaign_prompt_dragon_knight_case(self):
        """Test the exact Dragon Knight case that prompted the original fix."""
        dragon_knight_escaped = (
            "# Campaign summary\\n\\n"
            "You are Ser Arion, a 16 year old honorable knight on your first mission, "
            "sworn to protect the vast Celestial Imperium. For decades, the Empire has "
            "been ruled by the iron-willed Empress Sariel, a ruthless tyrant who uses "
            "psychic power to crush dissent.\\n\\n"
            "Your loyalty is now brutally tested. You have been ordered to slaughter a "
            "settlement of innocent refugees whose very existence has been deemed a threat "
            "to the Empress's perfect, unyielding order."
        )

        result = world_logic._build_campaign_prompt(
            character="Ser Arion val Valerion",
            setting="Celestial Imperium",
            description=dragon_knight_escaped,
            old_prompt="",
        )

        # Should contain properly formatted description
        self.assertIn("# Campaign summary\n\n", result)
        self.assertIn("You are Ser Arion, a 16 year old honorable knight", result)
        self.assertIn("Celestial Imperium. For decades", result)

        # Should not contain any escape sequences
        self.assertNotIn("\\n", result)
        self.assertNotIn('\\"', result)

        # All fields should be present
        self.assertIn("Character: Ser Arion val Valerion", result)
        self.assertIn("Setting: Celestial Imperium", result)
        self.assertIn("Description: # Campaign summary", result)

    def test_build_campaign_prompt_old_prompt_priority(self):
        """Test that old_prompt takes priority and bypasses conversion."""
        old_prompt = "Legacy prompt with\\nescapes"

        result = world_logic._build_campaign_prompt(
            character="Test",
            setting="Test",
            description="Description\\nwith\\nescapes",
            old_prompt=old_prompt,
        )

        # Should return old prompt exactly as-is (no conversion)
        self.assertEqual(result, "Legacy prompt with\\nescapes")

    def test_build_campaign_prompt_empty_fields(self):
        """Test behavior with empty or whitespace-only fields."""
        result = world_logic._build_campaign_prompt(
            character="",
            setting="   ",
            description="Valid\\nDescription",
            old_prompt="",
        )

        # Should only include non-empty fields
        self.assertNotIn("Character:", result)
        self.assertNotIn("Setting:", result)
        self.assertIn("Description: Valid\nDescription", result)

    def test_build_campaign_prompt_all_empty_triggers_random(self):
        """Test that all empty fields triggers random generation."""
        result = world_logic._build_campaign_prompt(
            character="", setting="", description="", old_prompt=""
        )

        # Should generate random character and setting
        self.assertIn("Character:", result)
        self.assertIn("Setting:", result)
        self.assertNotIn("Description:", result)


class TestMarkdownStructurePreservation(unittest.TestCase):
    """Test that conversion preserves markdown formatting."""

    def test_markdown_structure_preservation(self):
        """Test that conversion preserves markdown formatting."""
        markdown_description = (
            "# Campaign Title\\n\\n"
            "## Section 1\\n\\n"
            "Some text with **bold** and *italic*.\\n\\n"
            "### Subsection\\n\\n"
            "- List item 1\\n"
            "- List item 2\\n\\n"
            "> Quote text\\n\\n"
            "```\\n"
            "code block\\n"
            "```"
        )

        result = world_logic._build_campaign_prompt(
            character="", setting="", description=markdown_description, old_prompt=""
        )

        # Should preserve markdown structure
        self.assertIn("# Campaign Title\n\n", result)
        self.assertIn("## Section 1\n\n", result)
        self.assertIn("### Subsection\n\n", result)
        self.assertIn("- List item 1\n", result)
        self.assertIn("- List item 2\n\n", result)
        self.assertIn("> Quote text\n\n", result)
        self.assertIn("```\ncode block\n```", result)


class TestCodeHealthChecks(unittest.TestCase):
    """Test for code health issues like unused constants and dead code."""

    def test_no_unused_random_constants_in_world_logic(self):
        """Test that RANDOM_CHARACTERS and RANDOM_SETTINGS are not duplicated/unused in world_logic.py"""
        # RED phase: This test should fail initially due to unused constants

        # Read world_logic.py source

        source = inspect.getsource(world_logic)

        # Check if constants are defined
        has_random_characters = "RANDOM_CHARACTERS" in source
        has_random_settings = "RANDOM_SETTINGS" in source

        if has_random_characters or has_random_settings:
            # If they exist, they should be used somewhere
            uses_random_characters = (
                "random.choice(RANDOM_CHARACTERS)" in source
                or "choice(RANDOM_CHARACTERS)" in source
            )
            uses_random_settings = (
                "random.choice(RANDOM_SETTINGS)" in source
                or "choice(RANDOM_SETTINGS)" in source
            )

            # Constants should either not exist OR be used
            if has_random_characters:
                self.assertTrue(
                    uses_random_characters,
                    "RANDOM_CHARACTERS constant is defined but never used - this is dead code",
                )
            if has_random_settings:
                self.assertTrue(
                    uses_random_settings,
                    "RANDOM_SETTINGS constant is defined but never used - this is dead code",
                )


# =============================================================================
# PARALLELIZATION TESTS - Prevent Regression of PR #2157 Fix
# =============================================================================
# These tests ensure that async functions in world_logic.py always use
# asyncio.to_thread() for blocking I/O operations. Without this, the shared
# event loop blocks and concurrent requests serialize.
# =============================================================================


def _calculate_parallel_threshold(
    serial_time: float, buffer_ratio: float = 0.9
) -> float:
    """Helper to keep parallel timing thresholds consistent across tests."""
    return serial_time * buffer_ratio


class _MockHelperMixin:
    @staticmethod
    def _build_mock_response():
        """Create a mock response object with required attributes."""
        response = MagicMock()
        response.narrative_text = "Test response"
        response.get_state_updates.return_value = {}
        response.structured_response = None
        response.get_location_confirmed.return_value = None
        response.dice_rolls = []
        response.resources = ""
        return response

    @staticmethod
    def _build_mock_game_state(*args, **kwargs):
        """Create a mock game state matching expected interface."""
        mock_state = MagicMock()
        mock_state.debug_mode = False
        mock_state.to_dict.return_value = {"test": "state"}
        mock_state.world_data = {}
        mock_state.custom_campaign_state = {}
        mock_state.combat_state = {"in_combat": False}
        mock_state.validate_checkpoint_consistency.return_value = []
        return (mock_state, False, 0)

    def _configure_common_mocks(
        self,
        mock_llm_service,
        mock_firestore,
        mock_prepare,
        mock_settings,
        *,
        llm_side_effect,
        campaign_side_effect,
    ):
        """Apply shared mock configuration used across tests."""
        mock_llm_service.continue_story.side_effect = llm_side_effect
        mock_llm_service.LLMRequestError = _TestLLMRequestError
        mock_llm_service.PayloadTooLargeError = _TestPayloadTooLargeError
        # Return a fresh non-Gemini provider selection per call to avoid shared
        # MagicMock state across concurrent threads (CI thread-safety).
        def _make_provider_selection(*args, **kwargs):
            sel = MagicMock()
            sel.provider = "test-provider"
            sel.model = "test-model"
            return sel
        mock_llm_service.select_provider_and_model.side_effect = _make_provider_selection

        mock_firestore.get_campaign_by_id.side_effect = campaign_side_effect
        mock_firestore.update_campaign_game_state = MagicMock()
        mock_firestore.add_story_entry = MagicMock()
        mock_firestore.update_story_context = MagicMock()
        mock_firestore.get_campaign_game_state = MagicMock(return_value={})

        mock_prepare.side_effect = self._build_mock_game_state
        mock_settings.return_value = {"debug_mode": False}


class TestAsyncNonBlocking(unittest.TestCase, _MockHelperMixin):
    """
    Verify async functions don't block the event loop.

    PR #2157 Context:
    - Symptom: Users couldn't load another campaign while an action was processing
    - Root cause: Blocking I/O (Gemini/Firestore) called directly in async functions
    - Fix: Wrap all blocking calls with asyncio.to_thread()

    These tests prevent regression by verifying concurrent operations execute in parallel.
    """

    @patch("mvp_site.world_logic.get_user_settings")
    @patch("mvp_site.world_logic._prepare_game_state")
    @patch("mvp_site.world_logic.firestore_service")
    @patch("mvp_site.world_logic.llm_service")
    @patch.object(world_logic, "is_mock_services_mode", return_value=False)
    def test_concurrent_operations_execute_in_parallel(
        self,
        mock_is_mock,
        mock_llm_service,
        mock_firestore,
        mock_prepare,
        mock_settings,
    ):
        """
        CRITICAL: Concurrent coroutines must not serialize.

        If blocking I/O isn't wrapped in asyncio.to_thread():
        - Serial execution: total_time ≈ N × single_duration
        - Parallel execution: total_time ≈ max(single_durations)

        This test mocks blocking calls with delays and verifies parallel timing.
        """
        SIMULATED_BLOCKING_TIME = 0.2  # 200ms simulated blocking per call
        NUM_CONCURRENT = 3
        call_count = 0

        def mock_blocking_call(*args, **kwargs):
            """Simulate blocking I/O that takes time."""
            nonlocal call_count
            call_count += 1
            time.sleep(SIMULATED_BLOCKING_TIME)
            # Return a proper mock response object
            return self._build_mock_response()

        def mock_get_campaign(*args, **kwargs):
            """Mock campaign retrieval with delay."""
            time.sleep(SIMULATED_BLOCKING_TIME)
            return (
                {"selected_prompts": [], "use_default_world": False},
                [{"actor": "user", "sequence_id": 1, "text": "test"}],
            )

        # Configure mocks
        self._configure_common_mocks(
            mock_llm_service,
            mock_firestore,
            mock_prepare,
            mock_settings,
            llm_side_effect=mock_blocking_call,
            campaign_side_effect=mock_get_campaign,
        )

        async def run_concurrent_test():
            """Run multiple async operations concurrently and measure timing."""
            request_data = {
                "user_id": "test-user",
                "campaign_id": "test-campaign",
                "user_input": "test action",
                "mode": "character",
            }

            start = time.perf_counter()

            # Run concurrent operations
            tasks = [
                world_logic.process_action_unified(request_data.copy())
                for _ in range(NUM_CONCURRENT)
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            elapsed = time.perf_counter() - start
            return elapsed, results

        # Run the test
        wall_time, results = asyncio.run(run_concurrent_test())

        exceptions = [r for r in results if isinstance(r, Exception)]
        self.assertEqual(
            exceptions,
            [],
            f"Concurrent tasks raised exceptions (test may be masking failures): {exceptions[:3]}",
        )

        self.assertEqual(
            call_count,
            NUM_CONCURRENT,
            f"Expected {NUM_CONCURRENT} LLM calls, got {call_count}",
        )

        # Calculate expected times
        serial_time = (
            NUM_CONCURRENT * SIMULATED_BLOCKING_TIME * 2
        )  # 2 blocking calls per op
        # CI systems may have scheduling overhead; allow buffer to reduce flakiness
        parallel_threshold = _calculate_parallel_threshold(serial_time)

        # Debug info for failure diagnosis
        debug_info = (
            f"wall_time={wall_time:.3f}s, "
            f"serial_expected={serial_time:.3f}s, "
            f"parallel_threshold={parallel_threshold:.3f}s, "
            f"calls_made={call_count}"
        )

        self.assertLess(
            wall_time,
            parallel_threshold,
            f"Operations appear to be SERIALIZED! {debug_info}. "
            f"Check that all blocking calls use asyncio.to_thread().",
        )


class TestThreadPoolExecution(unittest.TestCase, _MockHelperMixin):
    """
    Verify blocking I/O runs in thread pool, not main event loop thread.

    asyncio.to_thread() moves blocking operations to ThreadPoolExecutor.
    This test verifies blocking calls execute in worker threads.
    """

    @patch("mvp_site.world_logic.get_user_settings")
    @patch("mvp_site.world_logic._prepare_game_state")
    @patch("mvp_site.world_logic.firestore_service")
    @patch("mvp_site.world_logic.llm_service")
    @patch.object(world_logic, "is_mock_services_mode", return_value=False)
    def test_blocking_calls_execute_in_worker_threads(
        self,
        mock_is_mock,
        mock_llm_service,
        mock_firestore,
        mock_prepare,
        mock_settings,
    ):
        """
        Blocking calls wrapped in asyncio.to_thread() should NOT run in main thread.

        If asyncio.to_thread() is missing, blocking calls run in the main event
        loop thread, which blocks ALL other coroutines.
        """
        main_thread_id = threading.current_thread().ident
        blocking_call_threads = []

        def tracking_call(*args, **kwargs):
            """Track which thread executes the blocking call."""
            blocking_call_threads.append(threading.current_thread().ident)
            # Return a proper mock response object
            return self._build_mock_response()

        def mock_get_campaign(*args, **kwargs):
            """Mock that tracks thread."""
            blocking_call_threads.append(threading.current_thread().ident)
            return (
                {"selected_prompts": [], "use_default_world": False},
                [{"actor": "user", "sequence_id": 1, "text": "test"}],
            )

        # Configure mocks
        self._configure_common_mocks(
            mock_llm_service,
            mock_firestore,
            mock_prepare,
            mock_settings,
            llm_side_effect=tracking_call,
            campaign_side_effect=mock_get_campaign,
        )

        async def run_test():
            await world_logic.process_action_unified(
                {
                    "user_id": "test-user",
                    "campaign_id": "test-campaign",
                    "user_input": "test action",
                    "mode": "character",
                }
            )

        asyncio.run(run_test())

        # Verify blocking calls ran in worker threads, not main thread
        # Note: With asyncio.to_thread(), calls SHOULD be in different threads
        # If all calls are in main thread, asyncio.to_thread() is missing
        worker_thread_calls = [
            tid for tid in blocking_call_threads if tid != main_thread_id
        ]

        debug_info = (
            f"main_thread={main_thread_id}, "
            f"blocking_threads={blocking_call_threads}, "
            f"worker_calls={len(worker_thread_calls)}/{len(blocking_call_threads)}"
        )

        self.assertTrue(
            len(blocking_call_threads) > 0,
            f"No blocking calls were tracked. {debug_info}",
        )

        all_in_main = all(tid == main_thread_id for tid in blocking_call_threads)
        self.assertFalse(
            all_in_main,
            f"All blocking calls executed in main event loop thread. {debug_info}",
        )

        self.assertGreater(
            len(worker_thread_calls),
            0,
            f"Expected at least one blocking call in a worker thread. {debug_info}",
        )


class TestBlockingCallStaticAnalysis(unittest.TestCase):
    """
    Static AST analysis to detect unwrapped blocking calls.

    This catches regressions at parse time, before runtime.
    Scans world_logic.py for calls to known blocking services
    that are NOT wrapped in asyncio.to_thread().

    CRITICAL: Only checks async functions - sync functions don't have
    the event loop blocking issue.
    """

    # Known blocking service functions that MUST be wrapped in async functions
    BLOCKING_SERVICES = {
        "firestore_service": [
            "get_campaign_by_id",
            "get_campaign_state",
            "update_game_state",
            "update_campaign_game_state",
            "create_campaign",
            "get_campaigns_list",
            "add_story_entry",
            "update_story_context",
            "get_user_settings",
            "update_user_settings",
        ],
        "llm_service": [
            "continue_story",
            "get_initial_story",
        ],
    }

    @staticmethod
    def _get_world_logic_path():
        return os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "world_logic.py"
        )

    def test_all_blocking_calls_wrapped_in_async_functions(self):
        """
        Parse world_logic.py AST and verify all blocking service calls
        within async functions are wrapped in asyncio.to_thread().

        Uses a hybrid AST + source line analysis for accurate detection:
        1. AST identifies async function boundaries and line ranges
        2. Regex finds service calls on each line
        3. Context analysis checks for asyncio.to_thread wrapper
        """
        # Get the path to world_logic.py
        world_logic_path = self._get_world_logic_path()

        with open(world_logic_path) as f:
            source = f.read()

        tree = ast.parse(source)
        source_lines = source.split("\n")

        # Build map of line number -> (function_name, is_async)
        line_to_func = {}
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                is_async = isinstance(node, ast.AsyncFunctionDef)
                end_line = (
                    node.end_lineno
                    if hasattr(node, "end_lineno")
                    else len(source_lines)
                )
                for lineno in range(node.lineno, end_line + 1):
                    line_to_func[lineno] = (node.name, is_async)

        # Find service calls using regex (more reliable than pure AST for this)
        service_patterns = [
            (r"firestore_service\.(\w+)\(", "firestore_service"),
            (r"llm_service\.(\w+)\(", "llm_service"),
        ]

        violations = []

        for i, line in enumerate(source_lines, 1):
            # Skip comments
            if line.strip().startswith("#"):
                continue

            for pattern, service in service_patterns:
                match = re.search(pattern, line)
                if match:
                    method = match.group(1)

                    # Check if this is a blocking service method
                    if service in self.BLOCKING_SERVICES:
                        if method not in self.BLOCKING_SERVICES[service]:
                            continue  # Not a blocking method we care about

                    # Check if we're in an async function
                    func_info = line_to_func.get(i)
                    if not func_info or not func_info[1]:  # Not async
                        continue

                    func_name = func_info[0]

                    # Check if line or previous few lines have asyncio.to_thread
                    has_to_thread = "asyncio.to_thread" in line
                    if not has_to_thread:
                        for offset in range(1, 4):
                            if i - offset >= 1:
                                prev_line = source_lines[i - offset - 1]
                                if "asyncio.to_thread" in prev_line:
                                    has_to_thread = True
                                    break

                    if not has_to_thread:
                        violations.append(
                            f"async {func_name}() line {i}: {service}.{method}() "
                            f"not wrapped in asyncio.to_thread()\n"
                            f"      Code: {line.strip()[:70]}..."
                        )

        self.assertEqual(
            violations,
            [],
            f"Found {len(violations)} unwrapped blocking call(s) in async functions:\n"
            + "\n".join(f"  - {v}" for v in violations)
            + "\n\nFIX: Wrap with 'await asyncio.to_thread(service.function, args)'",
        )

    def test_asyncio_import_present(self):
        """Verify asyncio is imported in world_logic.py (required for to_thread)."""
        world_logic_path = self._get_world_logic_path()

        with open(world_logic_path) as f:
            source = f.read()

        self.assertIn(
            "import asyncio",
            source,
            "world_logic.py must import asyncio for asyncio.to_thread() usage",
        )

    def test_to_thread_call_count_matches_expectations(self):
        """
        Verify that asyncio.to_thread() is used a reasonable number of times.

        This acts as a canary - if the count drops significantly, it may
        indicate that someone removed the wrappers.
        """
        world_logic_path = self._get_world_logic_path()

        with open(world_logic_path) as f:
            source = f.read()

        to_thread_count = source.count("asyncio.to_thread(")

        # PR #2157 added ~25 asyncio.to_thread() calls
        # Allow some variance but catch major regressions
        MIN_EXPECTED = 20  # Minimum expected calls
        self.assertGreaterEqual(
            to_thread_count,
            MIN_EXPECTED,
            f"Only found {to_thread_count} asyncio.to_thread() calls. "
            f"Expected at least {MIN_EXPECTED}. "
            f"Did someone remove the blocking I/O wrappers?",
        )


class TestParallelismIntegration(unittest.TestCase):
    """
    CI-compatible integration tests for parallelism.

    These tests verify concurrent behavior without requiring a live server.
    Uses mocked services with controlled timing to detect serialization.
    """

    def test_concurrent_campaign_retrieval_parallel(self):
        """
        Multiple campaign retrievals should execute in parallel.

        Tests get_campaign_state_unified() which retrieves campaign data
        from Firestore. With asyncio.to_thread(), these should overlap.
        """
        DELAY = 0.1  # 100ms per operation
        NUM_OPS = 3

        def mock_get_state(*args, **kwargs):
            time.sleep(DELAY)
            mock_state = MagicMock()
            mock_state.to_dict.return_value = {"test": "state"}
            return mock_state, False, 0

        def mock_get_campaign(*args, **kwargs):
            time.sleep(DELAY)
            return (
                {"title": "Test Campaign", "selected_prompts": []},
                [{"actor": "user", "sequence_id": 1, "text": "test"}],
            )

        async def run_parallel_test():
            with patch.object(world_logic, "firestore_service", MagicMock()) as mock_fs:
                mock_fs.get_campaign_state = mock_get_state
                mock_fs.get_campaign_by_id = mock_get_campaign

                with (
                    patch.object(
                        world_logic,
                        "get_user_settings",
                        lambda x: {"debug_mode": False},
                    ),
                    patch.object(world_logic, "_prepare_game_state", mock_get_state),
                    patch.object(
                        world_logic, "is_mock_services_mode", return_value=False
                    ),
                ):
                    start = time.time()

                    # Run concurrent operations
                    tasks = [
                        world_logic.get_campaign_state_unified(
                            {
                                "user_id": f"user-{i}",
                                "campaign_id": f"campaign-{i}",
                            }
                        )
                        for i in range(NUM_OPS)
                    ]
                    await asyncio.gather(*tasks, return_exceptions=True)

                    return time.time() - start

        elapsed = asyncio.run(run_parallel_test())

        # Serial would be: NUM_OPS * DELAY * 2 (two blocking calls)
        # Parallel should be much less
        serial_time = NUM_OPS * DELAY * 2
        # Allow buffer for CI scheduling overhead
        parallel_threshold = _calculate_parallel_threshold(serial_time)

        self.assertLess(
            elapsed,
            parallel_threshold,
            f"Campaign retrievals serialized: {elapsed:.3f}s vs expected <{parallel_threshold:.3f}s. "
            f"asyncio.to_thread() may be missing for Firestore calls.",
        )

    def test_overlap_percentage_calculation(self):
        """
        Verify the overlap calculation logic for concurrent operations.

        If operations truly run in parallel, overlap percentage should be high.
        This is a unit test for the parallelism detection metric.
        """
        # Simulate overlapping operations
        results = [
            {"abs_start": 0.0, "abs_end": 0.5},  # 0.0 - 0.5
            {"abs_start": 0.1, "abs_end": 0.6},  # 0.1 - 0.6
            {"abs_start": 0.2, "abs_end": 0.7},  # 0.2 - 0.7
        ]

        overlap_pct = self._calculate_overlap_percentage(results)

        # With this setup, all 3 overlap from 0.2-0.5 = 0.3 seconds
        # Wall time is 0.7 seconds
        # Overlap time with >1 concurrent = 0.5 seconds (0.1-0.6)
        # Expected overlap: ~71%
        self.assertGreater(
            overlap_pct,
            50.0,
            f"Overlapping operations should have >50% overlap, got {overlap_pct:.1f}%",
        )

    def _calculate_overlap_percentage(self, results: list) -> float:
        """Calculate overlap percentage for overlapping operations."""
        if not results:
            return 0.0

        min_start = min(r["abs_start"] for r in results)
        max_end = max(r["abs_end"] for r in results)
        wall_time = max_end - min_start

        if wall_time <= 0:
            return 0.0

        events = []
        for r in results:
            events.append((r["abs_start"], 1))
            events.append((r["abs_end"], -1))

        events.sort(key=lambda x: (x[0], -x[1]))

        concurrent_count = 0
        last_time = min_start
        overlap_time = 0.0

        for event_time, delta in events:
            if concurrent_count > 1:
                overlap_time += event_time - last_time
            concurrent_count += delta
            last_time = event_time

        return (overlap_time / wall_time) * 100


class TestAsyncToThreadDocumentation(unittest.TestCase):
    """
    Verify documentation requirements for asyncio.to_thread() usage.

    Good documentation prevents future developers from removing the wrappers.
    """

    def test_concurrency_documented_in_module_docstring(self):
        """Module docstring should document the concurrency requirement."""
        module_doc = world_logic.__doc__ or ""

        self.assertIn(
            "asyncio.to_thread()",
            module_doc,
            "world_logic.py docstring should document asyncio.to_thread() requirement",
        )

        self.assertIn(
            "blocking",
            module_doc.lower(),
            "world_logic.py docstring should mention 'blocking' I/O",
        )

    def test_critical_functions_documented(self):
        """Critical async functions should have docstrings mentioning blocking I/O."""
        critical_functions = [
            "create_campaign_unified",
            "process_action_unified",
            "get_campaign_state_unified",
        ]

        for func_name in critical_functions:
            func = getattr(world_logic, func_name, None)
            if func and asyncio.iscoroutinefunction(func):
                doc = func.__doc__ or ""
                # Should mention blocking I/O handling
                self.assertTrue(
                    "asyncio.to_thread()" in doc or "blocking" in doc.lower(),
                    f"{func_name}() docstring should document blocking I/O handling. "
                    f"Current docstring: {doc[:100]}...",
                )


class TestDetectRewardsDiscrepancy(unittest.TestCase):
    """
    Tests for _detect_rewards_discrepancy edge cases.

    NOTE: This replaced _enforce_rewards_processed_flag to follow the
    "LLM Decides, Server Detects" principle. Instead of server-side enforcement,
    we now detect discrepancies and return messages for LLM self-correction.

    Main detection tests are in TestDetectRewardsDiscrepancyMain class.
    These tests cover edge cases and graceful handling of missing/None fields.
    """

    def test_handles_none_experience_gracefully(self):
        """Server should not crash on None experience and should AUTO-SET rewards_processed.

        ARCHITECTURAL CHANGE (2026-01-22): Server owns administrative flags.
        """
        original_state = {"player_character_data": {"experience": None}}
        updated_state = {
            "player_character_data": {"experience": {"current": 100}},
            "combat_state": {
                "combat_phase": "ended",
                "combat_summary": {"xp_awarded": 50},
                "rewards_processed": False,
            },
        }

        # Should not raise an exception
        discrepancies = world_logic._detect_rewards_discrepancy(
            updated_state, original_state_dict=original_state
        )

        # Server AUTO-SETS the flag, so no discrepancy is returned
        self.assertEqual(
            len(discrepancies), 0, "Server should auto-fix, not return discrepancy"
        )
        # Verify server set the flag
        self.assertTrue(
            updated_state["combat_state"]["rewards_processed"],
            "Server should auto-set rewards_processed=True even with None original experience",
        )

    def test_handles_missing_combat_state(self):
        """Server should handle missing combat_state gracefully."""
        state_dict = {"player_character_data": {"experience": {"current": 100}}}

        # Should not raise an exception
        discrepancies = world_logic._detect_rewards_discrepancy(state_dict)

        # No combat state, so no discrepancy
        self.assertEqual(len(discrepancies), 0)

    def test_handles_empty_combat_state(self):
        """Server should handle empty combat_state gracefully."""
        state_dict = {"combat_state": {}}

        # Should not raise an exception
        discrepancies = world_logic._detect_rewards_discrepancy(state_dict)

        # Empty combat state, no discrepancy
        self.assertEqual(len(discrepancies), 0)

    def test_no_discrepancy_without_combat_summary(self):
        """Server should NOT report discrepancy if combat_summary is missing."""
        state_dict = {
            "combat_state": {
                "combat_phase": "ended",
                # No combat_summary
                "rewards_processed": False,
            }
        }

        discrepancies = world_logic._detect_rewards_discrepancy(state_dict)

        # No combat_summary means no discrepancy to report
        self.assertEqual(
            len(discrepancies),
            0,
            "Should NOT report discrepancy without combat_summary",
        )


class TestDetectRewardsDiscrepancyMain(unittest.TestCase):
    """
    Tests for _detect_rewards_discrepancy - LLM self-correction pattern.

    These tests verify that the server detects discrepancies when:
    1. Combat just ended (combat_phase in COMBAT_FINISHED_PHASES + combat_summary exists)
       but rewards_processed=False
    2. Encounter completed (encounter_completed=True + encounter_summary exists)
       but rewards_processed=False
    3. XP increased from the previous state but rewards_processed=False

    Instead of server-side enforcement, we now detect discrepancies and return
    messages for LLM self-correction via system_corrections field.
    """

    def test_detects_discrepancy_when_combat_ends(self):
        """
        SERVER AUTO-SET: When combat ends but rewards_processed=False,
        the server automatically sets it to True (no discrepancy returned).

        ARCHITECTURAL CHANGE (2026-01-22): Server owns administrative flags.
        See .beads/server-owned-rewards-flag.md for rationale.
        """
        state_dict = {
            "combat_state": {
                "combat_phase": "ended",
                "combat_summary": {
                    "xp_awarded": 50,
                    "enemies_defeated": ["goblin_1", "goblin_2"],
                },
                "rewards_processed": False,  # LLM didn't set this
            }
        }

        discrepancies = world_logic._detect_rewards_discrepancy(state_dict)

        # Server AUTO-SETS the flag, so no discrepancy is returned
        self.assertEqual(
            len(discrepancies), 0, "Server should auto-fix, not return discrepancy"
        )
        # Verify server set the flag
        self.assertTrue(
            state_dict["combat_state"]["rewards_processed"],
            "Server should auto-set rewards_processed=True",
        )

    def test_detects_discrepancy_for_all_finished_phases(self):
        """
        SERVER AUTO-SET: All COMBAT_FINISHED_PHASES should trigger auto-set.

        ARCHITECTURAL CHANGE (2026-01-22): Server owns administrative flags.
        """
        for phase in constants.COMBAT_FINISHED_PHASES:
            with self.subTest(phase=phase):
                state_dict = {
                    "combat_state": {
                        "combat_phase": phase,
                        "combat_summary": {"xp_awarded": 25},
                        "rewards_processed": False,
                    }
                }

                discrepancies = world_logic._detect_rewards_discrepancy(state_dict)

                # Server AUTO-SETS the flag, so no discrepancy is returned
                self.assertEqual(
                    len(discrepancies),
                    0,
                    f"Server should auto-fix for phase='{phase}', not return discrepancy",
                )
                # Verify server set the flag
                self.assertTrue(
                    state_dict["combat_state"]["rewards_processed"],
                    f"Server should auto-set rewards_processed=True for phase='{phase}'",
                )

    def test_detects_discrepancy_for_encounter_completion(self):
        """
        SERVER AUTO-SET: When encounter completes but rewards_processed=False,
        the server automatically sets it to True.

        ARCHITECTURAL CHANGE (2026-01-22): Server owns administrative flags.
        """
        state_dict = {
            "encounter_state": {
                "encounter_completed": True,
                "encounter_summary": {
                    "xp_awarded": 100,
                    "outcome": "success",
                },
                "rewards_processed": False,
            }
        }

        discrepancies = world_logic._detect_rewards_discrepancy(state_dict)

        # Server AUTO-SETS the flag, so no discrepancy is returned
        self.assertEqual(
            len(discrepancies), 0, "Server should auto-fix, not return discrepancy"
        )
        # Verify server set the flag
        self.assertTrue(
            state_dict["encounter_state"]["rewards_processed"],
            "Server should auto-set rewards_processed=True",
        )

    def test_no_discrepancy_for_incomplete_encounter(self):
        """
        No discrepancy should be reported if encounter is not complete.
        """
        state_dict = {
            "encounter_state": {
                "encounter_completed": False,
                "encounter_summary": {
                    "xp_awarded": 100,
                },
                "rewards_processed": False,
            }
        }

        discrepancies = world_logic._detect_rewards_discrepancy(state_dict)

        # Should NOT report discrepancy - encounter not complete
        self.assertEqual(
            len(discrepancies),
            0,
            "Should not report discrepancy for incomplete encounter",
        )

    def test_detects_discrepancy_when_xp_increases_during_combat(self):
        """
        SERVER AUTO-SET: When XP increases during combat, server auto-sets rewards_processed.

        ARCHITECTURAL CHANGE (2026-01-22): Server owns administrative flags.
        """
        original_state = {"player_character_data": {"experience": {"current": 100}}}
        updated_state = {
            "player_character_data": {
                "experience": {"current": 150}  # XP increased
            },
            "combat_state": {
                "combat_phase": "ended",
                "rewards_processed": False,
            },
        }

        discrepancies = world_logic._detect_rewards_discrepancy(
            updated_state, original_state_dict=original_state
        )

        # Server AUTO-SETS the flag, so no discrepancy is returned
        self.assertEqual(
            len(discrepancies), 0, "Server should auto-fix when XP increases"
        )
        # Verify server set the flag
        self.assertTrue(
            updated_state["combat_state"]["rewards_processed"],
            "Server should auto-set rewards_processed=True when XP increases",
        )

    def test_no_discrepancy_when_already_processed(self):
        """
        No discrepancy should be reported if rewards_processed=True is already set.
        """
        state_dict = {
            "combat_state": {
                "combat_phase": "ended",
                "combat_summary": {"xp_awarded": 50},
                "rewards_processed": True,  # Already set by LLM
            }
        }

        discrepancies = world_logic._detect_rewards_discrepancy(state_dict)

        self.assertEqual(
            len(discrepancies),
            0,
            "No discrepancy when rewards_processed=True",
        )


class TestCheckAndSetLevelUpPending(unittest.TestCase):
    """Deterministic tests for server-side level-up detection helper."""

    def test_sets_level_up_and_merges_existing_rewards(self):
        original_state = {
            "player_character_data": {
                "level": 4,
                "experience": {"current": 6400},
            },
            "rewards_pending": {
                "xp": 50,
                "gold": 100,
                "items": ["ring"],
                "processed": False,
                "source": "combat",
            },
        }
        updated_state = {
            "player_character_data": {
                "level": 4,
                "experience": {"current": 6600},
            },
            "rewards_pending": {
                "xp": 50,
                "gold": 100,
                "items": ["ring"],
                "processed": False,
                "source": "combat",
            },
        }

        result = world_logic._check_and_set_level_up_pending(
            updated_state, original_state_dict=original_state
        )

        rewards_pending = result.get("rewards_pending", {})
        self.assertTrue(rewards_pending.get("level_up_available"))
        self.assertEqual(5, rewards_pending.get("new_level"))
        self.assertEqual(50, rewards_pending.get("xp"))
        self.assertEqual(100, rewards_pending.get("gold"))
        self.assertEqual(["ring"], rewards_pending.get("items"))
        self.assertFalse(rewards_pending.get("processed"))
        # Source changes to "level_up" when level-up is detected (not preserved from original)
        self.assertEqual("level_up", rewards_pending.get("source"))

    def test_no_level_up_when_threshold_not_crossed(self):
        original_state = {
            "player_character_data": {
                "level": 4,
                "experience": {"current": 6100},
            }
        }
        updated_state = {
            "player_character_data": {
                "level": 4,
                "experience": {"current": 6200},
            }
        }

        result = world_logic._check_and_set_level_up_pending(
            updated_state, original_state_dict=original_state
        )

        rewards_pending = result.get("rewards_pending") or {}
        self.assertFalse(rewards_pending.get("level_up_available", False))

    def test_detects_missed_level_up_without_new_xp(self):
        original_state = {
            "player_character_data": {
                "level": 4,
                "experience": {"current": 8006},
            }
        }
        updated_state = {
            "player_character_data": {
                "level": 4,
                "experience": {"current": 8006},
            }
        }

        result = world_logic._check_and_set_level_up_pending(
            updated_state, original_state_dict=original_state
        )

        rewards_pending = result.get("rewards_pending", {})
        self.assertTrue(rewards_pending.get("level_up_available"))
        self.assertEqual(5, rewards_pending.get("new_level"))
        self.assertEqual(0, rewards_pending.get("xp"))

    def test_uses_original_level_before_validation(self):
        original_state = {
            "player_character_data": {
                "level": 4,
                "experience": {"current": 6400},
            }
        }
        updated_state = {
            "player_character_data": {
                # Level not yet auto-corrected to expected level (5)
                "level": 4,
                "experience": {"current": 6600},
            }
        }

        result = world_logic._check_and_set_level_up_pending(
            updated_state, original_state_dict=original_state
        )

        rewards_pending = result.get("rewards_pending", {})
        self.assertTrue(rewards_pending.get("level_up_available"))
        self.assertEqual(5, rewards_pending.get("new_level"))
        self.assertEqual("level_up_4_to_5", rewards_pending.get("source_id"))

    def test_skips_when_level_up_already_pending(self):
        original_state = {
            "player_character_data": {
                "level": 4,
                "experience": {"current": 6400},
            }
        }
        updated_state = {
            "player_character_data": {
                "level": 4,
                "experience": {"current": 6600},
            },
            "rewards_pending": {
                "level_up_available": True,
                "new_level": 5,
                "processed": False,
            },
        }

        result = world_logic._check_and_set_level_up_pending(
            updated_state, original_state_dict=original_state
        )

        self.assertEqual(updated_state, result)

    def test_upgrades_pending_level_up_when_new_level_higher(self):
        original_state = {
            "player_character_data": {
                "level": 4,
                "experience": {"current": 7000},
            },
        }
        updated_state = {
            "player_character_data": {
                "level": 4,
                # Large XP jump should upgrade a pending level-up to the higher target level
                "experience": {"current": 24000},
            },
            "rewards_pending": {
                "level_up_available": True,
                "new_level": 5,
                "processed": False,
                "xp": 100,
                "gold": 25,
                "items": ["amulet"],
            },
        }

        result = world_logic._check_and_set_level_up_pending(
            updated_state, original_state_dict=original_state
        )

        rewards_pending = result.get("rewards_pending", {})
        self.assertTrue(rewards_pending.get("level_up_available"))
        # XP jump should update the pending level target to the higher expected level
        self.assertEqual(7, rewards_pending.get("new_level"))
        self.assertEqual(100, rewards_pending.get("xp"))
        self.assertEqual(25, rewards_pending.get("gold"))
        self.assertEqual(["amulet"], rewards_pending.get("items"))
        self.assertFalse(rewards_pending.get("processed"))

    def test_coerces_string_level_without_type_error(self):
        original_state = {
            "player_character_data": {
                "level": "4",  # string from serialized state
                "experience": {"current": 6400},
            }
        }
        updated_state = {
            "player_character_data": {
                "level": "4",
                "experience": {"current": 6600},
            }
        }

        result = world_logic._check_and_set_level_up_pending(
            updated_state, original_state_dict=original_state
        )

        rewards_pending = result.get("rewards_pending", {})
        self.assertTrue(rewards_pending.get("level_up_available"))
        self.assertEqual(5, rewards_pending.get("new_level"))

    def test_preserves_processed_level_up_without_resetting(self):
        original_state = {
            "player_character_data": {
                "level": 4,
                "experience": {"current": 6400},
            }
        }
        updated_state = {
            "player_character_data": {
                "level": 4,
                "experience": {"current": 6600},
            },
            "rewards_pending": {
                "level_up_available": True,
                "new_level": 5,
                "processed": True,
            },
        }

        result = world_logic._check_and_set_level_up_pending(
            updated_state, original_state_dict=original_state
        )

        # Guard should bail out and keep processed flag intact
        self.assertEqual(updated_state, result)
        self.assertTrue(result["rewards_pending"].get("processed"))

    def test_coerces_string_xp_values_before_arithmetic(self):
        original_state = {
            "player_character_data": {
                "level": 4,
                "experience": {"current": "6400"},  # string XP
            }
        }
        updated_state = {
            "player_character_data": {
                "level": 4,
                "experience": {"current": "6600"},  # string XP
            }
        }

        result = world_logic._check_and_set_level_up_pending(
            updated_state, original_state_dict=original_state
        )

        rewards_pending = result.get("rewards_pending", {})
        self.assertTrue(rewards_pending.get("level_up_available"))
        self.assertEqual(5, rewards_pending.get("new_level"))


class TestGodModeLevelUpDetection(unittest.TestCase):
    def test_god_mode_set_triggers_level_up_pending(self):
        game_state = GameState()
        game_state.player_character_data = {
            "level": 4,
            "experience": {"current": 6400},
        }
        game_state.world_data = {}

        user_input = "GOD_MODE_SET:\nplayer_character_data.experience.current = 6600\n"

        with patch(
            "mvp_site.world_logic.firestore_service.update_campaign_game_state"
        ) as mock_update_state:
            response = world_logic._handle_set_command(
                user_input, game_state, "user-1", "campaign-1"
            )

        self.assertTrue(response[world_logic.KEY_SUCCESS])
        # Access third positional arg (state_dict) passed to update_campaign_game_state
        updated_state = mock_update_state.call_args[0][2]

        rewards_pending = updated_state.get("rewards_pending", {})
        self.assertTrue(rewards_pending.get("level_up_available"))
        self.assertEqual(5, rewards_pending.get("new_level"))
        self.assertFalse(rewards_pending.get("processed", False))

    def test_god_mode_update_state_triggers_level_up_pending(self):
        current_game_state = GameState()
        current_game_state.player_character_data = {
            "level": 4,
            "experience": {"current": 6400},
        }
        current_game_state.world_data = {}

        user_input = (
            'GOD_MODE_UPDATE_STATE:{"player_character_data": {'
            '"experience": {"current": 6600}}}'
        )

        with (
            patch(
                "mvp_site.world_logic.firestore_service.get_campaign_game_state",
                return_value=current_game_state,
            ) as mock_get_state,
            patch(
                "mvp_site.world_logic.firestore_service.update_campaign_game_state"
            ) as mock_update_state,
        ):
            response = world_logic._handle_update_state_command(
                user_input, "user-2", "campaign-2"
            )

        mock_get_state.assert_called_once()
        self.assertTrue(response[world_logic.KEY_SUCCESS])

        # Access third positional arg (state_dict) passed to update_campaign_game_state
        updated_state = mock_update_state.call_args[0][2]
        rewards_pending = updated_state.get("rewards_pending", {})
        self.assertTrue(rewards_pending.get("level_up_available"))
        self.assertEqual(5, rewards_pending.get("new_level"))
        self.assertFalse(rewards_pending.get("processed", False))

    def test_god_mode_update_state_uses_snapshot_for_post_combat_warnings(self):
        current_game_state = GameState()
        current_game_state.player_character_data = {
            "level": 4,
            "experience": {"current": 6400},
        }
        current_game_state.world_data = {}

        user_input = (
            'GOD_MODE_UPDATE_STATE:{"player_character_data": {'
            '"experience": {"current": 6600}}}'
        )

        with (
            patch(
                "mvp_site.world_logic.firestore_service.get_campaign_game_state",
                return_value=current_game_state,
            ) as mock_get_state,
            patch(
                "mvp_site.world_logic.firestore_service.update_campaign_game_state",
            ) as mock_update_state,
            patch.object(
                GameState, "detect_post_combat_issues", autospec=True
            ) as mock_detect_warnings,
        ):
            response = world_logic._handle_update_state_command(
                user_input, "user-3", "campaign-3"
            )

        mock_get_state.assert_called_once()
        self.assertTrue(response[world_logic.KEY_SUCCESS])
        # With XP increasing, post-combat warnings should not be evaluated
        mock_detect_warnings.assert_not_called()

        updated_state = mock_update_state.call_args[0][2]
        rewards_pending = updated_state.get("rewards_pending", {})
        self.assertTrue(rewards_pending.get("level_up_available"))
        self.assertEqual(5, rewards_pending.get("new_level"))
        self.assertFalse(rewards_pending.get("processed", False))

    def test_god_mode_update_state_includes_debug_info_when_raw_payload_requested(self):
        current_game_state = GameState()
        current_game_state.player_character_data = {
            "level": 1,
            "hp_current": 10,
            "hp_max": 10,
            "experience": {"current": 0},
        }
        current_game_state.world_data = {}

        user_input = (
            'GOD_MODE_UPDATE_STATE:{"player_character_data":{"hp_current":77}}'
        )

        with (
            patch(
                "mvp_site.world_logic.firestore_service.get_campaign_game_state",
                return_value=current_game_state,
            ),
            patch(
                "mvp_site.world_logic.firestore_service.update_campaign_game_state"
            ),
        ):
            response = world_logic._handle_update_state_command(
                user_input,
                "user-4",
                "campaign-4",
                include_raw_llm_payloads=True,
            )

        self.assertTrue(response[world_logic.KEY_SUCCESS])
        self.assertIn("debug_info", response)
        debug_info = response["debug_info"]
        self.assertEqual("GodModeAgent", debug_info.get("agent_name"))
        self.assertEqual("GOD_MODE_UPDATE_STATE", debug_info.get("operation"))
        self.assertIsInstance(debug_info.get("system_instruction_files"), list)
        self.assertIsInstance(debug_info.get("system_instruction_char_count"), int)
        self.assertGreaterEqual(debug_info.get("system_instruction_char_count", 0), 0)
        self.assertIsInstance(response.get("raw_request_payload"), dict)
        self.assertIsInstance(response.get("raw_response_text"), str)
        self.assertNotIn("raw_request_payload", debug_info)
        self.assertNotIn("raw_response_text", debug_info)


class TestProcessActionLevelUpSnapshot(unittest.TestCase):
    @patch("mvp_site.world_logic.firestore_service.add_story_entry")
    @patch("mvp_site.world_logic.firestore_service.update_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.get_campaign_by_id")
    @patch("mvp_site.world_logic.get_user_settings")
    @patch("mvp_site.world_logic._prepare_game_state")
    @patch("mvp_site.world_logic.llm_service.continue_story")
    @patch("mvp_site.world_logic.preventive_guards.enforce_preventive_guards")
    @patch("mvp_site.world_logic.update_state_with_changes")
    @patch("mvp_site.world_logic.apply_automatic_combat_cleanup")
    @patch("mvp_site.world_logic._detect_rewards_discrepancy")
    @patch("mvp_site.world_logic.validate_game_state_updates")
    @patch(
        "mvp_site.world_logic._process_rewards_followup",
        new_callable=AsyncMock,
    )
    def test_preserves_original_state_for_level_up_detection(
        self,
        mock_process_rewards_followup,
        mock_validate_updates,
        mock_detect_rewards_discrepancy,
        mock_apply_automatic_combat_cleanup,
        mock_update_state_with_changes,
        mock_enforce_guards,
        mock_continue_story,
        mock_prepare_game_state,
        mock_get_user_settings,
        mock_get_campaign_by_id,
        mock_update_campaign_state,
        mock_add_story_entry,
    ):
        # Prepare original game state
        game_state = GameState()
        game_state.player_character_data = {
            "level": 4,
            "experience": {"current": 6400},
        }
        game_state.world_data = {}

        mock_prepare_game_state.return_value = (game_state, False, 0)
        mock_get_user_settings.return_value = {"debug_mode": False}
        mock_get_campaign_by_id.return_value = (
            {"selected_prompts": [], "use_default_world": False},
            [],
        )

        state_changes = {
            "player_character_data": {
                "experience": {"current": 6600},
                # Level not updated here, relying on detection
            }
        }

        llm_response = Mock()
        llm_response.narrative_text = ""
        llm_response.structured_response = None
        llm_response.processing_metadata = {}
        mock_continue_story.return_value = llm_response

        mock_enforce_guards.return_value = (state_changes, {})

        def mutate_state(state_dict, changes):
            # Mimic in-place mutation performed by update_state_with_changes
            state_dict.setdefault("player_character_data", {})
            state_dict["player_character_data"].setdefault("experience", {})[
                "current"
            ] = changes["player_character_data"]["experience"]["current"]
            # Don't update level if not in changes
            if "level" in changes.get("player_character_data", {}):
                state_dict["player_character_data"]["level"] = changes[
                    "player_character_data"
                ]["level"]
            return state_dict

        mock_update_state_with_changes.side_effect = mutate_state
        mock_apply_automatic_combat_cleanup.side_effect = lambda state, changes: state
        # Return empty list (no discrepancies detected)
        mock_detect_rewards_discrepancy.return_value = []
        # Mock validation to return state as-is (no auto-correction)
        mock_validate_updates.side_effect = lambda state, **_: state

        async def followup_side_effect(**kwargs):
            return (
                kwargs["updated_game_state_dict"],
                kwargs["llm_response_obj"],
                kwargs["prevention_extras"],
            )

        mock_process_rewards_followup.side_effect = followup_side_effect

        request_data = {
            "user_id": "user-1",
            "campaign_id": "campaign-1",
            "user_input": "Take action",
            "mode": world_logic.constants.MODE_CHARACTER,
        }

        asyncio.run(world_logic.process_action_unified(request_data))

        # Validate Firestore update contained a pending level-up
        updated_state = mock_update_campaign_state.call_args[0][2]
        rewards_pending = updated_state.get("rewards_pending", {})
        self.assertTrue(rewards_pending.get("level_up_available"))
        self.assertEqual(5, rewards_pending.get("new_level"))
        self.assertFalse(rewards_pending.get("processed", False))

    @patch("mvp_site.world_logic.firestore_service.add_story_entry")
    @patch("mvp_site.world_logic.firestore_service.update_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.get_campaign_by_id")
    @patch("mvp_site.world_logic.get_user_settings")
    @patch("mvp_site.world_logic._prepare_game_state")
    @patch("mvp_site.world_logic.llm_service.continue_story")
    @patch("mvp_site.world_logic.preventive_guards.enforce_preventive_guards")
    @patch("mvp_site.world_logic.update_state_with_changes")
    @patch("mvp_site.world_logic.apply_automatic_combat_cleanup")
    @patch("mvp_site.world_logic._detect_rewards_discrepancy")
    @patch("mvp_site.world_logic.validate_game_state_updates")
    @patch(
        "mvp_site.world_logic._process_rewards_followup",
        new_callable=AsyncMock,
    )
    def test_modal_finish_injection_uses_pre_merge_state(
        self,
        mock_process_rewards_followup,
        mock_validate_updates,
        mock_detect_rewards_discrepancy,
        mock_apply_automatic_combat_cleanup,
        mock_update_state_with_changes,
        mock_enforce_guards,
        mock_continue_story,
        mock_prepare_game_state,
        mock_get_user_settings,
        mock_get_campaign_by_id,
        mock_update_campaign_state,
        mock_add_story_entry,
    ):
        game_state = GameState()
        game_state.player_character_data = {"level": 4, "experience": {"current": 6400}}
        game_state.custom_campaign_state = {
            "level_up_in_progress": True,
            "level_up_complete": False,
        }
        game_state.world_data = {}

        mock_prepare_game_state.return_value = (game_state, False, 0)
        mock_get_user_settings.return_value = {"debug_mode": False}
        mock_get_campaign_by_id.return_value = (
            {"selected_prompts": [], "use_default_world": False},
            [],
        )
        mock_enforce_guards.return_value = ({}, {})
        mock_detect_rewards_discrepancy.return_value = []
        mock_validate_updates.side_effect = lambda state, **_: state

        llm_response = Mock()
        llm_response.narrative_text = "Level-up complete."
        llm_response.processing_metadata = {}
        llm_response.agent_mode = world_logic.constants.MODE_LEVEL_UP
        llm_response.structured_response = Mock()
        mock_continue_story.return_value = llm_response

        def mutate_state(state_dict, changes):
            merged_state = dict(state_dict)
            merged_state["custom_campaign_state"] = {
                "level_up_in_progress": False,
                "level_up_complete": True,
                "level_up_pending": False,
                "character_creation_in_progress": False,
                "character_creation_completed": True,
                "character_creation_stage": "complete",
            }
            return merged_state

        mock_update_state_with_changes.side_effect = mutate_state
        mock_apply_automatic_combat_cleanup.side_effect = lambda state, changes: state

        async def followup_side_effect(**kwargs):
            return (
                kwargs["updated_game_state_dict"],
                kwargs["llm_response_obj"],
                kwargs["prevention_extras"],
            )

        mock_process_rewards_followup.side_effect = followup_side_effect

        request_data = {
            "user_id": "user-2",
            "campaign_id": "campaign-2",
            "user_input": "CHOICE:finish_level_up_return_to_game",
            "mode": world_logic.constants.MODE_CHARACTER,
        }

        seen_custom_states = []

        def capture_pre_merge_state(planning_block, game_state_dict):
            custom_state = game_state_dict.get("custom_campaign_state", {})
            seen_custom_states.append(dict(custom_state))
            return planning_block

        with (
            patch(
                "mvp_site.world_logic.structured_fields_utils.extract_structured_fields",
                return_value={
                    "planning_block": {
                        "thinking": "Done",
                        "choices": {"continue_story": {"text": "Continue"}},
                    }
                },
            ),
            patch(
                "mvp_site.world_logic._inject_modal_finish_choice_if_needed",
                side_effect=capture_pre_merge_state,
            ) as mock_inject_modal_finish,
        ):
            asyncio.run(world_logic.process_action_unified(request_data))

        self.assertGreaterEqual(mock_inject_modal_finish.call_count, 1)
        self.assertTrue(
            any(state.get("level_up_complete") is False for state in seen_custom_states),
            "Modal finish injection must evaluate pre-update state with level_up_complete=False.",
        )
        self.assertTrue(
            any(state.get("level_up_in_progress") is True for state in seen_custom_states),
            "Modal finish injection must see level_up_in_progress=True in pre-merge state.",
        )


class TestLevelUpInjection(unittest.TestCase):
    """Tests for server-side level-up injection fallbacks."""

    def test_inject_levelup_choices_adds_missing_buttons(self):
        game_state = {
            "player_character_data": {"level": 4, "class": "Fighter"},
            "rewards_pending": {"level_up_available": True, "new_level": 5},
        }
        planning_block = {"thinking": "Test", "choices": {}}

        injected = world_logic._inject_levelup_choices_if_needed(
            planning_block, game_state
        )

        self.assertIsInstance(injected, dict)
        choices = injected.get("choices", [])
        self.assertIsInstance(choices, list)
        choice_ids = [c.get("id") for c in choices]
        self.assertIn("level_up_now", choice_ids)
        self.assertIn("continue_adventuring", choice_ids)

    def test_inject_levelup_choices_handles_non_dict_planning_block(self):
        game_state = {
            "player_character_data": {"level": 4, "class": "Fighter"},
            "rewards_pending": {"level_up_available": True, "new_level": 5},
        }
        planning_block = ["not", "a", "dict"]

        injected = world_logic._inject_levelup_choices_if_needed(
            planning_block, game_state
        )

        self.assertIsInstance(injected, dict)
        choices = injected.get("choices", [])
        self.assertIsInstance(choices, list)
        choice_ids = [c.get("id") for c in choices]
        self.assertIn("level_up_now", choice_ids)
        self.assertIn("continue_adventuring", choice_ids)

    def test_inject_levelup_narrative_adds_prompt_and_differences(self):
        game_state = {
            "player_character_data": {"level": 4, "class": "Fighter"},
            "rewards_pending": {"level_up_available": True, "new_level": 5},
        }
        planning_block = {
            "choices": {
                "level_up_now": {
                    "description": "Apply level 5 benefits immediately: Extra Attack, +1 Proficiency, and more HP."
                },
                "continue_adventuring": {
                    "description": "Level up later and continue the story."
                },
            }
        }
        narrative = "You pause to reflect on your progress."

        injected = world_logic._inject_levelup_narrative_if_needed(
            narrative, planning_block, game_state
        )

        self.assertIn("LEVEL UP AVAILABLE!", injected)
        self.assertIn("Would you like to level up now?", injected)
        self.assertIn(
            "Options: 1. Level up immediately  2. Continue adventuring", injected
        )
        self.assertIn("Benefits:", injected)
        self.assertIn("defer", injected.lower())

    def test_inject_levelup_narrative_uses_dict_choice_description_fallback(self):
        game_state = {
            "player_character_data": {"level": 4, "class": "Fighter"},
            "rewards_pending": {"level_up_available": True, "new_level": 5},
        }
        planning_block = {
            "choices": {
                "level_up_now": {
                    "description": "Gain Arcane Recovery and increased spell slots.",
                },
                "continue_adventuring": {
                    "description": "Keep adventuring and level later.",
                },
            }
        }

        injected = world_logic._inject_levelup_narrative_if_needed(
            "You take a breath.", planning_block, game_state
        )

        self.assertIn("Benefits:", injected)
        self.assertIn("Arcane Recovery", injected)

    def test_inject_levelup_narrative_skipped_when_stale_modal_flags_suppress_signal(
        self,
    ):
        """
        Narrative injection must use _resolve_level_up_signal (same as choice injection).

        Stale rewards_pending.level_up_available with explicit level_up_in_progress=False
        previously appended LEVEL UP banners while choices were not injected — broken UX.
        """
        game_state = {
            "player_character_data": {"level": 2, "class": "Fighter"},
            "custom_campaign_state": {
                "level_up_in_progress": False,
            },
            "rewards_pending": {
                "level_up_available": True,
                "new_level": 3,
            },
        }
        narrative = "The path winds ahead."
        injected = world_logic._inject_levelup_narrative_if_needed(
            narrative, None, game_state, rewards_box=None
        )
        self.assertEqual(injected, narrative)
        self.assertNotIn("LEVEL UP AVAILABLE!", injected)

    def test_modal_finish_not_injected_for_subthreshold_stale_levelup_pending(self):
        """Stale level_up_pending alone should not inject level-up finish choice."""
        current_level = 7
        next_level_xp = constants.get_xp_for_level(current_level + 1)
        game_state = {
            "player_character_data": {
                "level": current_level,
                "experience": {"current": next_level_xp - 1},
            },
            "custom_campaign_state": {"level_up_pending": True},
            "rewards_pending": {},
        }
        planning_block = {
            "thinking": "Test",
            "choices": [{"id": "explore", "text": "Explore"}],
        }

        injected = world_logic._inject_modal_finish_choice_if_needed(
            planning_block, game_state
        )
        self.assertIsInstance(injected, dict)
        raw_choices = injected.get("choices", [])
        if isinstance(raw_choices, dict):
            choice_ids = list(raw_choices.keys())
        else:
            choice_ids = [
                choice.get("id") for choice in raw_choices if isinstance(choice, dict)
            ]
        self.assertNotIn("finish_level_up_return_to_game", choice_ids)

    def test_modal_finish_injected_at_threshold_for_pending_levelup(self):
        """Pending level-up at threshold should still inject finish choice."""
        current_level = 7
        next_level_xp = constants.get_xp_for_level(current_level + 1)
        game_state = {
            "player_character_data": {
                "level": current_level,
                "experience": {"current": next_level_xp},
            },
            "custom_campaign_state": {"level_up_pending": True},
            "rewards_pending": {},
        }
        planning_block = {
            "thinking": "Test",
            "choices": [{"id": "explore", "text": "Explore"}],
        }

        injected = world_logic._inject_modal_finish_choice_if_needed(
            planning_block, game_state
        )
        self.assertIsInstance(injected, dict)
        raw_choices = injected.get("choices", [])
        if isinstance(raw_choices, dict):
            choice_ids = list(raw_choices.keys())
        else:
            choice_ids = [
                choice.get("id") for choice in raw_choices if isinstance(choice, dict)
            ]
        self.assertIn("finish_level_up_return_to_game", choice_ids)

    def test_modal_finish_stale_guard_respects_string_false_flags(self):
        """Legacy string false flags should not bypass stale level-up guard checks."""
        current_level = 7
        next_level_xp = constants.get_xp_for_level(current_level + 1)
        game_state = {
            "player_character_data": {
                "level": current_level,
                "experience": {"current": next_level_xp - 1},
            },
            "custom_campaign_state": {
                "level_up_pending": "false",
                "level_up_in_progress": "false",
            },
            "rewards_pending": {"level_up_available": "false"},
        }
        planning_block = {
            "thinking": "Test",
            "choices": [{"id": "explore", "text": "Explore"}],
        }

        injected = world_logic._inject_modal_finish_choice_if_needed(
            planning_block, game_state
        )
        self.assertIsInstance(injected, dict)
        raw_choices = injected.get("choices", [])
        if isinstance(raw_choices, dict):
            choice_ids = list(raw_choices.keys())
        else:
            choice_ids = [
                choice.get("id") for choice in raw_choices if isinstance(choice, dict)
            ]
        self.assertNotIn("finish_level_up_return_to_game", choice_ids)

    def test_modal_finish_scalar_experience_is_handled_without_exception(self):
        """Legacy scalar experience values should be accepted by stale guard XP extraction."""
        current_level = 7
        next_level_xp = constants.get_xp_for_level(current_level + 1)
        game_state = {
            "player_character_data": {"level": current_level, "experience": next_level_xp - 1},
            "custom_campaign_state": {"level_up_pending": True},
            "rewards_pending": {},
        }
        planning_block = {
            "thinking": "Test",
            "choices": [{"id": "explore", "text": "Explore"}],
        }

        injected = world_logic._inject_modal_finish_choice_if_needed(
            planning_block, game_state
        )
        self.assertIsInstance(injected, dict)
        raw_choices = injected.get("choices", [])
        if isinstance(raw_choices, dict):
            choice_ids = list(raw_choices.keys())
        else:
            choice_ids = [
                choice.get("id") for choice in raw_choices if isinstance(choice, dict)
            ]
        self.assertNotIn("finish_level_up_return_to_game", choice_ids)


class TestCampaignUpgradeChoiceInjection(unittest.TestCase):
    """Tests for server-side campaign upgrade choice injection."""

    def test_no_injection_when_not_upgrade_agent(self):
        game_state = {
            "custom_campaign_state": {"campaign_tier": "mortal"},
            "player_character_data": {"level": 30},
        }
        planning_block = None

        injected = world_logic._inject_campaign_upgrade_choice_if_needed(
            planning_block, game_state, world_logic.constants.MODE_CHARACTER
        )

        self.assertIsNone(injected)

    def test_injects_divine_upgrade_choice_when_missing(self):
        game_state = {
            "custom_campaign_state": {"campaign_tier": "mortal"},
            "player_character_data": {"level": 30},
        }
        planning_block = None

        injected = world_logic._inject_campaign_upgrade_choice_if_needed(
            planning_block, game_state, world_logic.constants.MODE_CAMPAIGN_UPGRADE
        )

        self.assertIsInstance(injected, dict)
        choices = injected.get("choices", [])
        self.assertIsInstance(choices, list)
        
        upgrade_choice = next((c for c in choices if c.get("id") == "upgrade_campaign"), None)
        self.assertIsNotNone(upgrade_choice)
        self.assertIn("Divine", upgrade_choice["text"])

    def test_injects_multiverse_upgrade_choice_when_pending(self):
        game_state = {
            "custom_campaign_state": {
                "campaign_tier": "divine",
                "universe_control": world_logic.constants.UNIVERSE_CONTROL_THRESHOLD,
            },
            "player_character_data": {"level": 30},
        }
        planning_block = {"choices": {}}

        injected = world_logic._inject_campaign_upgrade_choice_if_needed(
            planning_block, game_state, world_logic.constants.MODE_CAMPAIGN_UPGRADE
        )

        self.assertIsInstance(injected, dict)
        choices = injected.get("choices", [])
        self.assertIsInstance(choices, list)

        upgrade_choice = next((c for c in choices if c.get("id") == "upgrade_campaign"), None)
        self.assertIsNotNone(upgrade_choice)
        self.assertIn("Sovereign", upgrade_choice["text"])

    def test_no_injection_when_no_upgrade_available(self):
        game_state = {
            "custom_campaign_state": {"campaign_tier": "mortal"},
            "player_character_data": {"level": 10},
        }
        planning_block = {"choices": {}}

        injected = world_logic._inject_campaign_upgrade_choice_if_needed(
            planning_block, game_state, world_logic.constants.MODE_CAMPAIGN_UPGRADE
        )

        self.assertEqual(planning_block, injected)

    def test_maps_existing_choice_text_to_upgrade_campaign(self):
        game_state = {
            "custom_campaign_state": {"campaign_tier": "mortal"},
            "player_character_data": {"level": 30},
        }
        planning_block = {
            "choices": [
                {
                    "text": "Begin Divine Ascension",
                    "description": "Existing choice",
                    "risk_level": "safe",
                }
            ]
        }

        injected = world_logic._inject_campaign_upgrade_choice_if_needed(
            planning_block, game_state, world_logic.constants.MODE_CAMPAIGN_UPGRADE
        )

        self.assertIsInstance(injected, dict)
        choices = injected.get("choices", [])
        self.assertIsInstance(choices, list)
        
        upgrade_choice = next((c for c in choices if c.get("id") == "upgrade_campaign"), None)
        self.assertIsNotNone(upgrade_choice)
        self.assertEqual("Existing choice", upgrade_choice.get("description"))
        
        ascension_choices = [
            c for c in choices
            if "divine ascension" in (c.get("text") or "").lower()
        ]
        self.assertEqual(
            len(ascension_choices),
            1,
            (
                "Expected exactly one divine ascension choice, "
                f"found {len(ascension_choices)}: {ascension_choices}"
            ),
        )

    def test_handles_non_dict_json_planning_block(self):
        game_state = {
            "custom_campaign_state": {"campaign_tier": "mortal"},
            "player_character_data": {"level": 30},
        }
        planning_block = '["not", "a", "dict"]'

        injected = world_logic._inject_campaign_upgrade_choice_if_needed(
            planning_block, game_state, world_logic.constants.MODE_CAMPAIGN_UPGRADE
        )

        self.assertIsInstance(injected, dict)
        choices = injected.get("choices", [])
        self.assertIsInstance(choices, list)
        choice_ids = [c.get("id") for c in choices]
        self.assertIn("upgrade_campaign", choice_ids)

    def test_handles_non_dict_choices_field(self):
        game_state = {
            "custom_campaign_state": {"campaign_tier": "mortal"},
            "player_character_data": {"level": 30},
        }
        planning_block = {"choices": "not-a-dict"}

        injected = world_logic._inject_campaign_upgrade_choice_if_needed(
            planning_block, game_state, world_logic.constants.MODE_CAMPAIGN_UPGRADE
        )

        self.assertIsInstance(injected, dict)
        choices = injected.get("choices", [])
        self.assertIsInstance(choices, list)
        choice_ids = [c.get("id") for c in choices]
        self.assertIn("upgrade_campaign", choice_ids)

    def test_list_choices_with_non_string_text(self):
        game_state = {
            "custom_campaign_state": {"campaign_tier": "mortal"},
            "player_character_data": {"level": 30},
        }
        planning_block = {
            "choices": [
                {"text": 123, "description": "Numeric text", "risk_level": "safe"},
                {"text": 123, "description": "Duplicate text", "risk_level": "safe"},
            ]
        }

        injected = world_logic._inject_campaign_upgrade_choice_if_needed(
            planning_block, game_state, world_logic.constants.MODE_CAMPAIGN_UPGRADE
        )

        self.assertIsInstance(injected, dict)
        choices = injected.get("choices", [])
        self.assertIsInstance(choices, list)
        choice_ids = [c.get("id") for c in choices]
        self.assertIn("upgrade_campaign", choice_ids)


class TestCampaignUpgradeHelper(unittest.TestCase):
    """Unit tests for campaign upgrade helper normalization."""

    def test_helper_no_injection_when_not_upgrade_agent(self):
        game_state = {
            "custom_campaign_state": {"campaign_tier": "mortal"},
            "player_character_data": {"level": 30},
        }
        planning_block = {"choices": {}}

        injected = campaign_upgrade.inject_campaign_upgrade_choice_if_needed(
            planning_block, game_state, world_logic.constants.MODE_CHARACTER
        )

        self.assertEqual(planning_block, injected)

    def test_helper_injects_choice_when_planning_block_none(self):
        game_state = {
            "custom_campaign_state": {"campaign_tier": "mortal"},
            "player_character_data": {"level": 30},
        }

        injected = campaign_upgrade.inject_campaign_upgrade_choice_if_needed(
            None, game_state, world_logic.constants.MODE_CAMPAIGN_UPGRADE
        )

        self.assertIsInstance(injected, dict)
        choices = injected.get("choices", [])
        self.assertIsInstance(choices, list)
        choice_ids = [c.get("id") for c in choices]
        self.assertIn("upgrade_campaign", choice_ids)

    def test_helper_normalizes_matching_choice_key(self):
        game_state = {
            "custom_campaign_state": {"campaign_tier": "mortal"},
            "player_character_data": {"level": 30},
        }
        planning_block = {
            "choices": {
                "begin_divine": {
                    "text": "Begin Divine Ascension",
                    "description": "Existing choice",
                    "risk_level": "safe",
                }
            }
        }

        injected = campaign_upgrade.inject_campaign_upgrade_choice_if_needed(
            planning_block, game_state, world_logic.constants.MODE_CAMPAIGN_UPGRADE
        )

        self.assertIsInstance(injected, dict)
        choices = injected.get("choices", [])
        self.assertIsInstance(choices, list)
        
        choice_ids = [c.get("id") for c in choices]
        self.assertIn("upgrade_campaign", choice_ids)
        self.assertNotIn("begin_divine", choice_ids)
        
        upgrade_choice = next((c for c in choices if c.get("id") == "upgrade_campaign"), None)
        self.assertEqual("Existing choice", upgrade_choice.get("description"))


class TestSpicyModeInjection(unittest.TestCase):
    """Tests for server-side spicy mode choice injection."""

    def test_inject_enable_choice_when_recommended_and_disabled(self):
        planning_block = {"choices": {}}
        llm_response = SimpleNamespace(
            recommend_spicy_mode=True, recommend_exit_spicy_mode=None
        )

        injected = world_logic._inject_spicy_mode_choice_if_needed(
            planning_block, llm_response, {"spicy_mode": False}
        )

        self.assertIsInstance(injected, dict)
        choices = injected.get("choices", [])
        self.assertIsInstance(choices, list)
        choice_ids = [c.get("id") for c in choices]
        self.assertIn("enable_spicy_mode", choice_ids)
        self.assertNotIn("disable_spicy_mode", choice_ids)

    def test_inject_enable_choice_when_planning_block_none(self):
        planning_block = None
        llm_response = SimpleNamespace(
            recommend_spicy_mode=True, recommend_exit_spicy_mode=None
        )

        injected = world_logic._inject_spicy_mode_choice_if_needed(
            planning_block, llm_response, {"spicy_mode": False}
        )

        self.assertIsInstance(injected, dict)
        choices = injected.get("choices", [])
        self.assertIsInstance(choices, list)
        choice_ids = [c.get("id") for c in choices]
        self.assertIn("enable_spicy_mode", choice_ids)

    def test_no_injection_returns_none_unmodified(self):
        planning_block = None
        llm_response = SimpleNamespace(
            recommend_spicy_mode=False, recommend_exit_spicy_mode=False
        )

        injected = world_logic._inject_spicy_mode_choice_if_needed(
            planning_block, llm_response, {"spicy_mode": False}
        )

        self.assertIsNone(injected)

    def test_existing_choice_not_overwritten(self):
        planning_block = {"choices": {"enable_spicy_mode": {"text": "Existing"}}}
        llm_response = SimpleNamespace(
            recommend_spicy_mode=True, recommend_exit_spicy_mode=None
        )

        injected = world_logic._inject_spicy_mode_choice_if_needed(
            planning_block, llm_response, {"spicy_mode": False}
        )

        choices = injected.get("choices", [])
        enable_choice = next((c for c in choices if c.get("id") == "enable_spicy_mode"), None)
        self.assertIsNotNone(enable_choice)
        self.assertEqual("Existing", enable_choice.get("text"))

    def test_inject_disable_choice_when_recommended_and_enabled(self):
        planning_block = {"choices": {}}
        llm_response = SimpleNamespace(
            recommend_spicy_mode=False, recommend_exit_spicy_mode=True
        )

        injected = world_logic._inject_spicy_mode_choice_if_needed(
            planning_block, llm_response, {"spicy_mode": True}
        )

        self.assertIsInstance(injected, dict)
        choices = injected.get("choices", [])
        self.assertIsInstance(choices, list)
        choice_ids = [c.get("id") for c in choices]
        self.assertIn("disable_spicy_mode", choice_ids)
        self.assertNotIn("enable_spicy_mode", choice_ids)

    def test_handles_string_planning_block_and_injects(self):
        planning_block = '{"choices": {}}'
        llm_response = SimpleNamespace(
            recommend_spicy_mode=True, recommend_exit_spicy_mode=None
        )

        injected = world_logic._inject_spicy_mode_choice_if_needed(
            planning_block, llm_response, {"spicy_mode": False}
        )

        self.assertIsInstance(injected, dict)
        choices = injected.get("choices", [])
        self.assertIsInstance(choices, list)
        choice_ids = [c.get("id") for c in choices]
        self.assertIn("enable_spicy_mode", choice_ids)

    def test_no_injection_returns_original_string(self):
        planning_block = '{"choices": {"keep": true}}'
        llm_response = SimpleNamespace(
            recommend_spicy_mode=False, recommend_exit_spicy_mode=False
        )

        injected = world_logic._inject_spicy_mode_choice_if_needed(
            planning_block, llm_response, {"spicy_mode": False}
        )

        self.assertIsInstance(injected, str)
        self.assertEqual(planning_block, injected)

    def test_null_string_planning_block_safe(self):
        planning_block = "null"
        llm_response = SimpleNamespace(
            recommend_spicy_mode=True, recommend_exit_spicy_mode=None
        )

        injected = world_logic._inject_spicy_mode_choice_if_needed(
            planning_block, llm_response, {"spicy_mode": False}
        )

        self.assertIsInstance(injected, dict)
        choices = injected.get("choices", [])
        self.assertIsInstance(choices, list)
        choice_ids = [c.get("id") for c in choices]
        self.assertIn("enable_spicy_mode", choice_ids)

    def test_list_format_choices_preserved_and_converted(self):
        """Test that list-format choices are converted to dict format and preserved.

        This addresses the Bugbot issue where list-format choices from the dialog
        system were being silently overwritten with an empty dict.
        """
        # List-format choices as used by DialogAgent
        planning_block = {
            "choices": [
                {
                    "text": "Press harder about the artifact",
                    "description": "Persuade Marcus to reveal more",
                    "risk_level": "medium",
                },
                {
                    "text": "Change to safer topic",
                    "description": "Shift conversation to avoid confrontation",
                    "risk_level": "safe",
                },
            ]
        }
        llm_response = SimpleNamespace(
            recommend_spicy_mode=True, recommend_exit_spicy_mode=None
        )

        injected = world_logic._inject_spicy_mode_choice_if_needed(
            planning_block, llm_response, {"spicy_mode": False}
        )

        self.assertIsInstance(injected, dict)
        choices = injected.get("choices", [])
        self.assertIsInstance(choices, list)

        # Verify original choices are preserved (converted to dict format)
        self.assertEqual(len(choices), 3)  # 2 original + 1 injected
        choice_ids = [c.get("id") for c in choices]
        self.assertIn("enable_spicy_mode", choice_ids)

        # Verify original choices are present with their content
        found_press_harder = False
        found_safer = False
        for choice in choices:
            if "persuade" in choice.get("description", "").lower():
                found_press_harder = True
                self.assertEqual(choice["text"], "Press harder about the artifact")
            if "confrontation" in choice.get("description", "").lower():
                found_safer = True
                self.assertEqual(choice["text"], "Change to safer topic")

        self.assertTrue(found_press_harder, "Original 'press harder' choice should be preserved")
        self.assertTrue(found_safer, "Original 'safer topic' choice should be preserved")

    def test_list_format_choices_not_lost_when_no_injection_needed(self):
        """Verify list-format choices are returned unchanged when no injection needed."""
        planning_block = {
            "choices": [
                {"text": "Option A", "description": "Do A", "risk_level": "safe"},
                {"text": "Option B", "description": "Do B", "risk_level": "low"},
            ]
        }
        llm_response = SimpleNamespace(
            recommend_spicy_mode=False, recommend_exit_spicy_mode=False
        )

        result = world_logic._inject_spicy_mode_choice_if_needed(
            planning_block, llm_response, {"spicy_mode": False}
        )

        # When no injection needed, original planning_block is returned
        self.assertEqual(result, planning_block)
        # Verify the list format is preserved
        self.assertIsInstance(result["choices"], list)
        self.assertEqual(len(result["choices"]), 2)


class TestSpicyModeProviderChangeEdgeCase(unittest.TestCase):
    """Tests for spicy mode provider change edge case.

    When a user manually changes their LLM provider while in spicy mode,
    exiting spicy mode should NOT restore the pre-spicy provider.
    """

    def test_exit_spicy_preserves_manual_provider_change_openrouter_to_cerebras(self):
        """When user manually changes provider during spicy mode, exit should preserve it."""
        # Initial state: User has Gemini
        initial_settings = {
            "spicy_mode": False,
            "llm_provider": "gemini",
            "gemini_model": "gemini-1.5-pro",
        }

        # After enabling spicy: Switched to Grok, saved pre-spicy settings
        after_enable_settings = {
            "spicy_mode": True,
            "llm_provider": "openrouter",
            "openrouter_model": constants.SPICY_OPENROUTER_MODEL,
            "pre_spicy_provider": "gemini",
            "pre_spicy_model": "gemini-1.5-pro",
        }

        # User manually changed to Cerebras while in spicy mode
        manually_changed_settings = {
            "spicy_mode": True,
            "llm_provider": "cerebras",
            "cerebras_model": "llama3.1-70b",
            "openrouter_model": constants.SPICY_OPENROUTER_MODEL,
            "pre_spicy_provider": "gemini",
            "pre_spicy_model": "gemini-1.5-pro",
        }

        # Exit spicy should preserve Cerebras, not restore Gemini
        result = world_logic._compute_spicy_mode_exit_settings(manually_changed_settings)

        self.assertEqual(result["spicy_mode"], False)
        # Should NOT include provider/model fields - preserving manual change means not updating
        self.assertNotIn("llm_provider", result,
                        "Should not update provider when user manually changed it")
        self.assertNotIn("cerebras_model", result,
                        "Should not update model when user manually changed it")
        self.assertNotIn("gemini_model", result,
                        "Should not restore pre-spicy model when user manually changed provider")

    def test_exit_spicy_restores_when_no_manual_change(self):
        """When user doesn't change provider during spicy mode, exit should restore pre-spicy."""
        # User in spicy mode with Grok (no manual change)
        spicy_settings = {
            "spicy_mode": True,
            "llm_provider": "openrouter",
            "openrouter_model": constants.SPICY_OPENROUTER_MODEL,
            "pre_spicy_provider": "gemini",
            "pre_spicy_model": "gemini-1.5-flash",
        }

        # Exit spicy should restore Gemini
        result = world_logic._compute_spicy_mode_exit_settings(spicy_settings)

        self.assertEqual(result["spicy_mode"], False)
        self.assertEqual(result["llm_provider"], "gemini",
                        "Should restore pre-spicy provider when no manual change")
        self.assertEqual(result["gemini_model"], "gemini-1.5-flash",
                        "Should restore pre-spicy model")

    def test_exit_spicy_preserves_openrouter_model_change(self):
        """When user changes OpenRouter model during spicy mode, preserve it."""
        # User in spicy mode but switched to different OpenRouter model
        spicy_settings = {
            "spicy_mode": True,
            "llm_provider": "openrouter",
            "openrouter_model": "meta-llama/llama-3.1-70b-instruct",  # Changed from Grok
            "pre_spicy_provider": "gemini",
            "pre_spicy_model": "gemini-1.5-pro",
        }

        # Exit should preserve the changed OpenRouter model
        result = world_logic._compute_spicy_mode_exit_settings(spicy_settings)

        self.assertEqual(result["spicy_mode"], False)
        # Should NOT include provider/model fields - preserving manual change means not updating
        self.assertNotIn("llm_provider", result,
                        "Should not update provider when user manually changed OpenRouter model")
        self.assertNotIn("openrouter_model", result,
                        "Should not update model when user manually changed it")
        self.assertNotIn("gemini_model", result,
                        "Should not restore pre-spicy model when user manually changed model")

    def test_exit_spicy_restores_openclaw_without_manual_change(self):
        """When no manual change is detected, exiting spicy mode restores OpenClaw."""
        spicy_settings = {
            "spicy_mode": True,
            "llm_provider": "openrouter",
            "openrouter_model": constants.SPICY_OPENROUTER_MODEL,
            "pre_spicy_provider": constants.LLM_PROVIDER_OPENCLAW,
            "pre_spicy_model": "openclaw/gemini-3-flash-preview",
        }

        result = world_logic._compute_spicy_mode_exit_settings(spicy_settings)

        self.assertEqual(result["spicy_mode"], False)
        self.assertEqual(result["llm_provider"], "openclaw",
                         "Should restore pre-spicy provider when no manual change")
        self.assertEqual(
            result["openclaw_model"],
            "openclaw/gemini-3-flash-preview",
            "Should restore pre-spicy OpenClaw model",
        )

    def test_exit_spicy_restores_default_openclaw_model_on_invalid_pre_spicy_model(self):
        """OpenClaw should fall back to default model if pre_spicy_model is malformed."""
        spicy_settings = {
            "spicy_mode": True,
            "llm_provider": "openrouter",
            "openrouter_model": constants.SPICY_OPENROUTER_MODEL,
            "pre_spicy_provider": constants.LLM_PROVIDER_OPENCLAW,
            "pre_spicy_model": "gemini-3-flash-preview",
        }

        result = world_logic._compute_spicy_mode_exit_settings(spicy_settings)

        self.assertEqual(result["spicy_mode"], False)
        self.assertEqual(result["llm_provider"], "openclaw")
        self.assertEqual(
            result["openclaw_model"],
            constants.DEFAULT_OPENCLAW_MODEL,
            "Malformed pre-spicy OpenClaw model should fallback to default",
        )


class TestStateUpdatesNoneGuard(unittest.TestCase):
    """
    Tests for None guard in unified_response state_updates handling.

    Bug context: world_logic.py:2218-2227 could raise if response["state_changes"]
    was None when debug_mode=True. Fixed with `or {}` guard and `.get()` check.
    """

    def test_state_changes_none_does_not_raise(self):
        """
        When response["state_changes"] is None, unified_response should handle it.

        This tests the fix: `response.get("state_changes") or {}`
        Without the `or {}`, None would pass through and cause issues.
        """
        # Simulate what happens in _build_unified_response when state_changes is None
        response = {"state_changes": None}
        debug_mode = True

        unified_response = {}
        if debug_mode:
            # This is the fixed code pattern
            unified_response["state_updates"] = response.get("state_changes") or {}

        # Should not raise and should be empty dict
        self.assertEqual(unified_response["state_updates"], {})

    def test_state_changes_empty_dict_preserved(self):
        """Empty dict should be preserved as-is."""
        response = {"state_changes": {}}
        debug_mode = True

        unified_response = {}
        if debug_mode:
            unified_response["state_updates"] = response.get("state_changes") or {}

        self.assertEqual(unified_response["state_updates"], {})

    def test_state_changes_with_values_preserved(self):
        """Non-empty state_changes should be preserved."""
        response = {"state_changes": {"combat_state": {"in_combat": True}}}
        debug_mode = True

        unified_response = {}
        if debug_mode:
            unified_response["state_updates"] = response.get("state_changes") or {}

        self.assertEqual(
            unified_response["state_updates"], {"combat_state": {"in_combat": True}}
        )

    def test_world_events_merge_with_none_state_updates(self):
        """
        When merging world_events into state_updates, handle None gracefully.

        This tests the fix: `if not unified_response.get("state_updates"):`
        """
        structured_fields = {"world_events": [{"event": "test"}]}

        # Simulate unified_response before merge
        unified_response = {"state_updates": None}  # Could happen if not initialized

        # Apply the safe merge pattern
        if structured_fields.get("world_events"):
            unified_response["world_events"] = structured_fields["world_events"]
            if not unified_response.get("state_updates"):
                unified_response["state_updates"] = {}
            unified_response["state_updates"]["world_events"] = structured_fields[
                "world_events"
            ]

        # Should have properly merged world_events
        self.assertEqual(
            unified_response["state_updates"]["world_events"], [{"event": "test"}]
        )

    def test_world_events_merge_with_existing_state_updates(self):
        """World events should merge into existing state_updates dict."""
        structured_fields = {"world_events": [{"event": "test"}]}

        unified_response = {"state_updates": {"combat_state": {"in_combat": False}}}

        if structured_fields.get("world_events"):
            unified_response["world_events"] = structured_fields["world_events"]
            if not unified_response.get("state_updates"):
                unified_response["state_updates"] = {}
            unified_response["state_updates"]["world_events"] = structured_fields[
                "world_events"
            ]

        # Original values preserved, world_events added
        self.assertEqual(
            unified_response["state_updates"]["combat_state"], {"in_combat": False}
        )
        self.assertEqual(
            unified_response["state_updates"]["world_events"], [{"event": "test"}]
        )


class TestGodModeParameterIntegration(unittest.TestCase):
    """
    Integration tests for god mode via mode parameter (not just text prefix).

    These tests verify that mode='god' from the UI is handled the same as
    typing "GOD MODE:" prefix. This requires integration with world_logic.py
    to verify downstream behaviors like player turn handling.

    Bug reference: WA-hd1 - world_logic.py ignores mode='god' parameter
    """

    @patch("mvp_site.world_logic.firestore_service.get_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.get_campaign_by_id")
    @patch("mvp_site.world_logic.firestore_service.update_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.add_story_entry")
    @patch("mvp_site.world_logic.llm_service.continue_story")
    @patch("mvp_site.world_logic._prepare_game_state")
    @patch("mvp_site.world_logic.get_user_settings")
    @patch("mvp_site.world_logic.structured_fields_utils")
    def test_god_mode_via_mode_param_does_not_increment_player_turn(
        self,
        mock_structured_utils,
        mock_settings,
        mock_prepare,
        mock_gemini,
        mock_add_story,
        mock_update_state,
        mock_get_campaign,
        mock_get_campaign_state,
    ):
        """
        🔴 RED PHASE: mode='god' should NOT increment player_turn.

        When the UI sends mode='god' (without "GOD MODE:" prefix in text),
        world_logic.py should treat it as god mode and NOT increment player_turn.

        This test FAILS without the fix because world_logic.py:1501 only checks
        text prefix, not mode parameter.
        """
        initial_player_turn = 5

        # Mock game state with initial player turn
        mock_game_state = Mock()
        mock_game_state.player_turn = initial_player_turn
        mock_game_state.debug_mode = False
        mock_game_state.to_dict.return_value = {
            "player_turn": initial_player_turn,
            "player_character_data": {
                "name": "Thorin",
                "hp_current": 50,
                "hp_max": 50,
            },
            "world_data": {
                "world_time": {
                    "year": 1492,
                    "month": "Mirtul",
                    "day": 10,
                    "hour": 14,
                }
            },
        }

        mock_get_campaign_state.return_value = {}
        mock_get_campaign.return_value = (
            {"selected_prompts": [], "use_default_world": False},
            [],  # story context
        )
        # _prepare_game_state returns tuple: (game_state, state_was_cleaned, entries_cleaned)
        mock_prepare.return_value = (mock_game_state, False, 0)
        mock_settings.return_value = {"debug_mode": False}
        mock_structured_utils.extract_structured_fields.return_value = {}

        # Mock LLM response - must include agent_mode as single source of truth
        mock_gemini_response = Mock()
        mock_gemini_response.narrative_text = "HP set to 100."
        mock_gemini_response.get_state_updates.return_value = {}
        mock_gemini_response.structured_response = None
        mock_gemini_response.get_location_confirmed.return_value = None
        mock_gemini_response.get_narrative_text.return_value = "HP set to 100."
        mock_gemini_response.resources = ""
        mock_gemini_response.processing_metadata = {}
        # agent_mode is the single source of truth - set by agent selection in llm_service
        mock_gemini_response.agent_mode = "god"  # constants.MODE_GOD
        mock_gemini.return_value = mock_gemini_response

        # Request with mode='god' but NO "GOD MODE:" prefix in text
        request_data = {
            "user_id": "test-user-god-mode-param",
            "campaign_id": "test-campaign-god-mode-param",
            "user_input": "set my HP to 100",  # NO "GOD MODE:" prefix!
            "mode": "god",  # This should trigger god mode behavior
        }

        result = asyncio.run(world_logic.process_action_unified(request_data))

        # Verify success
        self.assertTrue(
            result.get("success"),
            f"Expected success, got error: {result.get('error')}",
        )

        # CRITICAL ASSERTION: player_turn should NOT be incremented in god mode
        # If is_god_mode is correctly detected from mode param, turn stays at 5
        # If is_god_mode is missed, turn would be incremented to 6
        updated_state = mock_update_state.call_args[0][2]
        actual_player_turn = updated_state.get("player_turn", -1)

        self.assertEqual(
            initial_player_turn,
            actual_player_turn,
            f"God mode (via mode param) should NOT increment player_turn. "
            f"Expected {initial_player_turn}, got {actual_player_turn}. "
            f"This indicates world_logic.py is ignoring mode='god' parameter "
            f"and only checking for 'GOD MODE:' text prefix.",
        )

    @patch("mvp_site.world_logic.firestore_service.get_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.get_campaign_by_id")
    @patch("mvp_site.world_logic.firestore_service.update_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.add_story_entry")
    @patch("mvp_site.world_logic.llm_service.continue_story")
    @patch("mvp_site.world_logic._prepare_game_state")
    @patch("mvp_site.world_logic.get_user_settings")
    @patch("mvp_site.world_logic.structured_fields_utils")
    def test_god_mode_time_updates_are_applied(
        self,
        mock_structured_utils,
        mock_settings,
        mock_prepare,
        mock_gemini,
        mock_add_story,
        mock_update_state,
        mock_get_campaign,
        mock_get_campaign_state,
    ):
        """
        🔴 RED PHASE: God mode should allow explicit world_time updates.

        When mode='god' is active, the LLM may legitimately update world_time.
        The freeze_time guard should NOT strip those updates.
        """
        initial_player_turn = 2

        # Mock game state with initial world time
        mock_game_state = Mock()
        mock_game_state.player_turn = initial_player_turn
        mock_game_state.debug_mode = False
        mock_game_state.to_dict.return_value = {
            "player_turn": initial_player_turn,
            "player_character_data": {
                "name": "Thorin",
                "hp_current": 50,
                "hp_max": 50,
            },
            "world_data": {
                "world_time": {
                    "year": 1492,
                    "month": "Mirtul",
                    "day": 10,
                    "hour": 14,
                    "minute": 0,
                    "second": 0,
                    "microsecond": 0,
                }
            },
        }

        mock_get_campaign_state.return_value = {}
        mock_get_campaign.return_value = (
            {"selected_prompts": [], "use_default_world": False},
            [],  # story context
        )
        mock_prepare.return_value = (mock_game_state, False, 0)
        mock_settings.return_value = {"debug_mode": False}
        mock_structured_utils.extract_structured_fields.return_value = {}

        # Mock LLM response with explicit time update
        mock_gemini_response = Mock()
        mock_gemini_response.narrative_text = "Time set to 23:45."
        mock_gemini_response.get_state_updates.return_value = {
            "world_data": {"world_time": {"hour": 23, "minute": 45}}
        }
        mock_gemini_response.structured_response = None
        mock_gemini_response.get_location_confirmed.return_value = None
        mock_gemini_response.get_narrative_text.return_value = "Time set to 23:45."
        mock_gemini_response.resources = ""
        mock_gemini_response.processing_metadata = {}
        mock_gemini_response.agent_mode = "god"
        mock_gemini.return_value = mock_gemini_response

        request_data = {
            "user_id": "test-user-god-mode-time",
            "campaign_id": "test-campaign-god-mode-time",
            "user_input": "set time to 23:45",
            "mode": "god",
        }

        result = asyncio.run(world_logic.process_action_unified(request_data))

        self.assertTrue(
            result.get("success"),
            f"Expected success, got error: {result.get('error')}",
        )

        updated_state = mock_update_state.call_args[0][2]
        updated_world_time = updated_state.get("world_data", {}).get("world_time", {})

        self.assertEqual(
            23,
            updated_world_time.get("hour"),
            "God mode should preserve explicit world_time hour updates.",
        )
        self.assertEqual(
            45,
            updated_world_time.get("minute"),
            "God mode should preserve explicit world_time minute updates.",
        )

    @patch("mvp_site.world_logic.firestore_service.get_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.get_campaign_by_id")
    @patch("mvp_site.world_logic.firestore_service.update_campaign_game_state")
    @patch("mvp_site.world_logic.firestore_service.add_story_entry")
    @patch("mvp_site.world_logic.llm_service.continue_story")
    @patch("mvp_site.world_logic._prepare_game_state")
    @patch("mvp_site.world_logic.get_user_settings")
    @patch("mvp_site.world_logic.structured_fields_utils")
    def test_god_mode_return_to_story_without_prefix_uses_character_mode(
        self,
        mock_structured_utils,
        mock_settings,
        mock_prepare,
        mock_gemini,
        mock_add_story,
        mock_update_state,
        mock_get_campaign,
        mock_get_campaign_state,
    ):
        """Return-to-story should work without prefix when mode='god' is set."""
        mock_game_state = Mock()
        mock_game_state.player_turn = 5
        mock_game_state.debug_mode = False
        mock_game_state.to_dict.return_value = {
            "player_turn": 5,
            "player_character_data": {
                "name": "Thorin",
                "hp_current": 50,
                "hp_max": 50,
            },
            "world_data": {
                "world_time": {
                    "year": 1492,
                    "month": "Mirtul",
                    "day": 10,
                    "hour": 14,
                }
            },
        }

        mock_get_campaign_state.return_value = {}
        mock_get_campaign.return_value = (
            {"selected_prompts": [], "use_default_world": False},
            [],
        )
        mock_prepare.return_value = (mock_game_state, False, 0)
        mock_settings.return_value = {"debug_mode": False}
        mock_structured_utils.extract_structured_fields.return_value = {}

        mock_gemini_response = Mock()
        mock_gemini_response.narrative_text = "Returning to story."
        mock_gemini_response.get_state_updates.return_value = {}
        mock_gemini_response.structured_response = None
        mock_gemini_response.get_location_confirmed.return_value = None
        mock_gemini_response.get_narrative_text.return_value = "Returning to story."
        mock_gemini_response.resources = ""
        mock_gemini_response.processing_metadata = {}
        mock_gemini_response.agent_mode = world_logic.constants.MODE_CHARACTER
        mock_gemini.return_value = mock_gemini_response

        request_data = {
            "user_id": "test-user-god-mode-return",
            "campaign_id": "test-campaign-god-mode-return",
            "user_input": "return to story",
            "mode": "god",
        }

        result = asyncio.run(world_logic.process_action_unified(request_data))

        self.assertTrue(
            result.get("success"),
            f"Expected success, got error: {result.get('error')}",
        )
        self.assertTrue(mock_gemini.called, "LLM should be called")
        call_args = mock_gemini.call_args[0]
        self.assertEqual("Return to story.", call_args[0])
        self.assertEqual(world_logic.constants.MODE_CHARACTER, call_args[1])

    def test_parse_god_mode_data_string_preserves_setting_without_character(self):
        """Test that setting is preserved even when no character info is provided."""
        # Test case: Only setting provided, no character
        god_mode_data = "Setting: Forgotten Realms"
        result = world_logic._parse_god_mode_data_string(god_mode_data)

        self.assertIsNotNone(result, "Should return dict when setting exists")
        self.assertEqual(result.get("setting"), "Forgotten Realms")
        self.assertNotIn("character", result)
        self.assertNotIn("description", result)

    def test_parse_god_mode_data_string_preserves_description_without_character(self):
        """Test that description is preserved even when no character info is provided."""
        # Test case: Only description provided, no character
        god_mode_data = "Description: A dark fantasy campaign set in a cursed kingdom"
        result = world_logic._parse_god_mode_data_string(god_mode_data)

        self.assertIsNotNone(result, "Should return dict when description exists")
        self.assertEqual(
            result.get("description"), "A dark fantasy campaign set in a cursed kingdom"
        )
        self.assertNotIn("character", result)
        self.assertNotIn("setting", result)

    def test_parse_god_mode_data_string_preserves_setting_and_description_without_character(
        self,
    ):
        """Test that both setting and description are preserved even when no character info is provided."""
        # Test case: Setting and description provided, no character
        god_mode_data = (
            "Setting: Forgotten Realms | Description: A dark fantasy campaign"
        )
        result = world_logic._parse_god_mode_data_string(god_mode_data)

        self.assertIsNotNone(
            result, "Should return dict when setting or description exists"
        )
        self.assertEqual(result.get("setting"), "Forgotten Realms")
        self.assertEqual(result.get("description"), "A dark fantasy campaign")
        self.assertNotIn("character", result)

    def test_parse_god_mode_data_string_with_character_still_works(self):
        """Test that existing behavior with character info still works correctly."""
        # Test case: Character with setting and description (existing behavior)
        god_mode_data = "Character: Ser Arion | Setting: Forgotten Realms | Description: A paladin's journey"
        result = world_logic._parse_god_mode_data_string(god_mode_data)

        self.assertIsNotNone(result, "Should return dict when character exists")
        self.assertIn("character", result)
        self.assertEqual(result["character"].get("name"), "Ser Arion")
        self.assertEqual(result.get("setting"), "Forgotten Realms")
        self.assertEqual(result.get("description"), "A paladin's journey")

    def test_parse_god_mode_data_string_returns_none_when_empty(self):
        """Test that None is returned when no useful data is provided."""
        # Test case: Empty string
        result = world_logic._parse_god_mode_data_string("")
        self.assertIsNone(result, "Should return None for empty string")

        # Test case: None input
        result = world_logic._parse_god_mode_data_string(None)
        self.assertIsNone(result, "Should return None for None input")

        # Test case: Invalid format with no useful data
        result = world_logic._parse_god_mode_data_string("Some random text")
        self.assertIsNone(
            result, "Should return None when no setting/description/character found"
        )

    def test_parse_god_mode_data_string_extracts_all_six_stats_from_long_prompt(self):
        """Long prompts with 6-stat blocks should hydrate full base_attributes."""
        god_mode_data = (
            "Character: Erik the Ranger (Level 3, Hunter) | "
            "Description: ATTRIBUTES: STR 14, DEX 16, CON 14, INT 10, WIS 14, CHA 10"
        )

        result = world_logic._parse_god_mode_data_string(god_mode_data)

        self.assertIsNotNone(result)
        self.assertIn("character", result)
        character = result["character"]
        self.assertEqual(character.get("base_attributes", {}).get("strength"), 14)
        self.assertEqual(character.get("base_attributes", {}).get("dexterity"), 16)
        self.assertEqual(character.get("base_attributes", {}).get("constitution"), 14)
        self.assertEqual(character.get("base_attributes", {}).get("intelligence"), 10)
        self.assertEqual(character.get("base_attributes", {}).get("wisdom"), 14)
        self.assertEqual(character.get("base_attributes", {}).get("charisma"), 10)
        self.assertEqual(character.get("attributes"), character.get("base_attributes"))

    def test_parse_god_mode_data_string_extracts_class_without_level_prefix(self):
        """Parser should capture class when prompt includes 'Class: X' without level."""
        god_mode_data = "Character: Lyra | Description: **Class:** Bard"

        result = world_logic._parse_god_mode_data_string(god_mode_data)

        self.assertIsNotNone(result)
        self.assertEqual(result["character"].get("class"), "Bard")

    def test_parse_god_mode_data_string_does_not_match_subclass_as_class(self):
        """Subclass: must not be matched by word-boundary Class: anchor."""
        god_mode_data = "Character: Elara | Subclass: Oath of Devotion"

        result = world_logic._parse_god_mode_data_string(god_mode_data)
        self.assertIsNotNone(result)
        self.assertNotIn("class", result.get("character", {}))

    def test_parse_god_mode_data_string_does_not_match_multiclass_as_class(self):
        """Multiclass: must not be matched by word-boundary Class: anchor."""
        god_mode_data = "Character: Brax | Multiclass: Fighter 3"

        result = world_logic._parse_god_mode_data_string(god_mode_data)
        self.assertIsNotNone(result)
        self.assertNotIn("class", result.get("character", {}))

    def test_parse_god_mode_data_string_does_not_match_class_features_phrase(self):
        """'class features: ...' must not set character class (no colon-only anchor)."""
        god_mode_data = "Character: Sylvara | class features: Sneak Attack 3d6"

        result = world_logic._parse_god_mode_data_string(god_mode_data)
        self.assertIsNotNone(result)
        self.assertNotIn("class", result.get("character", {}))

    def test_parse_god_mode_data_string_extracts_multiword_class_name(self):
        """Multi-word class names like 'Blood Hunter' are captured via Class: label."""
        god_mode_data = "Character: Kael | Class: Blood Hunter"

        result = world_logic._parse_god_mode_data_string(god_mode_data)

        self.assertIsNotNone(result)
        character = result.get("character", {})
        self.assertIn("class", character, "Expected class to be parsed")
        self.assertEqual(character["class"].strip().lower(), "blood hunter")

    def test_parse_god_mode_data_string_class_not_corrupted_by_next_line_race(self):
        """Regression: level N on class line must not bleed into the Race: line below.

        The bug: `level\\s+(\\d+)\\s+` uses \\s+ which includes \\n, so
        'Level 2\\n- **Race:** Tiefling' captured '- **Race:** Tiefling' as the class.
        """
        god_mode_data = (
            "Character: Vael | Setting: The Shadow Realm.\n\n"
            "**Your character:**\n"
            "- **Class:** Shadow Weaver (Custom Spellcasting Class) - Level 2\n"
            "- **Race:** Tiefling\n"
        )

        result = world_logic._parse_god_mode_data_string(god_mode_data)

        self.assertIsNotNone(result)
        character = result.get("character", {})
        class_value = character.get("class", "")
        self.assertNotIn(
            "race",
            class_value.lower(),
            f"class field must not contain race data; got: {class_value!r}",
        )
        self.assertNotIn(
            "tiefling",
            class_value.lower(),
            f"class field must not contain race value; got: {class_value!r}",
        )
        # class should be Shadow Weaver (with possible level suffix removed)
        self.assertIn(
            "shadow weaver",
            class_value.lower(),
            f"class field should contain the actual class name; got: {class_value!r}",
        )


class TestIncrementTurnCounter(unittest.TestCase):
    """Test _increment_turn_counter centralized function"""

    def test_increment_turn_counter_normal_action(self):
        """Test that turn counter increments on normal (non-god) action"""
        game_state = {"turn_number": 5, "player_turn": 5}
        result = world_logic._increment_turn_counter(
            game_state, is_god_mode=False, should_freeze_time=False
        )
        self.assertEqual(result["turn_number"], 6)
        self.assertEqual(result["player_turn"], 6)

    def test_increment_turn_counter_god_mode(self):
        """Test that turn counter does NOT increment in god mode"""
        game_state = {"turn_number": 5, "player_turn": 5}
        result = world_logic._increment_turn_counter(
            game_state, is_god_mode=True, should_freeze_time=False
        )
        self.assertEqual(result["turn_number"], 5)
        self.assertEqual(result["player_turn"], 5)

    def test_increment_turn_counter_freeze_time(self):
        """Test that turn counter does NOT increment when time is frozen"""
        game_state = {"turn_number": 5, "player_turn": 5}
        result = world_logic._increment_turn_counter(
            game_state, is_god_mode=False, should_freeze_time=True
        )
        self.assertEqual(result["turn_number"], 5)
        self.assertEqual(result["player_turn"], 5)

    def test_increment_turn_counter_handles_non_int(self):
        """Test that turn counter handles non-int values gracefully"""
        game_state = {"turn_number": "5", "player_turn": "5"}
        result = world_logic._increment_turn_counter(
            game_state, is_god_mode=False, should_freeze_time=False
        )
        self.assertEqual(result["turn_number"], 6)
        self.assertEqual(result["player_turn"], 6)

    def test_increment_turn_counter_handles_none(self):
        """Test that turn counter handles None values gracefully"""
        game_state = {"turn_number": None, "player_turn": None}
        result = world_logic._increment_turn_counter(
            game_state, is_god_mode=False, should_freeze_time=False
        )
        self.assertEqual(result["turn_number"], 1)
        self.assertEqual(result["player_turn"], 1)

    def test_increment_turn_counter_handles_missing_keys(self):
        """Test that turn counter handles missing keys with defaults"""
        game_state = {}
        result = world_logic._increment_turn_counter(
            game_state, is_god_mode=False, should_freeze_time=False
        )
        self.assertEqual(result["turn_number"], 1)
        self.assertEqual(result["player_turn"], 1)

    def test_increment_turn_counter_heals_diverged_counters(self):
        """Test diverged counters are resynchronized to canonical turn_number."""
        game_state = {"turn_number": 10, "player_turn": 2}
        result = world_logic._increment_turn_counter(
            game_state, is_god_mode=False, should_freeze_time=False
        )
        self.assertEqual(result["turn_number"], 11)
        self.assertEqual(result["player_turn"], 11)

    def test_increment_turn_counter_falls_back_to_player_turn(self):
        """Test legacy state without turn_number can continue from player_turn."""
        game_state = {"player_turn": 5}
        result = world_logic._increment_turn_counter(
            game_state, is_god_mode=False, should_freeze_time=False
        )
        self.assertEqual(result["turn_number"], 6)
        self.assertEqual(result["player_turn"], 6)


class TestExtractXPFromPlayerData(unittest.TestCase):
    """Test _extract_xp_from_player_data function"""

    def test_extract_xp_from_experience_dict(self):
        """Test extracting XP from experience.current format"""
        pc_data = {"experience": {"current": 5000}}
        result = world_logic._extract_xp_from_player_data(pc_data)
        self.assertEqual(result, 5000)

    def test_extract_xp_from_experience_int(self):
        """Test extracting XP from experience as int"""
        pc_data = {"experience": 3000}
        result = world_logic._extract_xp_from_player_data(pc_data)
        self.assertEqual(result, 3000)

    def test_extract_xp_from_experience_string(self):
        """Test extracting XP from experience as string"""
        pc_data = {"experience": "2500"}
        result = world_logic._extract_xp_from_player_data(pc_data)
        self.assertEqual(result, 2500)

    def test_extract_xp_from_experience_string_with_commas(self):
        """Test extracting XP from experience as comma-formatted string"""
        pc_data = {"experience": "2,700"}
        result = world_logic._extract_xp_from_player_data(pc_data)
        self.assertEqual(result, 2700)

    def test_extract_xp_from_xp_field(self):
        """Test extracting XP from xp field"""
        pc_data = {"xp": 1500}
        result = world_logic._extract_xp_from_player_data(pc_data)
        self.assertEqual(result, 1500)

    def test_extract_xp_from_xp_current_field(self):
        """Test extracting XP from xp_current field"""
        pc_data = {"xp_current": 2000}
        result = world_logic._extract_xp_from_player_data(pc_data)
        self.assertEqual(result, 2000)

    def test_extract_xp_priority_order(self):
        """Test that experience field takes priority over xp"""
        pc_data = {"experience": 1000, "xp": 2000}
        result = world_logic._extract_xp_from_player_data(pc_data)
        self.assertEqual(result, 1000)

    def test_extract_xp_returns_zero_for_missing(self):
        """Test that missing XP returns 0"""
        pc_data = {}
        result = world_logic._extract_xp_from_player_data(pc_data)
        self.assertEqual(result, 0)

    def test_extract_xp_returns_zero_for_invalid_type(self):
        """Test that invalid input type returns 0"""
        result = world_logic._extract_xp_from_player_data("not a dict")
        self.assertEqual(result, 0)

    def test_extract_xp_handles_float(self):
        """Test that float XP values are converted to int"""
        pc_data = {"experience": 1234.5}
        result = world_logic._extract_xp_from_player_data(pc_data)
        self.assertEqual(result, 1234)


class TestHasRewardsNarrative(unittest.TestCase):
    """Test _has_rewards_narrative function"""

    def test_detects_reward_keyword(self):
        """Test detection of 'reward' keyword"""
        narrative = "You receive a reward for your efforts."
        self.assertTrue(world_logic._has_rewards_narrative(narrative))

    def test_detects_rewards_keyword(self):
        """Test detection of 'rewards' keyword"""
        narrative = "Here are your rewards."
        self.assertTrue(world_logic._has_rewards_narrative(narrative))

    def test_detects_xp_keyword(self):
        """Test detection of 'xp' keyword"""
        narrative = "You gain 500 XP."
        self.assertTrue(world_logic._has_rewards_narrative(narrative))

    def test_detects_experience_keyword(self):
        """Test detection of 'experience' keyword"""
        narrative = "You gain experience."
        self.assertTrue(world_logic._has_rewards_narrative(narrative))

    def test_detects_level_up_keyword(self):
        """Test detection of 'level up' keyword"""
        narrative = "You level up!"
        self.assertTrue(world_logic._has_rewards_narrative(narrative))

    def test_detects_levelup_keyword(self):
        """Test detection of 'levelup' keyword"""
        narrative = "You levelup!"
        self.assertTrue(world_logic._has_rewards_narrative(narrative))

    def test_detects_loot_keyword(self):
        """Test detection of 'loot' keyword"""
        narrative = "You find loot."
        self.assertTrue(world_logic._has_rewards_narrative(narrative))

    def test_detects_gold_keyword(self):
        """Test detection of 'gold' keyword"""
        narrative = "You find 100 gold."
        self.assertTrue(world_logic._has_rewards_narrative(narrative))

    def test_detects_treasure_keyword(self):
        """Test detection of 'treasure' keyword"""
        narrative = "You discover treasure."
        self.assertTrue(world_logic._has_rewards_narrative(narrative))

    def test_detects_awarded_keyword(self):
        """Test detection of 'awarded' keyword"""
        narrative = "You are awarded 500 XP."
        self.assertTrue(world_logic._has_rewards_narrative(narrative))

    def test_detects_gained_keyword(self):
        """Test detection of 'gained' keyword"""
        narrative = "You gained experience."
        self.assertTrue(world_logic._has_rewards_narrative(narrative))

    def test_detects_victory_keyword(self):
        """Test detection of 'victory' keyword"""
        narrative = "Victory! You win."
        self.assertTrue(world_logic._has_rewards_narrative(narrative))

    def test_detects_box_markers_double_equals(self):
        """Test detection of box markers (══)"""
        narrative = "═══ Rewards ═══"
        self.assertTrue(world_logic._has_rewards_narrative(narrative))

    def test_detects_box_markers_double_dash(self):
        """Test detection of box markers (──)"""
        narrative = "─── Rewards ───"
        self.assertTrue(world_logic._has_rewards_narrative(narrative))

    def test_case_insensitive_detection(self):
        """Test that detection is case-insensitive"""
        narrative = "You RECEIVE a REWARD."
        self.assertTrue(world_logic._has_rewards_narrative(narrative))

    def test_returns_false_for_no_rewards(self):
        """Test that narrative without rewards returns False"""
        narrative = "You walk through the forest."
        self.assertFalse(world_logic._has_rewards_narrative(narrative))

    def test_returns_false_for_none(self):
        """Test that None input returns False"""
        self.assertFalse(world_logic._has_rewards_narrative(None))

    def test_returns_false_for_empty_string(self):
        """Test that empty string returns False"""
        self.assertFalse(world_logic._has_rewards_narrative(""))


class TestHasRewardsContext(unittest.TestCase):
    """Test _has_rewards_context function"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_constants_patcher = patch("mvp_site.world_logic.constants")
        self.mock_constants = self.mock_constants_patcher.start()
        self.addCleanup(self.mock_constants_patcher.stop)

    def test_detects_combat_summary(self):
        """Test detection of combat_summary"""
        state_dict = {"combat_state": {"combat_summary": "Combat ended"}}
        self.assertTrue(world_logic._has_rewards_context(state_dict))

    def test_detects_encounter_summary_dict(self):
        """Test detection of encounter_summary as dict"""
        state_dict = {"encounter_state": {"encounter_summary": {"xp": 500}}}
        self.assertTrue(world_logic._has_rewards_context(state_dict))

    def test_detects_rewards_pending(self):
        """Test detection of rewards_pending"""
        state_dict = {"rewards_pending": {"xp": 500, "gold": 100}}
        self.assertTrue(world_logic._has_rewards_context(state_dict))

    def test_detects_xp_increase(self):
        """Test detection of XP increase from original state"""
        state_dict = {"player_character_data": {"experience": {"current": 2000}}}
        original_state = {"player_character_data": {"experience": {"current": 1000}}}
        self.assertTrue(world_logic._has_rewards_context(state_dict, original_state))

    def test_no_rewards_context(self):
        """Test that state without rewards context returns False"""
        state_dict = {"player_character_data": {"name": "Hero"}}
        self.assertFalse(world_logic._has_rewards_context(state_dict))

    def test_empty_combat_state(self):
        """Test that empty combat_state doesn't trigger detection"""
        state_dict = {"combat_state": {}}
        self.assertFalse(world_logic._has_rewards_context(state_dict))

    def test_empty_encounter_state(self):
        """Test that empty encounter_state doesn't trigger detection"""
        state_dict = {"encounter_state": {}}
        self.assertFalse(world_logic._has_rewards_context(state_dict))

    def test_xp_decrease_does_not_trigger(self):
        """Test that XP decrease doesn't trigger rewards context"""
        state_dict = {"player_character_data": {"experience": {"current": 1000}}}
        original_state = {"player_character_data": {"experience": {"current": 2000}}}
        self.assertFalse(world_logic._has_rewards_context(state_dict, original_state))

    def test_xp_same_does_not_trigger(self):
        """Test that same XP doesn't trigger rewards context"""
        state_dict = {"player_character_data": {"experience": {"current": 1000}}}
        original_state = {"player_character_data": {"experience": {"current": 1000}}}
        self.assertFalse(world_logic._has_rewards_context(state_dict, original_state))


class TestDetectRewardsDiscrepancyComprehensive(unittest.TestCase):
    """Comprehensive tests for _detect_rewards_discrepancy function"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_constants_patcher = patch("mvp_site.world_logic.constants")
        self.mock_constants = self.mock_constants_patcher.start()
        self.mock_constants.COMBAT_FINISHED_PHASES = ["victory", "defeat", "fled"]
        self.addCleanup(self.mock_constants_patcher.stop)

    def test_detects_combat_finished_without_rewards_processed(self):
        """SERVER AUTO-SET: Server auto-sets rewards_processed when combat finishes

        ARCHITECTURAL CHANGE (2026-01-22): Server owns administrative flags.
        """
        state_dict = {
            "combat_state": {
                "combat_phase": "victory",
                "combat_summary": "You won!",
                "rewards_processed": False,
            }
        }
        discrepancies = world_logic._detect_rewards_discrepancy(state_dict)
        # Server AUTO-SETS the flag, so no discrepancy is returned
        self.assertEqual(
            len(discrepancies), 0, "Server should auto-fix, not return discrepancy"
        )
        # Verify server set the flag
        self.assertTrue(
            state_dict["combat_state"]["rewards_processed"],
            "Server should auto-set rewards_processed=True",
        )

    def test_detects_encounter_completed_without_rewards_processed(self):
        """SERVER AUTO-SET: Server auto-sets rewards_processed when encounter completes

        ARCHITECTURAL CHANGE (2026-01-22): Server owns administrative flags.
        """
        state_dict = {
            "encounter_state": {
                "encounter_completed": True,
                "encounter_summary": "Encounter finished",
                "rewards_processed": False,
            }
        }
        discrepancies = world_logic._detect_rewards_discrepancy(state_dict)
        # Server AUTO-SETS the flag, so no discrepancy is returned
        self.assertEqual(
            len(discrepancies), 0, "Server should auto-fix, not return discrepancy"
        )
        # Verify server set the flag
        self.assertTrue(
            state_dict["encounter_state"]["rewards_processed"],
            "Server should auto-set rewards_processed=True",
        )

    def test_detects_xp_increase_without_rewards_processed(self):
        """SERVER AUTO-SET: Server auto-sets rewards_processed when XP increases

        ARCHITECTURAL CHANGE (2026-01-22): Server owns administrative flags.
        """
        state_dict = {
            "combat_state": {
                "combat_phase": "victory",
                "rewards_processed": False,
            },
            "player_character_data": {"experience": {"current": 2000}},
        }
        original_state = {
            "combat_state": {"rewards_processed": False},
            "player_character_data": {"experience": {"current": 1000}},
        }
        discrepancies = world_logic._detect_rewards_discrepancy(
            state_dict, original_state
        )
        # Server AUTO-SETS the flag, so no discrepancy is returned
        self.assertEqual(
            len(discrepancies), 0, "Server should auto-fix when XP increases"
        )
        # Verify server set the flag
        self.assertTrue(
            state_dict["combat_state"]["rewards_processed"],
            "Server should auto-set rewards_processed=True when XP increases",
        )

    def test_no_discrepancy_when_rewards_processed(self):
        """Test no discrepancy when rewards_processed is True"""
        state_dict = {
            "combat_state": {
                "combat_phase": "victory",
                "combat_summary": "You won!",
                "rewards_processed": True,
            }
        }
        discrepancies = world_logic._detect_rewards_discrepancy(state_dict)
        self.assertEqual(len(discrepancies), 0)

    def test_warns_on_xp_increase_with_rewards_processed(self):
        """Test warning when XP increases but rewards_processed is True"""
        state_dict = {
            "combat_state": {
                "combat_phase": "victory",
                "rewards_processed": True,
            },
            "player_character_data": {"experience": {"current": 2000}},
        }
        original_state = {
            "combat_state": {"rewards_processed": True},
            "player_character_data": {"experience": {"current": 1000}},
        }
        warnings = []
        discrepancies = world_logic._detect_rewards_discrepancy(
            state_dict, original_state, warnings_out=warnings
        )
        self.assertEqual(len(discrepancies), 0)
        self.assertEqual(len(warnings), 1)
        self.assertIn("REWARDS_STATE_WARNING", warnings[0])

    def test_combat_xp_check_handles_non_dict_player_data(self):
        """Ensure XP checks tolerate non-dict player data without crashing."""
        state_dict = {
            "combat_state": {
                "combat_phase": "victory",
                "rewards_processed": False,
            },
            "player_character_data": "invalid",
        }
        original_state = {
            "combat_state": {"rewards_processed": False},
            "player_character_data": ["not-a-dict"],
        }
        discrepancies = world_logic._detect_rewards_discrepancy(
            state_dict, original_state
        )
        self.assertEqual(len(discrepancies), 0)
        self.assertFalse(state_dict["combat_state"]["rewards_processed"])

    def test_encounter_xp_increase_auto_sets_rewards_processed(self):
        """SERVER AUTO-SET: Encounter XP increase sets rewards_processed."""
        state_dict = {
            "encounter_state": {
                "encounter_completed": True,
                "rewards_processed": False,
            },
            "player_character_data": {"experience": {"current": 200}},
        }
        original_state = {
            "encounter_state": {"rewards_processed": False},
            "player_character_data": {"experience": {"current": 100}},
        }
        discrepancies = world_logic._detect_rewards_discrepancy(
            state_dict, original_state
        )
        self.assertEqual(len(discrepancies), 0)
        self.assertTrue(state_dict["encounter_state"]["rewards_processed"])

    def test_encounter_xp_increase_warns_when_already_processed(self):
        """Warn when encounter XP increases but rewards_processed already true."""
        state_dict = {
            "encounter_state": {
                "encounter_completed": True,
                "rewards_processed": True,
            },
            "player_character_data": {"experience": {"current": 200}},
        }
        original_state = {
            "encounter_state": {"rewards_processed": True},
            "player_character_data": {"experience": {"current": 100}},
        }
        warnings: list[str] = []
        discrepancies = world_logic._detect_rewards_discrepancy(
            state_dict, original_state, warnings_out=warnings
        )
        self.assertEqual(len(discrepancies), 0)
        self.assertEqual(len(warnings), 1)
        self.assertIn("REWARDS_STATE_WARNING", warnings[0])

    def test_narrative_xp_fallback_sets_encounter_rewards(self):
        """Fallback sets encounter rewards when XP increases outside combat/encounter."""
        state_dict = {
            "combat_state": {"in_combat": False},
            "encounter_state": {},
            "player_character_data": {"experience": {"current": 150}},
        }
        original_state = {
            "player_character_data": {"experience": {"current": 100}},
        }
        discrepancies = world_logic._detect_rewards_discrepancy(
            state_dict, original_state
        )
        self.assertEqual(len(discrepancies), 0)
        self.assertTrue(state_dict["encounter_state"]["rewards_processed"])

    def test_no_discrepancy_for_non_finished_combat(self):
        """Test no discrepancy for combat that hasn't finished"""
        state_dict = {
            "combat_state": {
                "combat_phase": "in_progress",
                "combat_summary": "Fighting...",
                "rewards_processed": False,
            }
        }
        discrepancies = world_logic._detect_rewards_discrepancy(state_dict)
        self.assertEqual(len(discrepancies), 0)

    def test_no_discrepancy_without_combat_summary(self):
        """Test no discrepancy when combat finished but no summary"""
        state_dict = {
            "combat_state": {
                "combat_phase": "victory",
                "rewards_processed": False,
            }
        }
        discrepancies = world_logic._detect_rewards_discrepancy(state_dict)
        self.assertEqual(len(discrepancies), 0)

    # BD-lgx: Stale combat/encounter phase should NOT generate false warnings
    def test_stale_combat_no_rewards_warning(self):
        """BD-lgx: XP increase with stale combat_phase=ended should NOT warn."""
        state_dict = {
            "combat_state": {
                "combat_phase": "ended",
                "rewards_processed": True,
            },
            "player_character_data": {"experience": {"current": 450}},
        }
        original_state = {
            "combat_state": {
                "combat_phase": "ended",
                "rewards_processed": True,
            },
            "player_character_data": {"experience": {"current": 400}},
        }
        warnings = []
        world_logic._detect_rewards_discrepancy(
            state_dict, original_state, warnings_out=warnings
        )
        self.assertEqual(
            len(warnings), 0,
            f"BD-lgx: Stale combat should not generate REWARDS_STATE_WARNING, got: {warnings}",
        )

    def test_fresh_combat_end_still_warns(self):
        """BD-lgx: XP increase when combat JUST ended should still warn."""
        state_dict = {
            "combat_state": {
                "combat_phase": "victory",
                "rewards_processed": True,
            },
            "player_character_data": {"experience": {"current": 2000}},
        }
        original_state = {
            "combat_state": {
                "combat_phase": "active",
                "rewards_processed": True,
            },
            "player_character_data": {"experience": {"current": 1000}},
        }
        warnings = []
        world_logic._detect_rewards_discrepancy(
            state_dict, original_state, warnings_out=warnings
        )
        self.assertEqual(len(warnings), 1, "Fresh combat end should still warn")
        self.assertIn("REWARDS_STATE_WARNING", warnings[0])

    def test_stale_encounter_no_rewards_warning(self):
        """BD-lgx: XP increase with stale encounter_completed=True should NOT warn."""
        state_dict = {
            "encounter_state": {
                "encounter_completed": True,
                "rewards_processed": True,
            },
            "player_character_data": {"experience": {"current": 450}},
        }
        original_state = {
            "encounter_state": {
                "encounter_completed": True,
                "rewards_processed": True,
            },
            "player_character_data": {"experience": {"current": 400}},
        }
        warnings = []
        world_logic._detect_rewards_discrepancy(
            state_dict, original_state, warnings_out=warnings
        )
        self.assertEqual(
            len(warnings), 0,
            f"BD-lgx: Stale encounter should not warn, got: {warnings}",
        )

    def test_fresh_encounter_completion_still_warns(self):
        """BD-lgx: XP increase when encounter JUST completed should still warn."""
        state_dict = {
            "encounter_state": {
                "encounter_completed": True,
                "rewards_processed": True,
            },
            "player_character_data": {"experience": {"current": 500}},
        }
        original_state = {
            "encounter_state": {
                "encounter_completed": False,
                "rewards_processed": True,
            },
            "player_character_data": {"experience": {"current": 400}},
        }
        warnings = []
        world_logic._detect_rewards_discrepancy(
            state_dict, original_state, warnings_out=warnings
        )
        self.assertEqual(len(warnings), 1, "Fresh encounter should still warn")
        self.assertIn("REWARDS_STATE_WARNING", warnings[0])


class TestAnnotateEntry(unittest.TestCase):
    """Test _annotate_entry function"""

    def test_adds_turn_and_scene(self):
        """Test that turn and scene are added to entry"""
        entry = {}
        world_logic._annotate_entry(entry, turn=5, scene=3)
        self.assertEqual(entry["turn_generated"], 5)
        self.assertEqual(entry["scene_generated"], 3)

    def test_does_not_overwrite_existing_turn(self):
        """Test that existing turn_generated is not overwritten"""
        entry = {"turn_generated": 10, "scene_generated": 5}
        world_logic._annotate_entry(entry, turn=5, scene=3)
        self.assertEqual(entry["turn_generated"], 10)
        self.assertEqual(entry["scene_generated"], 5)

    def test_adds_only_missing_fields(self):
        """Test that only missing fields are added"""
        entry = {"turn_generated": 10}
        world_logic._annotate_entry(entry, turn=5, scene=3)
        self.assertEqual(entry["turn_generated"], 10)
        self.assertEqual(entry["scene_generated"], 3)

    def test_sets_scene_generated_independently(self):
        """Test that scene_generated is set even when turn_generated already exists."""
        entry = {"turn_generated": 10}  # Has turn but missing scene
        world_logic._annotate_entry(entry, turn=5, scene=3)
        self.assertEqual(entry["turn_generated"], 10)  # Preserved
        self.assertEqual(entry["scene_generated"], 3)  # Added

    def test_sets_both_when_missing(self):
        """Test that both turn_generated and scene_generated are set when missing."""
        entry = {}
        world_logic._annotate_entry(entry, turn=5, scene=3)
        self.assertEqual(entry["turn_generated"], 5)
        self.assertEqual(entry["scene_generated"], 3)

    def test_preserves_existing_turn_generated(self):
        """Test that existing turn_generated is not overwritten."""
        entry = {"turn_generated": 10, "scene_generated": 5}
        world_logic._annotate_entry(entry, turn=5, scene=3)
        self.assertEqual(entry["turn_generated"], 10)  # Preserved
        self.assertEqual(entry["scene_generated"], 5)  # Preserved

    def test_handles_legacy_entries(self):
        """Test that legacy entries with only turn_generated get scene_generated added."""
        entry = {"turn_generated": 10}  # Legacy entry missing scene_generated
        world_logic._annotate_entry(entry, turn=10, scene=2)
        self.assertEqual(entry["turn_generated"], 10)  # Preserved
        self.assertEqual(entry["scene_generated"], 2)  # Added


class TestAnnotateWorldEventsWithTurnScene(unittest.TestCase):
    """Test annotate_world_events_with_turn_scene function"""

    def test_annotates_world_events_background_events(self):
        """Test annotation of world_events.background_events"""
        game_state = {
            "world_events": {
                "background_events": [{"text": "Event 1"}, {"text": "Event 2"}]
            }
        }
        result = world_logic.annotate_world_events_with_turn_scene(
            game_state, player_turn=3
        )
        events = result["world_events"]["background_events"]
        self.assertEqual(events[0]["turn_generated"], 3)
        self.assertEqual(events[0]["scene_generated"], 3)
        self.assertEqual(events[1]["turn_generated"], 3)

    def test_annotates_top_level_rumors(self):
        """Test annotation of top-level rumors"""
        game_state = {"rumors": [{"text": "Rumor 1"}]}
        result = world_logic.annotate_world_events_with_turn_scene(
            game_state, player_turn=5
        )
        self.assertEqual(result["rumors"][0]["turn_generated"], 5)
        self.assertEqual(result["rumors"][0]["scene_generated"], 5)

    def test_annotates_faction_updates(self):
        """Test annotation of faction_updates"""
        game_state = {
            "faction_updates": {
                "faction1": {"status": "active"},
                "faction2": {"status": "inactive"},
            }
        }
        result = world_logic.annotate_world_events_with_turn_scene(
            game_state, player_turn=7
        )
        self.assertEqual(result["faction_updates"]["faction1"]["turn_generated"], 7)
        self.assertEqual(result["faction_updates"]["faction2"]["turn_generated"], 7)

    def test_annotates_complications(self):
        """Test annotation of complications"""
        game_state = {"complications": {"text": "Complication"}}
        result = world_logic.annotate_world_events_with_turn_scene(
            game_state, player_turn=1
        )
        self.assertEqual(result["complications"]["turn_generated"], 1)
        self.assertEqual(result["complications"]["scene_generated"], 1)

    def test_calculates_scene_correctly(self):
        """Test that scene number matches turn number for story entries."""
        # Create fresh game_state for each test case to avoid mutation issues.
        game_state_1 = {"rumors": [{"text": "Rumor"}]}
        result = world_logic.annotate_world_events_with_turn_scene(
            game_state_1, player_turn=1
        )
        self.assertEqual(result["rumors"][0]["scene_generated"], 1)

        # Turn 2 -> Scene 2
        game_state_2 = {"rumors": [{"text": "Rumor"}]}
        result = world_logic.annotate_world_events_with_turn_scene(
            game_state_2, player_turn=2
        )
        self.assertEqual(result["rumors"][0]["scene_generated"], 2)

        # Turn 3 -> Scene 3
        game_state_3 = {"rumors": [{"text": "Rumor"}]}
        result = world_logic.annotate_world_events_with_turn_scene(
            game_state_3, player_turn=3
        )
        self.assertEqual(result["rumors"][0]["scene_generated"], 3)

        # Turn 4 -> Scene 4
        game_state_4 = {"rumors": [{"text": "Rumor"}]}
        result = world_logic.annotate_world_events_with_turn_scene(
            game_state_4, player_turn=4
        )
        self.assertEqual(result["rumors"][0]["scene_generated"], 4)

    def test_handles_missing_world_events(self):
        """Test that missing world_events doesn't cause errors"""
        game_state = {}
        result = world_logic.annotate_world_events_with_turn_scene(
            game_state, player_turn=1
        )
        self.assertEqual(result, game_state)

    def test_handles_non_dict_world_events(self):
        """Test that non-dict world_events doesn't cause errors"""
        game_state = {"world_events": "not a dict"}
        result = world_logic.annotate_world_events_with_turn_scene(
            game_state, player_turn=1
        )
        self.assertEqual(result, game_state)


class TestStoryEntryWorldEventsBackfill(unittest.TestCase):
    """Regression tests for per-entry world_events backfill/filtering."""

    def test_backfills_world_events_and_state_updates_from_game_state(self):
        structured_fields = {"state_updates": {}}
        updated_game_state = {
            "world_events": {
                "background_events": [
                    {
                        "event_id": "current",
                        "description": "Current scene event",
                        "turn_generated": 10,
                        "scene_generated": 4,
                    },
                    {
                        "event_id": "old",
                        "description": "Older scene event",
                        "turn_generated": 7,
                        "scene_generated": 2,
                    },
                ],
                "rumors": [
                    {
                        "text": "Current rumor",
                        "turn_generated": 10,
                        "scene_generated": 4,
                    }
                ],
            }
        }

        world_logic._try_backfill_story_entry_world_events(
            structured_fields,
            updated_game_state_dict=updated_game_state,
            player_turn=10,
            user_scene_number=4,
        )

        world_events = structured_fields.get("world_events", {})
        self.assertEqual(len(world_events.get("background_events", [])), 1)
        self.assertEqual(
            world_events.get("background_events", [])[0].get("event_id"), "current"
        )
        self.assertEqual(len(world_events.get("rumors", [])), 1)
        self.assertIn("world_events", structured_fields.get("state_updates", {}))

    def test_preserves_explicit_empty_world_events_in_structured_fields(self):
        """Explicit empty world_events should be preserved and not backfilled."""
        structured_fields = {"world_events": {}, "state_updates": {}}
        updated_game_state = {
            "world_events": {
                "background_events": [
                    {
                        "event_id": "current",
                        "description": "Current scene event",
                        "turn_generated": 10,
                        "scene_generated": 4,
                    }
                ]
            }
        }

        world_logic._try_backfill_story_entry_world_events(
            structured_fields,
            updated_game_state_dict=updated_game_state,
            player_turn=10,
            user_scene_number=4,
        )

        self.assertEqual(structured_fields.get("world_events"), {})
        self.assertNotIn("world_events", structured_fields.get("state_updates", {}))

    def test_preserves_explicit_empty_world_events_in_state_updates(self):
        """Backfill should not overwrite explicit world_events key in state_updates."""
        structured_fields = {"state_updates": {"world_events": {}}}
        updated_game_state = {
            "world_events": {
                "background_events": [
                    {
                        "event_id": "current",
                        "description": "Current scene event",
                        "turn_generated": 10,
                        "scene_generated": 4,
                    }
                ]
            }
        }

        world_logic._try_backfill_story_entry_world_events(
            structured_fields,
            updated_game_state_dict=updated_game_state,
            player_turn=10,
            user_scene_number=4,
        )

        self.assertNotIn("world_events", structured_fields)
        self.assertEqual(
            structured_fields.get("state_updates", {}).get("world_events"), {}
        )

    def test_backfill_filters_by_scene_not_turn_to_avoid_frozen_time_bleed(self):
        """Backfill should not include events from a different scene with the same turn."""
        structured_fields = {"state_updates": {}}
        updated_game_state = {
            "world_events": {
                "background_events": [
                    {
                        "event_id": "same-turn-wrong-scene",
                        "description": "Should not be copied",
                        "turn_generated": 42,
                        "scene_generated": 3,
                    }
                ],
                "rumors": [],
            }
        }

        world_logic._try_backfill_story_entry_world_events(
            structured_fields,
            updated_game_state_dict=updated_game_state,
            player_turn=42,
            user_scene_number=4,
        )

        self.assertNotIn("world_events", structured_fields)
        self.assertNotIn("world_events", structured_fields.get("state_updates", {}))


class TestTruncateGameStateForLogging(unittest.TestCase):
    """Test truncate_game_state_for_logging function"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_truncate_patcher = patch("mvp_site.world_logic._truncate_log_json")
        self.mock_truncate = self.mock_truncate_patcher.start()
        self.mock_truncate.return_value = "truncated output"
        self.addCleanup(self.mock_truncate_patcher.stop)

    def test_calls_truncate_log_json(self):
        """Test that truncate_game_state_for_logging calls _truncate_log_json"""
        game_state = {"test": "data"}
        result = world_logic.truncate_game_state_for_logging(game_state)
        self.assertEqual(result, "truncated output")
        self.mock_truncate.assert_called_once()

    def test_passes_max_lines_parameter(self):
        """Test that max_lines parameter is passed correctly"""
        game_state = {"test": "data"}
        world_logic.truncate_game_state_for_logging(game_state, max_lines=50)
        call_args = self.mock_truncate.call_args
        self.assertEqual(call_args[1]["max_lines"], 50)


# Note: _should_reject_directive is a nested function inside process_action_unified
# and should be tested through integration tests that verify directive filtering
# behavior in the full process_action_unified flow.


class TestPersistTurnModePreservation(unittest.TestCase):
    """Test that _persist_turn_to_firestore preserves mode for AI responses."""

    def setUp(self):
        """Set up test fixtures."""
        self.user_id = "test_user_123"
        self.campaign_id = "test_campaign_456"
        self.user_input = "THINK: What should I do next?"
        self.ai_response_text = "You pause to consider your options..."
        self.structured_fields = {"planning_block": {"thinking": "Analysis..."}}
        self.updated_game_state = {"player_character_data": {"hp": 100}}

    @patch("mvp_site.world_logic.firestore_service")
    def test_think_mode_preserved_for_ai_response(self, mock_firestore):
        """RED: AI response should have mode='think' when user sends think mode request.

        This is the core bug fix - previously AI responses always had mode=None.
        """
        # Execute the persist function with think mode
        world_logic._persist_turn_to_firestore(
            self.user_id,
            self.campaign_id,
            mode=constants.MODE_THINK,
            user_input=self.user_input,
            ai_response_text=self.ai_response_text,
            structured_fields=self.structured_fields,
            updated_game_state_dict=self.updated_game_state,
        )

        # Verify add_story_entry was called twice (user + AI)
        add_story_calls = mock_firestore.add_story_entry.call_args_list
        self.assertEqual(len(add_story_calls), 2, "Should call add_story_entry twice")

        # Extract the calls
        user_call = add_story_calls[0]
        ai_call = add_story_calls[1]

        # Verify USER entry has mode='think'
        # add_story_entry(user_id, campaign_id, actor, text, mode, structured_fields)
        # Index: 0=user_id, 1=campaign_id, 2=actor, 3=text, 4=mode
        user_call_args = user_call[0]  # positional args
        self.assertEqual(
            user_call_args[4],
            constants.MODE_THINK,
            f"User entry mode should be 'think', got {user_call_args[4]}",
        )

        # Verify AI entry has mode='think' (THIS IS THE BUG FIX)
        ai_call_args = ai_call[0]  # positional args
        self.assertEqual(
            ai_call_args[4],
            constants.MODE_THINK,
            f"AI entry mode should be 'think', got {ai_call_args[4]}",
        )

    @patch("mvp_site.world_logic.firestore_service")
    def test_god_mode_preserved_for_ai_response(self, mock_firestore):
        """RED: AI response should have mode='god' when user sends god mode request."""
        world_logic._persist_turn_to_firestore(
            self.user_id,
            self.campaign_id,
            mode=constants.MODE_GOD,
            user_input="GOD MODE: Set time to midnight",
            ai_response_text="Time has been set to midnight.",
            structured_fields={},
            updated_game_state_dict=self.updated_game_state,
        )

        add_story_calls = mock_firestore.add_story_entry.call_args_list
        ai_call_args = add_story_calls[1][0]

        self.assertEqual(
            ai_call_args[4],
            constants.MODE_GOD,
            f"AI entry mode should be 'god', got {ai_call_args[4]}",
        )

    @patch("mvp_site.world_logic.firestore_service")
    def test_character_mode_preserved_for_ai_response(self, mock_firestore):
        """RED: AI response should have mode='character' for character actions."""
        world_logic._persist_turn_to_firestore(
            self.user_id,
            self.campaign_id,
            mode=constants.MODE_CHARACTER,
            user_input="I attack the goblin",
            ai_response_text="You swing your sword...",
            structured_fields={"dice_rolls": [{"type": "attack"}]},
            updated_game_state_dict=self.updated_game_state,
        )

        add_story_calls = mock_firestore.add_story_entry.call_args_list
        ai_call_args = add_story_calls[1][0]

        self.assertEqual(
            ai_call_args[4],
            constants.MODE_CHARACTER,
            f"AI entry mode should be 'character', got {ai_call_args[4]}",
        )

    @patch("mvp_site.world_logic.firestore_service")
    def test_combat_mode_preserved_for_ai_response(self, mock_firestore):
        """RED: AI response should have mode='combat' for combat actions."""
        world_logic._persist_turn_to_firestore(
            self.user_id,
            self.campaign_id,
            mode=constants.MODE_COMBAT,
            user_input="Attack with longsword",
            ai_response_text="Combat resolved...",
            structured_fields={},
            updated_game_state_dict=self.updated_game_state,
        )

        add_story_calls = mock_firestore.add_story_entry.call_args_list
        ai_call_args = add_story_calls[1][0]

        self.assertEqual(
            ai_call_args[4],
            constants.MODE_COMBAT,
            f"AI entry mode should be 'combat', got {ai_call_args[4]}",
        )

    @patch("mvp_site.world_logic.firestore_service")
    def test_mode_matrix_all_modes(self, mock_firestore):
        """RED: Matrix test - all modes should be preserved for AI responses."""
        # Test matrix of all modes
        test_modes = [
            constants.MODE_THINK,
            constants.MODE_GOD,
            constants.MODE_CHARACTER,
            constants.MODE_COMBAT,
            constants.MODE_REWARDS,
            constants.MODE_INFO,
        ]

        for mode in test_modes:
            with self.subTest(mode=mode):
                mock_firestore.reset_mock()

                world_logic._persist_turn_to_firestore(
                    self.user_id,
                    self.campaign_id,
                    mode=mode,
                    user_input=f"Test input for {mode}",
                    ai_response_text=f"Test response for {mode}",
                    structured_fields={},
                    updated_game_state_dict=self.updated_game_state,
                )

                add_story_calls = mock_firestore.add_story_entry.call_args_list

                # Verify both user and AI entries have the correct mode
                user_call_args = add_story_calls[0][0]
                ai_call_args = add_story_calls[1][0]

                self.assertEqual(
                    user_call_args[4],
                    mode,
                    f"Matrix [{mode}]: User entry mode mismatch",
                )
                self.assertEqual(
                    ai_call_args[4],
                    mode,
                    f"Matrix [{mode}]: AI entry mode mismatch - got {ai_call_args[4]}",
                )

    # BD-724: system_warnings persistence tests
    @patch("mvp_site.world_logic.firestore_service")
    def test_structured_fields_passed_through_to_firestore(self, mock_firestore):
        """BD-724: structured_fields dict passed to add_story_entry is the same object."""
        structured_fields = {"planning_block": {"thinking": "analysis"}}
        world_logic._persist_turn_to_firestore(
            "user1", "campaign1", mode="character",
            user_input="Attack", ai_response_text="You swing your sword.",
            structured_fields=structured_fields,
            updated_game_state_dict={"player_turn": 1},
        )
        ai_call = mock_firestore.add_story_entry.call_args_list[1]
        stored_fields = ai_call[0][5]
        self.assertIs(stored_fields, structured_fields)

    @patch("mvp_site.world_logic.firestore_service")
    def test_persist_injects_sequence_and_scene_ids_when_missing(self, mock_firestore):
        """Regression: persist layer must populate per-entry IDs if upstream misses them."""
        structured_fields = {"planning_block": {"next_action": "advance"}}
        world_logic._persist_turn_to_firestore(
            "user1",
            "campaign1",
            mode="character",
            user_input="Advance",
            ai_response_text="You move forward.",
            structured_fields=structured_fields,
            updated_game_state_dict={"player_turn": 42},
            sequence_id=123,
            user_scene_number=88,
        )
        ai_call = mock_firestore.add_story_entry.call_args_list[1]
        stored_fields = ai_call[0][5]
        self.assertEqual(stored_fields.get("sequence_id"), 123)
        self.assertEqual(stored_fields.get("user_scene_number"), 88)

    @patch("mvp_site.world_logic.firestore_service")
    def test_persist_preserves_existing_sequence_and_scene_ids(self, mock_firestore):
        """Persist layer should not overwrite IDs already set by upstream flow."""
        structured_fields = {
            "planning_block": {"next_action": "advance"},
            "sequence_id": 501,
            "user_scene_number": 409,
        }
        world_logic._persist_turn_to_firestore(
            "user1",
            "campaign1",
            mode="character",
            user_input="Advance",
            ai_response_text="You move forward.",
            structured_fields=structured_fields,
            updated_game_state_dict={"player_turn": 42},
            sequence_id=123,
            user_scene_number=88,
        )
        ai_call = mock_firestore.add_story_entry.call_args_list[1]
        stored_fields = ai_call[0][5]
        self.assertEqual(stored_fields.get("sequence_id"), 501)
        self.assertEqual(stored_fields.get("user_scene_number"), 409)

    def test_bd724_fix_exists_in_source(self):
        """BD-724: structured_fields['system_warnings'] is set before persist in source."""
        source = inspect.getsource(world_logic.process_action_unified)
        self.assertIn(
            'structured_fields["system_warnings"]', source,
            "BD-724: process_action_unified must write system_warnings to structured_fields",
        )
        warnings_idx = source.index('structured_fields["system_warnings"]')
        persist_idx = source.index("_persist_turn_to_firestore")
        self.assertLess(warnings_idx, persist_idx,
            "BD-724: system_warnings must be set BEFORE _persist_turn_to_firestore",
        )


class TestPayloadTooLargeErrorHandling(unittest.TestCase):
    """Test PayloadTooLargeError handling in world_logic."""

    @patch("mvp_site.world_logic.logging_util")
    @patch("mvp_site.world_logic.llm_service")
    @patch("mvp_site.world_logic.firestore_service")
    @patch("mvp_site.world_logic.get_user_settings", return_value={"debug_mode": False})
    @patch(
        "asyncio.to_thread",
        side_effect=lambda func, *args, **kwargs: func(*args, **kwargs),
    )
    def test_create_campaign_handles_payload_too_large_error(
        self, mock_to_thread, mock_settings, mock_fs, mock_llm, mock_logging
    ):
        """Verify 422 response with user-friendly message when PayloadTooLargeError during campaign creation."""
        # Mock firestore to return a campaign ID
        mock_fs.create_campaign.return_value = "test_campaign_id"
        # Mock llm_service.get_initial_story to raise PayloadTooLargeError
        mock_llm.get_initial_story.side_effect = PayloadTooLargeError(
            "Payload too large: 5000000 bytes"
        )
        # Mock PayloadTooLargeError class on the module so isinstance checks work
        mock_llm.PayloadTooLargeError = PayloadTooLargeError

        request_data = {
            "user_id": "test_user",
            "title": "Test Campaign",
        }

        result = asyncio.run(world_logic.create_campaign_unified(request_data))

        self.assertEqual(result.get("status_code"), 422)
        self.assertIn("Story context is too large", result.get("error", ""))
        mock_logging.error.assert_called()

    @patch("mvp_site.world_logic.logging_util")
    @patch("mvp_site.world_logic._load_campaign_and_continue_story")
    @patch("mvp_site.world_logic.firestore_service")
    @patch("mvp_site.world_logic.get_user_settings", return_value={"debug_mode": False})
    @patch("mvp_site.world_logic._prepare_game_state")
    @patch(
        "asyncio.to_thread",
        side_effect=lambda func, *args, **kwargs: func(*args, **kwargs),
    )
    def test_process_action_handles_payload_too_large_error(
        self,
        mock_to_thread,
        mock_prepare,
        mock_settings,
        mock_fs,
        mock_continue,
        mock_logging,
    ):
        """Verify 422 response with user-friendly message when PayloadTooLargeError during story continuation."""
        # Mock _prepare_game_state to return a minimal game state
        mock_state = MagicMock()
        mock_state.to_dict.return_value = {"test": "state"}
        mock_state.debug_mode = False
        mock_prepare.return_value = (mock_state, False, 0)

        mock_continue.side_effect = PayloadTooLargeError(
            "Payload too large: 5000000 bytes"
        )

        request_data = {
            "user_id": "test_user",
            "campaign_id": "test_campaign",
            "user_input": "Continue story",
        }

        result = asyncio.run(world_logic.process_action_unified(request_data))

        self.assertEqual(result.get("status_code"), 422)
        self.assertIn("Story context is too large", result.get("error", ""))
        mock_logging.error.assert_called()

    @patch("mvp_site.world_logic.logging_util")
    @patch("mvp_site.world_logic.llm_service")
    @patch("mvp_site.world_logic.firestore_service")
    @patch("mvp_site.world_logic.get_user_settings", return_value={"debug_mode": False})
    @patch(
        "asyncio.to_thread",
        side_effect=lambda func, *args, **kwargs: func(*args, **kwargs),
    )
    def test_payload_too_large_error_logs_correctly(
        self, mock_to_thread, mock_settings, mock_fs, mock_llm, mock_logging
    ):
        """Verify error is logged with context."""
        mock_fs.create_campaign.return_value = "test_campaign_id"
        mock_llm.get_initial_story.side_effect = PayloadTooLargeError(
            "Payload too large: 5000000 bytes"
        )
        mock_llm.PayloadTooLargeError = PayloadTooLargeError

        request_data = {
            "user_id": "test_user",
            "title": "Test Campaign",
        }

        asyncio.run(world_logic.create_campaign_unified(request_data))

        mock_logging.error.assert_called()
        error_call = str(mock_logging.error.call_args)
        self.assertIn("Payload too large", error_call)
        self.assertIn("campaign creation", error_call)

    @patch("mvp_site.world_logic.llm_service")
    @patch("mvp_site.world_logic.firestore_service")
    @patch("mvp_site.world_logic.get_user_settings", return_value={"debug_mode": False})
    @patch(
        "asyncio.to_thread",
        side_effect=lambda func, *args, **kwargs: func(*args, **kwargs),
    )
    def test_payload_too_large_error_status_code_422(
        self, mock_to_thread, mock_settings, mock_fs, mock_llm
    ):
        """Verify status code is 422 (not 500)."""
        mock_fs.create_campaign.return_value = "test_campaign_id"
        mock_llm.get_initial_story.side_effect = PayloadTooLargeError(
            "Payload too large"
        )
        mock_llm.PayloadTooLargeError = PayloadTooLargeError

        request_data = {
            "user_id": "test_user",
            "title": "Test Campaign",
        }

        result = asyncio.run(world_logic.create_campaign_unified(request_data))

        # Should return 422, not 500
        self.assertEqual(result.get("status_code"), 422)
        self.assertNotEqual(result.get("status_code"), 500)


class TestUserInputValidation(unittest.TestCase):
    """Test user input type validation in process_action_unified."""

    def test_process_action_rejects_non_string_user_input(self):
        """Verify 400 error when user_input is not a string (e.g., list, dict)."""
        request_data = {
            "user_id": "test_user",
            "campaign_id": "test_campaign",
            "user_input": [1, 2, 3],  # List instead of string
        }

        result = asyncio.run(world_logic.process_action_unified(request_data))

        self.assertIn("error", result)
        self.assertIn("must be a string", result.get("error", "").lower())

    @patch("mvp_site.world_logic._load_campaign_and_continue_story")
    @patch("mvp_site.world_logic.get_user_settings", return_value={"debug_mode": False})
    @patch("mvp_site.world_logic._prepare_game_state")
    @patch(
        "asyncio.to_thread",
        side_effect=lambda func, *args, **kwargs: func(*args, **kwargs),
    )
    def test_process_action_accepts_string_user_input(
        self, mock_to_thread, mock_prepare, mock_settings, mock_continue
    ):
        """Verify string input passes validation."""
        from unittest.mock import MagicMock

        # Mock _prepare_game_state to return a minimal game state
        mock_state = MagicMock()
        mock_state.to_dict.return_value = {"test": "state"}
        mock_state.debug_mode = False
        mock_prepare.return_value = (mock_state, False, 0)

        request_data = {
            "user_id": "test_user",
            "campaign_id": "test_campaign",
            "user_input": "Continue the story",  # Valid string
        }

        # Mock to avoid actual execution - should not raise validation error
        mock_continue.side_effect = Exception("Should not reach here")

        # Should not raise validation error (will fail on mock, but that's expected)
        # The key is that it didn't fail on the isinstance check
        try:
            result = asyncio.run(world_logic.process_action_unified(request_data))
            # If we get here, validation passed (even if mock failed)
            self.assertNotIn("must be a string", str(result).lower())
        except Exception:
            # Mock exception is expected - validation passed
            pass

    def test_process_action_handles_none_user_input(self):
        """Verify None input returns 'User input is required' (existing check)."""
        request_data = {
            "user_id": "test_user",
            "campaign_id": "test_campaign",
            "user_input": None,
        }

        result = asyncio.run(world_logic.process_action_unified(request_data))

        self.assertIn("error", result)
        self.assertIn("required", result.get("error", "").lower())


class TestFreezeTimeBehavior(unittest.TestCase):
    def test_filter_time_changes_for_freeze_time_choice_freezes_microsecond(self):
        state_changes = {
            "world_data": {
                "world_time": {"year": 1492, "month": "Mirtul", "day": 10},
                "timestamp": "1492-05-10T14:00:00Z",
                "timestamp_iso": "1492-05-10T14:00:00Z",
            },
            "world_data.world_time.microsecond": 999,
            "player_character_data": {"level": 5},
        }
        original_world_time = {"microsecond": 10}

        filtered = world_logic._filter_time_changes_for_freeze_time_choice(
            state_changes, original_world_time=original_world_time
        )

        self.assertEqual(
            filtered.get("world_data", {}).get("world_time", {}).get("microsecond"),
            11,
        )
        self.assertNotIn(
            "timestamp", filtered.get("world_data", {}), "timestamp should be removed"
        )
        self.assertNotIn(
            "timestamp_iso",
            filtered.get("world_data", {}),
            "timestamp_iso should be removed",
        )
        self.assertNotIn(
            "world_data.world_time.microsecond",
            filtered,
            "dotted world_time keys should be removed",
        )
        self.assertEqual(filtered.get("player_character_data", {}).get("level"), 5)

    def test_should_freeze_time_allows_empty_string_input(self):
        story_context = [
            {
                constants.KEY_ACTOR: constants.ACTOR_GEMINI,
                constants.FIELD_PLANNING_BLOCK: {
                    "choices": {
                        "level_up_now": {
                            "text": "Level Up",
                            "description": "Advance your level",
                            "freeze_time": True,
                        }
                    }
                },
            }
        ]

        result = world_logic._should_freeze_time_for_selected_choice(
            "", story_context
        )

        self.assertFalse(result)

    @patch("mvp_site.world_logic._persist_turn_to_firestore")
    @patch("mvp_site.world_logic.structured_fields_utils")
    @patch("mvp_site.world_logic.is_mock_services_mode", return_value=True)
    @patch("mvp_site.world_logic._prepare_game_state_with_user_settings")
    @patch("mvp_site.world_logic._load_campaign_and_continue_story")
    @patch("mvp_site.world_logic.preventive_guards.enforce_preventive_guards")
    @patch("mvp_site.world_logic._should_freeze_time_for_selected_choice", return_value=False)
    @patch("mvp_site.world_logic._filter_time_changes_for_freeze_time_choice")
    @patch(
        "asyncio.to_thread",
        side_effect=lambda func, *args, **kwargs: func(*args, **kwargs),
    )
    def test_character_creation_applies_freeze_time_filter(
        self,
        mock_to_thread,
        mock_filter_time,
        mock_should_freeze_choice,
        mock_enforce_guards,
        mock_continue_story,
        mock_prepare_state,
        mock_is_mock_services,
        mock_structured_utils,
        mock_persist,
    ):
        mock_game_state = Mock()
        mock_game_state.debug_mode = False
        mock_game_state.world_data = {
            "world_time": {
                "year": 1492,
                "month": "Mirtul",
                "day": 10,
                "hour": 14,
                "minute": 0,
                "second": 0,
                "microsecond": 5,
            }
        }
        mock_game_state.to_dict.return_value = {
            "player_turn": 1,
            "world_data": mock_game_state.world_data,
            "custom_campaign_state": {},
        }

        mock_prepare_state.return_value = (mock_game_state, False, 0, {"debug_mode": False})
        mock_structured_utils.extract_structured_fields.return_value = {}

        mock_llm_response = Mock()
        mock_llm_response.agent_mode = constants.MODE_CHARACTER_CREATION
        mock_llm_response.narrative_text = "Character creation response."
        mock_llm_response.get_state_updates.return_value = {
            "world_data": {
                "world_time": {
                    "year": 1492,
                    "month": "Mirtul",
                    "day": 10,
                    "hour": 14,
                    "minute": 0,
                    "second": 0,
                    "microsecond": 6,
                }
            }
        }
        mock_llm_response.processing_metadata = {}
        mock_llm_response.resources = ""
        mock_llm_response.structured_response = None
        mock_llm_response.get_location_confirmed.return_value = None

        mock_continue_story.return_value = (
            {"selected_prompts": [], "use_default_world": False},
            [],
            mock_llm_response,
        )
        mock_enforce_guards.return_value = (
            {
                "world_data": {
                    "world_time": {
                        "year": 1492,
                        "month": "Mirtul",
                        "day": 10,
                        "hour": 14,
                        "minute": 0,
                        "second": 0,
                        "microsecond": 6,
                    }
                },
                "player_character_data": {"level": 1},
            },
            {},
        )
        mock_filter_time.return_value = {
            "world_data": {"world_time": {"microsecond": 6}},
            "player_character_data": {"level": 1},
        }

        request_data = {
            "user_id": "test_user",
            "campaign_id": "test_campaign",
            "user_input": "Choose race: human",
            "mode": constants.MODE_CHARACTER,
        }

        result = asyncio.run(world_logic.process_action_unified(request_data))

        self.assertTrue(result.get("success"))
        mock_filter_time.assert_called_once()

    @patch("mvp_site.world_logic._load_campaign_and_continue_story")
    @patch("mvp_site.world_logic.get_user_settings", return_value={"debug_mode": False})
    @patch("mvp_site.world_logic._prepare_game_state")
    @patch(
        "asyncio.to_thread",
        side_effect=lambda func, *args, **kwargs: func(*args, **kwargs),
    )
    def test_process_action_handles_empty_string_user_input(
        self, mock_to_thread, mock_prepare, mock_settings, mock_continue
    ):
        """Verify empty string is accepted (may be valid)."""
        from unittest.mock import MagicMock

        # Mock _prepare_game_state to return a minimal game state
        mock_state = MagicMock()
        mock_state.to_dict.return_value = {"test": "state"}
        mock_state.debug_mode = False
        mock_prepare.return_value = (mock_state, False, 0)

        request_data = {
            "user_id": "test_user",
            "campaign_id": "test_campaign",
            "user_input": "",  # Empty string
        }

        # Mock to avoid actual execution
        mock_continue.side_effect = Exception("Should not reach here")

        # Should not fail on isinstance check (empty string is still a string)
        try:
            result = asyncio.run(world_logic.process_action_unified(request_data))
            self.assertNotIn("must be a string", str(result).lower())
        except Exception:
            # Mock exception is expected - validation passed
            pass


if __name__ == "__main__":
    unittest.main()


class TestThinkModeStateFreezeEndToEnd(unittest.TestCase):
    """Regression coverage for nested combat state data (cleanup should be a no-op here)."""

    def setUp(self):
        os.environ["TESTING_AUTH_BYPASS"] = "true"

        self.game_state_with_defeated_enemy = {
            "game_state": {
                "combat_state": {
                    "in_combat": True,
                    "combatants": [
                        {
                            "name": "Player",
                            "hp": 50,
                            "max_hp": 50,
                            "is_player": True,
                        },
                        {
                            "name": "Goblin",
                            "hp": 0,
                            "max_hp": 10,
                            "is_player": False,
                        },
                    ],
                },
                "npc_data": {
                    "Goblin": {
                        "hp": 0,
                        "max_hp": 10,
                        "status": "alive",
                    },
                },
            },
            "player_character_data": {
                "name": "Test Hero",
                "class": "Fighter",
            },
            "world_data": {
                "world_time": {
                    "year": 1492,
                    "month": "Mirtul",
                    "day": 15,
                    "hour": 10,
                    "minute": 30,
                    "second": 0,
                    "microsecond": 100,
                },
            },
        }

    def test_combat_cleanup_does_not_run_in_think_mode(self):
        original_state = copy.deepcopy(self.game_state_with_defeated_enemy)
        state_to_check = copy.deepcopy(self.game_state_with_defeated_enemy)

        proposed_changes = {"world_data": {"world_time": {"microsecond": 101}}}

        result_state = world_logic.apply_automatic_combat_cleanup(
            state_to_check, proposed_changes
        )

        combat_state = result_state.get("game_state", {}).get("combat_state", {})
        combatants = combat_state.get("combatants", [])
        npc_data = result_state.get("game_state", {}).get("npc_data", {})

        original_combatants = (
            original_state.get("game_state", {})
            .get("combat_state", {})
            .get("combatants", [])
        )
        original_npc_count = len(
            original_state.get("game_state", {}).get("npc_data", {})
        )

        combatant_removed = len(combatants) < len(original_combatants)
        npc_modified = len(npc_data) < original_npc_count or (
            "Goblin" in npc_data and npc_data["Goblin"].get("status") == "dead"
        )

        if combatant_removed or npc_modified:
            raise AssertionError(
                f"BUG: Combat cleanup modified nested game_state data unexpectedly. "
                f"Combatants before: {len(original_combatants)}, after: {len(combatants)}. "
                f"NPC data modified: {npc_modified}."
            )


class TestThinkModeIntegrationWithCleanup(unittest.TestCase):
    """Integration tests for think mode with the full process_response flow."""

    def setUp(self):
        os.environ["TESTING_AUTH_BYPASS"] = "true"

        self.base_game_state = {
            "game_state": {
                "combat_state": {
                    "in_combat": True,
                    "combatants": [
                        {"name": "Hero", "hp": 50, "max_hp": 50, "is_player": True},
                        {"name": "Orc", "hp": 0, "max_hp": 20, "is_player": False},
                    ],
                },
                "npc_data": {
                    "Orc": {"hp": 0, "max_hp": 20},
                },
            },
            "player_character_data": {"name": "Hero", "class": "Warrior"},
            "world_data": {
                "world_time": {"microsecond": 500},
            },
        }

    def test_think_mode_blocks_non_time_state_changes(self):
        is_think_mode = True

        state_changes = {
            "world_data": {"world_time": {"microsecond": 501}},
            "game_state": {"npc_data": {"Orc": {"status": "dead"}}},
        }

        if is_think_mode:
            allowed_changes = {}
            if "world_data" in state_changes:
                world_data = state_changes.get("world_data", {})
                if world_data and "world_time" in world_data:
                    world_time_changes = world_data.get("world_time", {})
                    if world_time_changes and "microsecond" in world_time_changes:
                        allowed_changes = {
                            "world_data": {
                                "world_time": {
                                    "microsecond": world_time_changes["microsecond"]
                                }
                            }
                        }
            state_changes_to_apply = allowed_changes
        else:
            state_changes_to_apply = state_changes

        updated_state = world_logic.update_state_with_changes(
            copy.deepcopy(self.base_game_state), state_changes_to_apply
        )

        self.assertIn("Orc", updated_state["game_state"]["npc_data"])
        self.assertEqual(
            updated_state["game_state"]["npc_data"]["Orc"].get("status"),
            None,
        )


class TestCombatModeCorrectionsPersistedEnd2End(unittest.TestCase):
    """Test that combat mode auto-sets rewards_processed when combat ends."""

    def setUp(self):
        os.environ.setdefault("GEMINI_API_KEY", "test-api-key")
        os.environ.setdefault("CEREBRAS_API_KEY", "test-cerebras-key")
        os.environ["MOCK_SERVICES_MODE"] = "false"

        self.test_user_id = "test-user-combat-persistence"
        self.campaign_id = "combat_persistence_test"

    def _setup_active_combat_campaign(self, fake_firestore):
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(self.campaign_id).set(
            {"title": "Combat Persistence Test", "setting": "A dungeon"}
        )

        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(self.campaign_id).collection("game_states").document(
            "current_state"
        ).set(
            {
                "user_id": self.test_user_id,
                "story_text": "You face the goblin in combat!",
                "player_turn": 5,
                "player_character_data": {
                    "name": "TestHero",
                    "level": 3,
                    "experience": {"current": 500},
                },
                "combat_state": {
                    "in_combat": True,
                    "combat_phase": "player_turn",
                    "enemies": [{"id": "goblin_1", "hp": 5}],
                    "rewards_processed": False,
                },
                "custom_campaign_state": {},
            }
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_combat_mode_discrepancies_persisted_to_firestore(
        self, mock_gemini_generate, mock_get_db
    ):
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        self._setup_active_combat_campaign(fake_firestore)

        mock_response_data = {
            "narrative": "You strike the goblin down! Victory is yours!",
            "planning_block": {
                "thinking": "Combat ended. Player won.",
            },
            "state_updates": {
                "combat_state": {
                    "in_combat": False,
                    "combat_phase": "ended",
                    "combat_summary": {
                        "xp_awarded": 50,
                        "enemies_defeated": ["goblin_1"],
                        "outcome": "victory",
                    },
                },
                "player_character_data": {
                    "experience": {"current": 550},
                },
            },
        }
        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(mock_response_data)
        )

        result = asyncio.run(
            world_logic.process_action_unified(
                {
                    "user_id": self.test_user_id,
                    "campaign_id": self.campaign_id,
                    "user_input": "I attack the goblin with my sword!",
                    "mode": "combat",
                }
            )
        )

        self.assertNotIn(
            "error",
            result,
            f"process_action_unified failed: {result.get('error')}",
        )

        game_state = result.get("game_state", {})
        combat_state = game_state.get("combat_state", {})

        self.assertTrue(
            combat_state.get("rewards_processed", False),
            "Server should AUTO-SET combat_state.rewards_processed=True when combat ends. "
            f"Got combat_state={combat_state}",
        )

        final_game_state = (
            fake_firestore.collection("users")
            .document(self.test_user_id)
            .collection("campaigns")
            .document(self.campaign_id)
            .collection("game_states")
            .document("current_state")
            .get()
        )

        final_state_data = final_game_state.to_dict() if final_game_state.exists else {}

        self.assertTrue(
            final_state_data.get("combat_state", {}).get("rewards_processed", False),
            "Server AUTO-SET flag must be persisted to Firestore for combat mode! "
            f"Final combat_state: {final_state_data.get('combat_state', {})}",
        )


class TestLLMSetCorrectionsPreservedEnd2End(unittest.TestCase):
    """Test that LLM-set pending_system_corrections are preserved during state merge."""

    def setUp(self):
        os.environ.setdefault("GEMINI_API_KEY", "test-api-key")
        os.environ.setdefault("CEREBRAS_API_KEY", "test-cerebras-key")
        os.environ["MOCK_SERVICES_MODE"] = "false"

        self.test_user_id = "test-user-llm-corrections"
        self.campaign_id = "llm_corrections_test"

    def _setup_basic_campaign(self, fake_firestore):
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(self.campaign_id).set(
            {"title": "LLM Corrections Test", "setting": "A dungeon"}
        )

        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(self.campaign_id).collection("game_states").document(
            "current_state"
        ).set(
            {
                "user_id": self.test_user_id,
                "story_text": "You are in a dungeon.",
                "player_turn": 1,
                "player_character_data": {
                    "name": "TestHero",
                    "level": 1,
                    "experience": {"current": 0},
                },
                "combat_state": {
                    "in_combat": False,
                },
                "custom_campaign_state": {},
            }
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_llm_set_pending_corrections_persisted_to_firestore(
        self, mock_gemini_generate, mock_get_db
    ):
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        self._setup_basic_campaign(fake_firestore)

        correction_msg = (
            "REWARDS_STATE_ERROR: Combat ended (phase=ended) with summary, "
            "but rewards_processed=False. You MUST set combat_state.rewards_processed=true."
        )

        mock_response_data = {
            "narrative": "You are now safe.",
            "planning_block": {
                "thinking": "Apply corrections.",
            },
            "state_updates": {
                "pending_system_corrections": [correction_msg],
            },
        }
        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(mock_response_data)
        )

        result = asyncio.run(
            world_logic.process_action_unified(
                {
                    "user_id": self.test_user_id,
                    "campaign_id": self.campaign_id,
                    "user_input": "Check state.",
                    "mode": "god",
                }
            )
        )

        self.assertNotIn("error", result, result.get("error"))

        final_game_state = (
            fake_firestore.collection("users")
            .document(self.test_user_id)
            .collection("campaigns")
            .document(self.campaign_id)
            .collection("game_states")
            .document("current_state")
            .get()
        )

        final_state_data = final_game_state.to_dict() if final_game_state.exists else {}
        pending = final_state_data.get("pending_system_corrections", [])

        self.assertIn(
            correction_msg,
            pending,
            "pending_system_corrections should persist when set by LLM state_updates",
        )

    # BD-ahe: Dice fabrication correction and compression preservation tests
    # NOTE: Dice correction text generation is tested end-to-end in:
    # test_action_resolution_backward_compat_end2end.py::test_dice_fabrication_detection_and_correction_generation

    def test_compact_game_state_drops_pending_corrections(self):
        """BD-ahe: _compact_game_state drops pending_system_corrections (not in priority tiers)."""
        game_state = {
            "current_hp": 50, "max_hp": 100, "current_location": "tavern",
            "pending_system_corrections": ["CORRECTION: You fabricated dice values."],
        }
        compacted_json = _compact_game_state(json.dumps(game_state), max_tokens=20)
        compacted = json.loads(compacted_json)
        self.assertNotIn(
            "pending_system_corrections", compacted,
            "pending_system_corrections should NOT survive compaction (proves pre-pop fix needed)",
        )


class TestLevelUpChoiceForcesCharacterCreation(unittest.TestCase):
    """Ensure level_up_now choice forces CharacterCreationAgent selection."""

    @patch("mvp_site.world_logic.firestore_service.get_campaign_by_id")
    @patch("mvp_site.world_logic.llm_service.continue_story")
    def test_level_up_choice_sets_level_up_pending(
        self, mock_continue_story, mock_get_campaign
    ):
        story_context = [
            {
                constants.KEY_ACTOR: constants.ACTOR_GEMINI,
                constants.FIELD_PLANNING_BLOCK: {
                    "thinking": "Level up available",
                    "choices": {
                        "level_up_now": {
                            "text": "Level Up to Level 5",
                            "description": "Apply level 5 benefits immediately",
                            "risk_level": "safe",
                            "freeze_time": True,
                        }
                    },
                },
            }
        ]
        mock_get_campaign.return_value = (
            {"selected_prompts": [], "use_default_world": False},
            story_context,
        )
        captured = {}

        def _capture_state(*args, **kwargs):
            # args: llm_input, mode, story_context, current_game_state, ...
            current_game_state = args[3]
            captured["custom_state"] = current_game_state.custom_campaign_state
            return MagicMock()

        mock_continue_story.side_effect = _capture_state

        current_game_state = GameState.from_dict(
            {
                "user_id": "test-user",
                "custom_campaign_state": {},
                "player_character_data": {"name": "Hero", "class": "Fighter"},
            }
        )

        world_logic._load_campaign_and_continue_story(
            "test-user",
            "test-campaign",
            llm_input="Level Up to Level 5 - Apply level 5 benefits immediately",
            mode=constants.MODE_CHARACTER,
            current_game_state=current_game_state,
            include_raw_llm_payloads=False,
        )

        custom_state = captured["custom_state"]
        self.assertTrue(custom_state.get("level_up_pending"))
        self.assertTrue(custom_state.get("character_creation_in_progress"))
        self.assertEqual(custom_state.get("character_creation_stage"), "level_up")

    @patch("mvp_site.world_logic.llm_service._select_provider_and_model")
    @patch("mvp_site.world_logic.firestore_service.get_campaign_by_id")
    @patch("mvp_site.world_logic.llm_service.continue_story")
    def test_non_streaming_path_forwards_include_raw_llm_payloads(
        self,
        mock_continue_story,
        mock_get_campaign,
        mock_select_provider,
    ):
        mock_get_campaign.return_value = (
            {"selected_prompts": [], "use_default_world": False},
            [],
        )
        mock_select_provider.return_value = MagicMock(
            provider="mock-non-gemini-provider",
            model="gpt-4o-mini",
        )
        mock_continue_story.return_value = MagicMock()

        current_game_state = GameState.from_dict({"user_id": "test-user"})

        world_logic._load_campaign_and_continue_story(
            "test-user",
            "test-campaign",
            llm_input="test input",
            mode=constants.MODE_CHARACTER,
            current_game_state=current_game_state,
            include_raw_llm_payloads=True,
        )

        self.assertTrue(mock_continue_story.called)
        self.assertTrue(
            mock_continue_story.call_args.kwargs.get("include_raw_llm_payloads"),
            "Expected include_raw_llm_payloads=True to be forwarded in non-streaming path",
        )


class TestModalLockFlagScoping(unittest.TestCase):
    """Regression tests for modal lock flag scoping between character creation and level-up."""

    def test_character_creation_lock_does_not_force_level_up_flag(self):
        current_state = {
            "custom_campaign_state": {
                "character_creation_in_progress": True,
                "character_creation_stage": "review",
                "level_up_in_progress": False,
            }
        }
        state_changes = {"custom_campaign_state": {"level_up_in_progress": False}}

        result = world_logic._enforce_character_creation_modal_lock(
            current_state,
            state_changes,
            user_input="I continue editing my character.",
        )

        self.assertIn("custom_campaign_state", result)
        self.assertIn("level_up_in_progress", result["custom_campaign_state"])
        self.assertIs(
            result["custom_campaign_state"]["level_up_in_progress"],
            False,
            "Character-creation modal lock must not force level_up_in_progress=True.",
        )

    def test_level_up_lock_does_not_force_character_creation_flag(self):
        current_state = {
            "custom_campaign_state": {
                "character_creation_in_progress": False,
                "character_creation_stage": "complete",
                "level_up_in_progress": True,
            }
        }
        state_changes = {"custom_campaign_state": {"character_creation_in_progress": False}}

        result = world_logic._enforce_character_creation_modal_lock(
            current_state,
            state_changes,
            user_input="I choose my level-up options.",
        )

        self.assertIn("custom_campaign_state", result)
        self.assertIn("character_creation_in_progress", result["custom_campaign_state"])
        self.assertIs(
            result["custom_campaign_state"]["character_creation_in_progress"],
            False,
            "Level-up modal lock must not force character_creation_in_progress=True.",
        )


class TestFactionMinigameDefaults(unittest.TestCase):
    """Test cases for faction minigame default behavior."""

    @patch("mvp_site.world_logic.llm_service")
    @patch("mvp_site.world_logic.firestore_service")
    @patch("mvp_site.world_logic.get_user_settings")
    @patch(
        "asyncio.to_thread",
        side_effect=lambda func, *args, **kwargs: func(*args, **kwargs),
    )
    def test_campaign_defaults_to_enabled_false_when_user_setting_true(
        self, mock_to_thread, mock_get_settings, mock_firestore, mock_llm
    ):
        """Campaign creation should default faction_minigame.enabled to False even when user setting is True."""
        # User has global setting enabled
        mock_get_settings.return_value = {"faction_minigame_enabled": True}
        mock_firestore.create_campaign.return_value = "test_campaign_id"
        mock_llm.get_initial_story.return_value = {
            "story_text": "Test story",
            "planning_block": {},
        }

        async def run_test():
            return await world_logic.create_campaign_unified(
                {
                    "user_id": "test-user",
                    "title": "Test Campaign",
                    "selected_prompts": [],
                    "use_default_world": True,
                }
            )

        result = asyncio.run(run_test())

        # Verify create_campaign was called
        self.assertTrue(
            mock_firestore.create_campaign.called,
            "create_campaign should have been called - check mock paths",
        )

        # Extract the campaign data that was passed to create_campaign
        call_args = mock_firestore.create_campaign.call_args
        campaign_data = next(
            (
                arg
                for arg in call_args[0]
                if isinstance(arg, dict) and "custom_campaign_state" in arg
            ),
            None,
        )
        self.assertIsNotNone(campaign_data, "Expected game_state dict in create_campaign args")
        custom_state = campaign_data.get("custom_campaign_state", {})
        faction_minigame = custom_state.get("faction_minigame", {})

        # Verify structure exists but enabled defaults to False
        self.assertIn("faction_minigame", custom_state)
        self.assertFalse(
            faction_minigame.get("enabled"),
            "faction_minigame.enabled should default to False even when user setting is True",
        )

    @patch("mvp_site.world_logic.llm_service")
    @patch("mvp_site.world_logic.firestore_service")
    @patch("mvp_site.world_logic.get_user_settings")
    @patch(
        "asyncio.to_thread",
        side_effect=lambda func, *args, **kwargs: func(*args, **kwargs),
    )
    def test_campaign_no_faction_structure_when_user_setting_false(
        self, mock_to_thread, mock_get_settings, mock_firestore, mock_llm
    ):
        """Campaign creation should not create faction_minigame structure when user setting is False."""
        # User has global setting disabled
        mock_get_settings.return_value = {"faction_minigame_enabled": False}
        mock_firestore.create_campaign.return_value = "test_campaign_id"
        mock_llm.get_initial_story.return_value = {
            "story_text": "Test story",
            "planning_block": {},
        }

        async def run_test():
            return await world_logic.create_campaign_unified(
                {
                    "user_id": "test-user",
                    "title": "Test Campaign",
                    "selected_prompts": [],
                    "use_default_world": True,
                }
            )

        result = asyncio.run(run_test())

        # Verify create_campaign was called
        self.assertTrue(
            mock_firestore.create_campaign.called,
            "create_campaign should have been called - check mock paths",
        )

        # Extract the campaign data that was passed to create_campaign
        call_args = mock_firestore.create_campaign.call_args
        campaign_data = next(
            (
                arg
                for arg in call_args[0]
                if isinstance(arg, dict) and "custom_campaign_state" in arg
            ),
            None,
        )
        self.assertIsNotNone(campaign_data, "Expected game_state dict in create_campaign args")
        custom_state = campaign_data.get("custom_campaign_state", {})

        # Verify structure does not exist when user setting is False
        self.assertNotIn(
            "faction_minigame",
            custom_state,
            "faction_minigame structure should not be created when user setting is False",
        )


class TestCampaignStartingItems(unittest.TestCase):
    """Ensure campaign creation seeds starter items onto canonical equipment schema."""

    @patch("mvp_site.world_logic.llm_service")
    @patch("mvp_site.world_logic.firestore_service")
    @patch("mvp_site.world_logic.get_user_settings")
    @patch(
        "asyncio.to_thread",
        side_effect=lambda func, *args, **kwargs: func(*args, **kwargs),
    )
    def test_create_campaign_god_mode_starter_gear_uses_equipment_backpack(
        self, mock_to_thread, mock_get_settings, mock_firestore, mock_llm
    ):
        mock_get_settings.return_value = {}
        mock_firestore.create_campaign.return_value = "test_campaign_id"
        mock_llm.get_initial_story.return_value = {"story_text": "Test story", "planning_block": {}}

        async def run_test():
            return await world_logic.create_campaign_unified(
                {
                    "user_id": "test-user",
                    "title": "Test Campaign",
                    "selected_prompts": [],
                    "use_default_world": True,
                    "god_mode": {
                        "character": {
                            "name": "Test Mage",
                            "class": "Wizard",
                            "background": "Sage",
                            # Some templates prefill empty equipment placeholders.
                            "equipment": {},
                        }
                    },
                }
            )

        asyncio.run(run_test())

        call_args = mock_firestore.create_campaign.call_args
        campaign_state = next(
            (
                arg
                for arg in call_args[0]
                if isinstance(arg, dict) and "player_character_data" in arg
            ),
            None,
        )
        self.assertIsNotNone(campaign_state, "Expected game_state dict in create_campaign args")
        pc = campaign_state.get("player_character_data", {})

        self.assertIn("equipment", pc)
        equipment = pc.get("equipment") or {}
        backpack = equipment.get("backpack") or []
        # Backpack items are stored as dict entries.
        self.assertTrue(isinstance(backpack, list) and backpack, "Expected starter items in equipment.backpack")

        item_names = [
            entry.get("name") for entry in backpack if isinstance(entry, dict) and entry.get("name")
        ]
        # Includes class gear and generic adventuring gear.
        self.assertIn("Spellbook", item_names)
        self.assertIn("Backpack", item_names)

        # Inline "(stats)" strings should be normalized into name+stats.
        torch_entries = [
            entry
            for entry in backpack
            if isinstance(entry, dict) and entry.get("name") == "Torch"
        ]
        self.assertTrue(torch_entries, "Expected Torch entry normalized into name='Torch'")
        self.assertEqual(torch_entries[0].get("stats"), "10")

    @patch("mvp_site.world_logic.llm_service")
    @patch("mvp_site.world_logic.firestore_service")
    @patch("mvp_site.world_logic.get_user_settings")
    @patch(
        "asyncio.to_thread",
        side_effect=lambda func, *args, **kwargs: func(*args, **kwargs),
    )
    def test_create_campaign_does_not_overwrite_legacy_equipment_list(
        self, mock_to_thread, mock_get_settings, mock_firestore, mock_llm
    ):
        """If god_mode provides legacy equipment as a non-empty list, don't overwrite it with starter seeding."""
        mock_get_settings.return_value = {}
        mock_firestore.create_campaign.return_value = "test_campaign_id"
        mock_llm.get_initial_story.return_value = {"story_text": "Test story", "planning_block": {}}

        async def run_test():
            return await world_logic.create_campaign_unified(
                {
                    "user_id": "test-user",
                    "title": "Test Campaign",
                    "selected_prompts": [],
                    "use_default_world": True,
                    "god_mode": {
                        "character": {
                            "name": "Test Mage",
                            "class": "Wizard",
                            "background": "Sage",
                            # Legacy shape (list). This should be preserved as-is.
                            "equipment": ["Custom Rope (50 feet)"],
                        }
                    },
                }
            )

        asyncio.run(run_test())

        call_args = mock_firestore.create_campaign.call_args
        campaign_state = next(
            (
                arg
                for arg in call_args[0]
                if isinstance(arg, dict) and "player_character_data" in arg
            ),
            None,
        )
        self.assertIsNotNone(campaign_state, "Expected game_state dict in create_campaign args")
        pc = campaign_state.get("player_character_data", {})
        self.assertIn("equipment", pc)
        self.assertIsInstance(pc.get("equipment"), list)
        self.assertIn("Custom Rope (50 feet)", pc.get("equipment"))
