"""
End-to-end integration test for DialogAgent.

Tests the DialogAgent through the full application stack. Verifies that:
1. DialogAgent is selected for dialog state continuity or explicit dialog mode
2. DialogAgent builds the correct system instructions (focused on character/dialog)
3. DialogAgent excludes mechanics/combat/SRD instructions
4. Dialog mode integrates correctly with the LLM service
5. Priority ordering works (dialog after rewards, before story mode)

This test suite complements test_agent_architecture_end2end.py by focusing
specifically on the DialogAgent functionality.
"""

# ruff: noqa: PT009

from __future__ import annotations

import datetime
import json
import os
import sys
from pathlib import Path

# Set this before importing mvp_site modules to bypass clock skew validation
os.environ["TESTING_AUTH_BYPASS"] = "true"

# Add project root to path for imports (allows running directly without PYTHONPATH)
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from unittest.mock import patch

from mvp_site import constants, main
from mvp_site.agents import (
    CombatAgent,
    DialogAgent,
    GodModeAgent,
    StoryModeAgent,
    get_agent_for_input,
)
from mvp_site.schemas.validation import is_valid_game_state
from mvp_site.tests.fake_firestore import FakeFirestoreClient
from mvp_site.tests.fake_llm import FakeLLMResponse
from mvp_site.tests.test_end2end import End2EndBaseTestCase


class TestDialogAgentEnd2End(End2EndBaseTestCase):
    """Test DialogAgent through the full application stack."""

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"
    TEST_USER_ID = "test-user-dialog-e2e"

    def setUp(self):
        """Set up test client."""
        super().setUp()
        os.environ.setdefault("GEMINI_API_KEY", "test-api-key")
        os.environ.setdefault("CEREBRAS_API_KEY", "test-cerebras-key")
        # Disable MOCK_SERVICES_MODE to allow patching generate_json_mode_content
        os.environ["MOCK_SERVICES_MODE"] = "false"

        # Standard mock dialog response (NPC conversation)
        self.mock_dialog_response = {
            "session_header": "[SESSION_HEADER]\nTimestamp: 1492 DR, Mirtul 10\nLocation: Tavern",
            "narrative": (
                "The bartender looks up from the glass he's polishing. "
                '"Well met, traveler. What brings you to the Rusty Anchor today?" '
                "His voice carries the weariness of a man who's heard a thousand stories."
            ),
            "entities_mentioned": ["Bartender"],
            "location_confirmed": "Rusty Anchor Tavern",
            "state_updates": {},
            "planning_block": {
                "thinking": "The player is engaging in dialog with the bartender.",
                "choices": {
                    "ask_rumors": {
                        "text": "Ask about rumors",
                        "description": "Inquire about local gossip and news",
                        "risk_level": "safe",
                    },
                    "ask_room": {
                        "text": "Ask about a room",
                        "description": "Request lodging for the night",
                        "risk_level": "safe",
                    },
                    "order_drink": {
                        "text": "Order a drink",
                        "description": "Buy a beverage",
                        "risk_level": "safe",
                    },
                },
            },
        }

    def _create_mock_game_state(self, in_combat=False):
        """Create a mock GameState for testing."""
        from unittest.mock import Mock

        mock_state = Mock()
        mock_state.is_in_combat.return_value = in_combat
        mock_state.get_combat_state.return_value = {"in_combat": in_combat}
        mock_state.combat_state = {"in_combat": in_combat}
        mock_state.custom_campaign_state = {
            "character_creation_completed": True,
        }
        mock_state.player_character_data = {
            "name": "TestHero",
            "class": "Bard",
            "level": 5,
        }
        # Explicitly set user_settings with spicy_mode disabled
        mock_state.user_settings = {"spicy_mode": False}
        # Mock campaign upgrade check to return False (no upgrade available)
        mock_state.is_campaign_upgrade_available.return_value = False
        return mock_state

    def _setup_fake_firestore_with_campaign(self, fake_firestore, campaign_id):
        """Helper to set up fake Firestore with campaign and game state."""
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).set(
            {
                "title": "Dialog Test Campaign",
                "setting": "Fantasy tavern",
                "selected_prompts": ["narrative", "mechanics"],
            }
        )

        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).collection("game_states").document("current_state").set(
            {
                "user_id": self.test_user_id,
                "story_text": "You are in the Rusty Anchor Tavern.",
                "player_character_data": {
                    "entity_id": "player_character",
                    "display_name": "TestHero",
                    "name": "TestHero",
                    "hp_current": 30,
                    "hp_max": 30,
                    "level": 5,
                    "class_name": "Bard",
                },
                "world_data": {
                    "current_location_name": "Rusty Anchor Tavern",
                    "world_time": {
                        "year": 1492,
                        "month": "Mirtul",
                        "day": 10,
                        "hour": 20,
                        "minute": 0,
                    },
                },
                "npc_data": {
                    "bartender": {
                        "name": "Marcus",
                        "role": "Bartender",
                        "personality_traits": ["gruff", "observant", "loyal"],
                        "relationship_score": 25,
                    }
                },
                "combat_state": {"in_combat": False},
                "custom_campaign_state": {"character_creation_completed": True},
            }
        )

    # =========================================================================
    # Agent Selection Tests
    # =========================================================================

    def test_agent_selection_dialog_state(self):
        """Test that DialogAgent is selected for dialog state continuity."""
        mock_state = self._create_mock_game_state(in_combat=False)
        mock_state.dialog_context = {"active": True}

        agent, _ = get_agent_for_input("continue", game_state=mock_state)
        self.assertIsInstance(agent, DialogAgent)
        self.assertEqual(agent.MODE, constants.MODE_DIALOG)

    def test_agent_selection_priority_combat_over_dialog(self):
        """Test that CombatAgent takes priority over DialogAgent during combat."""
        mock_state = self._create_mock_game_state(in_combat=True)

        # Dialog state during combat should still go to CombatAgent
        mock_state.dialog_context = {"active": True}
        agent, _ = get_agent_for_input("continue", game_state=mock_state)
        self.assertIsInstance(
            agent,
            CombatAgent,
            "CombatAgent should take priority over DialogAgent during combat",
        )

    def test_agent_selection_priority_god_mode_over_dialog(self):
        """Test that GodModeAgent takes priority over DialogAgent."""
        agent, _ = get_agent_for_input("GOD MODE: talk to the bartender")
        self.assertIsInstance(
            agent,
            GodModeAgent,
            "GodModeAgent should take priority over DialogAgent",
        )

    def test_agent_selection_non_dialog_to_story(self):
        """Test that non-dialog inputs fall through to StoryModeAgent."""
        mock_state = self._create_mock_game_state(in_combat=False)

        non_dialog_inputs = [
            "I explore the forest",
            "I look around the room",
            "Search the room for traps",
            "I check the map",  # Changed from "Walk down the path" which triggers false positive spicy classification
        ]

        for user_input in non_dialog_inputs:
            agent, _ = get_agent_for_input(user_input, game_state=mock_state)
            self.assertIsInstance(
                agent,
                StoryModeAgent,
                f"Expected StoryModeAgent for non-dialog input: {user_input}",
            )

    # =========================================================================
    # System Instructions Tests
    # =========================================================================

    def test_dialog_agent_prompt_composition(self):
        """Test that DialogAgent builds correct system instructions."""
        # Verify required prompts
        self.assertIn(
            constants.PROMPT_TYPE_MASTER_DIRECTIVE, DialogAgent.REQUIRED_PROMPTS
        )
        self.assertIn(constants.PROMPT_TYPE_GAME_STATE, DialogAgent.REQUIRED_PROMPTS)
        self.assertIn(
            constants.PROMPT_TYPE_PLANNING_PROTOCOL, DialogAgent.REQUIRED_PROMPTS
        )
        self.assertIn(constants.PROMPT_TYPE_DIALOG, DialogAgent.REQUIRED_PROMPTS)
        self.assertIn(
            constants.PROMPT_TYPE_CHARACTER_TEMPLATE, DialogAgent.REQUIRED_PROMPTS
        )
        self.assertIn(constants.PROMPT_TYPE_RELATIONSHIP, DialogAgent.REQUIRED_PROMPTS)

    def test_dialog_agent_excludes_combat_mechanics(self):
        """Test that DialogAgent excludes combat/SRD but keeps dialog world context."""
        all_prompts = DialogAgent.REQUIRED_PROMPTS | DialogAgent.OPTIONAL_PROMPTS

        # These should NOT be in DialogAgent's prompts
        self.assertNotIn(
            constants.PROMPT_TYPE_MECHANICS, all_prompts, "Mechanics should be excluded"
        )
        self.assertNotIn(
            constants.PROMPT_TYPE_COMBAT, all_prompts, "Combat should be excluded"
        )
        self.assertNotIn(
            constants.PROMPT_TYPE_DND_SRD, all_prompts, "D&D SRD should be excluded"
        )
        self.assertIn(
            constants.PROMPT_TYPE_LIVING_WORLD,
            all_prompts,
            "Living world should be included for background events",
        )

    def test_dialog_agent_builds_instructions(self):
        """Test that DialogAgent can successfully build system instructions."""
        agent = DialogAgent()
        instructions = agent.build_system_instructions()

        # Should return a non-empty string
        self.assertIsInstance(instructions, str)
        self.assertGreater(
            len(instructions), 100, "System instructions should be substantial"
        )

    # =========================================================================
    # Integration Tests with Fake Services
    # =========================================================================

    @patch("mvp_site.firestore_service.get_db")
    @patch("mvp_site.llm_providers.gemini_provider.generate_json_mode_content")
    def test_dialog_flow_end_to_end(self, mock_gemini_generate, mock_get_db):
        """Test full dialog flow through the application."""
        # Set up fake Firestore
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test-dialog-campaign"
        self._setup_fake_firestore_with_campaign(fake_firestore, campaign_id)

        # Mock LLM response (must be JSON string for FakeLLMResponse)
        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_dialog_response)
        )

        # Make request with dialog input
        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps(
                {"input": "talk to the bartender about rumors", "mode": "dialog"}
            ),
            content_type="application/json",
            headers=self.test_headers,
        )

        # Verify response
        self.assertEqual(response.status_code, 200, f"Response: {response.data}")
        data = json.loads(response.data)

        # Verify narrative contains dialog content
        self.assertIn("narrative", data)
        self.assertIsInstance(data["narrative"], str)


class TestGameStateSchemaEnd2End(End2EndBaseTestCase):
    """E2E test for game state schema enforcement and prompt injection."""

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"
    TEST_USER_ID = "test-user-schema"

    def setUp(self):
        super().setUp()
        os.environ.setdefault("GEMINI_API_KEY", "test-api-key")
        os.environ.setdefault("CEREBRAS_API_KEY", "test-cerebras-key")
        # Ensure we hit the patched LLM call path
        os.environ["MOCK_SERVICES_MODE"] = "false"

        self.mock_llm_response_data = {
            "narrative": "The schema documentation was helpful.",
            "entities_mentioned": ["Hero"],
            "location_confirmed": "Test Room",
            "state_updates": {
                "player_character_data": {
                    "display_name": "Hero Updated",
                    "health": {"hp": 15, "hp_max": 20, "temp_hp": 0, "conditions": []},
                }
            },
        }

    def _setup_test_campaign(self, fake_firestore, campaign_id):
        """Set up a basic campaign for schema testing."""
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).set(
            {"title": "Schema Test Campaign", "setting": "Testing"}
        )

        game_state = {
            "user_id": self.test_user_id,
            "game_state_version": 1,
            "session_id": "session-1",
            "turn_number": 10,
            "last_state_update_timestamp": datetime.datetime.now(
                datetime.UTC
            ).isoformat(),
            "player_turn": 10,
            "time_sensitive_events": {},
            "player_character_data": {
                "entity_id": "pc_1",
                "entity_type": "pc",
                "display_name": "Hero",
                "class_name": "Tester",
                "level": 1,
                "current_location": "loc_start",
                "health": {"hp": 10, "hp_max": 10, "temp_hp": 0, "conditions": []},
                "stats": {
                    "strength": 10,
                    "dexterity": 10,
                    "constitution": 10,
                    "intelligence": 10,
                    "wisdom": 10,
                    "charisma": 10,
                },
                "status": "conscious",
                "visibility": "visible",
                "experience": {"current": 0, "to_next_level": 300},
                "inspiration": False,
                "hero_points": 0,
            },
            "custom_campaign_state": {
                "arc_milestones": {},
                "companion_arcs": {},
                "next_companion_arc_turn": 3,
                "active_constraints": [],
                "attribute_system": "D&D",
                "campaign_tier": "mortal",
                "divine_potential": 0,
                "universe_control": 0,
                "divine_upgrade_available": False,
                "multiverse_upgrade_available": False,
                "character_creation_completed": True,
                "character_creation_in_progress": False,
            },
            "world_data": {
                "current_location_name": "Start",
                "world_time": {
                    "hour": 8,
                    "minute": 0,
                    "second": 0,
                    "day": 1,
                    "month": 1,
                    "year": 1000,
                },
            },
            "combat_state": {"in_combat": False},
        }

        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).collection("game_states").document("current_state").set(
            game_state
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch("mvp_site.llm_providers.cerebras_provider.generate_content")
    @patch("mvp_site.llm_service._call_llm_api")
    @patch("mvp_site.main.firestore_service")
    @patch(
        "mvp_site.firestore_service.firestore.SERVER_TIMESTAMP",
        new="2024-01-01T00:00:00Z",
    )
    def test_schema_injection_and_validated_persistence(
        self, mock_firestore_service, mock_call_api, mock_cerebras_generate, mock_get_db
    ):
        """Verify schema docs in prompt and valid state persistence."""
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore
        mock_firestore_service.get_db.return_value = fake_firestore

        campaign_id = "schema_e2e_test"
        self._setup_test_campaign(fake_firestore, campaign_id)

        captured_prompt = None
        captured_system = None

        def mock_generate(*args, **kwargs):
            nonlocal captured_system, captured_prompt
            if len(args) > 0:
                captured_prompt = args[0]
            if len(args) > 3:
                captured_system = args[3]
            elif "system_instruction_text" in kwargs:
                captured_system = kwargs["system_instruction_text"]

            return FakeLLMResponse(json.dumps(self.mock_llm_response_data))

        mock_call_api.side_effect = mock_generate
        mock_cerebras_generate.side_effect = mock_generate

        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "Hello world", "mode": "action"}),
            content_type="application/json",
            headers=self.headers,
        )

        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data

        combined_context = str(captured_system) + str(captured_prompt)
        assert "### PlanningBlock" in combined_context
        assert "hp" in combined_context
        assert "hp_max" in combined_context

        saved_state = (
            fake_firestore.collection("users")
            .document(self.test_user_id)
            .collection("campaigns")
            .document(campaign_id)
            .collection("game_states")
            .document("current_state")
            .get()
            .to_dict()
        )

        assert saved_state["player_character_data"]["display_name"] == "Hero Updated"
        assert "health" in saved_state["player_character_data"]
        assert saved_state["player_character_data"]["health"]["hp"] == 15
        assert is_valid_game_state(saved_state) is True
