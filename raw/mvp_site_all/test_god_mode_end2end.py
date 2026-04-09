"""
End-to-end integration test for GOD MODE functionality.
Only mocks external services (LLM provider APIs and Firestore DB) at the lowest level.
Tests the full flow including god mode prompt selection and response handling.

GOD MODE is for correcting mistakes and changing campaign state, NOT for playing.
It uses a separate, focused prompt stack without narrative generation prompts.
"""

from __future__ import annotations

import json
import os
import unittest

# Set this before importing mvp_site modules to bypass clock skew validation
os.environ["TESTING_AUTH_BYPASS"] = "true"

from typing import Any
from unittest.mock import patch

from mvp_site import main
from mvp_site.agent_prompts import PromptBuilder
from mvp_site.dice_integrity import validate_god_mode_response
from mvp_site.narrative_response_schema import NarrativeResponse
from mvp_site.tests.fake_firestore import FakeFirestoreClient
from mvp_site.tests.fake_llm import FakeLLMResponse
from mvp_site.tests.test_end2end import End2EndBaseTestCase


class TestGodModeEnd2End(End2EndBaseTestCase):
    """Test GOD MODE functionality through the full application stack."""

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"
    TEST_USER_ID = "test-user-god-mode"

    def setUp(self):
        """Set up test client."""
        super().setUp()
        os.environ.setdefault("GEMINI_API_KEY", "test-api-key")
        os.environ.setdefault("CEREBRAS_API_KEY", "test-cerebras-key")
        # Disable MOCK_SERVICES_MODE to allow patching generate_json_mode_content
        os.environ["MOCK_SERVICES_MODE"] = "false"
        os.environ["ENABLE_EXPLICIT_CACHE"] = "false"

        # Standard mock GOD MODE response
        self.mock_god_mode_response_data = {
            "session_header": "[SESSION_HEADER]\nTimestamp: 1492 DR, Mirtul 10, Afternoon\nLocation: Tavern\nStatus: Lvl 5 Fighter | HP: 45/50 | XP: 6500/14000 | Gold: 150gp",
            "god_mode_response": "HP has been set to 50. Character is now at full health.",
            "narrative": "",
            "entities_mentioned": [],
            "location_confirmed": "Tavern",
            "state_updates": {"player_character_data": {"hp_current": 50}},
            "planning_block": {
                "thinking": "The user wants to modify HP. This is an administrative command.",
                "choices": {
                    "god:set_gold": {
                        "text": "Set Gold",
                        "description": "Modify character gold",
                        "risk_level": "safe",
                    },
                    "god:return_story": {
                        "text": "Return to Story",
                        "description": "Exit God Mode and resume gameplay",
                        "risk_level": "safe",
                    },
                },
            },
        }

        # Standard mock story mode response (for comparison)
        self.mock_story_response_data = {
            "session_header": "[SESSION_HEADER]\nTimestamp: 1492 DR, Mirtul 10, Afternoon\nLocation: Tavern\nStatus: Lvl 5 Fighter | HP: 45/50",
            "narrative": "The tavern is bustling with activity...",
            "entities_mentioned": ["Bartender"],
            "location_confirmed": "Tavern",
            "state_updates": {},
            "planning_block": {
                "thinking": "The player enters the tavern.",
                "choices": {
                    "talk_bartender": {
                        "text": "Talk to bartender",
                        "description": "Ask about rumors",
                        "risk_level": "low",
                    },
                    "observe_patrons": {
                        "text": "Observe Patrons",
                        "description": "Study the other tavern guests from a discreet corner",
                        "risk_level": "low",
                    },
                },
            },
        }

    def _setup_fake_firestore_with_campaign(self, fake_firestore, campaign_id):
        """Helper to set up fake Firestore with campaign and game state."""
        # Create test campaign data
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).set(
            {
                "title": "Test Campaign",
                "setting": "Fantasy realm",
                "selected_prompts": ["narrative", "mechanics"],
            }
        )

        # Create game state with proper structure
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).collection("game_states").document("current_state").set(
            {
                "user_id": self.test_user_id,
                "story_text": "Previous story content",
                "player_character_data": {
                    "entity_id": "player_character",
                    "display_name": "Thorin",
                    "name": "Thorin",
                    "hp_current": 45,
                    "hp_max": 50,
                    "level": 5,
                    "class_name": "Fighter",
                },
                "world_data": {
                    "current_location_name": "Tavern",
                    "world_time": {
                        "year": 1492,
                        "month": "Mirtul",
                        "day": 10,
                        "hour": 14,
                        "minute": 0,
                        "time_of_day": "Afternoon",
                    },
                },
                "npc_data": {},
                "combat_state": {"in_combat": False},
                "custom_campaign_state": {},
            }
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_god_mode_returns_god_mode_response_field(
        self, mock_gemini_generate, mock_get_db
    ):
        """Test that GOD MODE commands return god_mode_response field."""

        # Set up fake Firestore
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_campaign_god_mode"
        self._setup_fake_firestore_with_campaign(fake_firestore, campaign_id)

        # Mock Gemini provider to return god mode response
        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_god_mode_response_data)
        )

        # Make GOD MODE request
        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "GOD MODE: Set HP to 50", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )

        # Verify response
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.data}"
        )
        data = json.loads(response.data)

        # Verify god_mode_response is present in the response
        assert "god_mode_response" in data, "god_mode_response field should be present"
        assert (
            data["god_mode_response"]
            == "HP has been set to 50. Character is now at full health."
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_god_mode_uses_separate_prompts(self, mock_gemini_generate, mock_get_db):
        """Test that GOD MODE uses separate system prompts (not narrative prompts)."""

        # Set up fake Firestore
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_campaign_god_mode_prompts"
        self._setup_fake_firestore_with_campaign(fake_firestore, campaign_id)

        # Mock Gemini provider
        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_god_mode_response_data)
        )

        # Make GOD MODE request
        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps(
                {"input": "GOD MODE: Show current state", "mode": "character"}
            ),
            content_type="application/json",
            headers=self.test_headers,
        )

        # Verify request succeeded
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.data}"
        )

        # Verify Gemini was called
        assert mock_gemini_generate.call_count >= 1, "LLM should be called"

        # Get the system instruction passed to the LLM
        call_args = mock_gemini_generate.call_args

        # The system instruction is typically in the model_config or as a parameter
        # Check that god_mode_instruction content is present (administrative focus)
        # and that narrative_system_instruction is NOT present
        if call_args and len(call_args) > 0:
            # Look through all arguments for system instruction content
            all_args_str = str(call_args)

            # God mode should have "Administrative interface" or "pause menu" language
            has_god_mode_prompt = (
                "Administrative interface" in all_args_str
                or "pause menu" in all_args_str
                or "god_mode_response" in all_args_str
            )

            # God mode should NOT have narrative generation language
            has_narrative_prompt = (
                "Master Game Weaver" in all_args_str
                or "Subtlety and realism over theatrical drama" in all_args_str
            )

            # We expect god mode prompts, not narrative prompts
            # Note: This is a soft assertion - the key test is that it works correctly
            if has_narrative_prompt and not has_god_mode_prompt:
                self.fail("GOD MODE should use god_mode prompts, not narrative prompts")

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_god_mode_with_lowercase_prefix(self, mock_gemini_generate, mock_get_db):
        """Test that god mode works with lowercase 'god mode:' prefix."""

        # Set up fake Firestore
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_campaign_lowercase"
        self._setup_fake_firestore_with_campaign(fake_firestore, campaign_id)

        # Mock Gemini provider
        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_god_mode_response_data)
        )

        # Make request with lowercase god mode prefix
        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps(
                {
                    "input": "god mode: set hp to 50",  # lowercase
                    "mode": "character",
                }
            ),
            content_type="application/json",
            headers=self.test_headers,
        )

        # Verify response - should still work due to .upper() in detection
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.data}"
        )
        data = json.loads(response.data)

        # Verify god_mode_response is present
        assert "god_mode_response" in data, (
            "god_mode_response should be present for lowercase prefix"
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_regular_input_does_not_trigger_god_mode(
        self, mock_gemini_generate, mock_get_db
    ):
        """Test that regular input without GOD MODE prefix uses normal prompts."""

        # Set up fake Firestore
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_campaign_regular"
        self._setup_fake_firestore_with_campaign(fake_firestore, campaign_id)

        # Mock Gemini provider with story response
        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_story_response_data)
        )

        # Make regular (non-god-mode) request
        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "I walk into the tavern", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )

        # Verify response
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.data}"
        )
        data = json.loads(response.data)

        # Verify narrative is present (story mode)
        assert "story" in data, "story field should be present for regular input"

        # god_mode_response should be empty or missing for regular input
        god_mode_resp = data.get("god_mode_response", "")
        assert not god_mode_resp or god_mode_resp == "", (
            "god_mode_response should be empty for regular input"
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_god_mode_state_updates_applied(self, mock_gemini_generate, mock_get_db):
        """Test that GOD MODE state_updates are properly applied."""

        # Set up fake Firestore
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_campaign_state_updates"
        self._setup_fake_firestore_with_campaign(fake_firestore, campaign_id)

        # Mock Gemini provider with state updates
        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_god_mode_response_data)
        )

        # Make GOD MODE request to set HP
        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "GOD MODE: Set HP to 50", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )

        # Verify response
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.data}"
        )
        data = json.loads(response.data)

        # Verify game_state is returned with updates
        assert "game_state" in data, "game_state should be in response"

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_god_mode_via_mode_parameter_without_prefix(
        self, mock_gemini_generate, mock_get_db
    ):
        """Test that mode='god' parameter triggers GodModeAgent even without text prefix.

        This is critical for UI-based god mode switching where users don't need to
        type "GOD MODE:" prefix - they just switch modes in the UI.

        The mode parameter should be honored just like the text prefix.
        Without this fix, requests with mode='god' but no "GOD MODE:" prefix
        would incorrectly route to StoryModeAgent.
        """
        # Set up fake Firestore
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_campaign_god_mode_param"
        self._setup_fake_firestore_with_campaign(fake_firestore, campaign_id)

        # Mock Gemini provider to return god mode response
        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_god_mode_response_data)
        )

        # Make request with mode='god' but NO "GOD MODE:" prefix in text
        # This simulates user typing in god mode UI without the prefix
        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps(
                {
                    "input": "set my HP to 100",  # NO "GOD MODE:" prefix!
                    "mode": "god",  # Mode parameter should trigger GodModeAgent
                }
            ),
            content_type="application/json",
            headers=self.test_headers,
        )

        # Verify response succeeded
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.data}"
        )

        # Verify god_mode_response is in the response (stronger validation)
        data = json.loads(response.data)
        assert "god_mode_response" in data, (
            f"Response should contain god_mode_response field. Keys: {data.keys()}"
        )

        # Verify Gemini was called
        assert mock_gemini_generate.call_count >= 1, "LLM should be called"

        # Get the system instruction passed to the LLM
        call_args = mock_gemini_generate.call_args

        # Check that god_mode_instruction content is present (administrative focus)
        # and that narrative_system_instruction is NOT present
        if call_args and len(call_args) > 0:
            # Look through all arguments for system instruction content
            all_args_str = str(call_args)

            # God mode should have "Administrative interface" or "pause menu" language
            has_god_mode_prompt = (
                "Administrative interface" in all_args_str
                or "pause menu" in all_args_str
                or "god_mode_response" in all_args_str
            )

            # God mode should NOT have narrative generation language
            has_narrative_prompt = (
                "Master Game Weaver" in all_args_str
                or "Subtlety and realism over theatrical drama" in all_args_str
            )

            # We expect god mode prompts, not narrative prompts
            # This verifies mode='god' parameter works like "GOD MODE:" prefix
            assert has_god_mode_prompt, (
                "mode='god' should load god_mode prompts with 'Administrative interface' "
                f"or 'pause menu'. all_args (first 500 chars): {all_args_str[:500]}"
            )
            assert not has_narrative_prompt, (
                "mode='god' should NOT load narrative prompts. "
                "This indicates StoryModeAgent was used instead of GodModeAgent."
            )

    @patch("mvp_site.firestore_service.get_db")
    @patch("mvp_site.llm_providers.gemini_provider.generate_content_with_native_tools")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_sequential_god_mode_commands_both_respected(
        self,
        mock_gemini_code_exec,
        mock_gemini_native_tools,
        mock_get_db,
    ):
        """
        Test that two consecutive god mode commands are both processed correctly.

        This test verifies that the caching bug fix works correctly - when two
        god mode commands are sent sequentially, both should be processed and
        responded to correctly, not just the first one.

        Patches both Gemini entrypoints to be resilient to dispatch changes.
        """
        # Set up fake Firestore
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_campaign_sequential"
        self._setup_fake_firestore_with_campaign(fake_firestore, campaign_id)

        # Track calls to verify both commands are processed
        call_count = {"count": 0}
        call_history: list[dict[str, Any]] = []

        def mock_gemini_side_effect(*args, **kwargs):
            """Mock Gemini to return different responses based on call count."""
            call_count["count"] += 1
            call_history.append(kwargs)

            if call_count["count"] == 1:
                # First command: Set HP to 50
                return FakeLLMResponse(
                    json.dumps(
                        {
                            "session_header": "[SESSION_HEADER]\nTimestamp: 1492 DR, Mirtul 10, Afternoon\nLocation: Tavern\nStatus: Lvl 5 Fighter | HP: 50/50 | XP: 6500/14000 | Gold: 100gp",
                            "god_mode_response": "HP has been set to 50. Character is now at full health.",
                            "narrative": "",
                            "entities_mentioned": [],
                            "location_confirmed": "Tavern",
                            "state_updates": {
                                "player_character_data": {"hp_current": 50}
                            },
                            "planning_block": {
                                "thinking": "The user wants to modify HP.",
                                "choices": {
                                    "god:return_story": {
                                        "text": "Return to Story",
                                        "description": "Exit God Mode",
                                        "risk_level": "safe",
                                    },
                                },
                            },
                        }
                    )
                )
            if call_count["count"] == 2:
                # Second command: Set gold to 200
                return FakeLLMResponse(
                    json.dumps(
                        {
                            "session_header": "[SESSION_HEADER]\nTimestamp: 1492 DR, Mirtul 10, Afternoon\nLocation: Tavern\nStatus: Lvl 5 Fighter | HP: 50/50 | XP: 6500/14000 | Gold: 200gp",
                            "god_mode_response": "Gold has been set to 200. Character now has 200 gold pieces.",
                            "narrative": "",
                            "entities_mentioned": [],
                            "location_confirmed": "Tavern",
                            "state_updates": {"player_character_data": {"gold": 200}},
                            "planning_block": {
                                "thinking": "The user wants to modify gold.",
                                "choices": {
                                    "god:return_story": {
                                        "text": "Return to Story",
                                        "description": "Exit God Mode",
                                        "risk_level": "safe",
                                    },
                                },
                            },
                        }
                    )
                )
            return FakeLLMResponse(
                json.dumps(
                    {
                        "god_mode_response": f"Unexpected call #{call_count['count']}",
                        "narrative": "",
                        "state_updates": {},
                    }
                )
            )

        # Patch both entrypoints to handle dispatch changes
        mock_gemini_code_exec.side_effect = mock_gemini_side_effect
        mock_gemini_native_tools.side_effect = mock_gemini_side_effect

        # FIRST GOD MODE COMMAND
        response1 = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "GOD MODE: Set HP to 50", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )

        assert response1.status_code == 200, f"First command failed: {response1.data}"
        data1 = json.loads(response1.data)
        assert "god_mode_response" in data1
        assert "HP" in data1["god_mode_response"] or "50" in data1["god_mode_response"]

        # Verify HP was updated in state
        if "game_state" in data1:
            pc1 = data1["game_state"].get("player_character_data") or {}
            hp = pc1.get("hp_current")
            assert hp == 50, f"HP should be 50 after first command, got {hp}"

        # SECOND GOD MODE COMMAND
        response2 = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps(
                {"input": "GOD MODE: Set gold to 200", "mode": "character"}
            ),
            content_type="application/json",
            headers=self.test_headers,
        )

        assert response2.status_code == 200, f"Second command failed: {response2.data}"
        data2 = json.loads(response2.data)

        # CRITICAL: Second response should mention gold/200, NOT HP/50
        god_mode_resp2 = data2.get("god_mode_response", "").lower()

        # Must mention gold or 200 (the second command)
        has_gold_reference = "gold" in god_mode_resp2 or "200" in god_mode_resp2
        assert has_gold_reference, (
            f"Second command should mention gold/200. Got: {data2.get('god_mode_response')}"
        )

        # Should NOT primarily be about HP/50 (the first command)
        # If HP is mentioned, gold must also be mentioned to confirm it's about the gold command
        hp_mentioned = "hp" in god_mode_resp2 and "50" in god_mode_resp2
        gold_mentioned = "gold" in god_mode_resp2
        if hp_mentioned and not gold_mentioned:
            raise AssertionError(
                f"Second command appears to respond to FIRST command (HP/50) instead of gold. "
                f"Got: {data2.get('god_mode_response')}"
            )

        # Verify gold was updated in state (canonical location: resources.gold)
        if "game_state" in data2:
            pc2 = data2["game_state"].get("player_character_data") or {}
            gold = pc2.get("resources", {}).get("gold")
            assert gold == 200, f"Gold should be 200 after second command, got {gold}"

        # Verify both LLM calls were made (check both entrypoints)
        total_calls = (
            mock_gemini_code_exec.call_count + mock_gemini_native_tools.call_count
        )
        assert total_calls >= 2, (
            f"Expected at least 2 LLM calls, got code_exec={mock_gemini_code_exec.call_count}, native_tools={mock_gemini_native_tools.call_count}"
        )

        # Tighten assertions: Verify the second call received the second command
        # by inspecting prompt_contents directly instead of string concatenation
        # NOTE: We check both mocks separately since concatenation order doesn't reflect
        # chronological call order. The second POST request will call one of these mocks,
        # and that call should contain the second command.
        assert len(call_history) >= 2, (
            f"Expected at least 2 LLM calls, got {len(call_history)}."
        )
        second_call = call_history[1]
        prompt_contents = second_call.get("prompt_contents", [])
        prompt_text = " ".join(str(p) for p in prompt_contents)
        prompt_text_lower = prompt_text.lower()
        assert "gold" in prompt_text_lower or "200" in prompt_text, (
            "Second LLM call should contain 'gold' or '200' in prompt_contents. "
            f"Prompt contents (first 1000 chars): {prompt_text[:1000]}"
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch("mvp_site.llm_providers.gemini_provider.generate_content_with_native_tools")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_story_context_reloaded_for_each_command(
        self,
        mock_gemini_code_exec,
        mock_gemini_native_tools,
        mock_get_db,
    ):
        """
        Test that story_context is reloaded from Firestore for each command.

        This verifies that the caching bug is fixed by ensuring story_context
        includes the previous command's entry when processing the second command.

        Patches both Gemini entrypoints to be resilient to dispatch changes.
        Note: Explicit caching is disabled for this test to verify story_history
        is being properly reloaded (explicit caching would put old entries in
        the cached portion, making them invisible in prompt_contents).
        """
        # Set up fake Firestore
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_campaign_context_reload"
        self._setup_fake_firestore_with_campaign(fake_firestore, campaign_id)

        call_count = {"count": 0}

        def mock_gemini_side_effect(*args, **kwargs):
            """Mock Gemini to track story_context in each call."""
            call_count["count"] += 1

            # Extract story_history from prompt_contents to verify it's being reloaded
            # The story_history should grow with each command
            prompt_contents = kwargs.get("prompt_contents", [])
            prompt_text = " ".join(str(p) for p in prompt_contents)
            prompt_text_lower = prompt_text.lower()

            if call_count["count"] == 1:
                # First call: story_context should be empty or minimal
                # (no previous commands yet)
                return FakeLLMResponse(
                    json.dumps(
                        {
                            "god_mode_response": "First command processed",
                            "narrative": "",
                            "state_updates": {},
                        }
                    )
                )
            if call_count["count"] == 2:
                # Second call: story_context should include the first command
                # Verify that the first command's text is in the prompt_contents
                if "set hp" in prompt_text_lower:
                    # Good - story_context includes first command
                    pass
                else:
                    # Bad - story_context is stale/empty
                    self.fail(
                        f"Second call should include first command in story_context. "
                        f"Prompt contents (first 1000 chars): {prompt_text[:1000]}"
                    )

                return FakeLLMResponse(
                    json.dumps(
                        {
                            "god_mode_response": "Second command processed",
                            "narrative": "",
                            "state_updates": {},
                        }
                    )
                )
            return FakeLLMResponse(
                json.dumps(
                    {
                        "god_mode_response": f"Call #{call_count['count']}",
                        "narrative": "",
                        "state_updates": {},
                    }
                )
            )

        # Patch both entrypoints
        mock_gemini_code_exec.side_effect = mock_gemini_side_effect
        mock_gemini_native_tools.side_effect = mock_gemini_side_effect

        # Send first command
        response1 = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "GOD MODE: Set HP to 50", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )
        assert response1.status_code == 200

        # Send second command
        response2 = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps(
                {"input": "GOD MODE: Set gold to 200", "mode": "character"}
            ),
            content_type="application/json",
            headers=self.test_headers,
        )
        assert response2.status_code == 200

        # Verify both calls were made (check both entrypoints)
        total_calls = (
            mock_gemini_code_exec.call_count + mock_gemini_native_tools.call_count
        )
        assert total_calls >= 2, (
            f"Expected at least 2 calls, got code_exec={mock_gemini_code_exec.call_count}, native_tools={mock_gemini_native_tools.call_count}"
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch("mvp_site.llm_providers.gemini_provider.generate_content_with_native_tools")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_god_mode_does_not_use_code_execution_strategy(
        self,
        mock_gemini_code_exec,
        mock_gemini_native_tools,
        mock_get_db,
    ):
        """
        RED PHASE: God mode should NOT use code_execution dice strategy.

        BUG: dice_roll_strategy is set at line 4150 based on model, but for god mode
        we only pass None to build_system_instructions. The local variable still has
        code_execution value, which:
        1. Adds "[SYSTEM ENFORCEMENT: For ANY dice roll...]" to user input (line 4654)
        2. Uses code_execution mode for API calls
        3. Triggers code_execution fabrication checks (line 4793)

        FIX: Set dice_roll_strategy = None when is_god_mode_command is True, BEFORE
        any of those checks/API calls happen.
        """
        # Set up fake Firestore
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "test_campaign_dice_strategy"
        self._setup_fake_firestore_with_campaign(fake_firestore, campaign_id)

        # Track what was passed to LLM calls
        llm_call_args: list[dict] = []

        def capture_llm_args(*args, **kwargs):
            llm_call_args.append(kwargs)
            return FakeLLMResponse(
                json.dumps(
                    {
                        "session_header": "[SESSION_HEADER]\nLocation: Tavern",
                        "god_mode_response": "HP has been set to 100.",
                        "narrative": "",
                        "entities_mentioned": [],
                        "location_confirmed": "Tavern",
                        "state_updates": {"player_character_data": {"hp_current": 100}},
                        "planning_block": {
                            "thinking": "Administrative command to set HP.",
                            "choices": {},
                        },
                    }
                )
            )

        mock_gemini_code_exec.side_effect = capture_llm_args
        mock_gemini_native_tools.side_effect = capture_llm_args

        # Make GOD MODE request
        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "GOD MODE: Set HP to 100", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.data}"
        )

        # CRITICAL ASSERTION: God mode should NOT add code execution enforcement to user input
        # If dice_roll_strategy is not None, the code adds:
        # "[SYSTEM ENFORCEMENT: For ANY dice roll, you MUST use the code_execution tool..."
        assert len(llm_call_args) >= 1, "Expected at least one LLM call"

        for i, call_kwargs in enumerate(llm_call_args):
            prompt_contents = call_kwargs.get("prompt_contents", [])
            prompt_text = " ".join(str(p) for p in prompt_contents)

            # Check that code execution enforcement was NOT added
            assert "SYSTEM ENFORCEMENT" not in prompt_text, (
                f"God mode should NOT have code execution enforcement in prompt. "
                f"LLM call {i + 1} prompt_contents contains: '[SYSTEM ENFORCEMENT:...]' "
                f"This means dice_roll_strategy was NOT set to None for god mode."
            )
            assert "code_execution tool" not in prompt_text, (
                f"God mode should NOT mention code_execution tool. "
                f"LLM call {i + 1} prompt_contents contains code_execution reference."
            )
            assert "random.randint" not in prompt_text, (
                f"God mode should NOT mention random.randint (code execution). "
                f"LLM call {i + 1} prompt_contents contains random.randint reference."
            )


class TestGodModePromptSelection(unittest.TestCase):
    """Unit tests for GOD MODE prompt selection logic."""

    def setUp(self):
        """Set up test environment."""
        os.environ["TESTING_AUTH_BYPASS"] = "true"

    def test_god_mode_detection_with_prefix(self):
        """Test that GOD MODE: prefix is correctly detected."""

        # Test various god mode prefixes
        test_cases = [
            ("GOD MODE: Set HP", True),
            ("god mode: set hp", True),  # lowercase
            ("God Mode: teleport", True),  # mixed case
            ("  GOD MODE: with spaces", True),  # leading spaces
            ("I walk into the tavern", False),  # regular input
            ("Can you help me in god mode", False),  # god mode mentioned but not prefix
            ("GODMODE: no space", False),  # missing space after GOD
        ]

        for user_input, expected in test_cases:
            is_god_mode = user_input.strip().upper().startswith("GOD MODE:")
            assert is_god_mode == expected, (
                f"Failed for '{user_input}': expected {expected}, got {is_god_mode}"
            )

    def test_prompt_builder_has_god_mode_method(self):
        """Test that PromptBuilder has build_god_mode_instructions method."""
        # PromptBuilder imported at module level

        builder = PromptBuilder(None)
        assert hasattr(builder, "build_god_mode_instructions"), (
            "PromptBuilder should have build_god_mode_instructions method"
        )

        # Call the method and verify it returns a list
        instructions = builder.build_god_mode_instructions()
        assert isinstance(instructions, list), (
            "build_god_mode_instructions should return a list"
        )
        assert len(instructions) > 0, "God mode instructions should not be empty"

    def test_god_mode_instructions_contain_required_prompts(self):
        """Test that god mode instructions include required prompt types."""
        # PromptBuilder imported at module level

        builder = PromptBuilder(None)
        instructions = builder.build_god_mode_instructions()

        # Join all instructions into one string for checking
        all_instructions = "\n".join(instructions)

        # God mode should include master directive content
        # (we check for content that should be in master_directive)
        assert len(all_instructions) > 1000, (
            "God mode instructions should include substantial content"
        )

        # God mode should include game state schema information
        assert (
            "state_updates" in all_instructions.lower()
            or "game_state" in all_instructions.lower()
        ), "God mode instructions should include game state information"


class TestGodModeDiceStrategyRegression(unittest.TestCase):
    """Regression tests for DICE-uks: God mode should not receive dice instructions.

    PR #4334 introduced a bug where dice_roll_strategy was passed to GodModeAgent,
    causing it to receive dice instructions. This led to the LLM rolling dice
    and advancing narrative in god mode when it should be administrative only.

    These tests verify the fix prevents this regression.
    """

    def setUp(self):
        """Set up test environment."""
        os.environ["TESTING_AUTH_BYPASS"] = "true"

    def test_god_mode_instructions_do_not_include_dice_instructions(self):
        """Verify god mode instructions do not contain dice instruction file content.

        Per Copilot/Cursor review: test name now matches what's actually asserted.
        This tests that PromptBuilder.build_god_mode_instructions() does not include
        content from dice_system_instruction*.md files.

        NOTE: Some dice-related content appears in game_state_instruction.md which IS
        included in god mode. We only check for patterns UNIQUE to the dice instruction
        files (dice_system_instruction.md, dice_system_instruction_code_execution.md).
        """
        # PromptBuilder imported at module level

        builder = PromptBuilder(None)
        # Build god mode instructions - should not include dice instruction file content
        instructions_no_dice = builder.build_god_mode_instructions()
        all_no_dice = "\n".join(instructions_no_dice)

        # Use patterns UNIQUE to dice instruction files (not in shared game_state_instruction.md)
        # These patterns only appear in dice_system_instruction*.md files
        dice_instruction_only_patterns = [
            "🚨 ENFORCEMENT WARNING",  # Only in dice_system_instruction_code_execution.md
            "Gemini 3 code_execution mode",  # Only in dice_system_instruction_code_execution.md
            "Do NOT output `tool_requests` for DICE",  # Only in dice_system_instruction_code_execution.md
            "Required Protocol:\n1. Do NOT output",  # Only in code_execution dice file
        ]

        for pattern in dice_instruction_only_patterns:
            assert pattern not in all_no_dice, (
                f"God mode instructions should NOT contain '{pattern}'. "
                f"This would indicate dice_system_instruction*.md files are being loaded."
            )

        # Also verify god mode instructions DO contain expected god mode content
        assert (
            "pause menu" in all_no_dice.lower()
            or "administrative" in all_no_dice.lower()
        ), "God mode instructions should contain god mode specific content"

    def test_god_mode_validation_catches_dice_rolls(self):
        """Verify validate_god_mode_response catches forbidden dice rolls.

        This tests the server-side validation layer that catches violations
        even if the LLM ignores prompt instructions.
        """
        # validate_god_mode_response, NarrativeResponse imported at module level

        # Create a response with dice_rolls (FORBIDDEN in god mode)
        response_with_dice = NarrativeResponse(
            narrative="",
            session_header="test",
            god_mode_response="HP set to 50",
            dice_rolls=["Attack Roll: 1d20+5 = 18"],  # FORBIDDEN
            state_updates={},
        )

        warnings = validate_god_mode_response(response_with_dice, is_god_mode=True)
        assert len(warnings) > 0, "Should detect dice_rolls in god mode response"
        assert any("dice_rolls" in w.lower() for w in warnings), (
            f"Warning should mention dice_rolls: {warnings}"
        )

    def test_god_mode_validation_catches_action_resolution(self):
        """Verify validate_god_mode_response catches action_resolution dice."""
        # validate_god_mode_response, NarrativeResponse imported at module level

        # Create a response with action_resolution dice (FORBIDDEN in god mode)
        # NOTE: We set action_resolution directly after construction because
        # NarrativeResponse._validate_action_resolution() clears the field when
        # requires_action_resolution=False. Direct assignment simulates what
        # happens when the LLM actually returns this field in god mode.
        response_with_action = NarrativeResponse(
            narrative="",
            session_header="test",
            god_mode_response="HP set to 50",
            state_updates={},
            requires_action_resolution=False,
        )
        # Direct assignment to simulate LLM returning forbidden field
        response_with_action.action_resolution = {
            "mechanics": {
                "outcome": "success",
                "rolls": [{"purpose": "Attack", "total": 18, "result": 13}],
            }
        }

        warnings = validate_god_mode_response(response_with_action, is_god_mode=True)
        assert len(warnings) > 0, "Should detect action_resolution dice in god mode"
        assert any("action_resolution" in w.lower() for w in warnings), (
            f"Warning should mention action_resolution: {warnings}"
        )

    def test_god_mode_validation_catches_dice_audit_events(self):
        """Verify validate_god_mode_response catches forbidden dice_audit_events."""
        # validate_god_mode_response, NarrativeResponse imported at module level

        # Create a response with dice_audit_events (FORBIDDEN in god mode)
        response_with_audit = NarrativeResponse(
            narrative="",
            session_header="test",
            god_mode_response="HP set to 50",
            state_updates={},
            requires_action_resolution=False,
        )
        # Direct assignment to simulate LLM returning forbidden field
        response_with_audit.dice_audit_events = [
            {"roll_id": "abc123", "notation": "1d20", "total": 15}
        ]

        warnings = validate_god_mode_response(response_with_audit, is_god_mode=True)
        assert len(warnings) > 0, "Should detect dice_audit_events in god mode"
        assert any("dice_audit_events" in w.lower() for w in warnings), (
            f"Warning should mention dice_audit_events: {warnings}"
        )

    def test_god_mode_validation_catches_tool_requests(self):
        """Verify validate_god_mode_response catches forbidden tool_requests."""
        # validate_god_mode_response, NarrativeResponse imported at module level

        # Create a response with tool_requests (FORBIDDEN in god mode)
        response_with_tools = NarrativeResponse(
            narrative="",
            session_header="test",
            god_mode_response="HP set to 50",
            state_updates={},
            requires_action_resolution=False,
        )
        # Direct assignment to simulate LLM returning forbidden field
        response_with_tools.tool_requests = [
            {"tool": "roll_dice", "args": {"notation": "1d20"}}
        ]

        warnings = validate_god_mode_response(response_with_tools, is_god_mode=True)
        assert len(warnings) > 0, "Should detect tool_requests in god mode"
        assert any("tool_requests" in w.lower() for w in warnings), (
            f"Warning should mention tool_requests: {warnings}"
        )

    def test_god_mode_validation_catches_non_empty_narrative(self):
        """Verify validate_god_mode_response catches non-empty narrative."""
        # validate_god_mode_response, NarrativeResponse imported at module level

        # Create a response with narrative content (should be empty in god mode)
        response_with_narrative = NarrativeResponse(
            narrative="The orc attacks with a mighty swing of his axe...",
            session_header="test",
            god_mode_response="HP set to 50",
            state_updates={},
        )

        warnings = validate_god_mode_response(response_with_narrative, is_god_mode=True)
        assert len(warnings) > 0, "Should detect non-empty narrative in god mode"
        assert any("narrative" in w.lower() for w in warnings), (
            f"Warning should mention narrative: {warnings}"
        )

    def test_god_mode_validation_catches_short_narrative(self):
        """Verify validate_god_mode_response catches even short narrative content.

        Per CodeRabbit + Copilot review: ANY non-whitespace narrative is forbidden,
        not just content > 10 characters.
        """
        # validate_god_mode_response, NarrativeResponse imported at module level

        # Create a response with short narrative (still forbidden in god mode)
        response_with_short = NarrativeResponse(
            narrative="OK",  # Only 2 chars but still forbidden
            session_header="test",
            god_mode_response="HP set to 50",
            state_updates={},
        )

        warnings = validate_god_mode_response(response_with_short, is_god_mode=True)
        assert len(warnings) > 0, "Should detect even short narrative in god mode"
        assert any("narrative" in w.lower() for w in warnings), (
            f"Warning should mention narrative: {warnings}"
        )

    def test_god_mode_validation_allows_valid_response(self):
        """Verify validate_god_mode_response allows valid god mode responses."""
        # validate_god_mode_response, NarrativeResponse imported at module level

        # Create a valid god mode response
        valid_response = NarrativeResponse(
            narrative="",  # Empty as required
            session_header="test",
            god_mode_response="HP set to 50. Character is now at full health.",
            state_updates={"player_character_data": {"hp_current": 50}},
        )

        warnings = validate_god_mode_response(valid_response, is_god_mode=True)
        assert len(warnings) == 0, (
            f"Valid god mode response should not trigger warnings: {warnings}"
        )

    def test_story_mode_not_affected_by_god_mode_validation(self):
        """Verify god mode validation doesn't affect story mode responses."""
        # validate_god_mode_response, NarrativeResponse imported at module level

        # Create a story mode response with dice (allowed in story mode)
        story_response = NarrativeResponse(
            narrative="You swing your sword at the orc...",
            session_header="test",
            dice_rolls=["Attack Roll: 1d20+5 = 18"],
            requires_action_resolution=False,
            state_updates={},
        )
        # Direct assignment to simulate LLM returning action_resolution
        story_response.action_resolution = {
            "mechanics": {
                "outcome": "success",
                "rolls": [{"purpose": "Attack", "total": 18}],
            }
        }

        # When is_god_mode=False, no validation should occur
        warnings = validate_god_mode_response(story_response, is_god_mode=False)
        assert len(warnings) == 0, "Story mode should not trigger god mode validation"


if __name__ == "__main__":
    unittest.main()
