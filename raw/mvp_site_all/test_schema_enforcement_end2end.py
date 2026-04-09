"""
End-to-end integration test for schema enforcement in the full request path.

REV-jgd8: Dedicated end2end test (CI-friendly) that:
- Mocks external services only (Firestore + LLM provider)
- Exercises the real Flask API interaction endpoint
- Validates schema validation runs on every turn (via GameState.to_validated_dict)
- Validates canonical field placement for new writes (gold)
"""

from __future__ import annotations

import json
import os
import unittest
from unittest.mock import patch

# Ensure TESTING_AUTH_BYPASS is set before importing app modules (world_logic applies
# clock-skew patch at import time).
os.environ["TESTING_AUTH_BYPASS"] = "true"
# Force the Gemini provider into its stub client so token counting and generation
# never hit the network in CI or dev environments (even if a real key is present).
os.environ["GEMINI_API_KEY"] = "test-api-key"
# Default to mock services mode for CI safety at import time. The test flips this
# off at runtime to exercise the real request/LLM pipeline while still patching
# external I/O (Firestore + Gemini generation).
os.environ["MOCK_SERVICES_MODE"] = "true"

from mvp_site import main
from mvp_site.game_state import GameState
from mvp_site.llm_providers import gemini_provider
from mvp_site.tests.fake_firestore import FakeFirestoreClient
from mvp_site.tests.fake_llm import FakeLLMResponse
from mvp_site.tests.test_end2end import End2EndBaseTestCase


class TestSchemaEnforcementEnd2End(End2EndBaseTestCase):
    """Validate schema enforcement + canonical placement in an end-to-end flow."""

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"

    def setUp(self) -> None:
        super().setUp()
        # Run the real pipeline (not the generic MOCK_SERVICES_MODE short-circuit),
        # but keep external calls mocked via patches and Gemini stub client.
        os.environ["MOCK_SERVICES_MODE"] = "false"
        # Ensure cached Gemini client can't leak across tests and accidentally
        # re-enable real HTTP behavior.
        gemini_provider.clear_cached_client()

    def _seed_user_settings(self, fake_firestore: FakeFirestoreClient) -> None:
        # Enable debug_mode so response includes state_updates for assertions.
        fake_firestore.collection("users").document(self.test_user_id).set(
            {"settings": {"debug_mode": True}}
        )

    def _seed_campaign(self, fake_firestore: FakeFirestoreClient, campaign_id: str) -> None:
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).set({"title": "Schema Enforcement Campaign"})

        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).collection("game_states").document("current_state").set(
            {
                "user_id": self.test_user_id,
                "combat_state": {"in_combat": False},
                "custom_campaign_state": {},
                "player_character_data": {
                    "entity_id": "pc_schema_test",
                    "display_name": "Schema Tester",
                    "level": 1,
                    "resources": {"gold": 10},
                    "inventory": [],
                },
            }
        )

    def _get_persisted_state_dict(
        self, fake_firestore: FakeFirestoreClient, campaign_id: str
    ) -> dict:
        return (
            fake_firestore.collection("users")
            .document(self.test_user_id)
            .collection("campaigns")
            .document(campaign_id)
            .collection("game_states")
            .document("current_state")
            .get()
            .to_dict()
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch("mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution")
    def test_schema_enforcement_every_turn_and_canonical_gold(
        self, mock_gemini_generate, mock_get_db
    ):
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        self._seed_user_settings(fake_firestore)

        campaign_id = "test_campaign_schema_enforcement"
        self._seed_campaign(fake_firestore, campaign_id)

        # Turn 1: Set gold directly in canonical location (schema-compliant)
        turn1 = {
            "narrative": "You rummage through your pack and find coins.",
            "entities_mentioned": ["Schema Tester"],
            "location_confirmed": "Camp",
            "session_header": "Session 1: Camp",
            "planning_block": {"thinking": "Update gold.", "choices": {}},
            "state_updates": {
                "player_character_data": {
                    "resources": {"gold": 77}
                }
            },
        }

        # Turn 2: Legacy flat gold location (should backfill canonical).
        turn2 = {
            "narrative": "You count your winnings.",
            "entities_mentioned": ["Schema Tester"],
            "location_confirmed": "Camp",
            "session_header": "Session 2: Camp",
            "planning_block": {"thinking": "Normalize gold.", "choices": {}},
            "state_updates": {"player_character_data": {"resources": {"gold": 123}}},
        }

        # Turn 3: No state updates; should still validate persisted state.
        turn3 = {
            "narrative": "The night passes quietly.",
            "entities_mentioned": ["Schema Tester"],
            "location_confirmed": "Camp",
            "session_header": "Session 3: Camp",
            "planning_block": {"thinking": "Continue.", "choices": {}},
            "state_updates": {},
        }

        mock_gemini_generate.side_effect = [
            FakeLLMResponse(json.dumps(turn1)),
            FakeLLMResponse(json.dumps(turn2)),
            FakeLLMResponse(json.dumps(turn3)),
        ]

        def _post_interaction(user_input: str) -> dict:
            resp = self.client.post(
                f"/api/campaigns/{campaign_id}/interaction",
                data=json.dumps({"input": user_input, "mode": "character"}),
                content_type="application/json",
                headers=self.test_headers,
            )
            assert resp.status_code == 200, (
                f"Expected 200, got {resp.status_code}: {resp.data}"
            )
            return json.loads(resp.data)

        # Turn 1 assertions
        data1 = _post_interaction("I search my backpack for coins.")
        assert data1.get("success") is True
        assert isinstance(data1.get("state_updates"), dict)
        pc_updates_1 = (data1["state_updates"].get("player_character_data") or {})
        assert pc_updates_1.get("resources", {}).get("gold") == 77

        # Persisted state must validate against schema and have canonical gold.
        persisted1 = self._get_persisted_state_dict(fake_firestore, campaign_id)
        gs1 = GameState.from_dict(persisted1)
        assert gs1 is not None
        _ = gs1.to_validated_dict()  # should not raise
        assert (
            (gs1.player_character_data or {}).get("resources", {}).get("gold") == 77
        )

        # Turn 2 assertions (legacy flat gold -> canonical)
        data2 = _post_interaction("I update my gold total.")
        pc_updates_2 = (data2["state_updates"].get("player_character_data") or {})
        assert pc_updates_2.get("resources", {}).get("gold") == 123

        persisted2 = self._get_persisted_state_dict(fake_firestore, campaign_id)
        gs2 = GameState.from_dict(persisted2)
        assert gs2 is not None
        _ = gs2.to_validated_dict()  # should not raise
        assert (
            (gs2.player_character_data or {}).get("resources", {}).get("gold") == 123
        )

        # Turn 3: still validate persisted state.
        _ = _post_interaction("Wait until morning.")
        persisted3 = self._get_persisted_state_dict(fake_firestore, campaign_id)
        gs3 = GameState.from_dict(persisted3)
        assert gs3 is not None
        _ = gs3.to_validated_dict()  # should not raise


if __name__ == "__main__":
    unittest.main()
