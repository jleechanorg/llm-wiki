"""End-to-end test for empty Phase 2 streaming response handling.

Reproduces production bug: "Scene #3: [Error: Empty response from server]"

This test verifies that when Phase 2 streaming returns empty chunks:
1. llm_service.py detects the empty response and yields error event
2. streaming_orchestrator.py handles the error gracefully
3. Frontend would show appropriate error (not "[Error: Empty response from server]")

The test uses real Flask app endpoints but mocks the Gemini API at the lowest level
to simulate the exact empty Phase 2 scenario that occurred in production.
"""

from __future__ import annotations

import json
import os
import unittest
from unittest.mock import MagicMock, patch

# Ensure TESTING_AUTH_BYPASS is set before importing app modules
os.environ.setdefault("TESTING_AUTH_BYPASS", "true")
os.environ.setdefault("GEMINI_API_KEY", "test-api-key")
os.environ.setdefault("CEREBRAS_API_KEY", "test-cerebras-key")

from mvp_site import main
from mvp_site.game_state import GameState
from mvp_site.stream_events import StreamEvent
from mvp_site.tests.fake_firestore import FakeFirestoreClient
from mvp_site.tests.test_end2end import End2EndBaseTestCase


class TestStreamingEmptyPhase2End2End(End2EndBaseTestCase):
    """Test empty Phase 2 streaming response through full application stack."""

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"

    def setUp(self):
        """Set up test client and Firestore mocks."""
        super().setUp()
        os.environ.setdefault("GEMINI_API_KEY", "test-api-key")
        os.environ.setdefault("CEREBRAS_API_KEY", "test-cerebras-key")
        # Use MOCK_SERVICES_MODE=true for CI compatibility (avoids /dev/null Firebase credentials)
        os.environ["MOCK_SERVICES_MODE"] = "true"

    def _setup_campaign_with_story(self, fake_firestore, campaign_id):
        """Set up a campaign with existing story context."""
        # Create campaign
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).set(
            {
                "title": "Empty Phase 2 Test Campaign",
                "setting": "Combat scenario",
                "selected_prompts": [],
                "use_default_world": False,
            }
        )

        # Create game state with combat scenario
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).collection("game_states").document("current_state").set(
            {
                "user_id": self.test_user_id,
                "story_text": "You encounter a goblin warrior blocking your path.",
                "characters": ["Hero"],
                "locations": ["Forest Path"],
                "items": ["Sword", "Shield"],
                "combat_state": {"in_combat": True, "enemies": ["Goblin"]},
                "custom_campaign_state": {},
            }
        )

        # Add story entries
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).collection("story").add(
            {
                "actor": "user",
                "text": "I prepare for battle",
                "timestamp": "2024-01-01T00:00:00Z",
                "user_scene_number": 1,
            }
        )

    @unittest.skip("Test mocking strategy needs update - gemini_provider mock not intercepting actual code path")
    def test_empty_phase2_yields_error_not_done(self):
        """
        Test that empty Phase 2 response yields error event instead of done.

        Scenario:
        1. User input triggers tool_requests (Phase 1)
        2. Phase 2 streaming returns empty chunks (bug scenario)
        3. llm_service.py should yield error event
        4. streaming_orchestrator.py should handle error gracefully
        5. Frontend should NOT see "[Error: Empty response from server]"

        SKIPPED: Mocking strategy doesn't properly intercept the actual streaming code path.
        Need to refactor to mock at the correct layer (provider selection or generate_content_stream_sync calls).
        """

        with patch("mvp_site.main.firestore_service") as mock_firestore_service, \
             patch("mvp_site.streaming_orchestrator.firestore_service") as mock_streaming_firestore:
            # Setup fake Firestore
            fake_firestore = FakeFirestoreClient()
            mock_firestore_service.get_db.return_value = fake_firestore
            mock_streaming_firestore.get_db.return_value = fake_firestore

            # Mock campaign_exists to return True
            mock_firestore_service.campaign_exists.return_value = True
            mock_streaming_firestore.campaign_exists.return_value = True

            mock_firestore_service.get_campaign_by_id.return_value = (
                {
                    "id": "test-campaign-empty-phase2",
                    "title": "Empty Phase 2 Test",
                    "selected_prompts": [],
                    "use_default_world": False,
                },
                [],
            )
            mock_streaming_firestore.get_campaign_by_id.return_value = mock_firestore_service.get_campaign_by_id.return_value

            game_state = GameState(debug_mode=False)
            game_state.combat_state = {"in_combat": True, "enemies": ["Goblin"]}
            mock_firestore_service.get_campaign_game_state.return_value = game_state
            mock_streaming_firestore.get_campaign_game_state.return_value = game_state

            mock_firestore_service.get_user_settings.return_value = {"debug_mode": False}
            mock_streaming_firestore.get_user_settings.return_value = {"debug_mode": False}

            mock_firestore_service.add_story_entry = MagicMock()
            mock_streaming_firestore.add_story_entry = MagicMock()

            self._setup_campaign_with_story(fake_firestore, "test-campaign-empty-phase2")

            # Mock Gemini provider to simulate empty Phase 2
            with patch("mvp_site.llm_service.gemini_provider") as mock_gemini:
                # Phase 1: Return JSON with tool_requests (triggers Phase 2)
                phase1_response = json.dumps({
                    "narrative": "You attack the goblin!",
                    "tool_requests": [
                        {"tool": "roll_dice", "args": {"notation": "1d20+3"}}
                    ]
                })

                # Phase 2: Return EMPTY (bug scenario)
                phase2_response = ""

                # Mock the streaming generator
                def mock_generate_stream(*args, **kwargs):
                    """Simulate two-phase streaming with empty Phase 2."""
                    # Phase 1: Return tool_requests
                    yield phase1_response
                    # Phase 2: Return empty (bug trigger)
                    # (second call to generate_content_stream_sync returns empty)

                mock_gemini.generate_content_stream_sync = MagicMock(
                    side_effect=[
                        iter([phase1_response]),  # Phase 1
                        iter([]),  # Phase 2: EMPTY
                    ]
                )

                # Mock tool execution
                with patch("mvp_site.llm_service.execute_tool_requests") as mock_tools:
                    mock_tools.return_value = [
                        {"tool": "roll_dice", "result": {"total": 18, "rolls": [15, 3]}}
                    ]

                    # Mock token calculation
                    with patch("mvp_site.llm_service._calculate_prompt_and_system_tokens") as mock_calc, \
                         patch("mvp_site.llm_service._get_safe_output_token_limit") as mock_limit:
                        mock_calc.return_value = (100, 50)
                        mock_limit.return_value = 4096

                        # Make streaming request
                        response = self.client.post(
                            "/api/campaigns/test-campaign-empty-phase2/interaction/stream",
                            headers=self.test_headers,
                            json={
                                "input": "I attack the goblin with my sword!",
                                "mode": "character",
                            },
                        )

                        # Debug: Print response if not 200
                        if response.status_code != 200:
                            print(f"\n❌ Response status: {response.status_code}")
                            print(f"Response data: {response.data}")
                            print(f"Response headers: {dict(response.headers)}")

                        # Should return 200 (streaming endpoint always starts successfully)
                        self.assertEqual(response.status_code, 200)

                        # Collect SSE events
                        events = []
                        event_data = response.data.decode("utf-8")
                        for line in event_data.split("\n\n"):
                            if line.startswith("data: "):
                                try:
                                    event_json = json.loads(line[6:])  # Skip "data: "
                                    events.append(event_json)
                                except json.JSONDecodeError:
                                    pass

                        # Debug: Print events
                        print("\n=== SSE EVENTS ===")
                        for i, event in enumerate(events):
                            print(f"{i}: type={event.get('type')}, payload={event.get('payload', {}).keys()}")

                        # Extract event types
                        event_types = [e.get("type") for e in events]

                        # ASSERTION 1: Should have error event for empty Phase 2
                        error_events = [e for e in events if e.get("type") == "error"]
                        self.assertGreater(
                            len(error_events),
                            0,
                            "Expected error event for empty Phase 2 response"
                        )

                        # ASSERTION 2: Error should mention "empty"
                        error_message = error_events[0].get("payload", {}).get("message", "")
                        self.assertIn(
                            "empty",
                            error_message.lower(),
                            f"Error message should mention 'empty', got: {error_message}"
                        )

                        # ASSERTION 3: Should NOT have done event with empty narrative
                        done_events = [e for e in events if e.get("type") == "done"]
                        if done_events:
                            # If there's a done event, it should NOT have empty narrative
                            done_payload = done_events[0].get("payload", {})
                            full_narrative = done_payload.get("full_narrative", "")
                            self.assertTrue(
                                full_narrative and full_narrative.strip(),
                                "If done event exists, narrative must not be empty"
                            )

                        # ASSERTION 4: Verify no persistence of AI response with empty narrative
                        # (Only user input should be persisted when error occurs)
                        add_story_calls = mock_firestore_service.add_story_entry.call_args_list
                        ai_persists = [
                            call for call in add_story_calls
                            if call[0][2] == "gemini"  # actor parameter
                        ]

                        # With our fix, AI response should NOT be persisted when error occurs
                        self.assertEqual(
                            len(ai_persists),
                            0,
                            "AI response should NOT be persisted when empty Phase 2 error occurs"
                        )

                        print("\n✅ Empty Phase 2 test passed:")
                        print(f"   - Error event present: {len(error_events)} events")
                        print(f"   - Error message: {error_message}")
                        print(f"   - AI persists: {len(ai_persists)} (should be 0)")


if __name__ == "__main__":
    unittest.main()
