"""
TDD Test: Single Budget Path Consistency (worktree_logs6-drk)

Tests verify that:
1. No merge conflict markers exist in llm_service.py (worktree_logs6-cv8)
2. Only one budget path is used (new allocator, not legacy scaffold) (worktree_logs6-drk)
3. Budget allocation integrates correctly with continue_story
"""

import os

import pytest

from mvp_site import constants, llm_service
from mvp_site.context_compaction import _allocate_request_budget
from mvp_site.game_state import GameState

import inspect

# Cache source once; under coverage instrumentation this avoids repeated expensive lookups.
_CONTINUE_STORY_SOURCE = inspect.getsource(llm_service._prepare_story_continuation)


class TestMergeConflictResolution:
    """Test that merge conflict markers are resolved (worktree_logs6-cv8)."""

    def test_no_merge_conflict_markers_in_file(self):
        """Verify no merge conflict markers in llm_service.py."""
        file_path = os.path.join(os.path.dirname(__file__), "..", "llm_service.py")

        with open(file_path) as f:
            lines = f.readlines()

        # Check for actual merge conflict markers (at start of line)
        # Comment separators like "# ========" are OK
        for i, line in enumerate(lines, 1):
            assert not line.startswith("<<<<<<< HEAD"), (
                f"Found HEAD conflict marker at line {i}"
            )
            assert not line.startswith("=======\n"), (
                f"Found separator conflict marker at line {i}"
            )
            assert not line.startswith(">>>>>>>"), (
                f"Found end conflict marker at line {i}"
            )

    def test_llm_service_imports_successfully(self):
        """Verify llm_service.py is valid Python and imports."""
        # If we got this far, the import at module level succeeded
        assert hasattr(llm_service, "continue_story")
        assert hasattr(llm_service, "_allocate_request_budget")


class TestBudgetPathConsistency:
    """Test single budget path is used (worktree_logs6-drk)."""

    def test_uses_new_allocator_not_legacy_scaffold(self):
        """Verify continue_story uses new budget allocator, not legacy scaffold."""
        # Check that _allocate_request_budget is imported from context_compaction
        from mvp_site.context_compaction import _allocate_request_budget as allocator

        # Verify it's the same function used in llm_service
        assert llm_service._allocate_request_budget == allocator
        assert allocator is not None

    def test_no_legacy_scaffold_tokens_calculation(self):
        """Verify no legacy scaffold_tokens calculation in budget path."""
        source = _CONTINUE_STORY_SOURCE

        # Legacy pattern: scaffold_tokens_raw = estimate_tokens(prompt_scaffold)
        # This should NOT exist in the new budget path
        assert "scaffold_tokens_raw" not in source, (
            "Found legacy scaffold_tokens_raw calculation"
        )

        # New pattern: budget_result = _allocate_request_budget(...)
        # This SHOULD exist
        assert "budget_result" in source, "New budget_result allocation not found"
        assert "_allocate_request_budget" in source, "New allocator function not called"

    def test_budget_result_used_consistently(self):
        """Verify budget_result is used for story budget, not scaffold calculation."""
        source = _CONTINUE_STORY_SOURCE

        # Should use budget_result.get_story_budget(), not manual calculation
        assert "budget_result.get_story_budget()" in source, (
            "budget_result.get_story_budget() not found"
        )

        # Should NOT have legacy "max_input_allowed - scaffold_tokens" pattern
        assert "max_input_allowed - scaffold_tokens" not in source, (
            "Found legacy budget calculation pattern"
        )

    def test_sequence_id_budget_uses_truncated_context(self):
        """Verify sequence_id budgeting uses a truncated story context."""
        source = _CONTINUE_STORY_SOURCE

        assert "_get_sequence_id_context_for_budget" in source, (
            "continue_story should use _get_sequence_id_context_for_budget for sequence_id sizing"
        )

    def test_sequence_id_context_for_budget_truncates(self):
        """Verify sequence_id budget helper truncates oversized story context."""
        # Keep this deliberately small so the test is fast even with coverage overhead,
        # while still forcing truncation via a very low max_input_allowed.
        story_context = [{"text": "X" * 400, "sequence_id": i} for i in range(1, 31)]
        game_state = GameState(user_id="test_user")

        truncated = llm_service._get_sequence_id_context_for_budget(
            story_context=story_context,
            max_input_allowed=5000,
            model_name=constants.DEFAULT_GEMINI_MODEL,
            current_game_state=game_state,
            provider_name=constants.LLM_PROVIDER_CEREBRAS,
        )

        assert truncated, "Expected truncated story context to be non-empty"
        assert len(truncated) < len(story_context), (
            "Expected sequence_id budget context to be shorter than full story_context"
        )
        assert truncated[-1].get("sequence_id") == story_context[-1].get(
            "sequence_id"
        ), "Expected truncated context to preserve most recent sequence_id"

    def test_compacted_game_state_preserves_campaign_id(self):
        """Verify campaign_id is retained when using compacted game_state."""
        base_state = {"foo": "bar"}
        compacted_game_state = '{"foo": "bar"}'

        updated = llm_service._apply_compacted_game_state(
            game_state_for_llm=base_state,
            compacted_game_state=compacted_game_state,
            campaign_id="camp-123",
        )

        assert updated.get("campaign_id") == "camp-123"

    def test_compacted_game_state_preserves_user_settings(self):
        """Verify user_settings is retained when using compacted game_state."""
        base_state = {"foo": "bar"}
        compacted_game_state = '{"foo": "bar"}'
        user_settings = {"spicy_mode": True}

        updated = llm_service._apply_compacted_game_state(
            game_state_for_llm=base_state,
            compacted_game_state=compacted_game_state,
            campaign_id=None,
            user_settings=user_settings,
        )

        assert updated.get("user_settings") == {"spicy_mode": True}


class TestBudgetAllocationIntegration:
    """Test budget allocation integrates with continue_story."""

    @pytest.mark.skip(reason="Integration test - requires full mock setup")
    def test_continue_story_uses_budget_allocator(self):
        """Integration test: continue_story calls budget allocator."""
        # This would require extensive mocking of GameState, Firebase, etc.
        # Placeholder for future integration test

    def test_allocator_returns_expected_structure(self):
        """Verify budget allocator returns expected result structure."""
        result = _allocate_request_budget(
            max_input_allowed=100_000,
            system_instruction="Test instruction",
            game_state_json='{"hp": 100}',
            core_memories="Test memories",
            entity_tracking_estimate=1000,
            story_context=[{"text": "Test story"}],
        )

        # Verify result has required methods/attributes
        assert hasattr(result, "get_story_budget")
        assert hasattr(result, "allocations")
        assert hasattr(result, "warnings")
        assert hasattr(result, "compacted_content")

        # Verify get_story_budget returns int
        story_budget = result.get_story_budget()
        assert isinstance(story_budget, int)
        assert story_budget > 0


class TestBudgetPathDocumentation:
    """Test that budget path is documented (acceptance criteria)."""

    def test_budget_allocation_has_comments(self):
        """Verify budget allocation block has explanatory comments."""
        source = _CONTINUE_STORY_SOURCE

        # Should have comment explaining the new budget allocation
        # Look for comments around budget_result assignment
        lines = source.split("\n")
        budget_line_idx = None

        for i, line in enumerate(lines):
            if "budget_result = _allocate_request_budget" in line:
                budget_line_idx = i
                break

        assert budget_line_idx is not None, "budget_result allocation not found"

        # Check preceding lines for comment
        preceding_lines = "\n".join(
            lines[max(0, budget_line_idx - 5) : budget_line_idx]
        )

        # Should have comment about component allocation or min/max percentages
        assert (
            "component" in preceding_lines.lower()
            or "allocate" in preceding_lines.lower()
            or "budget" in preceding_lines.lower()
        ), "No explanatory comment before budget allocation"
