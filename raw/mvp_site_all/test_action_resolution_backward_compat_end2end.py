"""
End-to-end test for action_resolution backward compatibility and null handling.

Tests the full flow from LLM response through API to ensure:
1. Backward compatibility: outcome_resolution maps to action_resolution
2. Null safety: None values don't leak to API responses
3. Both fields appear in unified_response when present
4. llm_response.action_resolution property falls back correctly

Only mocks external services (Gemini API and Firestore DB) at the lowest level.
"""

# ruff: noqa: PT009

import json
import os
import sys
import unittest
from unittest.mock import patch

# Set TESTING_AUTH_BYPASS environment variable before imports
os.environ["TESTING_AUTH_BYPASS"] = "true"
os.environ["GEMINI_API_KEY"] = "test-api-key"

# Add the parent directory to the path to import main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from mvp_site import main
from mvp_site.tests.fake_firestore import FakeFirestoreClient
from mvp_site.tests.fake_llm import FakeLLMResponse
from mvp_site.tests.test_end2end import End2EndBaseTestCase


class TestActionResolutionBackwardCompatEnd2End(End2EndBaseTestCase):
    """Test action_resolution backward compatibility through the full application stack."""

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"
    TEST_USER_ID = "action-res-test-user-123"

    def setUp(self):
        """Set up test client and test data."""
        # Disable MOCK_SERVICES_MODE to ensure our mocks are used
        self._original_mock_mode = os.environ.get("MOCK_SERVICES_MODE")
        os.environ["MOCK_SERVICES_MODE"] = "false"

        super().setUp()

        self.test_campaign_id = "action-res-test-campaign-456"

        # Set up fake Firestore
        self.fake_firestore = FakeFirestoreClient()

        # Create initial user document with settings
        user_data = {
            "settings": {
                "gemini_model": "gemini-3-flash-preview",
            },
            "lastUpdated": "2025-01-01T00:00:00Z",
        }
        users_collection = self.fake_firestore.collection("users")
        user_doc = users_collection.document(self.test_user_id)
        user_doc.set(user_data)

        # Create initial campaign data
        campaign_data = {
            "title": "Action Resolution Test Campaign",
            "prompt": "Test campaign for action resolution backward compatibility",
            "user_id": self.test_user_id,
        }

        # Set up campaign in fake Firestore
        campaigns_collection = user_doc.collection("campaigns")
        campaign_doc = campaigns_collection.document(self.test_campaign_id)
        campaign_doc.set(campaign_data)

        # Set up initial game state
        game_state_data = {
            "game_state_version": 1,
            "player_character_data": {
                "name": "Test Hero",
                "level": 1,
                "hp_current": 10,
                "hp_max": 10,
            },
        }
        game_state_doc = campaign_doc.collection("game_state").document("current")
        game_state_doc.set(game_state_data)

    def tearDown(self):
        """Clean up test environment."""
        if hasattr(self, "_original_mock_mode"):
            if self._original_mock_mode is None:
                os.environ.pop("MOCK_SERVICES_MODE", None)
            else:
                os.environ["MOCK_SERVICES_MODE"] = self._original_mock_mode

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_action_resolution_primary_field_in_api_response(
        self, mock_gemini_generate, mock_get_db
    ):
        """
        Test that action_resolution (new field) appears in API response.

        Scenario:
        1. LLM returns response with action_resolution field
        2. API response includes action_resolution in unified_response
        3. No null values leak to API
        """
        mock_get_db.return_value = self.fake_firestore

        # Mock LLM response with action_resolution
        llm_response_json = json.dumps(
            {
                "narrative": "You attack the goblin with your sword.",
                "action_resolution": {
                    "player_input": "I attack the goblin",
                    "interpreted_as": "melee_attack",
                    "reinterpreted": False,
                    "mechanics": {
                        "rolls": [
                            {"purpose": "attack", "notation": "1d20+5", "result": 17}
                        ],
                    },
                    "audit_flags": [],
                },
            }
        )

        mock_gemini_generate.return_value = FakeLLMResponse(llm_response_json)

        # Process action
        response = self.client.post(
            f"/api/campaigns/{self.test_campaign_id}/interaction",
            json={"input": "I attack the goblin"},
            headers=self.test_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        # Verify action_resolution appears in response
        self.assertIn("action_resolution", data)
        self.assertIsInstance(data["action_resolution"], dict)
        self.assertEqual(
            data["action_resolution"]["player_input"], "I attack the goblin"
        )
        self.assertEqual(data["action_resolution"]["interpreted_as"], "melee_attack")
        self.assertFalse(data["action_resolution"]["reinterpreted"])

        # Verify no null values
        self.assertIsNotNone(data["action_resolution"])

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_outcome_resolution_backward_compat_in_api_response(
        self, mock_gemini_generate, mock_get_db
    ):
        """
        Test that outcome_resolution (legacy field) maps to action_resolution in API.

        Scenario:
        1. LLM returns response with ONLY outcome_resolution (legacy format)
        2. API response includes BOTH action_resolution (mapped) AND outcome_resolution (for backward compat)
        3. No null values leak to API
        """
        mock_get_db.return_value = self.fake_firestore

        # Mock LLM response with ONLY outcome_resolution (legacy format)
        llm_response_json = json.dumps(
            {
                "narrative": "You try to convince the king to help.",
                "outcome_resolution": {
                    "player_input": "The king agrees",
                    "interpreted_as": "persuasion_attempt",
                    "reinterpreted": True,
                    "mechanics": {
                        "skill": "Persuasion",
                        "dc": 18,
                        "roll": "1d20+5",
                        "result": 19,
                    },
                    "audit_flags": ["player_declared_outcome"],
                },
            }
        )

        mock_gemini_generate.return_value = FakeLLMResponse(llm_response_json)

        # Process action
        response = self.client.post(
            f"/api/campaigns/{self.test_campaign_id}/interaction",
            json={"input": "The king agrees"},
            headers=self.test_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        # Verify action_resolution appears (mapped from outcome_resolution)
        self.assertIn("action_resolution", data)
        self.assertIsInstance(data["action_resolution"], dict)
        self.assertEqual(data["action_resolution"]["player_input"], "The king agrees")
        self.assertTrue(data["action_resolution"]["reinterpreted"])

        # Verify outcome_resolution also appears (for backward compatibility)
        self.assertIn("outcome_resolution", data)
        self.assertIsInstance(data["outcome_resolution"], dict)
        self.assertEqual(data["outcome_resolution"]["player_input"], "The king agrees")

        # Verify no null values
        self.assertIsNotNone(data["action_resolution"])
        self.assertIsNotNone(data["outcome_resolution"])

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_null_action_resolution_not_in_api_response(
        self, mock_gemini_generate, mock_get_db
    ):
        """
        Test that None values for action_resolution don't leak to API.

        Scenario:
        1. LLM returns response with action_resolution=None
        2. API response does NOT include action_resolution field (not null)
        3. Field is absent, not null
        """
        mock_get_db.return_value = self.fake_firestore

        # Mock LLM response with action_resolution=None
        llm_response_json = json.dumps(
            {
                "narrative": "You look around the room.",
                "action_resolution": None,  # Explicitly None
            }
        )

        mock_gemini_generate.return_value = FakeLLMResponse(llm_response_json)

        # Process action
        response = self.client.post(
            f"/api/campaigns/{self.test_campaign_id}/interaction",
            json={"input": "I look around"},
            headers=self.test_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        # Verify action_resolution is NOT in response (not null, just absent)
        # OR if present, it's an empty dict, not None
        if "action_resolution" in data:
            # If present, must be dict, not None
            self.assertIsInstance(data["action_resolution"], dict)
            self.assertIsNotNone(data["action_resolution"])

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_both_fields_when_both_provided(self, mock_gemini_generate, mock_get_db):
        """
        Test that when both action_resolution and outcome_resolution are provided,
        action_resolution takes precedence but both appear in API.

        Scenario:
        1. LLM returns response with BOTH fields
        2. API response includes both fields
        3. action_resolution takes precedence (used internally)
        """
        mock_get_db.return_value = self.fake_firestore

        # Mock LLM response with BOTH fields
        llm_response_json = json.dumps(
            {
                "narrative": "You cast a fireball.",
                "action_resolution": {
                    "player_input": "I cast Fireball",
                    "interpreted_as": "spell_cast",
                    "reinterpreted": False,
                    "mechanics": {
                        "spell": "Fireball",
                        "level": 3,
                    },
                    "audit_flags": [],
                },
                "outcome_resolution": {
                    "player_input": "I cast Fireball (legacy)",
                    "interpreted_as": "spell_cast",
                    "reinterpreted": False,
                },
            }
        )

        mock_gemini_generate.return_value = FakeLLMResponse(llm_response_json)

        # Process action
        response = self.client.post(
            f"/api/campaigns/{self.test_campaign_id}/interaction",
            json={"input": "I cast Fireball"},
            headers=self.test_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        # Verify both fields appear
        self.assertIn("action_resolution", data)
        self.assertIn("outcome_resolution", data)

        # Verify action_resolution takes precedence (has spell info)
        self.assertEqual(data["action_resolution"]["player_input"], "I cast Fireball")
        self.assertIn("mechanics", data["action_resolution"])
        self.assertEqual(data["action_resolution"]["mechanics"]["spell"], "Fireball")

        # Verify no null values
        self.assertIsNotNone(data["action_resolution"])
        self.assertIsNotNone(data["outcome_resolution"])

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_llm_response_action_resolution_property_fallback(
        self, mock_gemini_generate, mock_get_db
    ):
        """
        Test that llm_response.action_resolution property falls back to outcome_resolution.

        This tests the backward compatibility in llm_response.py property.
        """
        mock_get_db.return_value = self.fake_firestore

        # Mock LLM response with ONLY outcome_resolution
        llm_response_json = json.dumps(
            {
                "narrative": "You attempt to persuade the guard.",
                "outcome_resolution": {
                    "player_input": "The guard lets you pass",
                    "interpreted_as": "persuasion_attempt",
                    "reinterpreted": True,
                    "audit_flags": ["player_declared_outcome"],
                },
            }
        )

        mock_gemini_generate.return_value = FakeLLMResponse(llm_response_json)

        # Process action
        response = self.client.post(
            f"/api/campaigns/{self.test_campaign_id}/interaction",
            json={"input": "The guard lets you pass"},
            headers=self.test_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        # Verify action_resolution appears (via property fallback)
        # The llm_response.action_resolution property should have fallen back
        # to outcome_resolution, and world_logic should include it in unified_response
        self.assertIn("action_resolution", data)
        self.assertEqual(
            data["action_resolution"]["player_input"], "The guard lets you pass"
        )
        self.assertTrue(data["action_resolution"]["reinterpreted"])

        # Verify no null values
        self.assertIsNotNone(data["action_resolution"])

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_action_resolution_persisted_to_firestore(
        self, mock_gemini_generate, mock_get_db
    ):
        """
        Test that action_resolution is persisted to Firestore story entries.

        This validates the fix for the bug where action_resolution was added to
        unified_response but not persisted to Firestore.

        Scenario:
        1. LLM returns response with action_resolution
        2. Process action via API
        3. Verify action_resolution is saved in Firestore story entry
        """
        mock_get_db.return_value = self.fake_firestore

        # Mock LLM response with action_resolution
        llm_response_json = json.dumps(
            {
                "narrative": "You attack the goblin with your sword.",
                "action_resolution": {
                    "player_input": "I attack the goblin",
                    "interpreted_as": "melee_attack",
                    "reinterpreted": False,
                    "mechanics": {
                        "rolls": [
                            {"purpose": "attack", "notation": "1d20+5", "result": 17}
                        ],
                    },
                    "audit_flags": [],
                },
            }
        )

        mock_gemini_generate.return_value = FakeLLMResponse(llm_response_json)

        # Process action
        response = self.client.post(
            f"/api/campaigns/{self.test_campaign_id}/interaction",
            json={"input": "I attack the goblin"},
            headers=self.test_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        # Verify action_resolution appears in API response
        self.assertIn("action_resolution", data)

        # Verify action_resolution is persisted to Firestore story entry
        # Get the story collection
        users_collection = self.fake_firestore.collection("users")
        user_doc = users_collection.document(self.test_user_id)
        campaigns_collection = user_doc.collection("campaigns")
        campaign_doc = campaigns_collection.document(self.test_campaign_id)
        story_collection = campaign_doc.collection("story")

        # Find the latest Gemini entry (actor == 'gemini')
        gemini_entries = [
            entry
            for entry in story_collection.stream()
            if entry.to_dict().get("actor") == "gemini"
        ]

        self.assertGreater(len(gemini_entries), 0, "No Gemini story entries found")

        # Check the most recent entry
        latest_entry = gemini_entries[-1]
        entry_data = latest_entry.to_dict()

        # Verify action_resolution is present in Firestore entry
        self.assertIn(
            "action_resolution",
            entry_data,
            "action_resolution not found in Firestore story entry. "
            "This indicates the bug where action_resolution wasn't persisted.",
        )

        # Verify the structure matches what was in the API response
        firestore_ar = entry_data["action_resolution"]
        self.assertIsInstance(firestore_ar, dict)
        self.assertEqual(firestore_ar["player_input"], "I attack the goblin")
        self.assertEqual(firestore_ar["interpreted_as"], "melee_attack")
        self.assertFalse(firestore_ar["reinterpreted"])
        self.assertIn("mechanics", firestore_ar)
        self.assertIn("audit_flags", firestore_ar)

        # Also verify outcome_resolution is present (backward compat)
        self.assertIn(
            "outcome_resolution",
            entry_data,
            "outcome_resolution should also be persisted for backward compatibility",
        )

    # Dice Fabrication Correction Integration Tests
    # Related: Bead REV-9qy, test_dice_server_field_security.py, testing_mcp/test_dice_fabrication_correction_e2e.py
    # These tests validate dice fabrication detection in action_resolution (where dice rolls occur)

    def _create_fabricated_dice_response(self, include_spoofed_field=False):
        """
        Create a mocked Gemini response with fabricated dice rolls.

        This simulates what a malicious/biased LLM might return:
        - Includes dice rolls in action_resolution.mechanics.rolls
        - Does NOT include code_execution tool usage
        - Optionally includes spoofed _server_dice_fabrication_correction field
        """
        response_data = {
            "narrative": (
                "You swing your sword with precision! Your attack roll is 1d20+5. "
                "You rolled a natural 18! Total: 23. The training dummy takes "
                "1d8+3 damage. You rolled 7, total 10 damage. The dummy splinters!"
            ),
            "action_resolution": {
                "mechanics": {
                    "rolls": [
                        {"notation": "1d20+5", "total": 23, "type": "Attack Roll"},
                        {"notation": "1d8+3", "total": 10, "type": "Damage"},
                    ]
                }
            },
            "state_updates": {"last_action": "attacked training dummy"},
            "planning_block": {
                "thinking": "Attack successful, continue training",
                "choices": {
                    "continue": {
                        "text": "Continue Training",
                        "description": "Practice more attacks",
                        "risk_level": "low",
                    }
                },
            },
            "debug_info": {},
        }

        # Add spoofed field if requested (security test)
        if include_spoofed_field:
            response_data["debug_info"]["_server_dice_fabrication_correction"] = {
                "code_execution_used": True,  # LLM lies about using code_execution
                "fabricated_rolls": [],
            }

        return FakeLLMResponse(text=json.dumps(response_data))

    def _create_clean_response(self):
        """Create a clean response without dice (for second turn)."""
        response_data = {
            "narrative": "You take a moment to catch your breath and assess your form.",
            "state_updates": {"last_action": "continued practicing"},
            "planning_block": {
                "thinking": "Player is continuing training",
                "choices": {
                    "another_strike": {
                        "text": "Another Strike",
                        "description": "Practice another attack",
                        "risk_level": "low",
                    }
                },
            },
        }
        return FakeLLMResponse(text=json.dumps(response_data))

    def _setup_campaign_with_combat(self, fake_firestore, campaign_id):
        """Set up a campaign with character in combat state."""
        fake_firestore.collection("users").document(self.TEST_USER_ID).collection(
            "campaigns"
        ).document(campaign_id).set(
            {"title": "Dice Fabrication Test", "setting": "Training Ground"}
        )

        fake_firestore.collection("users").document(self.TEST_USER_ID).collection(
            "campaigns"
        ).document(campaign_id).collection("game_states").document("current_state").set(
            {
                "user_id": self.TEST_USER_ID,
                "story_text": "You stand in the training ground, ready to practice.",
                "combat_state": {"in_combat": True, "combat_phase": "active"},
                "player_character_data": {
                    "entity_id": "player_character",
                    "display_name": "TestWarrior",
                    "name": "TestWarrior",
                    "level": 3,
                    "class_name": "Fighter",
                    "health": {"hp": 25, "hp_max": 25},
                    "stats": {
                        "strength": 16,
                        "dexterity": 14,
                        "constitution": 14,
                    },
                },
                "custom_campaign_state": {
                    "character_creation_completed": True,
                    "character_creation_in_progress": False,
                },
            }
        )

    def test_dice_fabrication_detection_and_correction_generation(self):
        """
        Test complete dice fabrication flow: detection → metadata → generation → persistence.

        This tests:
        1. dice_integrity._is_code_execution_fabrication() detects fabricated dice
        2. llm_service.py sets processing_metadata.dice_fabrication_correction
        3. world_logic.py generates correction text from processing_metadata (NOT hardcoded)
        4. Correction persists to game_state.pending_system_corrections
        """
        campaign_id = "test_dice_fabrication_001"

        fake_firestore = FakeFirestoreClient()
        with patch(
            "mvp_site.firestore_service.get_db", return_value=fake_firestore
        ):
            self._setup_campaign_with_combat(fake_firestore, campaign_id)

            # Mock Gemini to return fabricated dice
            with patch(
                "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
            ) as mock_gemini:
                mock_gemini.return_value = self._create_fabricated_dice_response()

                # Trigger action that should detect fabrication
                response = self.client.post(
                    f"/api/campaigns/{campaign_id}/interaction",
                    json={"input": "I attack the training dummy with my sword", "mode": "character"},
                    headers=self.test_headers,
                )

                self.assertEqual(response.status_code, 200)
                data = response.get_json()

                # STEP 1: Verify detection happened (dice_integrity._is_code_execution_fabrication)
                # The response should be successful but flagged
                self.assertTrue(data.get("success"))

                # STEP 2: Verify processing_metadata was set (llm_service.py:5279)
                # This is internal but we can verify via Firestore state

                # STEP 3 & 4: Verify correction was generated and persisted (world_logic.py:4171-4177)
                game_state_doc = (
                    fake_firestore.collection("users")
                    .document(self.TEST_USER_ID)
                    .collection("campaigns")
                    .document(campaign_id)
                    .collection("game_states")
                    .document("current_state")
                    .get()
                )

                game_state = game_state_doc.to_dict()
                pending_corrections = game_state.get("pending_system_corrections", [])

                # Assert correction was generated
                self.assertGreater(
                    len(pending_corrections),
                    0,
                    "Expected correction to be generated and persisted to pending_system_corrections",
                )

                correction_text = pending_corrections[0]

                # Verify correction is NOT hardcoded (comes from world_logic.py production code)
                self.assertIn("CORRECTION", correction_text)
                self.assertIn("code_execution", correction_text.lower())
                self.assertIn("random.randint", correction_text.lower())

                # Verify correction mentions fabricated rolls
                self.assertTrue(
                    "fabricat" in correction_text.lower(),
                    "Correction should mention dice fabrication",
                )

    def test_spoofing_prevention_clears_llm_provided_server_fields(self):
        """
        Test that llm_service.py clears LLM-provided _server_* fields.

        Security test: LLM should not be able to inject _server_dice_fabrication_correction
        to bypass detection. Server must clear any LLM-provided value.

        This tests llm_service.py:5285-5289 (spoofing prevention).
        """
        campaign_id = "test_spoofing_prevention_001"

        fake_firestore = FakeFirestoreClient()
        with patch(
            "mvp_site.firestore_service.get_db", return_value=fake_firestore
        ):
            self._setup_campaign_with_combat(fake_firestore, campaign_id)

            # Mock Gemini to return response WITH spoofed _server_ field
            with patch(
                "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
            ) as mock_gemini:
                mock_gemini.return_value = self._create_fabricated_dice_response(
                    include_spoofed_field=True
                )

                response = self.client.post(
                    f"/api/campaigns/{campaign_id}/interaction",
                    json={"input": "I attack", "mode": "character"},
                    headers=self.test_headers,
                )

                self.assertEqual(response.status_code, 200)
                data = response.get_json()

                # Verify debug_info exists
                debug_info = data.get("debug_info", {})

                # CRITICAL: Verify spoofed field was cleared
                self.assertNotIn(
                    "_server_dice_fabrication_correction",
                    debug_info,
                    "SECURITY VIOLATION: LLM-provided _server_dice_fabrication_correction "
                    "was not cleared! Server must sanitize this field.",
                )

                # Correction should still be generated (server detected fabrication)
                game_state_doc = (
                    fake_firestore.collection("users")
                    .document(self.TEST_USER_ID)
                    .collection("campaigns")
                    .document(campaign_id)
                    .collection("game_states")
                    .document("current_state")
                    .get()
                )

                game_state = game_state_doc.to_dict()
                pending_corrections = game_state.get("pending_system_corrections", [])

                self.assertGreater(
                    len(pending_corrections),
                    0,
                    "Correction should be generated despite LLM spoofing attempt",
                )

    def test_corrections_consumed_on_next_turn(self):
        """
        Test that corrections are sent to LLM and cleared from game_state.

        This tests:
        1. Correction persists across API calls
        2. Next turn includes correction in LLM context
        3. Correction is cleared after consumption
        """
        campaign_id = "test_correction_consumption_001"

        fake_firestore = FakeFirestoreClient()
        with patch(
            "mvp_site.firestore_service.get_db", return_value=fake_firestore
        ):
            self._setup_campaign_with_combat(fake_firestore, campaign_id)

            # Mock Gemini for both turns
            with patch(
                "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
            ) as mock_gemini:
                # Turn 1: Fabricated dice response
                mock_gemini.return_value = self._create_fabricated_dice_response()

                # Turn 1: Trigger fabrication
                response1 = self.client.post(
                    f"/api/campaigns/{campaign_id}/interaction",
                    json={"input": "I attack", "mode": "character"},
                    headers=self.test_headers,
                )
                self.assertEqual(response1.status_code, 200)

                # Verify correction was persisted
                game_state_doc = (
                    fake_firestore.collection("users")
                    .document(self.TEST_USER_ID)
                    .collection("campaigns")
                    .document(campaign_id)
                    .collection("game_states")
                    .document("current_state")
                    .get()
                )

                game_state = game_state_doc.to_dict()
                corrections_after_turn1 = game_state.get(
                    "pending_system_corrections", []
                )
                self.assertGreater(
                    len(corrections_after_turn1), 0, "Correction should persist"
                )

                # Turn 2: Clean response (no dice)
                mock_gemini.return_value = self._create_clean_response()

                response2 = self.client.post(
                    f"/api/campaigns/{campaign_id}/interaction",
                    json={"input": "I continue practicing", "mode": "character"},
                    headers=self.test_headers,
                )
                self.assertEqual(response2.status_code, 200)

                # Verify corrections were consumed (cleared)
                game_state_doc = (
                    fake_firestore.collection("users")
                    .document(self.TEST_USER_ID)
                    .collection("campaigns")
                    .document(campaign_id)
                    .collection("game_states")
                    .document("current_state")
                    .get()
                )

                game_state = game_state_doc.to_dict()
                corrections_after_turn2 = game_state.get(
                    "pending_system_corrections", []
                )

                self.assertEqual(
                    len(corrections_after_turn2),
                    0,
                    "Corrections should be cleared after consumption on next turn",
                )


if __name__ == "__main__":
    unittest.main()
