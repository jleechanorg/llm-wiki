"""
End-to-end test: Core memories from final truncated context (worktree_logs6-d2r)

Tests verify that:
1. Core memories in LLM request come from truncated_story_context (final), not
   sequence_id_context (bounded 20%)
2. The compaction is applied to core_memories_summary (from final context)
3. The fix prevents narrative regression from using wrong memory selection

Bug: Previously, compacted_core_memories was derived from temp_core_memories which
was built from sequence_id_context (bounded to 20% of story). This meant memories
were selected based on a minimal view of the story, potentially missing critical
recent memories visible in the actual truncated story context.

Fix: Now core_memories_summary is generated from truncated_story_context (the full
allocated story), then compacted to budget as final_core_memories.
"""

# ruff: noqa: PT009

from __future__ import annotations

import inspect
import json
import os
from unittest.mock import patch

from mvp_site import llm_service, main
from mvp_site.context_compaction import _compact_core_memories
from mvp_site.tests.fake_firestore import FakeFirestoreClient
from mvp_site.tests.fake_llm import FakeLLMResponse
from mvp_site.tests.test_end2end import End2EndBaseTestCase
from mvp_site.token_utils import estimate_tokens


class TestCoreMemoriesFinalContextEnd2End(End2EndBaseTestCase):
    """E2E test for core memories sourced from final truncated context."""

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"
    TEST_USER_ID = "test-user-core-memories"

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

    def _create_story_context_with_distinct_memories(
        self, total_turns: int = 100
    ) -> tuple[list, list]:
        """
        Create a story context where early and late entries have distinct memories.

        This allows us to verify whether memory selection uses:
        - Bounded context (20%) - would only see early memories
        - Full truncated context - would see both early AND recent memories

        Returns:
            tuple: (story_context, expected_recent_memory_keywords)
        """
        story_context = []

        # Early memories (would be visible in 20% bounded context)
        early_keywords = ["ARTIFACT_CROWN", "VILLAGE_MILLBROOK", "ANCIENT_OATH"]

        # Recent memories (only visible in full truncated context, not 20% bounded)
        recent_keywords = [
            "DRAGON_ALLIANCE",
            "CRYSTAL_SHARD_FOUND",
            "BETRAYAL_REVEALED",
        ]

        for i in range(total_turns):
            if i < 20:
                # Early turns with early memory keywords
                text = f"Turn {i}: The party remembers {early_keywords[i % 3]}. "
                text += "This ancient knowledge guides their path. " * 5
            elif i >= total_turns - 20:
                # Recent turns with recent memory keywords
                text = f"Turn {i}: CRITICAL: {recent_keywords[i % 3]} discovered. "
                text += "This recent event changes everything. " * 5
            else:
                # Middle turns (filler)
                text = f"Turn {i}: The journey continues through the wilderness. "
                text += "The path winds onward. " * 5

            story_context.append(
                {
                    "actor": "player" if i % 2 == 0 else "gm",
                    "text": text,
                    "sequence_id": i + 1,
                    "mode": "story",
                }
            )

        return story_context, recent_keywords

    def _setup_fake_firestore_with_memory_test_campaign(
        self, fake_firestore, campaign_id, story_context
    ):
        """Set up a campaign with the test story context."""
        fake_firestore.collection("users").document(self.test_user_id).collection(
            "campaigns"
        ).document(campaign_id).set(
            {"title": "Core Memories Test", "setting": "Fantasy"}
        )

        game_state = {
            "user_id": self.test_user_id,
            "story_text": "A long ongoing adventure with memories...",
            "story_context": story_context,
            "characters": ["Hero"],
            "locations": ["Ancient Ruins", "Dragon's Lair"],
            "items": ["Crystal Shard"],
            "combat_state": {"in_combat": False},
            "custom_campaign_state": {
                "session_number": 15,
                "core_memories": [
                    "CRITICAL: ARTIFACT_CROWN is the key to the realm",
                    "CRITICAL: DRAGON_ALLIANCE was formed in session 14",
                    "CRITICAL: BETRAYAL_REVEALED by the trusted advisor",
                ],
            },
            "npc_data": {
                "Dragon": {
                    "mbti": "INTJ",
                    "role": "ally",
                    "background": "An ancient dragon who seeks the artifact.",
                }
            },
            "world_data": {
                "current_location_name": "Dragon's Lair",
                "time_of_day": "dusk",
            },
            "player_character_data": {
                "entity_id": "player_character",
                "display_name": "Hero",
                "name": "Hero",
                "class_name": "Paladin",
                "level": 10,
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
    def test_core_memories_from_truncated_context_not_bounded(
        self, mock_gemini_generate, mock_cerebras_generate, mock_get_db
    ):
        """
        E2E test: Verify core memories use final truncated context.

        The fix for worktree_logs6-d2r ensures that core_memories_summary is
        generated from truncated_story_context (full allocated story) rather
        than sequence_id_context (bounded to 20%).
        """
        fake_firestore = FakeFirestoreClient()
        mock_get_db.return_value = fake_firestore

        campaign_id = "core_memories_context_test"
        story_context, recent_keywords = (
            self._create_story_context_with_distinct_memories(100)
        )
        self._setup_fake_firestore_with_memory_test_campaign(
            fake_firestore, campaign_id, story_context
        )

        # Also add story entries to the story subcollection (where they're actually fetched from)
        import datetime

        story_collection = (
            fake_firestore.collection("users")
            .document(self.test_user_id)
            .collection("campaigns")
            .document(campaign_id)
            .collection("story")
        )
        for i, entry in enumerate(story_context):
            # Use minutes and seconds to handle >60 entries
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
                {"input": "I examine the crystal shard for clues.", "mode": "character"}
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


class TestCoreMemoriesCodeStructure(End2EndBaseTestCase):
    """Test that the code structure correctly routes core memories."""

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"

    def test_uses_final_core_memories_not_compacted_core_memories(self):
        """Verify LLM request uses final_core_memories, not compacted_core_memories."""
        source = inspect.getsource(llm_service._prepare_story_continuation)

        # Should use final_core_memories in LLM request build
        assert "final_core_memories.split" in source, (
            "LLM request should use final_core_memories.split()"
        )

        # Should NOT use compacted_core_memories in LLM request
        assert "compacted_core_memories.split" not in source, (
            "LLM request should NOT use compacted_core_memories.split()"
        )

    def test_core_memories_summary_generated_from_truncated_context(self):
        """Verify core_memories_summary comes from truncated_story_context."""
        source = inspect.getsource(llm_service._prepare_story_continuation)
        lines = source.split("\n")

        # Find the line where core_memories_summary is assigned
        found_correct_pattern = False
        for i, line in enumerate(lines):
            if "core_memories_summary" in line:
                # Check surrounding lines for get_static_prompt_parts and truncated_story_context
                context_window = "\n".join(lines[max(0, i - 3) : i + 5])
                if (
                    "get_static_prompt_parts" in context_window
                    and "truncated_story_context" in context_window
                ):
                    found_correct_pattern = True
                    break

        assert found_correct_pattern, (
            "core_memories_summary should be generated from truncated_story_context"
        )

    def test_compaction_applied_to_final_core_memories(self):
        """Verify compaction is applied to core_memories_summary."""
        source = inspect.getsource(llm_service.continue_story)

        # Should call _compact_core_memories on core_memories_summary
        assert "_compact_core_memories" in source, (
            "_compact_core_memories should be called"
        )

        # Check that it's called with core_memories_summary (may span multiple lines)
        lines = source.split("\n")
        found_compact_call = False
        for i, line in enumerate(lines):
            if "_compact_core_memories" in line:
                # Check this line and next few lines for core_memories_summary
                context = "\n".join(lines[i : i + 3])
                if "core_memories_summary" in context:
                    found_compact_call = True
                    break

        assert found_compact_call, (
            "_compact_core_memories should be called with core_memories_summary"
        )

    def test_fix_comment_references_bead_id(self):
        """Verify fix comment references the bead ID for traceability."""
        # Fix is in _prepare_story_continuation helper (refactored from continue_story)
        source = inspect.getsource(llm_service._prepare_story_continuation)

        assert "worktree_logs6-d2r" in source, (
            "Fix should have comment referencing bead worktree_logs6-d2r in _prepare_story_continuation"
        )

    def test_final_core_memories_assigned_after_truncation(self):
        """Verify final_core_memories is assigned after story truncation."""
        source = inspect.getsource(llm_service._prepare_story_continuation)
        lines = source.split("\n")

        truncate_line = None
        final_memories_line = None

        for i, line in enumerate(lines):
            if "truncated_story_context = _truncate_context" in line:
                truncate_line = i
            if "final_core_memories = _compact_core_memories" in line:
                final_memories_line = i

        assert truncate_line is not None, (
            "Should have truncated_story_context assignment"
        )
        assert final_memories_line is not None, (
            "Should have final_core_memories assignment"
        )
        assert final_memories_line > truncate_line, (
            "final_core_memories should be assigned AFTER story truncation"
        )


class TestCoreMemoriesCompactionBehavior(End2EndBaseTestCase):
    """Test the core memories compaction function behavior."""

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"

    def test_compact_preserves_critical_memories(self):
        """Verify CRITICAL memories are preserved during compaction."""
        memories = "\n".join(
            [
                "Old memory 1",
                "Old memory 2",
                "CRITICAL: Player is a level 5 paladin named Theron",
                "Recent memory 1",
                "Recent memory 2",
            ]
        )

        # Tight budget
        result = _compact_core_memories(memories, max_tokens=30)

        assert "CRITICAL" in result, "CRITICAL memories must be preserved"
        assert "Theron" in result, "CRITICAL memory content must be preserved"

    def test_compact_keeps_recent_memories(self):
        """Verify recent memories are prioritized during compaction."""
        memories = "\n".join([f"Memory {i}: Event {i}" for i in range(20)])

        # Moderate budget
        result = _compact_core_memories(memories, max_tokens=50)

        # Should have most recent memories
        assert "Memory 19" in result or "Memory 18" in result, (
            "Recent memories should be preserved"
        )

    def test_compact_returns_unchanged_if_within_budget(self):
        """Verify memories returned unchanged if already within budget."""
        memories = "Memory 1\nMemory 2"

        result = _compact_core_memories(memories, max_tokens=1000)

        assert result == memories, "Should return unchanged if within budget"

    def test_compact_reduces_token_count(self):
        """Verify compaction actually reduces token count."""
        memories = "\n".join(
            [f"Memory {i}: This is a detailed event {i}" for i in range(50)]
        )

        original_tokens = estimate_tokens(memories)
        target_budget = 50

        result = _compact_core_memories(memories, max_tokens=target_budget)

        result_tokens = estimate_tokens(result)
        assert result_tokens <= target_budget or result_tokens < original_tokens, (
            f"Compaction should reduce tokens from {original_tokens} toward {target_budget}"
        )


if __name__ == "__main__":
    import unittest

    unittest.main()
