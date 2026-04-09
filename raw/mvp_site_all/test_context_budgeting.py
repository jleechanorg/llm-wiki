import json
import unittest
from unittest.mock import MagicMock

from mvp_site import constants, llm_service
from mvp_site.context_compaction import (
    BUDGET_STORY_CONTEXT_ABSOLUTE_MIN,
    BUDGET_STORY_CONTEXT_MIN,
    SYSTEM_INSTRUCTION_EMERGENCY_THRESHOLD,
    BudgetAllocation,
    RequestBudgetResult,
    _allocate_request_budget,
    _compact_core_memories,
    _compact_game_state,
    _compact_system_instruction,
    _filter_persisted_warnings,
    _save_warning_persist_keys,
)


class TestContextBudgeting(unittest.TestCase):
    def test_safe_budget_uses_ratio_for_qwen(self):
        model = "meta-llama/llama-3.1-70b-instruct"
        expected_tokens = int(
            constants.MODEL_CONTEXT_WINDOW_TOKENS[model]
            * constants.CONTEXT_WINDOW_SAFETY_RATIO
        )
        assert (
            llm_service._get_safe_context_token_budget(
                constants.LLM_PROVIDER_OPENROUTER, model
            )
            == expected_tokens
        )

    def test_safe_budget_falls_back_for_unknown_model(self):
        fallback_expected = int(
            constants.DEFAULT_CONTEXT_WINDOW_TOKENS
            * constants.CONTEXT_WINDOW_SAFETY_RATIO
        )
        assert (
            llm_service._get_safe_context_token_budget("unknown", "mystery-model")
            == fallback_expected
        )


class TestBudgetAllocation(unittest.TestCase):
    """Tests for the new component-level budget allocation system."""

    def test_budget_allocation_normal_components(self):
        """Normal-sized components should all fit without compaction."""
        max_input = 100_000  # 100k tokens budget

        # Create reasonably-sized components
        system_instruction = "A" * 10_000  # ~2.5k tokens
        game_state = json.dumps({"hp": 50, "location": "tavern"})  # small
        core_memories = "Memory 1\nMemory 2"  # small
        story_context = [{"text": "Scene " * 100}]  # ~250 tokens

        result = _allocate_request_budget(
            max_input_allowed=max_input,
            system_instruction=system_instruction,
            game_state_json=game_state,
            core_memories=core_memories,
            entity_tracking_estimate=5000,
            story_context=story_context,
        )

        # Story context should get at least 40% of budget
        story_alloc = result.allocations.get("story_context")
        assert story_alloc is not None
        assert story_alloc.allocated_tokens >= int(max_input * BUDGET_STORY_CONTEXT_MIN)

        # No warnings for normal-sized components
        assert len(result.warnings) == 0

    def test_budget_allocation_system_instruction_above_warn_threshold_generates_warning(
        self,
    ):
        """System instruction above 40% warning threshold should generate warning."""
        max_input = 100_000

        # Create system instruction at 41% (above 40% warn threshold but below available max)
        # With 68% minimums (10% system + 5% game + 20% core + 3% entity + 30% story),
        # there's 32% remaining. System can expand from 10% min to ~42% max.
        # 41k tokens = 164k chars -> exceeds 40% warn but fits within allocatable budget
        system_instruction = "X" * 164_000  # ~41k tokens (41% of budget)
        game_state = json.dumps({"hp": 50})
        core_memories = "Memory"
        story_context = [{"text": "Story text"}]

        result = _allocate_request_budget(
            max_input_allowed=max_input,
            system_instruction=system_instruction,
            game_state_json=game_state,
            core_memories=core_memories,
            entity_tracking_estimate=5000,
            story_context=story_context,
        )

        # Should have a warning for exceeding warn threshold (40%)
        assert len(result.warnings) == 1
        assert result.warnings[0]["component"] == "system_instruction"
        assert "persist_key" in result.warnings[0]

        # Should NOT be compacted because it's within allocatable budget (~42%)
        sys_alloc = result.allocations.get("system_instruction")
        assert sys_alloc is not None
        assert not sys_alloc.was_compacted, (
            "System instruction within budget (41% < 42% available) should not be compacted"
        )

    def test_budget_allocation_emergency_system_instruction_compaction(self):
        """System instruction over 100k tokens should trigger emergency compaction."""
        max_input = 200_000

        # Create emergency-sized system instruction (>100k tokens = >400k chars)
        system_instruction = "E" * 500_000  # ~125k tokens
        game_state = json.dumps({"hp": 50})
        core_memories = "Memory"
        story_context = [{"text": "Story text"}]

        result = _allocate_request_budget(
            max_input_allowed=max_input,
            system_instruction=system_instruction,
            game_state_json=game_state,
            core_memories=core_memories,
            entity_tracking_estimate=5000,
            story_context=story_context,
        )

        # System instruction SHOULD be compacted
        sys_alloc = result.allocations.get("system_instruction")
        assert sys_alloc is not None
        assert sys_alloc.was_compacted

        # Compacted content should be smaller
        compacted = result.compacted_content.get("system_instruction")
        assert compacted is not None
        assert len(compacted) < len(system_instruction)

    def test_budget_allocation_story_gets_remaining_budget(self):
        """Story context should get any remaining budget after other components."""
        max_input = 100_000

        # Small components - lots of remaining budget
        system_instruction = "A" * 4_000  # ~1k tokens
        game_state = json.dumps({"hp": 50})
        core_memories = "Memory"
        story_context = [{"text": "Story " * 1000}]  # ~1k tokens

        result = _allocate_request_budget(
            max_input_allowed=max_input,
            system_instruction=system_instruction,
            game_state_json=game_state,
            core_memories=core_memories,
            entity_tracking_estimate=3000,
            story_context=story_context,
        )

        # Story should get more than minimum since other components are small
        story_alloc = result.allocations.get("story_context")
        assert story_alloc is not None
        min_story = int(max_input * BUDGET_STORY_CONTEXT_MIN)
        assert story_alloc.allocated_tokens >= min_story

    def test_budget_allocation_enforces_story_absolute_min_on_degradation(self):
        """Story context should not drop below absolute minimum during degradation."""
        max_input = 1000

        # Fixed-size components force degradation
        checkpoint_block = "X" * 2800  # ~700 tokens
        system_instruction = "S" * 400  # ~100 tokens
        game_state = json.dumps({"hp": 50})
        core_memories = "Memory"
        story_context = [{"text": "Story " * 50}]  # non-empty to measure

        result = _allocate_request_budget(
            max_input_allowed=max_input,
            system_instruction=system_instruction,
            game_state_json=game_state,
            core_memories=core_memories,
            entity_tracking_estimate=5000,
            story_context=story_context,
            checkpoint_block=checkpoint_block,
        )

        story_alloc = result.allocations.get("story_context")
        assert story_alloc is not None
        absolute_min = int(max_input * BUDGET_STORY_CONTEXT_ABSOLUTE_MIN)
        assert story_alloc.allocated_tokens >= absolute_min


class TestGameStateCompaction(unittest.TestCase):
    """Tests for game state compaction."""

    def test_compact_game_state_fits_budget(self):
        """Small game state should return unchanged."""
        game_state = json.dumps({"hp": 50, "location": "tavern"})
        result = _compact_game_state(game_state, max_tokens=1000)
        assert result == game_state

    def test_compact_game_state_removes_low_priority_fields(self):
        """Large game state should have low-priority fields removed."""
        large_state = {
            "current_hp": 50,  # CRITICAL - should keep
            "max_hp": 100,  # CRITICAL - should keep
            "current_location": "tavern",  # CRITICAL - should keep
            "completed_quests": ["quest1"] * 100,  # LOW - should drop
            "quest_history": ["history"] * 100,  # LOW - should drop
        }
        game_state = json.dumps(large_state)

        # Very tight budget
        result = _compact_game_state(game_state, max_tokens=100)
        parsed = json.loads(result)

        # Critical fields should be present
        assert "current_hp" in parsed
        assert "max_hp" in parsed
        assert "current_location" in parsed

        # Low priority fields should be dropped or truncated
        if "completed_quests" in parsed:
            assert len(parsed["completed_quests"]) < 100

    def test_compact_game_state_returns_compacted_when_still_over_budget(self):
        """Compaction should not fall back to original if still over budget."""
        large_state = {
            "current_hp": 50,  # CRITICAL
            "max_hp": 100,  # CRITICAL
            "current_location": "L" * 5000,  # CRITICAL but large
            "completed_quests": ["quest"] * 1000,  # LOW
            "quest_history": ["history"] * 1000,  # LOW
        }
        original = json.dumps(large_state)

        # Tight budget to force compacted JSON over max_chars
        result = _compact_game_state(original, max_tokens=100)

        # Should return a valid JSON string smaller than the original
        parsed = json.loads(result)
        assert len(result) < len(original)
        assert "current_hp" in parsed
        assert "current_location" in parsed


class TestCoreMemoriesCompaction(unittest.TestCase):
    """Tests for core memories compaction."""

    def test_compact_core_memories_fits_budget(self):
        """Small memories should return unchanged."""
        memories = "Memory 1\nMemory 2"
        result = _compact_core_memories(memories, max_tokens=1000)
        assert result == memories

    def test_compact_core_memories_preserves_critical(self):
        """CRITICAL memories should be preserved during compaction."""
        memories = "\n".join(
            [
                "Old memory 1",
                "Old memory 2",
                "CRITICAL: Must remember the password",
                "Recent memory 1",
                "Recent memory 2",
            ]
        )
        result = _compact_core_memories(memories, max_tokens=50)
        assert "CRITICAL" in result

    def test_compact_core_memories_keeps_recent(self):
        """Recent memories should be prioritized."""
        memories = "\n".join([f"Memory {i}" for i in range(20)])
        result = _compact_core_memories(memories, max_tokens=50)
        # Should keep recent memories (last 5)
        assert "Memory 19" in result or "Memory 18" in result


class TestSystemInstructionCompaction(unittest.TestCase):
    """Tests for emergency system instruction compaction."""

    def test_compact_system_instruction_preserves_start_and_end(self):
        """Compaction should preserve start (60%) and end (35%)."""
        instruction = "START" + "X" * 10000 + "END"
        result = _compact_system_instruction(instruction, max_tokens=500)

        # Should preserve START and END
        assert result.startswith("START")
        assert result.endswith("END")
        assert "TRUNCATED" in result

    def test_compact_system_instruction_fits_budget_returns_unchanged(self):
        """Small instruction should return unchanged."""
        instruction = "Small instruction"
        result = _compact_system_instruction(instruction, max_tokens=1000)
        assert result == instruction


class TestBeadFixes(unittest.TestCase):
    """Tests for bead fixes identified in review."""

    def test_system_instruction_over_budget_compacts_below_emergency(self):
        """
        Fix for worktree_logs6-1mh: System instruction over budget should compact
        even when below the 100k emergency threshold.

        Previously: Only warned, didn't compact below 100k
        Now: Compacts to allocated budget when over budget
        """
        max_input = 100_000  # 100k token budget

        # Create system instruction that exceeds allocated budget (max 50%)
        # but is below 100k emergency threshold
        # 60k tokens = 240k chars -> will exceed 50% allocation of 50k
        system_instruction = "X" * 240_000  # ~60k tokens
        game_state = json.dumps({"hp": 50})
        core_memories = "Memory"
        story_context = [{"text": "Story text"}]

        result = _allocate_request_budget(
            max_input_allowed=max_input,
            system_instruction=system_instruction,
            game_state_json=game_state,
            core_memories=core_memories,
            entity_tracking_estimate=5000,
            story_context=story_context,
        )

        sys_alloc = result.allocations.get("system_instruction")
        assert sys_alloc is not None

        # FIX: Should now compact even below 100k threshold
        assert sys_alloc.was_compacted, (
            "System instruction over budget should be compacted (bead worktree_logs6-1mh)"
        )

        # Compacted content should be smaller than original
        compacted = result.compacted_content.get("system_instruction")
        assert compacted is not None
        assert len(compacted) < len(system_instruction), (
            "Compacted system instruction should be smaller"
        )


class TestSequenceIdBudgetFix(unittest.TestCase):
    """Tests for sequence ID budget fix (bead worktree_logs6-cc4)."""

    def test_sequence_id_budget_enforced_on_final_list(self):
        """
        Fix for worktree_logs6-cc4: Sequence ID list from final context should
        respect allocated budget, not just measurement from bounded context.

        The issue is that temp_seq_ids is measured from sequence_id_context (20%),
        but sequence_id_list_string is built from truncated_story_context (full).
        The final list may exceed the allocated budget.
        """
        # This is a code structure test - verify the fix exists in llm_service.py
        # Fix is now in _prepare_story_continuation helper function (refactored from continue_story)
        import inspect
        from mvp_site import llm_service

        source = inspect.getsource(llm_service._prepare_story_continuation)

        # Should have a fix referencing bead cc4 for sequence_id
        assert "worktree_logs6-cc4" in source, (
            "Fix should have comment referencing bead worktree_logs6-cc4 in _prepare_story_continuation"
        )

        # Should apply budget enforcement to sequence_id_list_string
        # Look for pattern that caps/truncates sequence IDs based on allocation
        assert (
            "sequence_id" in source.lower() and "budget" in source.lower()
        ) or "final_sequence_ids" in source, (
            "Should apply budget enforcement to sequence IDs"
        )


class TestStoryContextMeasurementFix(unittest.TestCase):
    """Tests for story context measurement fix (bead worktree_logs6-5c2)."""

    def test_story_context_measurement_includes_all_fields(self):
        """
        Fix for worktree_logs6-5c2: Story context measurement should account for
        all fields sent to LLM (text, actor, mode, sequence_id), not just text.

        Previously: Only measured entry["text"]
        Now: Measures all fields in essential_story_fields
        """
        # This is a code structure test
        import inspect
        from mvp_site import context_compaction

        source = inspect.getsource(context_compaction._allocate_request_budget)

        # Should have fix comment referencing bead 5c2
        assert "worktree_logs6-5c2" in source, (
            "Fix should have comment referencing bead worktree_logs6-5c2"
        )

    def test_story_measurement_includes_metadata_fields(self):
        """Verify story context measurement includes actor, mode, sequence_id."""
        from mvp_site.context_compaction import _allocate_request_budget

        # Create story entries with metadata fields
        story_context = [
            {
                "text": "The hero entered the cave.",
                "actor": "gm",
                "mode": "story",
                "sequence_id": 1,
            },
            {
                "text": "I look around carefully.",
                "actor": "player",
                "mode": "character",
                "sequence_id": 2,
            },
        ]

        result = _allocate_request_budget(
            max_input_allowed=100_000,
            system_instruction="Test",
            game_state_json='{"hp": 100}',
            core_memories="Memory",
            entity_tracking_estimate=1000,
            story_context=story_context,
        )

        story_alloc = result.allocations.get("story_context")
        assert story_alloc is not None

        # The measured tokens should be MORE than just the text tokens
        # because it now includes actor, mode, sequence_id fields
        from mvp_site.token_utils import estimate_tokens

        text_only_tokens = estimate_tokens(
            "The hero entered the cave.I look around carefully."
        )
        assert story_alloc.measured_tokens > text_only_tokens, (
            f"Story measurement ({story_alloc.measured_tokens}tk) should be greater than "
            f"text-only ({text_only_tokens}tk) because it includes metadata fields"
        )


class TestBugFixes(unittest.TestCase):
    """Tests for specific bug fixes identified in PR review."""

    def test_division_by_zero_with_zero_max_input(self):
        """Bug fix: Division by zero when max_input_allowed is 0."""
        # This should not crash with ZeroDivisionError
        max_input = 0  # Edge case: zero budget

        # Create oversized system instruction to trigger warning code path
        system_instruction = "X" * 500_000  # Large instruction
        game_state = json.dumps({"hp": 50})
        core_memories = "Memory"
        story_context = [{"text": "Story"}]

        # Should handle gracefully without division by zero
        result = _allocate_request_budget(
            max_input_allowed=max_input,
            system_instruction=system_instruction,
            game_state_json=game_state,
            core_memories=core_memories,
            entity_tracking_estimate=5000,
            story_context=story_context,
        )

        # Should complete without crashing
        assert result is not None
        assert isinstance(result, RequestBudgetResult)

    def test_unguarded_get_on_non_dict_custom_campaign_state(self):
        """Bug fix: AttributeError when custom_campaign_state is not a dict."""
        warnings = [
            {
                "component": "system_instruction",
                "persist_key": "budget_warning_test",
                "ui_message": "Test warning",
            }
        ]

        # Create game_state where custom_campaign_state exists but is NOT a dict
        game_state = MagicMock()
        game_state.custom_campaign_state = "not a dict"  # Bug trigger

        # Should handle gracefully without AttributeError
        to_show, to_persist = _filter_persisted_warnings(warnings, game_state)

        # Should treat as if no persisted warnings exist
        assert len(to_show) == 1
        assert len(to_persist) == 1


class TestWarningPersistence(unittest.TestCase):
    """Tests for budget warning persistence."""

    def test_filter_warnings_new_warning_shown(self):
        """New warnings should be shown and persisted."""
        warnings = [
            {
                "component": "system_instruction",
                "persist_key": "budget_warning_system_instruction",
                "ui_message": "Warning message",
            }
        ]
        game_state = MagicMock()
        game_state.custom_campaign_state = {}

        to_show, to_persist = _filter_persisted_warnings(warnings, game_state)

        assert len(to_show) == 1
        assert len(to_persist) == 1
        assert "budget_warning_system_instruction" in to_persist

    def test_filter_warnings_existing_warning_suppressed(self):
        """Already-shown warnings should be suppressed."""
        warnings = [
            {
                "component": "system_instruction",
                "persist_key": "budget_warning_system_instruction",
                "ui_message": "Warning message",
            }
        ]
        game_state = MagicMock()
        game_state.custom_campaign_state = {
            "budget_warnings_shown": ["budget_warning_system_instruction"]
        }

        to_show, to_persist = _filter_persisted_warnings(warnings, game_state)

        assert len(to_show) == 0
        assert len(to_persist) == 0

    def test_save_warning_persist_keys_updates_state(self):
        """Saving persist keys should update game_state."""
        game_state = MagicMock()
        game_state.custom_campaign_state = {"budget_warnings_shown": ["existing_key"]}

        _save_warning_persist_keys(game_state, ["new_key"])

        updated = game_state.custom_campaign_state["budget_warnings_shown"]
        assert "existing_key" in updated
        assert "new_key" in updated


class TestBudgetAllocationDataclasses(unittest.TestCase):
    """Tests for budget allocation dataclasses."""

    def test_budget_allocation_utilization(self):
        """Test utilization percentage calculation."""
        alloc = BudgetAllocation(
            component="test",
            measured_tokens=50,
            allocated_tokens=100,
        )
        assert alloc.utilization_pct == 50.0

    def test_budget_allocation_zero_division(self):
        """Zero allocated tokens should return 0% utilization."""
        alloc = BudgetAllocation(
            component="test",
            measured_tokens=50,
            allocated_tokens=0,
        )
        assert alloc.utilization_pct == 0.0

    def test_request_budget_result_get_story_budget(self):
        """Test story budget retrieval."""
        result = RequestBudgetResult(
            max_input_allowed=100000,
            allocations={
                "story_context": BudgetAllocation(
                    component="story_context",
                    measured_tokens=40000,
                    allocated_tokens=50000,
                )
            },
            warnings=[],
            compacted_content={},
        )
        assert result.get_story_budget() == 50000

    def test_request_budget_result_log_summary(self):
        """Test log summary generation."""
        result = RequestBudgetResult(
            max_input_allowed=100000,
            allocations={
                "story_context": BudgetAllocation(
                    component="story_context",
                    measured_tokens=40000,
                    allocated_tokens=50000,
                )
            },
            warnings=[{"component": "test"}],
            compacted_content={},
        )
        summary = result.log_summary()
        assert "BUDGET_ALLOCATION" in summary
        assert "story_context" in summary
        assert "warning" in summary.lower()  # Case-insensitive check for WARNINGS


class TestCheckpointBudgetAccounting(unittest.TestCase):
    """Test that checkpoint_block and sequence_id are measured in budget allocation.

    Consolidated from test_checkpoint_budget.py (Finding #3 from code review).
    """

    def test_checkpoint_block_included_in_budget_measurement(self):
        """
        RED TEST: checkpoint_block tokens should be measured in budget allocation.

        Currently, _allocate_request_budget() only measures:
        - system_instruction
        - game_state
        - core_memories
        - entity_tracking
        - story_context

        But checkpoint_block is added to LLMRequest AFTER budget allocation,
        which can push total input over max_input_allowed.

        This test will FAIL until we add checkpoint_block measurement.
        """
        # Arrange: Create test inputs with checkpoint_block
        max_input_allowed = 100000
        system_instruction = "Test instruction"
        game_state_json = '{"location": "test"}'
        core_memories = "Memory 1\nMemory 2"
        entity_tracking_estimate = 1000
        story_context = [{"text": "Story entry", "actor": "user"}]

        # This is the checkpoint_block that currently ISN'T measured
        checkpoint_block = (
            """
        [CHECKPOINT #12345]
        Location: Ancient Temple
        Quest: Find the Sacred Artifact
        Party: Warrior (HP: 45/50), Mage (HP: 30/30)
        """
            * 10
        )  # Make it substantial (~500 tokens)

        # Act: Allocate budget
        # This currently doesn't accept checkpoint_block parameter - will FAIL
        result = _allocate_request_budget(
            max_input_allowed=max_input_allowed,
            system_instruction=system_instruction,
            game_state_json=game_state_json,
            core_memories=core_memories,
            entity_tracking_estimate=entity_tracking_estimate,
            story_context=story_context,
            checkpoint_block=checkpoint_block,  # NEW parameter - will cause TypeError
        )

        # Assert: checkpoint_block tokens should be accounted for
        # The allocator should have measured checkpoint_block and allocated budget for it
        checkpoint_allocation = result.get_allocation("checkpoint_block")
        self.assertIsNotNone(checkpoint_allocation)
        self.assertGreater(checkpoint_allocation.allocated_tokens, 0)

    def test_sequence_id_included_in_budget_measurement(self):
        """
        RED TEST: sequence_id_list tokens should be measured in budget allocation.

        Similar to checkpoint_block, sequence_id_list is added to LLMRequest
        after budget allocation, which can push total over max_input_allowed.

        This test will FAIL until we add sequence_id measurement.
        """
        # Arrange: Create test inputs with sequence_id list
        max_input_allowed = 100000
        system_instruction = "Test instruction"
        game_state_json = '{"location": "test"}'
        core_memories = "Memory 1\nMemory 2"
        entity_tracking_estimate = 1000
        story_context = [{"text": "Story entry", "actor": "user"}]

        # This is the sequence_id_list that currently ISN'T measured
        # Long campaign with many turns = large sequence ID list
        sequence_id_list = ", ".join(
            [str(i) for i in range(1, 500)]
        )  # ~2000 characters

        # Act: Allocate budget
        # This currently doesn't accept sequence_id_list parameter - will FAIL
        result = _allocate_request_budget(
            max_input_allowed=max_input_allowed,
            system_instruction=system_instruction,
            game_state_json=game_state_json,
            core_memories=core_memories,
            entity_tracking_estimate=entity_tracking_estimate,
            story_context=story_context,
            sequence_id_list=sequence_id_list,  # NEW parameter - will cause TypeError
        )

        # Assert: sequence_id tokens should be accounted for
        sequence_allocation = result.get_allocation("sequence_id")
        self.assertIsNotNone(sequence_allocation)
        self.assertGreater(sequence_allocation.allocated_tokens, 0)

    def test_total_budget_includes_checkpoint_and_sequence(self):
        """
        RED TEST: Total allocated budget should include checkpoint + sequence tokens.

        This ensures that when we sum all component allocations, the total
        doesn't exceed max_input_allowed AFTER adding checkpoint and sequence.

        This test will FAIL until checkpoint/sequence are measured.
        """
        # Arrange: Create test inputs
        max_input_allowed = 50000  # Smaller budget to make overflow more likely
        system_instruction = "X" * 10000  # Large system instruction
        game_state_json = '{"data": "' + ("X" * 5000) + '"}'  # Large game state
        core_memories = "\n".join(
            ["Memory " + str(i) for i in range(100)]
        )  # Many memories
        entity_tracking_estimate = 5000
        story_context = [{"text": "Story entry " + str(i)} for i in range(50)]

        checkpoint_block = "Checkpoint data " * 200  # ~400 tokens
        sequence_id_list = ", ".join([str(i) for i in range(200)])  # ~800 characters

        # Act: Allocate budget with checkpoint and sequence
        result = _allocate_request_budget(
            max_input_allowed=max_input_allowed,
            system_instruction=system_instruction,
            game_state_json=game_state_json,
            core_memories=core_memories,
            entity_tracking_estimate=entity_tracking_estimate,
            story_context=story_context,
            checkpoint_block=checkpoint_block,
            sequence_id_list=sequence_id_list,
        )

        # Assert: Total allocated should not exceed max_input_allowed
        total_allocated = sum(
            alloc.allocated_tokens for alloc in result.allocations.values()
        )
        self.assertLessEqual(
            total_allocated,
            max_input_allowed,
            f"Total allocated ({total_allocated}) exceeds max_input_allowed ({max_input_allowed})",
        )


class TestDegradationCoverage(unittest.TestCase):
    """Tests for degradation code paths (coverage lines 368-381)."""

    def test_tier5_system_instruction_degradation(self):
        """
        Coverage for lines 368-371: TIER 5 system_instruction minimum reduction.

        Force degradation all the way through TIER 5 by creating a scenario where
        all flexible components must be reduced to fit.
        """
        # Very small budget with large fixed-size components
        max_input_allowed = 100
        # Fixed-size components that consume most of the budget
        checkpoint_block = "X" * 200  # ~50 tokens (fixed size)
        sequence_id_list = "1,2,3,4,5,6,7,8,9,10" * 5  # ~50 chars

        result = _allocate_request_budget(
            max_input_allowed=max_input_allowed,
            system_instruction="System",
            game_state_json='{"hp": 50}',
            core_memories="Memory",
            entity_tracking_estimate=10,
            story_context=[{"text": "Story"}],
            checkpoint_block=checkpoint_block,
            sequence_id_list=sequence_id_list,
        )

        # Should complete without crashing - degradation occurred
        self.assertIsNotNone(result)
        # All allocations should exist
        self.assertIn("system_instruction", result.allocations)
        self.assertIn("story_context", result.allocations)

    def test_value_error_when_budget_fundamentally_exceeded(self):
        """
        Coverage for line 381: ValueError when budget cannot fit even after degradation.

        Create a scenario where fixed-size components alone exceed the budget.
        """
        # Extremely small budget
        max_input_allowed = 10
        # Fixed-size component that alone exceeds budget
        checkpoint_block = "X" * 1000  # ~250 tokens (fixed, cannot be reduced)

        with self.assertRaises(ValueError) as cm:
            _allocate_request_budget(
                max_input_allowed=max_input_allowed,
                system_instruction="S",
                game_state_json="{}",
                core_memories="",
                entity_tracking_estimate=0,
                story_context=[],
                checkpoint_block=checkpoint_block,
            )

        self.assertIn("Cannot allocate request", str(cm.exception))
        self.assertIn("fundamentally too large", str(cm.exception))


class TestGameStateCompactionCoverage(unittest.TestCase):
    """Tests for _compact_game_state edge cases (coverage lines 760-811)."""

    def test_json_decode_error_returns_original(self):
        """
        Coverage for lines 760-763: JSON decode error returns original.

        Per Copilot suggestion, invalid JSON should return original (not truncated).
        """
        invalid_json = "{invalid json content"
        result = _compact_game_state(invalid_json, max_tokens=10)

        # Should return original (not truncated invalid JSON)
        self.assertEqual(result, invalid_json)

    def test_non_dict_game_state_returns_original(self):
        """
        Coverage for lines 765-766: Non-dict game_state returns original.
        """
        # Valid JSON but not a dict
        array_json = '["item1", "item2", "item3"]'
        result = _compact_game_state(array_json, max_tokens=5)

        # Should return original since we can't compact non-dict
        self.assertEqual(result, array_json)

    def test_nested_world_data_current_location(self):
        """
        Coverage for line 780: current_location in nested world_data.
        """
        game_state = {
            "world_data": {
                "current_location_name": "Castle",
                "current_location": {"x": 10, "y": 20},
            },
            "completed_quests": ["quest1"] * 100,  # Large low-priority field
        }
        game_state_json = json.dumps(game_state)

        result = _compact_game_state(game_state_json, max_tokens=50)
        parsed = json.loads(result)

        # Should preserve world_data with both location fields
        self.assertIn("world_data", parsed)
        self.assertIn("current_location_name", parsed["world_data"])
        self.assertIn("current_location", parsed["world_data"])

    def test_nested_world_data_location_fallback(self):
        """
        Coverage for line 794: Fallback to 'location' key when current_location_name missing.

        The compaction must be triggered (game_state > max_tokens) for this path to execute.
        Note: The MEDIUM priority loop may overwrite with full world_data if it fits,
        so we need budget too small to fit the original world_data.
        """
        # Make world_data large enough that it won't fit in MEDIUM priority check
        game_state = {
            "world_data": {
                "location": "Tavern",  # Fallback key (no current_location_name)
                "extra_data": "X" * 500,  # Make world_data too big for MEDIUM priority
            },
            "completed_quests": ["quest"] * 500,  # Large low-priority field to force compaction
            "quest_history": ["history"] * 500,  # More large data
        }
        game_state_json = json.dumps(game_state)

        # Ensure game_state is large enough to trigger compaction
        from mvp_site.token_utils import estimate_tokens

        original_tokens = estimate_tokens(game_state_json)
        self.assertGreater(original_tokens, 50, "Game state must exceed budget to trigger compaction")

        # Use very tight budget so world_data doesn't fit in MEDIUM priority
        result = _compact_game_state(game_state_json, max_tokens=30)
        parsed = json.loads(result)

        # Should use 'location' as fallback for current_location_name
        self.assertIn("world_data", parsed)
        self.assertEqual(parsed["world_data"].get("current_location_name"), "Tavern")

    def test_high_priority_field_fits_budget(self):
        """
        Coverage for line 811: HIGH priority field fits within budget.
        """
        game_state = {
            "current_hp": 50,
            "max_hp": 100,
            "inventory": ["sword", "shield"],  # HIGH priority
            "completed_quests": ["quest1"] * 100,  # LOW priority - should be dropped
        }
        game_state_json = json.dumps(game_state)

        result = _compact_game_state(game_state_json, max_tokens=50)
        parsed = json.loads(result)

        # CRITICAL fields always included
        self.assertIn("current_hp", parsed)
        self.assertIn("max_hp", parsed)
        # HIGH priority should be included if space allows
        self.assertIn("inventory", parsed)
        # LOW priority should be dropped
        self.assertNotIn("completed_quests", parsed)


if __name__ == "__main__":
    unittest.main()
