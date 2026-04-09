"""End-to-end API test for prompt loading via /interaction."""

from __future__ import annotations

import json
import os
from unittest.mock import patch

from mvp_site import main
from mvp_site.tests.fake_firestore import FakeFirestoreClient
from mvp_site.tests.fake_llm import FakeLLMResponse
from mvp_site.tests.test_end2end import End2EndBaseTestCase


class TestPromptLoadingApiEnd2End(End2EndBaseTestCase):
    """API-level end2end test for prompt loading through the Flask pipeline."""

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"
    TEST_USER_ID = "prompt-loading-api-user"

    def setUp(self):
        super().setUp()
        os.environ.setdefault("GEMINI_API_KEY", "test-api-key")
        os.environ.setdefault("CEREBRAS_API_KEY", "test-cerebras-key")
        os.environ["MOCK_SERVICES_MODE"] = "false"

    @patch("mvp_site.firestore_service.get_db")
    @patch("mvp_site.llm_providers.gemini_provider.generate_json_mode_content")
    def test_prompt_loading_via_interaction(self, mock_gemini_generate, mock_get_db):
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "prompt-loading-e2e"
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).set(
            {
                "title": "Prompt Loading Campaign",
                "setting": "Fantasy realm",
                "selected_prompts": ["narrative"],
            }
        )
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).collection("game_states").document("current_state").set(
            {
                "user_id": self.test_user_id,
                "story_text": "Previous story content",
                "combat_state": {"in_combat": False},
                "custom_campaign_state": {},
            }
        )

        captured_prompts = {}

        def fake_llm_call(*_args, **kwargs):
            captured_prompts["prompt_contents"] = kwargs.get("prompt_contents", [])
            captured_prompts["system_instruction_text"] = kwargs.get(
                "system_instruction_text", ""
            )
            return FakeLLMResponse(
                json.dumps(
                    {
                        "narrative": "You continue your journey.",
                        "entities_mentioned": [],
                        "location_confirmed": "Road",
                        "state_updates": {},
                        "planning_block": {"thinking": "Continue", "choices": {}},
                    }
                )
            )

        mock_gemini_generate.side_effect = fake_llm_call

        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "Continue", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )
        assert response.status_code == 200, f"Got: {response.data}"

        prompt_contents = captured_prompts.get("prompt_contents", [])
        assert prompt_contents, "Expected prompt contents for API interaction."
        first_prompt = prompt_contents[0]
        if isinstance(first_prompt, str):
            request_payload = json.loads(first_prompt)
        elif isinstance(first_prompt, dict):
            request_payload = first_prompt
        else:
            raise AssertionError(
                f"Unexpected prompt contents type: {type(first_prompt)}"
            )

        selected_prompts = request_payload.get("selected_prompts", [])
        assert "narrative" in selected_prompts, (
            "Narrative prompt should be selected for API interaction."
        )
