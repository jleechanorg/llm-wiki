"""
Story Context Tests - Consolidated

Consolidated tests for story_context handling in context_compaction.py:
1. Type safety guards against malformed Firestore data (Bug worktree_logs6-txx)
2. Warning logic - only emit warnings when reduction > 0

Test Matrix Coverage: [2,1,1] through [2,2,3] (8 type safety tests + 2 warning logic tests)
"""

import unittest
from unittest.mock import patch

from mvp_site.context_compaction import _allocate_request_budget


class TestStoryContextTypeSafety(unittest.TestCase):
    """Test defensive guards against non-dict story_context entries."""

    def setUp(self):
        """Common test setup."""
        self.max_input_allowed = 100000
        self.system_instruction = "Test instruction"
        self.game_state_json = '{"location": "test"}'
        self.core_memories = "Memory 1\nMemory 2"
        self.entity_tracking_estimate = 1000

    def test_all_valid_dicts_processes_normally(self):
        """
        [2,1,1] RED TEST: All valid dicts should process without errors.

        Baseline test - ensures normal operation isn't broken by guards.
        """
        # Arrange: Valid story_context with all dicts
        story_context = [
            {"text": "Turn 1: User attacks"},
            {"text": "Turn 2: Enemy retaliates"},
            {"text": "Turn 3: User dodges"},
        ]

        # Act: Allocate budget
        result = _allocate_request_budget(
            max_input_allowed=self.max_input_allowed,
            system_instruction=self.system_instruction,
            game_state_json=self.game_state_json,
            core_memories=self.core_memories,
            entity_tracking_estimate=self.entity_tracking_estimate,
            story_context=story_context,
        )

        # Assert: Should process successfully
        self.assertIsNotNone(result)
        self.assertIn("story_context", result.allocations)
        self.assertGreater(result.allocations["story_context"].measured_tokens, 0)

    def test_mixed_valid_invalid_skips_invalid_entries(self):
        """
        [2,1,2] RED TEST: Mixed valid/invalid should skip invalid, process valid.

        Currently FAILS with AttributeError on "string".get("text", "")
        """
        # Arrange: Mixed valid dicts and invalid non-dicts
        story_context = [
            {"text": "Turn 1: Valid entry"},
            "Invalid string entry",  # ← This should be skipped
            {"text": "Turn 2: Another valid entry"},
            123,  # ← This should also be skipped
            {"text": "Turn 3: Final valid entry"},
        ]

        # Act: Allocate budget (should not crash)
        result = _allocate_request_budget(
            max_input_allowed=self.max_input_allowed,
            system_instruction=self.system_instruction,
            game_state_json=self.game_state_json,
            core_memories=self.core_memories,
            entity_tracking_estimate=self.entity_tracking_estimate,
            story_context=story_context,
        )

        # Assert: Should process successfully, skipping invalid entries
        self.assertIsNotNone(result)
        self.assertIn("story_context", result.allocations)
        # Should have processed 3 valid entries (3 turns of text)
        self.assertGreater(result.allocations["story_context"].measured_tokens, 0)

    def test_all_invalid_entries_returns_empty_story_text(self):
        """
        [2,1,3] RED TEST: All invalid entries should return empty story_text.

        Currently FAILS with AttributeError on first invalid entry.
        """
        # Arrange: All invalid non-dict entries
        story_context = [
            "Invalid string 1",
            123,
            None,
            ["list", "entry"],
        ]

        # Act: Allocate budget (should not crash)
        result = _allocate_request_budget(
            max_input_allowed=self.max_input_allowed,
            system_instruction=self.system_instruction,
            game_state_json=self.game_state_json,
            core_memories=self.core_memories,
            entity_tracking_estimate=self.entity_tracking_estimate,
            story_context=story_context,
        )

        # Assert: Should process successfully with zero story tokens
        self.assertIsNotNone(result)
        self.assertIn("story_context", result.allocations)
        # No valid text entries = 0 measured tokens
        self.assertEqual(result.allocations["story_context"].measured_tokens, 0)

    def test_empty_story_context_list(self):
        """
        [2,1,4] RED TEST: Empty list should return empty string without errors.
        """
        # Arrange: Empty story_context
        story_context = []

        # Act: Allocate budget
        result = _allocate_request_budget(
            max_input_allowed=self.max_input_allowed,
            system_instruction=self.system_instruction,
            game_state_json=self.game_state_json,
            core_memories=self.core_memories,
            entity_tracking_estimate=self.entity_tracking_estimate,
            story_context=story_context,
        )

        # Assert: Should process successfully
        self.assertIsNotNone(result)
        self.assertEqual(result.allocations["story_context"].measured_tokens, 0)

    def test_none_values_in_list_skipped(self):
        """
        [2,1,5] RED TEST: None values should be skipped, not cause errors.

        Currently FAILS with AttributeError on None.get("text", "")
        """
        # Arrange: List with None values
        story_context = [
            None,
            {"text": "Valid entry"},
            None,
            {"text": "Another valid entry"},
        ]

        # Act: Allocate budget (should not crash)
        result = _allocate_request_budget(
            max_input_allowed=self.max_input_allowed,
            system_instruction=self.system_instruction,
            game_state_json=self.game_state_json,
            core_memories=self.core_memories,
            entity_tracking_estimate=self.entity_tracking_estimate,
            story_context=story_context,
        )

        # Assert: Should process 2 valid entries
        self.assertIsNotNone(result)
        self.assertGreater(result.allocations["story_context"].measured_tokens, 0)

    def test_missing_text_field_uses_empty_string(self):
        """
        [2,2,1] RED TEST: Dicts without "text" field should use empty string.

        Valid dict structure but missing the "text" key we're looking for.
        """
        # Arrange: Valid dicts but missing "text" field
        story_context = [
            {"actor": "user"},  # ← No "text" field
            {"text": "Valid entry with text"},
            {"actor": "gemini", "turn": 2},  # ← No "text" field
        ]

        # Act: Allocate budget
        result = _allocate_request_budget(
            max_input_allowed=self.max_input_allowed,
            system_instruction=self.system_instruction,
            game_state_json=self.game_state_json,
            core_memories=self.core_memories,
            entity_tracking_estimate=self.entity_tracking_estimate,
            story_context=story_context,
        )

        # Assert: Should process without errors (empty strings for missing text)
        self.assertIsNotNone(result)
        # Should have some tokens from the one valid text entry
        self.assertGreater(result.allocations["story_context"].measured_tokens, 0)

    def test_unicode_text_processes_normally(self):
        """
        [2,2,2] RED TEST: Unicode characters in text should process normally.
        """
        # Arrange: Story context with Unicode
        story_context = [
            {"text": "龍騎士が村を救う"},
            {"text": "Рыцарь сражается с драконом"},
            {"text": "🐉⚔️🏰"},  # Emoji
        ]

        # Act: Allocate budget
        result = _allocate_request_budget(
            max_input_allowed=self.max_input_allowed,
            system_instruction=self.system_instruction,
            game_state_json=self.game_state_json,
            core_memories=self.core_memories,
            entity_tracking_estimate=self.entity_tracking_estimate,
            story_context=story_context,
        )

        # Assert: Should process Unicode successfully
        self.assertIsNotNone(result)
        self.assertGreater(result.allocations["story_context"].measured_tokens, 0)

    def test_very_long_text_processes_normally(self):
        """
        [2,2,3] RED TEST: Very long text entries should process without errors.

        Tests large but valid data doesn't break the guard logic.
        """
        # Arrange: Very long story context
        long_text = "This is a very long story entry. " * 10000  # ~350k chars
        story_context = [
            {"text": long_text},
        ]

        # Act: Allocate budget
        result = _allocate_request_budget(
            max_input_allowed=self.max_input_allowed,
            system_instruction=self.system_instruction,
            game_state_json=self.game_state_json,
            core_memories=self.core_memories,
            entity_tracking_estimate=self.entity_tracking_estimate,
            story_context=story_context,
        )

        # Assert: Should process successfully
        self.assertIsNotNone(result)
        # Very long text should have substantial token count
        self.assertGreater(result.allocations["story_context"].measured_tokens, 50000)


class TestStoryContextWarningLogic(unittest.TestCase):
    """Test that story context warnings are only emitted when reduction occurs.

    Consolidated from test_story_context_warning_logic.py.

    Bug: Lines 298-321 in mvp_site/context_compaction.py were outside the
    `if story_reduction > 0:` block, causing misleading warnings when story_reduction == 0.
    """

    def test_no_warning_when_story_reduction_is_zero(self):
        """
        RED TEST: No warning should be generated when story_reduction == 0.

        When overage > 0 but available_reduction == 0 (already at minimum),
        story_reduction will be 0, and no warning should be emitted.

        Bug: The warning code is outside the `if story_reduction > 0:` block,
        causing misleading "Reduced by 0tk" messages.
        """
        # Setup: story_context already at absolute minimum (20%)
        max_input_allowed = 10000
        measurements = {
            "system_instruction": 3000,  # Large system instruction
            "game_state": 2000,
            "core_memories": 2000,
            "entity_tracking": 1000,
            "story_context": 2000,  # Already at 20% absolute minimum
        }

        # Total = 10000, but story_context already at minimum,
        # so further reduction requires emergency degradation

        # Mock logging to capture error messages
        with patch("mvp_site.context_compaction.logging_util") as mock_logging:
            result = _allocate_request_budget(
                max_input_allowed=max_input_allowed,
                system_instruction="x" * 12000,  # 3000 tokens (chars/4)
                game_state_json="x" * 8000,  # 2000 tokens
                core_memories="x" * 8000,  # 2000 tokens
                entity_tracking_estimate=1000,  # 1000 tokens
                story_context=[{"text": "x" * 400} for _ in range(20)],  # ~2000 tokens
            )

            # Check if story_context warning was emitted with 0 reduction
            # Filter for error logs about story_context reduction
            error_calls = [
                str(call)
                for call in mock_logging.error.call_args_list
                if "story_context" in str(call).lower()
            ]

            # ASSERTION: If story_reduction was 0, no error log should mention reduction
            for call_str in error_calls:
                if (
                    "reduced by 0tk" in call_str.lower()
                    or "reduced by 0 " in call_str.lower()
                ):
                    self.fail(
                        f"Should not log 'reduced by 0' error when story_reduction == 0: {call_str}"
                    )

            # ASSERTION: No warning should be added for story_context with 0 reduction
            story_warnings = [
                w
                for w in result.warnings
                if w.get("component") == "story_context"
                and "reduced by 0" in w.get("message", "").lower()
            ]
            self.assertEqual(
                len(story_warnings),
                0,
                f"Should not add 'reduced by 0' warning when story_reduction == 0, but got: {story_warnings}",
            )

    def test_warning_emitted_when_story_reduction_occurs(self):
        """
        Verify warning IS emitted when story_reduction > 0.
        """
        max_input_allowed = 10000
        # Create scenario where story_context EXCEEDS its allocation
        # Story gets 40% min = 4000, but if it measures >4000 it will be compacted
        # To ensure story exceeds allocation, make story very large (8000 tokens)
        # and limit other components so they consume budget
        measurements = {
            "system_instruction": 2000,  # Will get allocated up to max
            "game_state": 1500,
            "core_memories": 1000,
            "entity_tracking": 500,
            "story_context": 8000,  # 80% - will exceed allocated budget
        }
        # Total = 13000 (3000 over budget)
        # After fill-to-max phase, story_context will exceed its final allocation

        with patch("mvp_site.context_compaction.logging_util") as mock_logging:
            result = _allocate_request_budget(
                max_input_allowed=max_input_allowed,
                system_instruction="x" * 8000,  # 2000 tokens
                game_state_json="x" * 6000,  # 1500 tokens
                core_memories="x" * 4000,  # 1000 tokens
                entity_tracking_estimate=500,  # 500 tokens
                story_context=[{"text": "x" * 1600} for _ in range(20)],  # ~8000 tokens
            )

            # ASSERTION: Error log should be emitted about story reduction
            error_calls = [
                str(call)
                for call in mock_logging.error.call_args_list
                if "story_context" in str(call).lower()
                and "reduced" in str(call).lower()
            ]
            self.assertGreater(
                len(error_calls), 0, "Should log error when story_reduction > 0"
            )

            # ASSERTION: Should NOT have "reduced by 0" in the logs
            for call_str in error_calls:
                self.assertNotIn(
                    "reduced by 0",
                    call_str.lower(),
                    f"Should not log 'reduced by 0': {call_str}",
                )

            # ASSERTION: Warning should be added with non-zero reduction
            story_warnings = [
                w for w in result.warnings if w.get("component") == "story_context"
            ]
            if story_warnings:
                # If warning exists, should mention reduction
                self.assertIn("reduced", story_warnings[0]["message"].lower())


if __name__ == "__main__":
    unittest.main()
