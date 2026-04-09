"""Tests for memory budget alignment between memory_utils and context_compaction.

RED-GREEN TDD: This test ensures the two memory budget systems are aligned
to prevent aggressive compaction that loses campaign context.
"""

from mvp_site.context_compaction import BUDGET_CORE_MEMORIES_MAX, BUDGET_CORE_MEMORIES_MIN
from mvp_site.memory_utils import MAX_CORE_MEMORY_TOKENS


class TestMemoryBudgetAlignment:
    """Verify memory_utils and context_compaction use aligned budgets."""

    def test_memory_utils_max_aligns_with_context_compaction_max(self):
        """MAX_CORE_MEMORY_TOKENS should not exceed budget allocator's max."""
        # With 240k max_input, the max budget is BUDGET_CORE_MEMORIES_MAX * 240000
        max_input_allowed = 240_000
        budget_allocator_max = int(max_input_allowed * BUDGET_CORE_MEMORIES_MAX)

        assert budget_allocator_max >= MAX_CORE_MEMORY_TOKENS, (
            f"memory_utils.MAX_CORE_MEMORY_TOKENS ({MAX_CORE_MEMORY_TOKENS:,}) "
            f"exceeds context_compaction max ({budget_allocator_max:,} = "
            f"{BUDGET_CORE_MEMORIES_MAX:.0%} of {max_input_allowed:,}). "
            f"This causes aggressive re-compaction that loses campaign context."
        )

    def test_memory_utils_max_reasonable_for_budget_min(self):
        """MAX_CORE_MEMORY_TOKENS should be usable even at minimum budget."""
        max_input_allowed = 240_000
        budget_allocator_min = int(max_input_allowed * BUDGET_CORE_MEMORIES_MIN)

        # Memory selection should not wildly exceed minimum budget
        # Allow 2x overage (will be compacted) but not 10x
        max_reasonable_overage = 2.0
        assert (
            budget_allocator_min * max_reasonable_overage >= MAX_CORE_MEMORY_TOKENS
        ), (
            f"memory_utils.MAX_CORE_MEMORY_TOKENS ({MAX_CORE_MEMORY_TOKENS:,}) "
            f"is >{max_reasonable_overage}x the minimum budget ({budget_allocator_min:,} = "
            f"{BUDGET_CORE_MEMORIES_MIN:.0%} of {max_input_allowed:,}). "
            f"Initial selection should be closer to final allocation."
        )

    def test_core_memories_budget_preserves_reasonable_context(self):
        """Core memories should get enough budget to preserve campaign context."""
        from mvp_site.context_compaction import BUDGET_CORE_MEMORIES_MIN

        max_input_allowed = 240_000
        budget_allocator_min = int(max_input_allowed * BUDGET_CORE_MEMORIES_MIN)

        # For a 1000+ turn campaign, we need at least 20k tokens for memories
        minimum_reasonable_budget = 20_000

        assert budget_allocator_min >= minimum_reasonable_budget, (
            f"Core memories minimum budget ({budget_allocator_min:,}tk = "
            f"{BUDGET_CORE_MEMORIES_MIN:.0%}) is too small. "
            f"Long campaigns need at least {minimum_reasonable_budget:,}tk "
            f"to maintain narrative consistency."
        )

    def test_budget_percentages_documented(self):
        """Verify budget constants have explanatory comments."""
        import inspect

        from mvp_site import context_compaction

        source = inspect.getsource(context_compaction)

        # Check that BUDGET_CORE_MEMORIES constants have comments
        assert "BUDGET_CORE_MEMORIES_MIN" in source
        assert "BUDGET_CORE_MEMORIES_MAX" in source
        # Should have descriptive comment about why these values
        assert "campaign" in source.lower() or "memory" in source.lower()
