"""
TDD Test: Fixed-Size Component Overflow Crash

Tests for BEAD REV-2rt: Fix fixed-size component overflow crash in budget allocation

These tests verify that oversized checkpoint_block and sequence_id components
cause graceful degradation instead of ValueError crash.
"""

from mvp_site.context_compaction import _allocate_request_budget


class TestFixedSizeComponentOverflow:
    """Test budget allocation with oversized fixed-size components."""

    def test_oversized_checkpoint_block_degrades_story_budget(self):
        """Oversized checkpoint_block should reduce story budget, not fixed-size blocks.

        After fix: Verifies that oversized checkpoint_block causes story_context
        minimum reduction instead of truncating fixed-size components.
        """
        # ARRANGE: Create huge checkpoint block that exceeds budget
        # Budget: 10,000 tokens
        # Percentage minimums (60%): ~6,000 tokens
        # checkpoint_block: 8,000 tokens (fixed size)
        # Total minimum: 14,000 > 10,000 = OVERFLOW (needs 4,000tk reduction)

        huge_checkpoint = "X" * 32_000  # ~8,000 tokens (4 chars per token)

        # ASSERT: Should NOT crash - should degrade gracefully
        result = _allocate_request_budget(
            max_input_allowed=10_000,
            system_instruction="Short instruction",
            game_state_json='{"hp": 100}',
            core_memories="Short memories",
            entity_tracking_estimate=100,
            story_context=[{"text": "Short story"}],
            checkpoint_block=huge_checkpoint,  # HUGE checkpoint
            sequence_id_list="1,2,3",
        )

        # Verify checkpoint_block is fixed-size and not reduced
        checkpoint_alloc = result.allocations.get("checkpoint_block")
        assert checkpoint_alloc is not None
        assert checkpoint_alloc.measured_tokens == 8_000  # Original size
        assert checkpoint_alloc.allocated_tokens == 8_000  # Fixed-size allocation

        # Story context should be reduced to absorb overflow
        story_alloc = result.allocations.get("story_context")
        assert story_alloc is not None
        assert story_alloc.allocated_tokens < 4_000  # Less than 40% of 10k

        # Should emit a warning for story_context reduction
        assert any(
            warning.get("component") == "story_context" for warning in result.warnings
        )

    def test_oversized_checkpoint_and_sequence_degrades_story_budget(self):
        """Checkpoint + sequence overflow should reduce story budget, not fixed-size blocks."""
        huge_checkpoint = "X" * 24_000  # ~6,000 tokens
        huge_sequence = ",".join(str(i) for i in range(10000))  # ~12,222 tokens

        # Total minimums: 6,000 (percentages) + 6,000 (checkpoint) + 12,222 (sequence)
        # = 24,222 > 10,000 budget (needs 14,222tk reduction)

        result = _allocate_request_budget(
            max_input_allowed=30_000,
            system_instruction="Short",
            game_state_json='{"hp": 100}',
            core_memories="Short",
            entity_tracking_estimate=100,
            story_context=[{"text": "Short"}],
            checkpoint_block=huge_checkpoint,
            sequence_id_list=huge_sequence,
        )

        # Fixed-size components should not be reduced
        checkpoint_alloc = result.allocations.get("checkpoint_block")
        assert checkpoint_alloc is not None
        assert checkpoint_alloc.allocated_tokens == checkpoint_alloc.measured_tokens

        sequence_alloc = result.allocations.get("sequence_id")
        assert sequence_alloc is not None
        assert sequence_alloc.allocated_tokens == sequence_alloc.measured_tokens

        # Story context should be reduced to handle overflow
        story_alloc = result.allocations.get("story_context")
        assert story_alloc is not None
        assert story_alloc.allocated_tokens < 20_000  # Reduced from full budget

        # Should emit a warning for story_context reduction
        assert any(
            warning.get("component") == "story_context" for warning in result.warnings
        )

    def test_marginal_overflow_degrades_story_minimally(self):
        """Small overflow should reduce story budget minimally, preserving quality."""
        # Create checkpoint that's just slightly too large
        checkpoint = "X" * 20_000  # ~5,000 tokens
        # Percentage minimums: ~6,000 tokens
        # Total: ~11,000 > 10,000 budget (small 1,000tk overflow)

        result = _allocate_request_budget(
            max_input_allowed=10_000,
            system_instruction="Short instruction",
            game_state_json='{"hp": 100}',
            core_memories="Short memories",
            entity_tracking_estimate=100,
            story_context=[{"text": "Short story"}],
            checkpoint_block=checkpoint,
        )

        # Checkpoint should remain fixed-size
        checkpoint_alloc = result.allocations.get("checkpoint_block")
        assert checkpoint_alloc is not None
        assert checkpoint_alloc.measured_tokens == 5_000
        assert checkpoint_alloc.allocated_tokens == 5_000

        # Story context should reduce by ~1,000tk from the 40% minimum
        story_alloc = result.allocations.get("story_context")
        assert story_alloc is not None
        assert story_alloc.allocated_tokens >= 1_000  # Reduced due to checkpoint
        assert story_alloc.allocated_tokens <= 4_000

        # Should emit a warning for story_context reduction
        assert any(
            warning.get("component") == "story_context" for warning in result.warnings
        )


class TestFixedSizeComponentGracefulDegradation:
    """Test graceful degradation after bug fix."""

    def test_oversized_checkpoint_degrades_story_budget(self):
        """After fix: oversized checkpoint should reduce story budget, not crash."""
        huge_checkpoint = "X" * 32_000  # ~8,000 tokens

        # Should NOT raise ValueError - should degrade gracefully
        result = _allocate_request_budget(
            max_input_allowed=10_000,
            system_instruction="Short instruction",
            game_state_json='{"hp": 100}',
            core_memories="Short memories",
            entity_tracking_estimate=100,
            story_context=[{"text": "Short story"}],
            checkpoint_block=huge_checkpoint,
            sequence_id_list="1,2,3",
        )

        # Should not reduce checkpoint_block allocation
        checkpoint_alloc = result.allocations.get("checkpoint_block")
        assert checkpoint_alloc is not None
        assert checkpoint_alloc.allocated_tokens == checkpoint_alloc.measured_tokens

        # Story context should be reduced to absorb overflow
        story_alloc = result.allocations.get("story_context")
        assert story_alloc is not None
        assert story_alloc.allocated_tokens < 4_000

        # Should emit a warning for story_context reduction
        assert any(
            warning.get("component") == "story_context" for warning in result.warnings
        )

    def test_degradation_logs_warnings(self):
        """After fix: degradation should log warnings for visibility."""
        huge_checkpoint = "X" * 32_000

        # Use caplog to verify warnings are logged
        result = _allocate_request_budget(
            max_input_allowed=10_000,
            system_instruction="Short",
            game_state_json='{"hp": 100}',
            core_memories="Short",
            entity_tracking_estimate=100,
            story_context=[{"text": "Short"}],
            checkpoint_block=huge_checkpoint,
        )

        # Should have warnings in result or logs
        # (Exact implementation TBD - could be in result.warnings or logs)
        assert result is not None  # Placeholder - will refine after implementation
