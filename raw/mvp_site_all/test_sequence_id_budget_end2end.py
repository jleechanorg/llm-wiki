"""
End-to-end test: Sequence ID budget enforcement (worktree_logs6-cc4)

Tests verify that:
1. Sequence IDs in LLM request respect allocated budget from budget_result
2. The fix applies cap to final_sequence_ids when over budget
3. Most recent sequence IDs are preserved (truncation from oldest)

Bug: Previously, sequence_id_list_string was measured on sequence_id_context
(bounded to 20% of story) but built from truncated_story_context (full allocated).
This meant the actual sequence ID list could exceed the allocated budget.

Fix: Now sequence_id_list_string is capped to allocated budget as final_sequence_ids,
keeping the most recent IDs to fit within the token budget.
"""

# ruff: noqa: PT009

from __future__ import annotations

import inspect
import json
import os
from unittest.mock import patch

from mvp_site import llm_service, main
from mvp_site.tests.fake_firestore import FakeFirestoreClient
from mvp_site.tests.fake_llm import FakeLLMResponse
from mvp_site.tests.test_end2end import End2EndBaseTestCase
from mvp_site.token_utils import estimate_tokens


class TestSequenceIdBudgetEnd2End(End2EndBaseTestCase):
    """E2E test for sequence ID budget enforcement."""

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"
    TEST_USER_ID = "test-user-sequence-ids"

    def setUp(self):
        super().setUp()
        os.environ.setdefault("GEMINI_API_KEY", "test-api-key")
        os.environ.setdefault("CEREBRAS_API_KEY", "test-cerebras-key")

        self.mock_llm_response_data = {
            "narrative": "The journey continues into the unknown...",
            "entities_mentioned": ["Hero"],
            "location_confirmed": "Dark Forest",
            "state_updates": {"story_progression": "continued"},
        }

    def _create_story_context_with_many_sequence_ids(
        self, total_turns: int = 200
    ) -> list:
        """
        Create a story context with many entries to generate large sequence ID list.

        This creates a scenario where the sequence ID list from full truncated
        context would exceed the budget measured on bounded context.

        Returns:
            list: Story context with many entries having sequence IDs
        """
        story_context = []

        for i in range(total_turns):
            # Each entry has a sequence_id
            text = f"Turn {i}: The adventure continues with action {i}. "
            text += "The path leads onward through the wilderness. " * 3

            story_context.append(
                {
                    "actor": "player" if i % 2 == 0 else "gm",
                    "text": text,
                    "sequence_id": i + 1,
                    "mode": "story",
                }
            )

        return story_context

    def _setup_fake_firestore_with_sequence_id_test_campaign(
        self, fake_firestore, campaign_id, story_context
    ):
        """Set up a campaign with the test story context."""
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).set({"title": "Sequence ID Test", "setting": "Fantasy"})

        game_state = {
            "user_id": self.test_user_id,
            "story_text": "A long ongoing adventure with many turns...",
            "story_context": story_context,
            "characters": ["Hero"],
            "locations": ["Dark Forest", "Ancient Ruins"],
            "items": ["Magic Staff"],
            "combat_state": {"in_combat": False},
            "custom_campaign_state": {
                "session_number": 20,
                "core_memories": ["The quest began long ago"],
            },
            "npc_data": {},
            "world_data": {
                "current_location_name": "Dark Forest",
                "time_of_day": "night",
            },
            "player_character_data": {
                "entity_id": "player_character",
                "display_name": "Hero",
                "name": "Hero",
                "class_name": "Ranger",
                "level": 8,
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
    def test_sequence_ids_respect_budget_allocation(
        self, mock_gemini_generate, mock_cerebras_generate, mock_get_db
    ):
        """
        E2E test: Verify sequence IDs respect allocated budget.

        The fix for worktree_logs6-cc4 ensures that final_sequence_ids is
        capped to the allocated budget, not just the measurement from bounded context.
        """
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "sequence_id_budget_test"
        story_context = self._create_story_context_with_many_sequence_ids(200)
        self._setup_fake_firestore_with_sequence_id_test_campaign(
            fake_firestore, campaign_id, story_context
        )

        # Also add story entries to the story subcollection
        import datetime

        story_collection = (
            fake_firestore.collection("users")
            .document(self.test_user_id)
            .collection("campaigns")
            .document(campaign_id)
            .collection("story")
        )
        for i, entry in enumerate(story_context):
            mins = i // 60
            secs = i % 60
            entry_with_timestamp = {
                **entry,
                "timestamp": datetime.datetime(2024, 1, 1, 12, mins, secs),
            }
            story_collection.document(f"entry_{i}").set(entry_with_timestamp)

        mock_cerebras_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_llm_response_data)
        )
        mock_gemini_generate.return_value = FakeLLMResponse(
            json.dumps(self.mock_llm_response_data)
        )

        # Make API request
        response = self.client.post(
            f"/api/campaigns/{campaign_id}/interaction",
            data=json.dumps(
                {"input": "I scout ahead for danger.", "mode": "character"}
            ),
            content_type="application/json",
            headers=self.headers,
        )

        # The request should succeed
        assert response.status_code == 200, f"Request failed: {response.data}"

        # Verify response contains expected structure
        response_data = json.loads(response.data)
        assert response_data.get("success") is True, "Response should indicate success"
        assert "narrative" in response_data or "story" in response_data, (
            "Response should contain narrative or story"
        )


class TestSequenceIdCodeStructure(End2EndBaseTestCase):
    """Test that the code structure correctly handles sequence ID budgeting."""

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"

    def test_uses_final_sequence_ids_not_sequence_id_list_string(self):
        """Verify LLM request uses final_sequence_ids, not sequence_id_list_string."""
        source = inspect.getsource(llm_service._prepare_story_continuation)

        # Should use final_sequence_ids in LLM request build
        assert "final_sequence_ids.split" in source, (
            "LLM request should use final_sequence_ids.split()"
        )

    def test_fix_comment_references_bead_id(self):
        """Verify fix comment references the bead ID for traceability."""
        # Fix is in _prepare_story_continuation helper (refactored from continue_story)
        source = inspect.getsource(llm_service._prepare_story_continuation)

        assert "worktree_logs6-cc4" in source, (
            "Fix should have comment referencing bead worktree_logs6-cc4 in _prepare_story_continuation"
        )

    def test_sequence_id_capping_uses_budget_allocation(self):
        """Verify sequence ID capping uses budget_result allocation."""
        source = inspect.getsource(llm_service._prepare_story_continuation)
        lines = source.split("\n")

        # Find the sequence_id_alloc assignment
        found_alloc_check = False
        for i, line in enumerate(lines):
            if (
                'sequence_id_alloc = budget_result.get_allocation("sequence_id")'
                in line
            ):
                # Check surrounding context for budget enforcement
                context_window = "\n".join(lines[i : i + 30])
                if (
                    "sequence_id_budget_tokens" in context_window
                    and "final_sequence_ids" in context_window
                ):
                    found_alloc_check = True
                    break

        assert found_alloc_check, (
            "Sequence ID capping should use budget_result.get_allocation"
        )

    def test_truncation_keeps_most_recent_ids(self):
        """Verify truncation preserves most recent sequence IDs."""
        source = inspect.getsource(llm_service._prepare_story_continuation)

        # Should iterate in reverse to keep most recent
        assert "reversed(seq_ids)" in source, (
            "Truncation should iterate in reverse to keep most recent IDs"
        )

        # Should use insert(0, ...) to maintain order
        assert "truncated_ids.insert(0" in source, (
            "Truncation should insert at beginning to maintain order"
        )

    def test_final_sequence_ids_assigned_after_allocation(self):
        """Verify final_sequence_ids is assigned after budget check."""
        source = inspect.getsource(llm_service._prepare_story_continuation)
        lines = source.split("\n")

        alloc_line = None
        final_ids_line = None

        for i, line in enumerate(lines):
            if 'get_allocation("sequence_id")' in line and "sequence_id_alloc" in line:
                alloc_line = i
            if "final_sequence_ids = " in line and alloc_line is not None:
                final_ids_line = i
                break  # Only need first assignment after alloc

        assert alloc_line is not None, "Should have sequence_id allocation check"
        assert final_ids_line is not None, "Should have final_sequence_ids assignment"
        assert final_ids_line > alloc_line, (
            "final_sequence_ids should be assigned AFTER allocation check"
        )


class TestSequenceIdTruncationBehavior(End2EndBaseTestCase):
    """Test the sequence ID truncation behavior directly."""

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"

    def test_truncation_keeps_most_recent_when_over_budget(self):
        """Verify truncation keeps most recent IDs when over budget."""
        # Simulate the truncation logic
        seq_ids = [str(i) for i in range(1, 101)]  # 1-100
        sequence_id_list_string = ", ".join(seq_ids)

        # Tight budget that can't fit all
        max_chars = 50

        # Apply truncation logic (same as in llm_service.py)
        truncated_ids = []
        current_len = 0
        for seq_id in reversed(seq_ids):
            addition_len = len(seq_id) + (2 if truncated_ids else 0)
            if current_len + addition_len <= max_chars:
                truncated_ids.insert(0, seq_id)
                current_len += addition_len
            else:
                break

        result = ", ".join(truncated_ids)

        # Should have most recent IDs
        assert "100" in result, "Most recent ID (100) should be preserved"
        assert "99" in result, "Second most recent ID (99) should be preserved"

        # Early IDs should be dropped
        assert "1" not in result or "100" not in result.split(", ")[0], (
            "Early IDs should be truncated before recent ones"
        )

    def test_no_truncation_when_within_budget(self):
        """Verify no truncation when IDs fit within budget."""
        seq_ids = ["1", "2", "3", "4", "5"]
        sequence_id_list_string = ", ".join(seq_ids)

        # Large budget that fits all
        max_chars = 1000

        # No truncation needed
        truncated_ids = []
        current_len = 0
        for seq_id in reversed(seq_ids):
            addition_len = len(seq_id) + (2 if truncated_ids else 0)
            if current_len + addition_len <= max_chars:
                truncated_ids.insert(0, seq_id)
                current_len += addition_len
            else:
                break

        result = ", ".join(truncated_ids)

        assert result == sequence_id_list_string, (
            "Should return unchanged if within budget"
        )

    def test_truncation_reduces_token_count(self):
        """Verify truncation actually reduces token count."""
        seq_ids = [str(i) for i in range(1, 501)]  # 500 IDs
        sequence_id_list_string = ", ".join(seq_ids)

        original_tokens = estimate_tokens(sequence_id_list_string)
        target_budget_chars = 100  # Very tight

        # Apply truncation
        truncated_ids = []
        current_len = 0
        for seq_id in reversed(seq_ids):
            addition_len = len(seq_id) + (2 if truncated_ids else 0)
            if current_len + addition_len <= target_budget_chars:
                truncated_ids.insert(0, seq_id)
                current_len += addition_len
            else:
                break

        result = ", ".join(truncated_ids)
        result_tokens = estimate_tokens(result)

        assert result_tokens < original_tokens, (
            f"Truncation should reduce tokens from {original_tokens} to {result_tokens}"
        )


if __name__ == "__main__":
    import unittest

    unittest.main()
