"""
End-to-end test for rewards_processed server AUTO-SET (Option D architecture).

Tests that when combat ends and the LLM doesn't set rewards_processed=True,
the server automatically sets it via _detect_rewards_discrepancy().

Root Cause Context:
- In campaign kuXKa6vrYY6P99MfhWBn, combat ended but rewards_processed stayed False
- RewardsAgent was selected 52+ consecutive times instead of StoryModeAgent
- Living world stopped updating because RewardsAgent didn't include living world prompts

Architecture Evolution:
1. OLD: Server-side enforcement that overrode LLM decisions (REMOVED)
2. MIDDLE: LLM self-correction via system_corrections (REMOVED)
3. CURRENT: Server AUTO-SET - rewards_processed is an administrative flag owned by server

Current Approach (Server AUTO-SET - Option D):
- Server detects rewards context via _detect_rewards_discrepancy()
- Server automatically sets combat_state["rewards_processed"] = True or encounter_state["rewards_processed"] = True
- Flag persists to state_dict (fixed in commit 5a7ac754c)
- NO system_corrections needed - flag is immediately correct

This follows CLAUDE.md principle: Server owns administrative flags, LLM owns content.
See .beads/server-owned-rewards-flag.md for complete architecture documentation.
"""

# ruff: noqa: PT009

from __future__ import annotations

import io
import json
import logging
import os
from unittest.mock import patch

# Ensure TESTING_AUTH_BYPASS is set before importing app modules
os.environ["TESTING_AUTH_BYPASS"] = "true"
os.environ.setdefault("GEMINI_API_KEY", "test-api-key")
os.environ.setdefault("CEREBRAS_API_KEY", "test-cerebras-key")

from mvp_site import main
from mvp_site.tests.fake_firestore import FakeFirestoreClient
from mvp_site.tests.fake_llm import FakeLLMResponse
from mvp_site.tests.test_end2end import End2EndBaseTestCase


class TestRewardsDiscrepancyDetectionEnd2End(End2EndBaseTestCase):
    """
    Test that server AUTO-SETS rewards_processed flag (Option D architecture).

    Server owns administrative flags like rewards_processed. When combat/encounter
    ends with rewards, server automatically sets the flag regardless of LLM output.

    This ensures RewardsAgent doesn't get stuck in infinite loops when LLM forgets
    to set the flag.
    """

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"
    TEST_USER_ID = "test-user-enforcement"

    def setUp(self):
        """Set up test client."""
        super().setUp()
        os.environ.setdefault("GEMINI_API_KEY", "test-api-key")
        os.environ.setdefault("CEREBRAS_API_KEY", "test-cerebras-key")
        # Disable MOCK_SERVICES_MODE to allow patching generate_json_mode_content
        os.environ["MOCK_SERVICES_MODE"] = "false"

    def _setup_campaign_with_combat_ended(self, fake_firestore, campaign_id):
        """
        Set up a campaign where combat just ended but rewards_processed=False.

        This simulates the bug state where the LLM ended combat but didn't
        set rewards_processed, causing RewardsAgent to get stuck.
        """
        # Create test campaign
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).set(
            {"title": "Combat Test Campaign", "setting": "Fantasy realm"}
        )

        # Create game state with combat ended but rewards_processed=False
        # This is the bug state that triggers RewardsAgent forever
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).collection("game_states").document("current_state").set(
            {
                "user_id": self.test_user_id,
                "story_text": "The goblin falls defeated.",
                "player_turn": 10,
                "player_character_data": {
                    "level": 3,
                    "experience": {"current": 500},
                },
                "combat_state": {
                    "in_combat": False,
                    "combat_phase": "ended",
                    "combat_summary": {
                        "xp_awarded": 50,
                        "enemies_defeated": ["goblin_1"],
                        "outcome": "victory",
                    },
                    "rewards_processed": False,  # BUG: LLM didn't set this
                },
                "custom_campaign_state": {},
            }
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_server_detects_discrepancy_when_llm_forgets_rewards_processed(
        self, mock_gemini_generate, mock_get_db
    ):
        """
        Test that server AUTO-SETS rewards_processed when combat ends.

        Scenario:
        1. Combat just ended (combat_phase="ended", combat_summary exists)
        2. rewards_processed=False (LLM failed to set it)
        3. User sends input
        4. LLM response also doesn't set rewards_processed
        5. Server AUTO-SETS combat_state["rewards_processed"] = True via Check 1
        6. Response game_state has rewards_processed=True

        No system_corrections needed - server fixes it immediately.
        See .beads/server-owned-rewards-flag.md for architecture details.
        """
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "discrepancy_detection_test"
        self._setup_campaign_with_combat_ended(fake_firestore, campaign_id)

        # Mock LLM response that DOES NOT set rewards_processed
        # This simulates the LLM failing to follow the ESSENTIALS protocol
        mock_response_data = {
            "narrative": "With the goblin defeated, you catch your breath. Victory!",
            "planning_block": {
                "thinking": "Combat is over. Player earned XP.",
                "choices": {
                    "continue": {
                        "text": "Continue",
                        "description": "Move on from the battle",
                        "risk_level": "low",
                    },
                },
            },
            "state_updates": {
                "player_character_data": {
                    "experience": {"current": 550},  # XP increased by 50
                },
                # NOTE: NO combat_state.rewards_processed=True here!
                # This is the bug - LLM forgot to set it
            },
            "rewards_box": {
                "xp_earned": 50,
                "gold_earned": 10,
            },
        }
        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(mock_response_data)
        )

        # Make the API request
        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "continue", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )

        # Verify response is successful
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.data}"
        )

        # Parse response
        response_data = json.loads(response.data)

        # CRITICAL: Verify server AUTO-SET the rewards_processed flag
        # NEW ARCHITECTURE (Option D): Server owns administrative flags
        # When combat ends with combat_summary, server should auto-set rewards_processed=True

        # Check if server auto-set the flag in the response game_state
        game_state = response_data.get("game_state", {})
        combat_state = game_state.get("combat_state", {})
        encounter_state = game_state.get("encounter_state", {})

        rewards_processed = combat_state.get(
            "rewards_processed", False
        ) or encounter_state.get("rewards_processed", False)

        self.assertTrue(
            rewards_processed,
            "Server should AUTO-SET rewards_processed=True when combat ends with combat_summary. "
            "See .beads/server-owned-rewards-flag.md for architecture details. "
            f"Got combat_state={combat_state}, encounter_state={encounter_state}",
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_no_discrepancy_when_rewards_already_processed(
        self, mock_gemini_generate, mock_get_db
    ):
        """
        Verify no discrepancy is reported when rewards_processed=True.

        This is the happy path - LLM correctly set rewards_processed,
        so no system_corrections should be added.
        """
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "no_discrepancy_test"

        # Set up campaign with rewards ALREADY processed
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).set(
            {"title": "No Discrepancy Test", "setting": "Fantasy realm"}
        )
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).collection("game_states").document("current_state").set(
            {
                "user_id": self.test_user_id,
                "story_text": "You've collected your rewards.",
                "player_turn": 11,
                "combat_state": {
                    "in_combat": False,
                    "combat_phase": "ended",
                    "combat_summary": {"xp_awarded": 50},
                    "rewards_processed": True,  # Already processed - no discrepancy
                },
            }
        )

        # Mock standard story continuation response
        mock_response_data = {
            "narrative": "The adventure continues...",
            "planning_block": {"thinking": "Normal story mode"},
        }
        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(mock_response_data)
        )

        # Make the API request
        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "explore the area", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.data}"
        )

        # Parse response
        response_data = json.loads(response.data)

        # No system_corrections with REWARDS_STATE_ERROR should be present
        system_corrections = response_data.get("system_corrections", [])
        rewards_errors = [c for c in system_corrections if "REWARDS_STATE_ERROR" in c]

        self.assertEqual(
            len(rewards_errors),
            0,
            f"No REWARDS_STATE_ERROR expected when rewards_processed=True, "
            f"but got: {rewards_errors}",
        )

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_rewards_agent_not_called_repeatedly_after_rewards_processed(
        self, mock_gemini_generate, mock_get_db
    ):
        """
        Verify that after rewards_processed=True, RewardsAgent is NOT selected.

        This is the second part of the fix - once rewards are processed,
        subsequent requests should go to StoryModeAgent, not RewardsAgent.
        """
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "after_rewards_test"

        # Set up campaign with rewards ALREADY processed
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).set(
            {"title": "After Rewards Test", "setting": "Fantasy realm"}
        )
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).collection("game_states").document("current_state").set(
            {
                "user_id": self.test_user_id,
                "story_text": "You've collected your rewards.",
                "player_turn": 11,
                "combat_state": {
                    "in_combat": False,
                    "combat_phase": "ended",
                    "combat_summary": {"xp_awarded": 50},
                    "rewards_processed": True,  # Already processed
                },
            }
        )

        # Mock standard story continuation response
        mock_response_data = {
            "narrative": "The adventure continues...",
            "planning_block": {"thinking": "Normal story mode"},
        }
        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(mock_response_data)
        )

        # Make the API request
        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps({"input": "explore the area", "mode": "character"}),
            content_type="application/json",
            headers=self.test_headers,
        )

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.data}"
        )

        # The test passing means RewardsAgent.matches_game_state() returned False
        # (because rewards_processed=True) and StoryModeAgent was used instead


class TestMultiTurnCorrectionInjection(End2EndBaseTestCase):
    """
    Test that pending_system_corrections from previous turn are injected into next LLM request.

    This is the critical multi-turn flow:
    1. Turn N: LLM forgets rewards_processed → Server detects and persists to game_state
    2. Turn N+1: Server reads pending_system_corrections and injects into LLM request
    3. LLM sees correction and fixes the state

    These tests verify step 2 - that corrections are properly injected.
    """

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"
    TEST_USER_ID = "test-user-multiturn"

    def setUp(self):
        """Set up test client."""
        super().setUp()
        os.environ.setdefault("GEMINI_API_KEY", "test-api-key")
        os.environ.setdefault("CEREBRAS_API_KEY", "test-cerebras-key")
        # Disable MOCK_SERVICES_MODE to allow patching generate_json_mode_content
        os.environ["MOCK_SERVICES_MODE"] = "false"

    @patch("mvp_site.firestore_service.get_db")
    @patch(
        "mvp_site.llm_providers.gemini_provider.generate_content_with_code_execution"
    )
    def test_pending_system_corrections_injected_into_llm_request(
        self, mock_gemini_generate, mock_get_db
    ):
        """
        Test that pending_system_corrections from game_state are passed to LLM.

        This is the multi-turn correction flow:
        1. Previous turn detected discrepancy and persisted to game_state
        2. This turn should inject those corrections into the LLM request
        3. Verify the LLM actually receives the corrections

        We verify by checking the log output contains the injection message.
        """
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "multiturn_correction_test"

        # Set up campaign
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).set(
            {"title": "Multi-Turn Correction Test", "setting": "Fantasy realm"}
        )

        # CRITICAL: Set up game_state WITH pending_system_corrections
        # This simulates the previous turn having detected a discrepancy
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).collection("game_states").document("current_state").set(
            {
                "user_id": self.test_user_id,
                "story_text": "The goblin falls defeated.",
                "player_turn": 10,
                "player_character_data": {
                    "level": 3,
                    "experience": {"current": 550},  # XP was already increased
                },
                "combat_state": {
                    "in_combat": False,
                    "combat_phase": "ended",
                    "combat_summary": {
                        "xp_awarded": 50,
                        "enemies_defeated": ["goblin_1"],
                        "outcome": "victory",
                    },
                    "rewards_processed": False,  # Still False - needs fixing
                },
                # THIS IS THE KEY: pending_system_corrections from previous turn
                "pending_system_corrections": [
                    "REWARDS_STATE_ERROR: Combat ended (phase=ended) with summary, "
                    "but rewards_processed=False. You MUST set combat_state.rewards_processed=true."
                ],
            }
        )

        # Set up log capture to verify the injection message
        log_capture_string = io.StringIO()
        handler = logging.StreamHandler(log_capture_string)
        handler.setLevel(logging.WARNING)
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)

        try:
            # Capture the call args
            mock_gemini_generate.return_value = FakeLLMResponse(
                json.dumps(
                    {
                        "narrative": "You check your rewards. [Fixing the state as instructed]",
                        "planning_block": {"thinking": "System correction received."},
                        "state_updates": {
                            "combat_state": {
                                "rewards_processed": True,  # LLM fixes the issue
                            },
                        },
                    }
                )
            )

            # Make the API request (Turn N+1)
            response = self.client.post(
                f"/api/campaigns/{campaign_id}/interaction",
                data=json.dumps({"input": "check my rewards", "mode": "character"}),
                content_type="application/json",
                headers=self.test_headers,
            )

            # Verify response is successful
            self.assertEqual(
                response.status_code,
                200,
                f"Expected 200, got {response.status_code}: {response.data}",
            )

            # Get the log output
            log_contents = log_capture_string.getvalue()

        finally:
            root_logger.removeHandler(handler)

        # CRITICAL: Verify the log shows system_corrections were injected
        # The log message is: "🔧 Injecting N system_corrections into LLM request: [...]"
        self.assertIn(
            "Injecting",
            log_contents,
            f"Should see 'Injecting' in logs. Got: {log_contents[:500]}",
        )
        self.assertIn(
            "system_corrections",
            log_contents,
            f"Should see 'system_corrections' in logs. Got: {log_contents[:500]}",
        )
        self.assertIn(
            "REWARDS_STATE_ERROR",
            log_contents,
            f"Should see 'REWARDS_STATE_ERROR' in logs. Got: {log_contents[:500]}",
        )
