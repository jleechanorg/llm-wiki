"""
Division by Zero Guards in context_compaction.py

Consolidated tests for:
- BEAD REV-44t: Fix division by zero in compaction_ratio calculations
- Bug worktree_logs6-6lg: Fix division by zero in RequestBudgetResult.log_summary()

Test Matrix Coverage: [4,1,1] through [4,2,1] (13 tests total)

These tests verify:
1. compaction_ratio calculations handle zero-token components gracefully
2. RequestBudgetResult.log_summary() guards against division by zero
"""

import unittest

from mvp_site.context_compaction import (
    BudgetAllocation,
    RequestBudgetResult,
    _allocate_request_budget,
)


class TestDivisionGuards(unittest.TestCase):
    """Test division by zero guards in budget result logging."""

    def test_normal_division_calculates_percentage(self):
        """
        [4,1,1] RED TEST: Normal division should calculate percentage correctly.

        Baseline test - normal case should work.
        """
        # Arrange: Normal budget allocation
        allocations = {
            "system_instruction": BudgetAllocation(
                component="system_instruction",
                measured_tokens=50000,
                allocated_tokens=50000,
                was_compacted=False,
                compaction_ratio=1.0,
            )
        }
        result = RequestBudgetResult(
            max_input_allowed=100000,
            allocations=allocations,
            warnings=[],
            compacted_content={},
        )

        # Act: Generate log summary (should not crash)
        summary = result.log_summary()

        # Assert: Should calculate 50% correctly
        self.assertIn("50.0%", summary)
        self.assertIn("system_instruction", summary)

    def test_zero_budget_zero_tokens_no_exception(self):
        """
        [4,1,2] RED TEST: Zero budget with zero tokens → 0.0% (no exception).

        Currently FAILS with ZeroDivisionError at line 163.
        """
        # Arrange: Zero budget allocation (edge case)
        allocations = {
            "system_instruction": BudgetAllocation(
                component="system_instruction",
                measured_tokens=0,
                allocated_tokens=0,
                was_compacted=False,
                compaction_ratio=1.0,
            )
        }
        result = RequestBudgetResult(
            max_input_allowed=0,  # ← Zero budget triggers division by zero
            allocations=allocations,
            warnings=[],
            compacted_content={},
        )

        # Act: Generate log summary (should not crash)
        try:
            summary = result.log_summary()
            # Assert: Should handle gracefully with 0.0%
            self.assertIn("0.0%", summary)
        except ZeroDivisionError as e:
            self.fail(
                f"log_summary() raised ZeroDivisionError with max_input_allowed=0: {e}"
            )

    def test_zero_budget_nonzero_tokens_no_exception(self):
        """
        [4,1,3] RED TEST: Zero budget but nonzero tokens → 0.0% (no exception).

        Edge case: max_input_allowed=0 but allocated_tokens > 0
        (shouldn't happen in practice, but must be defensive)
        """
        # Arrange: Zero budget with tokens allocated (defensive edge case)
        allocations = {
            "story_context": BudgetAllocation(
                component="story_context",
                measured_tokens=5000,
                allocated_tokens=5000,
                was_compacted=False,
                compaction_ratio=1.0,
            )
        }
        result = RequestBudgetResult(
            max_input_allowed=0,  # ← Zero budget
            allocations=allocations,
            warnings=[],
            compacted_content={},
        )

        # Act: Generate log summary (should not crash)
        try:
            summary = result.log_summary()
            # Assert: Should return 0.0% (defensive guard)
            self.assertIn("0.0%", summary)
        except ZeroDivisionError as e:
            self.fail(f"log_summary() raised ZeroDivisionError: {e}")

    def test_very_small_budget_zero_tokens(self):
        """
        [4,1,4] RED TEST: Very small budget (1 token) with zero allocated → 0.0%
        """
        # Arrange: Minimal budget
        allocations = {
            "entity_tracking": BudgetAllocation(
                component="entity_tracking",
                measured_tokens=0,
                allocated_tokens=0,
                was_compacted=False,
                compaction_ratio=1.0,
            )
        }
        result = RequestBudgetResult(
            max_input_allowed=1,  # Minimal non-zero budget
            allocations=allocations,
            warnings=[],
            compacted_content={},
        )

        # Act: Generate log summary
        summary = result.log_summary()

        # Assert: Should calculate 0.0% correctly
        self.assertIn("0.0%", summary)

    def test_very_small_budget_with_tokens(self):
        """
        [4,1,5] RED TEST: Very small budget (1 token) fully allocated → 100.0%
        """
        # Arrange: Minimal budget, fully used
        allocations = {
            "checkpoint_block": BudgetAllocation(
                component="checkpoint_block",
                measured_tokens=1,
                allocated_tokens=1,
                was_compacted=False,
                compaction_ratio=1.0,
            )
        }
        result = RequestBudgetResult(
            max_input_allowed=1,  # Minimal budget
            allocations=allocations,
            warnings=[],
            compacted_content={},
        )

        # Act: Generate log summary
        summary = result.log_summary()

        # Assert: Should calculate 100.0% correctly
        self.assertIn("100.0%", summary)

    def test_negative_budget_defensive_guard(self):
        """
        [4,2,1] RED TEST: Negative budget (error case) → 0.0% (defensive guard).

        Negative budget shouldn't happen, but defensive programming requires guard.
        """
        # Arrange: Negative budget (error scenario)
        allocations = {
            "game_state": BudgetAllocation(
                component="game_state",
                measured_tokens=50,
                allocated_tokens=50,
                was_compacted=False,
                compaction_ratio=1.0,
            )
        }
        result = RequestBudgetResult(
            max_input_allowed=-100,  # ← Invalid negative budget
            allocations=allocations,
            warnings=[],
            compacted_content={},
        )

        # Act: Generate log summary (should not crash)
        try:
            summary = result.log_summary()
            # Assert: Should handle defensively (0.0%)
            self.assertIn("0.0%", summary)
        except ZeroDivisionError as e:
            self.fail(
                f"log_summary() raised ZeroDivisionError with negative budget: {e}"
            )

    def test_matches_existing_guard_pattern(self):
        """
        Verification test: Ensure guard matches pattern from lines 256-258, 318-319.

        Existing guards use: (x / y) if y > 0 else 0.0
        New guard at line 163 should match this pattern.
        """
        # Arrange: Test zero budget scenario
        allocations = {
            "core_memories": BudgetAllocation(
                component="core_memories",
                measured_tokens=1000,
                allocated_tokens=1000,
                was_compacted=False,
                compaction_ratio=1.0,
            )
        }
        result = RequestBudgetResult(
            max_input_allowed=0,
            allocations=allocations,
            warnings=[],
            compacted_content={},
        )

        # Act: Generate log summary
        summary = result.log_summary()

        # Assert: Should use same pattern as existing guards
        # Expected pattern: (allocated_tokens / max_input_allowed * 100) if max_input_allowed > 0 else 0.0
        self.assertIn("0.0%", summary)
        self.assertNotIn("inf%", summary)  # No infinity
        self.assertNotIn("nan%", summary)  # No NaN


class TestCompactionRatioZeroGuard:
    """Test compaction_ratio calculations with zero-token components.

    Consolidated from test_compaction_ratio_zero_guard.py (BEAD REV-44t).
    """

    def test_zero_token_system_instruction_over_threshold_no_crash(self):
        """System instruction with zero tokens but >100k threshold should not crash.

        This tests the edge case where token estimation returns 0 but the check
        for SYSTEM_INSTRUCTION_EMERGENCY_THRESHOLD (100k) somehow passes.
        While unlikely in production, the division guard should prevent crashes.
        """
        # Use tiny budget to force all components over budget
        result = _allocate_request_budget(
            max_input_allowed=100,  # Very small budget
            system_instruction="",  # Empty = 0 tokens
            game_state_json='{"hp": 100}',
            core_memories="Some memories",
            entity_tracking_estimate=10,
            story_context=[{"text": "Story entry"}],
        )

        # ASSERT: No crash, compaction_ratio should be 1.0 for zero tokens
        sys_alloc = result.allocations.get("system_instruction")
        assert sys_alloc is not None
        # Even with zero tokens, should not crash
        assert sys_alloc.compaction_ratio >= 0

    def test_zero_token_game_state_no_crash(self):
        """Game state with zero tokens should not crash."""
        result = _allocate_request_budget(
            max_input_allowed=100_000,
            system_instruction="System instruction",
            game_state_json="",  # Empty = 0 tokens
            core_memories="Some memories",
            entity_tracking_estimate=1000,
            story_context=[{"text": "Story entry"}],
        )

        state_alloc = result.allocations.get("game_state")
        assert state_alloc is not None
        assert state_alloc.measured_tokens == 0
        assert state_alloc.compaction_ratio == 1.0

    def test_zero_token_core_memories_no_crash(self):
        """Core memories with zero tokens should not crash."""
        result = _allocate_request_budget(
            max_input_allowed=100_000,
            system_instruction="System instruction",
            game_state_json='{"hp": 100}',
            core_memories="",  # Empty = 0 tokens
            entity_tracking_estimate=1000,
            story_context=[{"text": "Story entry"}],
        )

        mem_alloc = result.allocations.get("core_memories")
        assert mem_alloc is not None
        assert mem_alloc.measured_tokens == 0
        assert mem_alloc.compaction_ratio == 1.0

    def test_zero_token_entity_tracking_no_crash(self):
        """Entity tracking with zero tokens should not crash."""
        result = _allocate_request_budget(
            max_input_allowed=100_000,
            system_instruction="System instruction",
            game_state_json='{"hp": 100}',
            core_memories="Some memories",
            entity_tracking_estimate=0,  # Zero estimate
            story_context=[{"text": "Story entry"}],
        )

        entity_alloc = result.allocations.get("entity_tracking")
        assert entity_alloc is not None
        assert entity_alloc.measured_tokens == 0
        assert entity_alloc.compaction_ratio == 1.0

    def test_zero_token_story_context_no_crash(self):
        """Story context with zero tokens should not crash."""
        result = _allocate_request_budget(
            max_input_allowed=100_000,
            system_instruction="System instruction",
            game_state_json='{"hp": 100}',
            core_memories="Some memories",
            entity_tracking_estimate=1000,
            story_context=[],  # Empty list = 0 tokens
        )

        story_alloc = result.allocations.get("story_context")
        assert story_alloc is not None
        assert story_alloc.measured_tokens == 0
        assert story_alloc.compaction_ratio == 1.0

    def test_all_zero_tokens_no_crash(self):
        """All components with zero tokens should not crash."""
        result = _allocate_request_budget(
            max_input_allowed=100_000,
            system_instruction="",
            game_state_json="",
            core_memories="",
            entity_tracking_estimate=0,
            story_context=[],
        )

        # All allocations should exist and have compaction_ratio = 1.0
        for component in [
            "system_instruction",
            "game_state",
            "core_memories",
            "entity_tracking",
            "story_context",
        ]:
            alloc = result.allocations.get(component)
            assert alloc is not None, f"{component} allocation missing"
            assert alloc.measured_tokens == 0, f"{component} should have 0 tokens"
            assert alloc.compaction_ratio == 1.0, (
                f"{component} compaction_ratio should be 1.0"
            )


if __name__ == "__main__":
    unittest.main()
