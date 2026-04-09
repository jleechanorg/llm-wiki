"""
End-to-end integration test for Agent Architecture.

Tests the agent-based mode handling (StoryModeAgent vs GodModeAgent) through
the full application stack. Verifies that:
1. Agent selection works correctly based on user input
2. Each agent builds the correct system instructions
3. Mode detection (GOD MODE: prefix) works end-to-end
4. Both agents integrate correctly with the LLM service

This test suite complements test_god_mode_end2end.py by focusing specifically
on the agent architecture rather than god mode functionality.
"""

# ruff: noqa: PT009

from __future__ import annotations

import json
import os
from pathlib import Path

# Set this before importing mvp_site modules to bypass clock skew validation
os.environ["TESTING_AUTH_BYPASS"] = "true"

import unittest
from unittest.mock import patch

from mvp_site import constants, main
from mvp_site.agents import (
    GodModeAgent,
    SpicyModeAgent,
    StoryModeAgent,
    get_agent_for_input,
)
from mvp_site.intent_classifier import ANCHOR_PHRASES
from mvp_site.tests.fake_firestore import FakeFirestoreClient
from mvp_site.tests.fake_llm import FakeLLMResponse
from mvp_site.tests.test_end2end import End2EndBaseTestCase

MVP_SITE_ROOT = Path(__file__).resolve().parents[2]


class FakeGameState:
    def __init__(
        self,
        *,
        user_settings: dict | None,
        in_combat: bool = False,
        custom_campaign_state: dict | None = None,
    ) -> None:
        self._in_combat = in_combat
        self.user_settings = user_settings
        self.data = {}
        self.dialog_context = None
        self.last_action_type = None
        self.planning_block = None
        self.custom_campaign_state = custom_campaign_state or {
            "character_creation_completed": True,
            "character_creation_in_progress": False,
        }

    def is_in_combat(self) -> bool:
        return self._in_combat

    def is_campaign_upgrade_available(self) -> bool:
        return False


def _create_fake_game_state(spicy_mode: bool, in_combat: bool = False) -> FakeGameState:
    """Helper to create a fake GameState with required methods for spicy mode tests."""
    return FakeGameState(
        user_settings={"spicy_mode": spicy_mode},
        in_combat=in_combat,
    )


class TestAgentArchitectureEnd2End(End2EndBaseTestCase):
    """Test agent architecture through the full application stack."""

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"
    TEST_USER_ID = "test-user-agent-e2e"

    def setUp(self):
        """Set up test client."""
        super().setUp()
        os.environ.setdefault("GEMINI_API_KEY", "test-api-key")
        os.environ.setdefault("CEREBRAS_API_KEY", "test-cerebras-key")
        # Disable MOCK_SERVICES_MODE to allow patching generate_json_mode_content
        os.environ["MOCK_SERVICES_MODE"] = "false"
        os.environ["ENABLE_EXPLICIT_CACHE"] = "false"

        # Standard mock story mode response
        self.mock_story_response = {
            "session_header": "[SESSION_HEADER]\nTimestamp: 1492 DR, Mirtul 10\nLocation: Forest",
            "narrative": "You walk through the dense forest, leaves crunching under your feet...",
            "entities_mentioned": ["Forest Spirit"],
            "location_confirmed": "Enchanted Forest",
            "state_updates": {},
            "planning_block": {
                "thinking": "The player is exploring the forest.",
                "choices": {
                    "continue": {
                        "text": "Continue",
                        "description": "Keep walking",
                        "risk_level": "low",
                    },
                    "rest": {
                        "text": "Rest",
                        "description": "Take a break",
                        "risk_level": "safe",
                    },
                },
            },
        }

        # Standard mock god mode response
        self.mock_god_mode_response = {
            "session_header": "[SESSION_HEADER]\nTimestamp: 1492 DR, Mirtul 10\nLocation: Forest",
            "god_mode_response": "Level has been set to 10. Character stats updated accordingly.",
            "narrative": "",
            "entities_mentioned": [],
            "location_confirmed": "Enchanted Forest",
            "state_updates": {"player_character_data": {"level": 10}},
            "planning_block": {
                "thinking": "Administrative command to modify character level.",
                "choices": {},
            },
        }

    def _setup_fake_firestore_with_campaign(
        self, fake_firestore, campaign_id, *, in_combat=False
    ):
        """Helper to set up fake Firestore with campaign and game state."""
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).set(
            {
                "title": "Agent Test Campaign",
                "setting": "Fantasy realm",
                "selected_prompts": ["narrative", "mechanics"],
            }
        )

        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).collection("game_states").document("current_state").set(
            {
                "user_id": self.test_user_id,
                "story_text": "Previous story content",
                "player_character_data": {
                    "entity_id": "player_character",
                    "display_name": "TestHero",
                    "name": "TestHero",
                    "hp_current": 30,
                    "hp_max": 30,
                    "level": 5,
                    "class_name": "Wizard",
                },
                "world_data": {
                    "current_location_name": "Enchanted Forest",
                    "world_time": {
                        "year": 1492,
                        "month": "Mirtul",
                        "day": 10,
                        "hour": 10,
                        "minute": 0,
                    },
                },
                "npc_data": {},
                "combat_state": {"in_combat": in_combat},
                "custom_campaign_state": {},
            }
        )

    # =========================================================================
    # Agent Selection Tests
    # =========================================================================

    @patch("mvp_site.firestore_service.get_db")
    @patch("mvp_site.llm_providers.gemini_provider.generate_json_mode_content")
    def test_agent_selection_via_api(
        self, mock_gemini_generate, mock_get_db
    ):
        """Test agent routing via the Flask API.

        Verifies that the API correctly routes different input types:
        - Regular inputs -> story mode (narrative response)
        - GOD MODE: prefix -> god mode (god_mode_response field)
        - THINK: prefix -> think mode (narrative with planning)
        """

        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "agent-selection-e2e"
        self._setup_fake_firestore_with_campaign(fake_firestore, campaign_id)

        mock_gemini_generate.side_effect = [
            FakeLLMResponse(json.dumps(self.mock_story_response)),
            FakeLLMResponse(json.dumps(self.mock_god_mode_response)),
            FakeLLMResponse(json.dumps(self.mock_story_response)),
        ]

        response_story = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "I explore the forest", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )
        self.assertEqual(response_story.status_code, 200)
        story_payload = json.loads(response_story.data)
        self.assertIn("narrative", story_payload)
        self.assertNotIn("god_mode_response", story_payload)

        response_god = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps(
                {"input": "GOD MODE: Set my level to 10", "mode": "character"}
            ),
            content_type="application/json",
            headers=self.test_headers,
        )
        self.assertEqual(response_god.status_code, 200)
        god_payload = json.loads(response_god.data)
        self.assertIn("god_mode_response", god_payload)

        response_think = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "THINK: plan my next move", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )
        self.assertEqual(response_think.status_code, 200)
        think_payload = json.loads(response_think.data)
        self.assertIn("narrative", think_payload)

        # Note: We don't verify classifier invocation here because mocking through
        # the Flask app boundary doesn't work reliably (singleton created during
        # app initialization). The end-to-end behavior is tested above - story mode
        # returns narratives, god mode returns god_mode_response, think mode works.
        # Unit tests in test_intent_classifier.py verify classifier behavior directly.

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_spicy_intent_overrides_dialog_context(self, mock_classify):
        """Spicy intent should bypass dialog state continuity routing."""
        mock_classify.return_value = (constants.MODE_SPICY, 0.92)
        game_state = _create_fake_game_state(spicy_mode=False, in_combat=False)
        game_state.dialog_context = {"active": True}

        agent, _ = get_agent_for_input(
            "We share a lingering, intimate kiss.",
            game_state=game_state,
        )

        self.assertIsInstance(agent, SpicyModeAgent)

    @patch("mvp_site.firestore_service.get_db")
    @patch("mvp_site.llm_providers.gemini_provider.generate_json_mode_content")
    def test_agent_selection_god_mode(self, mock_gemini_generate, mock_get_db):
        """Test that GodModeAgent is selected for GOD MODE inputs."""
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "agent-god-mode-e2e"
        self._setup_fake_firestore_with_campaign(fake_firestore, campaign_id)

        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_god_mode_response)
        )

        test_inputs = [
            "GOD MODE: Set HP to 50",
            "god mode: change my level",
            "GOD MODE: teleport me to town",
            "  GOD MODE: fix my inventory",
        ]

        for user_input in test_inputs:
            response = self.client.post(
                f"/api/campaigns/{campaign_id}/interaction",
                data=json.dumps({"input": user_input, "mode": "character"}),
                content_type="application/json",
                headers=self.test_headers,
            )
            self.assertEqual(response.status_code, 200, f"Got: {response.data}")
            payload = json.loads(response.data)
            self.assertIn("god_mode_response", payload)

    @patch("mvp_site.firestore_service.get_db")
    @patch("mvp_site.llm_providers.gemini_provider.generate_json_mode_content")
    def test_agent_selection_edge_cases(self, mock_gemini_generate, mock_get_db):
        """Test edge cases in agent selection."""
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "agent-edge-e2e"
        self._setup_fake_firestore_with_campaign(fake_firestore, campaign_id)

        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_story_response)
        )

        # These should NOT trigger god mode
        edge_cases = [
            "god",  # Just the word
            "tell me about god mode",  # Contains but doesn't start
            "GODMODE: test",  # Missing space
            "GOD_MODE: test",  # Wrong format
            "The god mode is powerful",  # In middle of text
        ]

        for user_input in edge_cases:
            response = self.client.post(
                f"/api/campaigns/{campaign_id}/interaction",
                data=json.dumps({"input": user_input, "mode": "character"}),
                content_type="application/json",
                headers=self.test_headers,
            )
            self.assertEqual(response.status_code, 200, f"Got: {response.data}")
            payload = json.loads(response.data)
            self.assertIn("narrative", payload)
            self.assertNotIn("god_mode_response", payload)

    # =========================================================================
    # Agent Prompt Set Tests
    # =========================================================================

    def test_story_mode_agent_has_correct_prompts(self):
        """Test that StoryModeAgent has the correct prompt set."""
        agent = StoryModeAgent()

        # Required prompts
        self.assertIn(constants.PROMPT_TYPE_MASTER_DIRECTIVE, agent.REQUIRED_PROMPTS)
        self.assertIn(constants.PROMPT_TYPE_GAME_STATE, agent.REQUIRED_PROMPTS)
        self.assertIn(constants.PROMPT_TYPE_DND_SRD, agent.REQUIRED_PROMPTS)

        # Optional prompts
        self.assertIn(constants.PROMPT_TYPE_NARRATIVE, agent.OPTIONAL_PROMPTS)
        self.assertIn(constants.PROMPT_TYPE_MECHANICS, agent.OPTIONAL_PROMPTS)

        # Should NOT have god mode prompt
        all_prompts = agent.get_all_prompts()
        self.assertNotIn(constants.PROMPT_TYPE_GOD_MODE, all_prompts)

    def test_god_mode_agent_has_correct_prompts(self):
        """Test that GodModeAgent has the correct prompt set."""
        agent = GodModeAgent()

        # Required prompts
        self.assertIn(constants.PROMPT_TYPE_MASTER_DIRECTIVE, agent.REQUIRED_PROMPTS)
        self.assertIn(constants.PROMPT_TYPE_GOD_MODE, agent.REQUIRED_PROMPTS)
        self.assertIn(constants.PROMPT_TYPE_GAME_STATE, agent.REQUIRED_PROMPTS)
        self.assertIn(constants.PROMPT_TYPE_DND_SRD, agent.REQUIRED_PROMPTS)
        self.assertIn(constants.PROMPT_TYPE_MECHANICS, agent.REQUIRED_PROMPTS)

        # Should NOT have narrative prompts
        all_prompts = agent.get_all_prompts()
        self.assertNotIn(constants.PROMPT_TYPE_NARRATIVE, all_prompts)
        self.assertNotIn(constants.PROMPT_TYPE_CHARACTER_TEMPLATE, all_prompts)

    # =========================================================================
    # End-to-End Flow Tests
    # =========================================================================

    @patch("mvp_site.firestore_service.get_db")
    @patch("mvp_site.llm_providers.gemini_provider.generate_json_mode_content")
    def test_story_mode_flow_end2end(self, mock_gemini_generate, mock_get_db):
        """Test that story mode works end-to-end through agent architecture."""
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_story_agent_e2e"
        self._setup_fake_firestore_with_campaign(fake_firestore, campaign_id)

        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_story_response)
        )

        # Make story mode request
        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps(
                {"input": "I explore the forest deeper", "mode": "character"}
            ),
            content_type="application/json",
            headers=self.test_headers,
        )

        self.assertEqual(response.status_code, 200, f"Got: {response.data}")
        data = json.loads(response.data)

        # Verify story mode response characteristics
        self.assertIn("narrative", data)
        self.assertGreater(
            len(data.get("narrative", "")),
            0,
            "Expected non-empty narrative in story mode response",
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch("mvp_site.llm_providers.gemini_provider.generate_json_mode_content")
    def test_god_mode_flow_end2end(self, mock_gemini_generate, mock_get_db):
        """Test that god mode works end-to-end through agent architecture."""
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_god_agent_e2e"
        self._setup_fake_firestore_with_campaign(fake_firestore, campaign_id)

        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_god_mode_response)
        )

        # Make god mode request
        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps(
                {"input": "GOD MODE: Set my level to 10", "mode": "character"}
            ),
            content_type="application/json",
            headers=self.test_headers,
        )

        self.assertEqual(response.status_code, 200, f"Got: {response.data}")
        data = json.loads(response.data)

        # Verify god mode response characteristics
        self.assertIn("god_mode_response", data)
        self.assertEqual(
            data["god_mode_response"],
            "Level has been set to 10. Character stats updated accordingly.",
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch("mvp_site.llm_providers.gemini_provider.generate_json_mode_content")
    def test_mode_switching_in_same_session(self, mock_gemini_generate, mock_get_db):
        """Test switching between story mode and god mode in the same session."""
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_mode_switch_e2e"
        self._setup_fake_firestore_with_campaign(fake_firestore, campaign_id)

        # First request: Story mode
        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_story_response)
        )

        response1 = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "I look around", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )

        self.assertEqual(response1.status_code, 200)
        data1 = json.loads(response1.data)
        self.assertIn("narrative", data1)
        self.assertNotIn("god_mode_response", data1)

        # Second request: God mode
        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_god_mode_response)
        )

        response2 = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps(
                {"input": "GOD MODE: Set level to 10", "mode": "character"}
            ),
            content_type="application/json",
            headers=self.test_headers,
        )

        self.assertEqual(response2.status_code, 200)
        data2 = json.loads(response2.data)
        self.assertIn("god_mode_response", data2)

        # Third request: Back to story mode
        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_story_response)
        )

        response3 = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "Continue exploring", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )

        self.assertEqual(response3.status_code, 200)
        data3 = json.loads(response3.data)
        self.assertIn("narrative", data3)

    # =========================================================================
    # Agent Instruction Building Tests
    # =========================================================================

    def test_story_mode_agent_builds_instructions(self):
        """Test that StoryModeAgent builds correct system instructions."""
        agent = StoryModeAgent()
        instructions = agent.build_system_instructions(
            selected_prompts=[
                constants.PROMPT_TYPE_NARRATIVE,
                constants.PROMPT_TYPE_MECHANICS,
            ],
            use_default_world=False,
            include_continuation_reminder=True,
        )

        self.assertIsInstance(instructions, str)
        self.assertGreater(
            len(instructions),
            0,
            "StoryModeAgent should build non-empty instructions",
        )

    def test_god_mode_agent_builds_instructions(self):
        """Test that GodModeAgent builds correct system instructions."""
        agent = GodModeAgent()
        instructions = agent.build_system_instructions()

        self.assertIsInstance(instructions, str)
        self.assertGreater(
            len(instructions),
            0,
            "GodModeAgent should build non-empty instructions",
        )

    def test_god_mode_ignores_selected_prompts(self):
        """Test that GodModeAgent ignores selected_prompts parameter."""
        agent = GodModeAgent()

        # Both calls should work without error
        instructions1 = agent.build_system_instructions(selected_prompts=None)
        instructions2 = agent.build_system_instructions(
            selected_prompts=[constants.PROMPT_TYPE_NARRATIVE]
        )

        self.assertIsInstance(instructions1, str)
        self.assertIsInstance(instructions2, str)


class TestSpicyModeAgentRouting(unittest.TestCase):
    """Verify SpicyModeAgent is routed correctly based on classifier detection."""

    def setUp(self):
        """Set up test fixtures with fake game state."""
        self.game_state_enabled = _create_fake_game_state(spicy_mode=True)
        self.game_state_disabled = _create_fake_game_state(spicy_mode=False)
        self.game_state_none = FakeGameState(
            user_settings=None,
            in_combat=False,
            custom_campaign_state={"character_creation_completed": True},
        )

    def test_spicy_mode_agent_matches_game_state_when_enabled(self):
        """SpicyModeAgent.matches_game_state returns True when spicy_mode is enabled."""
        result = SpicyModeAgent.matches_game_state(self.game_state_enabled)
        self.assertTrue(result, "Should match when spicy_mode=True in user_settings")

    def test_spicy_mode_agent_matches_game_state_when_disabled(self):
        """SpicyModeAgent.matches_game_state returns False when spicy_mode is disabled."""
        result = SpicyModeAgent.matches_game_state(self.game_state_disabled)
        self.assertFalse(result, "Should not match when spicy_mode=False")

    def test_spicy_mode_agent_matches_game_state_when_none(self):
        """SpicyModeAgent.matches_game_state returns False when user_settings is None."""
        result = SpicyModeAgent.matches_game_state(self.game_state_none)
        self.assertFalse(result, "Should not match when user_settings is None")

    def test_spicy_mode_agent_does_not_match_with_mode_param(self):
        """SpicyModeAgent.matches_input returns False even when mode='spicy'."""
        # Note: Parameter is _mode in parent class signature
        result = SpicyModeAgent.matches_input("any input", _mode="spicy")
        self.assertFalse(result, "Should not match with explicit mode param")

    def test_spicy_mode_agent_does_not_match_without_mode_param(self):
        """SpicyModeAgent.matches_input returns False without explicit mode param."""
        result = SpicyModeAgent.matches_input("seduce her")
        self.assertFalse(result, "Should not match on input alone")

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_routes_to_spicy_agent_when_classifier_detects_and_enabled(
        self, mock_classifier
    ):
        """Routes to SpicyModeAgent when classifier returns MODE_SPICY and spicy_mode enabled."""
        mock_classifier.return_value = (constants.MODE_SPICY, 0.85)

        # Use input WITHOUT explicit spicy keywords to bypassing the 5c override
        # and force reliance on the semantic classifier (Priority 7).
        agent, _ = get_agent_for_input(
            "I propose we retire to a private room",
            game_state=self.game_state_enabled,
        )

        self.assertIsInstance(agent, SpicyModeAgent)
        mock_classifier.assert_called_once()

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_routes_to_spicy_agent_when_classifier_detects_and_disabled(
        self, mock_classifier
    ):
        """Routes to SpicyModeAgent when classifier returns MODE_SPICY even if disabled."""
        mock_classifier.return_value = (constants.MODE_SPICY, 0.80)

        agent, _ = get_agent_for_input(
            "kiss her passionately",
            game_state=self.game_state_disabled,
        )

        # Should route to SpicyModeAgent (not DialogAgent) per new behavior
        self.assertIsInstance(agent, SpicyModeAgent)
        mock_classifier.assert_called_once()

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_spicy_toggle_command_routes_to_story_even_when_classifier_spicy(
        self, mock_classifier
    ):
        """Toggle commands should not route to SpicyModeAgent even if classifier says spicy."""
        mock_classifier.return_value = (constants.MODE_SPICY, 0.90)
        self.game_state_disabled.dialog_context = {"active": True}

        agent, _ = get_agent_for_input(
            "Enable Spicy Mode",
            game_state=self.game_state_disabled,
        )

        self.assertIsInstance(agent, StoryModeAgent)
        mock_classifier.assert_called_once()

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_spicy_toggle_command_routes_to_story_when_classifier_non_spicy(
        self, mock_classifier
    ):
        """Toggle commands should fall through to StoryModeAgent when classifier is non-spicy."""
        mock_classifier.return_value = (constants.MODE_CHARACTER, 0.42)

        agent, _ = get_agent_for_input(
            "Enable Spicy Mode",
            game_state=self.game_state_disabled,
        )

        self.assertIsInstance(agent, StoryModeAgent)
        mock_classifier.assert_called_once()

    @patch("mvp_site.agents.intent_classifier.classify_intent")
    def test_routes_to_story_agent_for_non_spicy_content(self, mock_classifier):
        """Routes to StoryModeAgent for normal content."""
        mock_classifier.return_value = (constants.MODE_CHARACTER, 0.70)

        agent, _ = get_agent_for_input(
            "I look around the room",
            game_state=self.game_state_enabled,
        )

        self.assertIsInstance(agent, StoryModeAgent)


class TestSpicyModeAgentConfiguration(unittest.TestCase):
    """Verify SpicyModeAgent is properly configured."""

    def test_agent_has_correct_mode(self):
        """SpicyModeAgent.MODE should be constants.MODE_SPICY."""
        self.assertEqual(SpicyModeAgent.MODE, constants.MODE_SPICY)

    def test_agent_has_required_prompts(self):
        """SpicyModeAgent should have spicy_mode prompt in required prompts."""
        self.assertIn(constants.PROMPT_TYPE_SPICY_MODE, SpicyModeAgent.REQUIRED_PROMPTS)

    def test_agent_has_master_directive_first(self):
        """SpicyModeAgent prompt order should start with master_directive."""
        self.assertEqual(
            SpicyModeAgent.REQUIRED_PROMPT_ORDER[0],
            constants.PROMPT_TYPE_MASTER_DIRECTIVE,
        )

    def test_agent_does_not_include_world_content(self):
        """SpicyModeAgent should not include world content (focused on intimacy)."""
        self.assertFalse(SpicyModeAgent.INCLUDE_WORLD_CONTENT)

    def test_builder_flags_exclude_debug(self):
        """SpicyModeAgent.builder_flags should exclude debug (focused on narrative)."""
        game_state = _create_fake_game_state(spicy_mode=False)
        agent = SpicyModeAgent(game_state)
        flags = agent.builder_flags()
        self.assertFalse(flags.get("include_debug", True))


class TestSpicyModeClassifierIntegration(unittest.TestCase):
    """Test classifier anchor phrases for spicy mode detection."""

    def test_mode_spicy_constant_exists(self):
        """Verify MODE_SPICY constant is defined."""
        self.assertTrue(hasattr(constants, "MODE_SPICY"))
        self.assertEqual(constants.MODE_SPICY, "spicy")

    def test_spicy_anchor_phrases_in_classifier(self):
        """Verify spicy mode anchor phrases exist in classifier."""
        self.assertIn(constants.MODE_SPICY, ANCHOR_PHRASES)
        spicy_phrases = ANCHOR_PHRASES[constants.MODE_SPICY]
        self.assertGreater(
            len(spicy_phrases), 10, "Should have multiple anchor phrases"
        )

        # Check for expected phrases
        expected_phrases = ["seduce her", "kiss her", "flirt with"]
        for phrase in expected_phrases:
            self.assertIn(
                phrase,
                spicy_phrases,
                f"Expected '{phrase}' in spicy anchor phrases",
            )


class TestSpicyModePromptLoading(unittest.TestCase):
    """Test that spicy mode prompt can be loaded."""

    def test_spicy_mode_instruction_path_exists(self):
        """Verify SPICY_MODE_INSTRUCTION_PATH constant exists."""
        self.assertTrue(hasattr(constants, "SPICY_MODE_INSTRUCTION_PATH"))

    def test_spicy_mode_prompt_file_exists(self):
        """Verify spicy_mode_instruction.md file exists."""
        prompt_path = MVP_SITE_ROOT / constants.SPICY_MODE_INSTRUCTION_PATH
        self.assertTrue(
            prompt_path.exists(),
            f"Spicy mode prompt should exist at {prompt_path}",
        )

    def test_spicy_mode_prompt_has_required_content(self):
        """Verify spicy mode prompt contains key sections."""
        prompt_path = MVP_SITE_ROOT / constants.SPICY_MODE_INSTRUCTION_PATH
        content = prompt_path.read_text()

        # Check for key sections
        self.assertIn("Spicy Mode", content)
        self.assertIn("Literary", content)
        self.assertIn("suggest", content.lower())
        self.assertIn("turn", content.lower())


if __name__ == "__main__":
    unittest.main()
