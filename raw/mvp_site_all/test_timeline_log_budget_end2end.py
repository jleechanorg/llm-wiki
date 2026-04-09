"""
End-to-end coverage for timeline_log budgeting guardrails.
"""

# ruff: noqa: PT009

from __future__ import annotations

import json
import os
from unittest.mock import patch

from mvp_site import main
from mvp_site.tests.fake_firestore import FakeFirestoreClient
from mvp_site.tests.fake_llm import FakeLLMResponse
from mvp_site.tests.test_end2end import End2EndBaseTestCase


class TestTimelineLogBudgetEnd2End(End2EndBaseTestCase):
    """E2E regression for large story contexts and the dormant duplication guard."""

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"
    TEST_USER_ID = "test-user-timeline-budget"

    def setUp(self):
        super().setUp()
        os.environ.setdefault("GEMINI_API_KEY", "test-api-key")
        os.environ.setdefault("CEREBRAS_API_KEY", "test-cerebras-key")

        self.mock_llm_response_data = {
            "narrative": "The party continues their journey...",
            "entities_mentioned": ["Hero"],
            "location_confirmed": "Ancient Forest",
            "state_updates": {"story_progression": "continued"},
        }

    def _create_large_story_context_for_timeline_bug(self, turns: int = 80) -> list:
        story_context = []

        narrative_templates = [
            "The ancient ruins stretch before you, their weathered stones telling "
            "tales of civilizations long forgotten. Mysterious runes pulse with "
            "ethereal energy as you step through the crumbling archway. ",
            "Your footsteps echo through the vast chamber, disturbing centuries "
            "of dust. Strange shadows dance along the walls, cast by torches "
            "that seem to burn without fuel. The air grows thick with magic. ",
            "A distant rumble echoes through the corridors as something ancient "
            "stirs in the depths below. The party exchanges nervous glances, "
            "weapons drawn and spells at the ready for whatever comes next. ",
        ]

        player_actions = [
            "I carefully examine the glowing runes, trying to decipher their meaning. ",
            "I signal the party to halt and listen for any sounds of danger ahead. ",
            "I cast a detection spell to reveal any hidden traps or magical wards. ",
            "I move forward cautiously, keeping my shield raised and ready. ",
        ]

        for i in range(turns):
            if i % 2 == 0:
                action = player_actions[i % len(player_actions)]
                story_context.append(
                    {
                        "actor": "player",
                        "text": f"Turn {i}: {action}" + action * 2,
                        "sequence_id": i + 1,
                    }
                )
            else:
                narrative = narrative_templates[i % len(narrative_templates)]
                story_context.append(
                    {
                        "actor": "gm",
                        "text": f"Turn {i}: {narrative}" + narrative,
                        "sequence_id": i + 1,
                    }
                )

        return story_context

    def _setup_fake_firestore_with_timeline_bug_campaign(
        self, fake_firestore, campaign_id
    ):
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).set(
            {"title": "Timeline Log Bug Test", "setting": "Fantasy"}
        )

        game_state = {
            "user_id": self.test_user_id,
            "story_text": "A long ongoing adventure...",
            "story_context": self._create_large_story_context_for_timeline_bug(80),
            "characters": ["Hero"],
            "locations": ["Ancient Ruins", "Dark Forest"],
            "items": ["Magic Sword"],
            "combat_state": {"in_combat": False},
            "custom_campaign_state": {
                "session_number": 10,
                "core_memories": ["The quest began in the village of Millbrook"],
            },
            "npc_data": {
                "Guide": {
                    "mbti": "ENFJ",
                    "role": "ally",
                    "background": "A mysterious guide who knows the ancient paths.",
                }
            },
            "world_data": {
                "current_location_name": "Ancient Ruins",
                "time_of_day": "night",
            },
            "player_character_data": {
                "entity_id": "player_character",
                "display_name": "Hero",
                "name": "Hero",
                "class_name": "Fighter",
                "level": 5,
            },
        }

        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).collection("game_states").document("current_state").set(
            game_state
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch("mvp_site.llm_providers.cerebras_provider.generate_content")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_large_story_context_does_not_overflow_due_to_timeline_log(
        self, mock_gemini_generate, mock_cerebras_generate, mock_get_db
    ):
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "timeline_log_bug_test"
        self._setup_fake_firestore_with_timeline_bug_campaign(
            fake_firestore, campaign_id
        )

        mock_cerebras_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_llm_response_data)
        )
        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_llm_response_data)
        )

        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps(
                {"input": "I examine the ancient altar carefully", "mode": "character"}
            ),
            content_type="application/json",
            headers=self.test_headers,
        )

        response_data = response.data.decode()

        if response.status_code == 400:
            self.assertNotIn(
                "Context too large",
                response_data,
                "Timeline log budget bug triggered; scaffold estimate does not account for timeline_log.",
            )

        self.assertEqual(
            response.status_code,
            200,
            f"Expected 200, got {response.status_code}: {response_data[:500]}",
        )
