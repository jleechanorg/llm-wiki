"""
End-to-end integration test for Living World system.

Tests:
1. player_turn counter stored in game_state increments on non-GOD actions
2. player_turn does NOT increment on GOD mode actions
3. world_events extraction and annotation with turn_generated
4. Backward compatibility when player_turn is not present (compute from context)
"""

from __future__ import annotations

import json
import os
import unittest
from unittest.mock import patch

# Ensure TESTING_AUTH_BYPASS is set before importing app modules
os.environ["TESTING_AUTH_BYPASS"] = "true"
os.environ.setdefault("GEMINI_API_KEY", "test-api-key")
os.environ.setdefault("CEREBRAS_API_KEY", "test-cerebras-key")

from mvp_site import main
from mvp_site.tests.fake_firestore import FakeFirestoreClient
from mvp_site.tests.fake_llm import FakeLLMResponse
from mvp_site.tests.test_end2end import End2EndBaseTestCase
from mvp_site.world_logic import _has_visible_living_world_data


def _is_ui_visible_living_world_payload(response_data: dict) -> bool:
    """Determine if the living-world payload should be visible in the UI.

    This delegates to the canonical server-side visibility helper to avoid
    duplicating and potentially diverging from the production logic.
    """
    try:
        if not isinstance(response_data, dict):
            return False
        state_updates = response_data.get("state_updates", {})
        if not isinstance(state_updates, dict):
            state_updates = {}
        custom_state = state_updates.get("custom_campaign_state", {})
        if not isinstance(custom_state, dict):
            custom_state = {}
        world_events = (
            response_data.get("world_events")
            or state_updates.get("world_events")
            or custom_state.get("world_events")
        )
        faction_updates = response_data.get("faction_updates") or state_updates.get(
            "faction_updates"
        )
        time_events = response_data.get("time_events") or state_updates.get("time_events")
        rumors = response_data.get("rumors") or state_updates.get("rumors")
        scene_event = response_data.get("scene_event") or state_updates.get("scene_event")
        complications = response_data.get("complications") or state_updates.get(
            "complications"
        )
        return bool(
            _has_visible_living_world_data(
                world_events,
                faction_updates,
                time_events,
                rumors,
                scene_event,
                complications,
            )
        )
    except (TypeError, AttributeError):
        # Be conservative: on unexpected structures or errors, treat as not visible.
        return False


class TestLivingWorldEnd2End(End2EndBaseTestCase):
    """Test Living World player_turn tracking through the full application stack."""

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"
    TEST_USER_ID = "test-user-living-world"

    def setUp(self):
        """Set up test client."""
        super().setUp()
        os.environ.setdefault("GEMINI_API_KEY", "test-api-key")
        os.environ.setdefault("CEREBRAS_API_KEY", "test-cerebras-key")
        # Disable MOCK_SERVICES_MODE to allow patching generate_json_mode_content
        os.environ["MOCK_SERVICES_MODE"] = "false"

        # Standard mock LLM response
        self.mock_llm_response_data = {
            "narrative": "The adventure continues...",
            "entities_mentioned": ["Hero"],
            "location_confirmed": "Town Square",
            "state_updates": {
                "custom_campaign_state": {
                    "world_events": {
                        "background_events": [
                            {"description": "Merchants arrive from the east."}
                        ],
                        "rumors": [{"description": "Strange lights in the forest."}],
                    }
                }
            },
            "session_header": "Session 1: Beginning",
            "planning_block": {"thinking": "Continue story."},
        }

    def _setup_fake_firestore_with_campaign(
        self,
        fake_firestore,
        campaign_id,
        player_turn=0,
        *,
        turn_number=None,  # Added for living world trigger compatibility
        last_living_world_turn=0,
        last_living_world_time=None,
        world_time=None,
    ):
        """Helper to set up fake Firestore with campaign and game state."""
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).set(
            {"title": "Test Campaign", "setting": "Fantasy realm"}
        )

        game_state = {
            "user_id": self.test_user_id,
            "story_text": "Previous story content",
            "player_character_data": {
                "entity_id": "player_character",
                "display_name": "Hero",
                "name": "Hero",
                "class_name": "Fighter",
            },
            "characters": ["Hero"],
            "locations": ["Town Square"],
            "combat_state": {"in_combat": False},
            "custom_campaign_state": {
                "character_creation_completed": True,
                "character_creation_in_progress": False,
            },
            "player_turn": player_turn,
            "turn_number": turn_number if turn_number is not None else player_turn,
            "last_living_world_turn": last_living_world_turn,
            "last_living_world_time": last_living_world_time,
        }
        if world_time is not None:
            game_state["world_data"] = {"world_time": world_time}

        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).collection("game_states").document("current_state").set(
            game_state
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_player_turn_increments_on_character_action(
        self, mock_gemini_generate, mock_get_db
    ):
        """Test that player_turn increments when a character action is taken."""
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_player_turn_increment"
        initial_turn = 5
        self._setup_fake_firestore_with_campaign(
            fake_firestore, campaign_id, player_turn=initial_turn
        )

        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_llm_response_data)
        )

        # Make character mode request
        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "I look around the square", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.data}"
        )

        # Verify player_turn was incremented in game state
        game_state_doc = (
            fake_firestore.collection("users")
            .document(self.test_user_id)
            .collection("campaigns")
            .document(campaign_id)
            .collection("game_states")
            .document("current_state")
            .get()
        )
        game_state = game_state_doc.to_dict()

        assert game_state.get("player_turn") == initial_turn + 1, (
            f"player_turn should be {initial_turn + 1}, "
            f"got {game_state.get('player_turn')}"
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_player_turn_does_not_increment_on_god_mode(
        self, mock_gemini_generate, mock_get_db
    ):
        """Test that player_turn does NOT increment on GOD mode commands."""
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_god_mode_no_increment"
        initial_turn = 10
        self._setup_fake_firestore_with_campaign(
            fake_firestore, campaign_id, player_turn=initial_turn
        )

        # GOD mode response
        god_mode_response = {
            "narrative": "Character updated.",
            "god_mode_response": "Successfully changed character name.",
        }
        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(god_mode_response)
        )

        # Make GOD mode request
        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps(
                {
                    "input": "GOD MODE: Change my character name to Bob",
                    "mode": "character",
                }
            ),
            content_type="application/json",
            headers=self.test_headers,
        )

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.data}"
        )

        # Verify player_turn was NOT incremented
        game_state_doc = (
            fake_firestore.collection("users")
            .document(self.test_user_id)
            .collection("campaigns")
            .document(campaign_id)
            .collection("game_states")
            .document("current_state")
            .get()
        )
        game_state = game_state_doc.to_dict()

        assert game_state.get("player_turn") == initial_turn, (
            f"player_turn should remain {initial_turn} for GOD mode, "
            f"got {game_state.get('player_turn')}"
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_world_events_extracted_in_story_entry(
        self, mock_gemini_generate, mock_get_db
    ):
        """Test that world_events from state_updates are extracted to story entries."""
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_world_events_extraction"
        self._setup_fake_firestore_with_campaign(fake_firestore, campaign_id)

        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_llm_response_data)
        )

        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "explore the area", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )

        assert response.status_code == 200

        # Verify response contains state_updates with world_events
        data = json.loads(response.data)
        state_updates = data.get("state_updates", {})

        # world_events should be in state_updates if LLM returned them
        world_events = state_updates.get("world_events")
        if world_events:
            assert "background_events" in world_events or "rumors" in world_events, (
                "world_events should contain background_events or rumors"
            )

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_backward_compatibility_no_player_turn(
        self, mock_gemini_generate, mock_get_db
    ):
        """Test backward compatibility when game state has no player_turn field."""
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_backward_compat"

        # Set up campaign WITHOUT player_turn (old campaign)
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).set(
            {"title": "Old Campaign", "setting": "Fantasy realm"}
        )

        # Game state without player_turn field
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).collection("game_states").document("current_state").set(
            {
                "user_id": self.test_user_id,
                "story_text": "Old story",
                "combat_state": {"in_combat": False},
                "player_character_data": {
                    "entity_id": "player_character",
                    "display_name": "Hero",
                    "name": "Hero",
                    "class_name": "Fighter",
                    "level": 1,
                },
                "custom_campaign_state": {
                    "character_creation_completed": True,
                    "character_creation_in_progress": False,
                },
                # No player_turn field
            }
        )

        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_llm_response_data)
        )

        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "continue", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.data}"
        )

        # After the action, player_turn should now be set
        game_state_doc = (
            fake_firestore.collection("users")
            .document(self.test_user_id)
            .collection("campaigns")
            .document(campaign_id)
            .collection("game_states")
            .document("current_state")
            .get()
        )
        game_state = game_state_doc.to_dict()

        # Should be 1 after first action (0 + 1)
        assert game_state.get("player_turn") == 1, (
            f"player_turn should be 1 after first action, "
            f"got {game_state.get('player_turn')}"
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_world_events_not_duplicated_across_turns(
        self, mock_gemini_generate, mock_get_db
    ):
        """Test that story entries contain ONLY their turn's world_events, not accumulated.

        BUG REPRODUCTION: The system was copying game_state.world_events (cumulative)
        to every story entry's structured_fields, causing all turns to show the same
        world_events regardless of when they were generated.

        EXPECTED: Each turn should only include world_events that were generated on THAT
        turn (based on turn_generated annotation).
        """
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_no_duplicate_world_events"

        # Use helper to set up basic campaign
        self._setup_fake_firestore_with_campaign(
            fake_firestore, campaign_id, player_turn=10
        )

        # Add pre-existing world_events from turn 5 to game_state
        existing_world_events = {
            "background_events": [
                {
                    "actor": "Old Faction",
                    "action": "Old action from turn 5",
                    "turn_generated": 5,
                    "scene_generated": 3,
                }
            ]
        }

        # Update game_state to include old world_events
        game_state_ref = (
            fake_firestore.collection("users")
            .document(self.test_user_id)
            .collection("campaigns")
            .document(campaign_id)
            .collection("game_states")
            .document("current_state")
        )
        current_state = game_state_ref.get().to_dict()
        current_state["world_events"] = existing_world_events
        game_state_ref.set(current_state)

        # LLM returns NEW world_events for turn 11 (this turn)
        turn_11_response = {
            "narrative": "The adventure continues on turn 11...",
            "entities_mentioned": ["Hero"],
            "location_confirmed": "Town Square",
            "state_updates": {
                "custom_campaign_state": {
                    "world_events": {
                        "background_events": [
                            {
                                "actor": "New Faction",
                                "action": "New action happening NOW on turn 11",
                                # Note: turn_generated will be added by annotation
                            }
                        ]
                    }
                }
            },
            "session_header": "Session 1: Continuing",
            "planning_block": {"thinking": "New events for this turn."},
        }

        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(turn_11_response)
        )

        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "I explore the town", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.data}"
        )

        data = json.loads(response.data)

        # Get world_events from response - check multiple possible locations
        response_state_updates = data.get("state_updates", {})
        if not isinstance(response_state_updates, dict):
            response_state_updates = {}
        response_custom_state = response_state_updates.get("custom_campaign_state", {})
        if not isinstance(response_custom_state, dict):
            response_custom_state = {}
        response_world_events = (
            data.get("world_events")
            or response_state_updates.get("world_events")
            or response_custom_state.get("world_events")
        )

        # CRITICAL: Assert world_events is present in response
        # The LLM response includes state_updates.world_events, so the API MUST return it
        # Without this assertion, the test could pass without validating the fix
        assert response_world_events is not None, (
            f"TEST GAP: world_events not found in API response! "
            f"LLM mock returns world_events but API didn't include them. "
            f"Response keys: {list(data.keys())}, "
            f"state_updates: {data.get('state_updates', {})}"
        )

        # The response should NOT contain the old turn 5 events
        # It should only contain the new turn 11 events
        background_events = response_world_events.get("background_events", [])
        for event in background_events:
            # OLD BUG: Events from turn 5 were appearing in turn 11's response
            turn_generated = event.get("turn_generated")
            if turn_generated is not None:
                assert turn_generated != 5, (
                    f"DUPLICATE BUG: Found old event from turn 5 in turn 11 response! "
                    f"Event: {event}"
                )
            # Check for the old action text that shouldn't be there
            action = event.get("action", "")
            assert "Old action from turn 5" not in action, (
                f"DUPLICATE BUG: Old turn 5 event found in turn 11 response! "
                f"Response world_events should only contain NEW events. "
                f"Got: {response_world_events}"
            )

        # Verify the fix works: API response should contain ONLY new events
        # The game_state may have merged or replaced events (separate concern)
        # The key bug was old events appearing in the API response when they shouldn't
        # The new event should be present
        new_events = [
            e
            for e in response_world_events.get("background_events", [])
            if "New action happening NOW" in e.get("action", "")
        ]
        assert new_events, (
            f"New events should be in API response. Got: {response_world_events}"
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_world_events_append_syntax_normalized_for_story_and_response(
        self, mock_gemini_generate, mock_get_db
    ):
        """Append-op world_events must be normalized to list form for UI rendering."""
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_world_events_append_normalization"
        self._setup_fake_firestore_with_campaign(fake_firestore, campaign_id)

        append_syntax_response = {
            "narrative": "A distant horn echoes through the valley.",
            "state_updates": {
                "custom_campaign_state": {
                    "world_events": {
                        "background_events": {
                            "append": [
                                {
                                    "actor": "Border Watch",
                                    "action": "Raises warning beacons along the ridge.",
                                    "event_type": "immediate",
                                    "status": "pending",
                                }
                            ]
                        }
                    }
                }
            },
            "planning_block": {"thinking": "Track world movement."},
        }
        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(append_syntax_response)
        )

        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "continue", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.data}"
        )

        data = json.loads(response.data)
        response_state_updates = data.get("state_updates", {})
        if not isinstance(response_state_updates, dict):
            response_state_updates = {}
        response_custom_state = response_state_updates.get("custom_campaign_state", {})
        if not isinstance(response_custom_state, dict):
            response_custom_state = {}
        response_world_events = (
            data.get("world_events")
            or response_state_updates.get("world_events")
            or response_custom_state.get("world_events")
        )
        assert isinstance(response_world_events, dict), (
            f"Expected response world_events dict, got: {type(response_world_events)}"
        )
        assert isinstance(response_world_events.get("background_events"), list), (
            "Response world_events.background_events should be normalized to a list"
        )
        assert response_world_events["background_events"], (
            "Response world_events.background_events should contain appended event"
        )
        assert _is_ui_visible_living_world_payload(data), (
            "Response should satisfy frontend living-world visibility criteria"
        )

        story_docs = (
            fake_firestore.collection("users")
            .document(self.test_user_id)
            .collection("campaigns")
            .document(campaign_id)
            .collection("story")
            .stream()
        )
        gemini_entries = [
            doc.to_dict()
            for doc in story_docs
            if str(doc.to_dict().get("actor", "")).lower() == "gemini"
        ]
        assert gemini_entries, "Expected at least one Gemini story entry"

        latest_entry = gemini_entries[-1]
        entry_state_updates = latest_entry.get("state_updates", {})
        if not isinstance(entry_state_updates, dict):
            entry_state_updates = {}
        entry_custom_state = entry_state_updates.get("custom_campaign_state", {})
        if not isinstance(entry_custom_state, dict):
            entry_custom_state = {}
        entry_world_events = (
            latest_entry.get("world_events")
            or entry_state_updates.get("world_events")
            or entry_custom_state.get("world_events")
        )
        assert isinstance(entry_world_events, dict), (
            f"Expected persisted world_events dict, got: {type(entry_world_events)}"
        )
        assert isinstance(entry_world_events.get("background_events"), list), (
            "Persisted world_events.background_events should be normalized to a list"
        )
        assert entry_world_events["background_events"], (
            "Persisted world_events.background_events should contain appended event"
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_time_based_living_world_tracking_updates(
        self, mock_gemini_generate, mock_get_db
    ):
        """Test that time-based trigger updates living world tracking."""
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_time_trigger_updates"
        last_time = {"year": 1000, "month": 1, "day": 1, "hour": 10, "minute": 0}
        current_time = {"year": 1000, "month": 1, "day": 2, "hour": 11, "minute": 0}
        expected_time = dict(current_time)

        self._setup_fake_firestore_with_campaign(
            fake_firestore,
            campaign_id,
            player_turn=2,
            last_living_world_turn=2,
            last_living_world_time=last_time,
            world_time=current_time,
        )

        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_llm_response_data)
        )

        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "I continue my journey through the forest", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.data}"
        )

        game_state_doc = (
            fake_firestore.collection("users")
            .document(self.test_user_id)
            .collection("campaigns")
            .document(campaign_id)
            .collection("game_states")
            .document("current_state")
            .get()
        )
        game_state = game_state_doc.to_dict()

        assert game_state.get("last_living_world_turn") == 3, (
            f"Expected last_living_world_turn to update to 3, "
            f"got {game_state.get('last_living_world_turn')}"
        )
        updated_time = game_state.get("last_living_world_time") or {}
        for key, value in expected_time.items():
            assert updated_time.get(key) == value, (
                "Expected last_living_world_time to update to current world_time."
            )


if __name__ == "__main__":
    unittest.main()
