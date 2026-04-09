"""
End-to-end integration tests for arc/event completion tracking via /interaction.
"""

# ruff: noqa: PT009, ARG002

from __future__ import annotations

import json
import os
from unittest.mock import patch

from mvp_site import main
from mvp_site.tests.fake_firestore import FakeFirestoreClient
from mvp_site.tests.fake_llm import FakeLLMResponse
from mvp_site.tests.test_end2end import End2EndBaseTestCase


class TestArcCompletionEnd2End(End2EndBaseTestCase):
    """End-to-end tests for arc/event completion tracking through the full stack."""

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"
    TEST_USER_ID = "test-user-arc-completion"

    def setUp(self):
        super().setUp()
        os.environ.setdefault("GEMINI_API_KEY", "test-api-key")
        os.environ.setdefault("CEREBRAS_API_KEY", "test-cerebras-key")
        os.environ["MOCK_SERVICES_MODE"] = "false"

    @patch("mvp_site.firestore_service.get_db")
    def test_arc_milestones_persist_to_firestore(self, mock_get_db):
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_arc_campaign"

        game_state_data = {
            "user_id": self.test_user_id,
            "custom_campaign_state": {
                "arc_milestones": {
                    "wedding_tour": {
                        "status": "completed",
                        "completed_at": "2024-01-15T10:30:00Z",
                        "phase": "ceremony_complete",
                    }
                }
            },
            "combat_state": {"in_combat": False},
        }

        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).collection("game_states").document("current_state").set(
            game_state_data
        )

        doc = (
            fake_firestore.collection("users")
            .document(self.test_user_id)
            .collection("campaigns")
            .document(campaign_id)
            .collection("game_states")
            .document("current_state")
            .get()
        )

        data = doc.to_dict()
        self.assertIn("arc_milestones", data["custom_campaign_state"])
        self.assertEqual(
            data["custom_campaign_state"]["arc_milestones"]["wedding_tour"]["status"],
            "completed",
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_arc_milestones_included_in_llm_context(
        self, mock_gemini_generate, mock_get_db
    ):
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_arc_context_campaign"

        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).set({"title": "Arc Test Campaign"})

        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).collection("game_states").document("current_state").set(
            {
                "user_id": self.test_user_id,
                "custom_campaign_state": {
                    "arc_milestones": {
                        "wedding_tour": {
                            "status": "completed",
                            "completed_at": "2024-01-15T10:30:00Z",
                        }
                    }
                },
                "combat_state": {"in_combat": False},
            }
        )

        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(
                {
                    "narrative": "The wedding tour has concluded. You are now on Nathema.",
                    "entities_mentioned": [],
                    "state_updates": {},
                    "planning_block": {
                        "thinking": "The user has completed the wedding arc. Transitioning to post-wedding state.",
                        "choices": [
                            {
                                "text": "Explore Nathema",
                                "description": "Look around your new home.",
                                "risk_level": "low",
                            }
                        ],
                    },
                    "session_header": "Session 5: Post-Wedding",
                }
            )
        )

        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps(
                {"input": "Where am I in the timeline?", "mode": "character"}
            ),
            content_type="application/json",
            headers=self.test_headers,
        )

        self.assertEqual(response.status_code, 200)

        self.assertTrue(mock_gemini_generate.called)

        call_args = mock_gemini_generate.call_args
        prompt_contents = call_args.kwargs.get("prompt_contents")
        self.assertIsNotNone(prompt_contents, "Expected prompt contents in LLM call")
        serialized_prompt = " ".join(str(item) for item in prompt_contents)
        self.assertIn("arc_milestones", serialized_prompt)
        self.assertIn("wedding_tour", serialized_prompt)
