"""
RED TEST: JSON truncation handling in _compact_game_state (Bug worktree_logs6-v7q)

Test Matrix Coverage: [3,1,1] through [3,2,4] (8 tests)

This test verifies that _compact_game_state never returns invalid JSON.
When compaction would exceed budget, it should return original game_state.

Current FAILURE: Lines 579-581 truncate JSON string, producing invalid JSON.
"""

import json
import unittest

from mvp_site.context_compaction import _compact_game_state


class TestJSONTruncationHandling(unittest.TestCase):
    """Test that JSON compaction never returns invalid JSON."""

    def test_fits_budget_returns_compacted_json(self):
        """
        [3,1,1] RED TEST: Compacted JSON fits budget → return compacted.

        Baseline test - normal case should work correctly.
        """
        # Arrange: Small game_state that fits budget
        game_state = {
            "location": "village",
            "time": "morning",
            "party": {"hp": 50, "max_hp": 50},
        }
        game_state_json = json.dumps(game_state)
        max_chars = 1000  # Plenty of budget

        # Act: Compact game_state
        result = _compact_game_state(game_state_json, max_chars)

        # Assert: Should return valid JSON
        self.assertIsInstance(result, str)
        parsed = json.loads(result)  # Must not raise JSONDecodeError
        self.assertIsInstance(parsed, dict)

    def test_exactly_at_budget_returns_compacted_json(self):
        """
        [3,1,2] RED TEST: Compacted JSON exactly at budget → return compacted.
        """
        # Arrange: Game state that compacts to exactly max_chars
        game_state = {"location": "test"}
        game_state_json = json.dumps(game_state)
        # Set max_chars to exact size of compacted JSON
        max_chars = len(json.dumps(game_state, separators=(",", ":")))

        # Act: Compact game_state
        result = _compact_game_state(game_state_json, max_chars)

        # Assert: Should return valid JSON
        parsed = json.loads(result)
        self.assertIsInstance(parsed, dict)

    def test_slightly_over_budget_returns_original(self):
        """
        [3,1,3] RED TEST: Compacted JSON slightly over budget → return original.

        Currently FAILS because code truncates, producing invalid JSON like:
        {"location":"village","time":"morn
        """
        # Arrange: Game state that exceeds budget after compaction
        game_state = {
            "location": "A very long location name that will push us over budget",
            "time": "morning",
            "weather": "sunny",
            "party": {"name": "Heroes", "hp": 50},
        }
        game_state_json = json.dumps(game_state)
        # Set budget too small for compacted version
        max_chars = 50  # Will exceed after compaction

        # Act: Compact game_state
        result = _compact_game_state(game_state_json, max_chars)

        # Assert: Should return original (valid JSON), not truncated invalid JSON
        parsed = json.loads(result)  # Must not raise JSONDecodeError
        self.assertIsInstance(parsed, dict)
        # Should have original data (not truncated)
        self.assertIn("location", parsed)

    def test_way_over_budget_returns_original_with_warning(self):
        """
        [3,1,4] RED TEST: Way over budget → return original + log warning.

        Currently FAILS by truncating and producing invalid JSON.
        """
        # Arrange: Massive game_state way over budget using actual priority fields
        game_state = {
            "current_location": "X" * 10000,  # CRITICAL but huge
            "combat_participants": [
                {"name": f"NPC_{i}", "hp": 50} for i in range(100)
            ],  # CRITICAL
            "inventory": [f"item_{i}" for i in range(500)],  # HIGH priority
        }
        game_state_json = json.dumps(game_state)
        max_chars = 1000  # Way too small

        # Act: Compact game_state
        result = _compact_game_state(game_state_json, max_chars)

        # Assert: Should return original (valid JSON)
        parsed = json.loads(result)  # Must not raise JSONDecodeError
        self.assertIsInstance(parsed, dict)
        # Should have original massive data
        self.assertIn("combat_participants", parsed)
        self.assertEqual(len(parsed["combat_participants"]), 100)

    def test_truncation_would_break_json_returns_original(self):
        """
        [3,2,1] RED TEST: Truncation mid-object → return original (safe fallback).

        This is the CRITICAL bug - line 581 truncates:
        compacted_json = compacted_json[:max_chars]

        If max_chars cuts off mid-object, result is invalid JSON.
        """
        # Arrange: Game state where truncation would break JSON structure
        game_state = {
            "location": "village",
            "nested": {
                "deep": {"structure": "This will be cut off mid-object by truncation"}
            },
        }
        game_state_json = json.dumps(game_state)
        # Set max_chars to cut off mid-nested-object
        max_chars = 60  # Will cut off inside nested structure

        # Act: Compact game_state
        result = _compact_game_state(game_state_json, max_chars)

        # Assert: Must return valid JSON (original, not truncated)
        try:
            parsed = json.loads(result)
            self.assertIsInstance(parsed, dict)
        except json.JSONDecodeError as e:
            self.fail(
                f"_compact_game_state returned invalid JSON: {e}\n"
                f"Result was: {result[:200]}..."
            )

    def test_empty_game_state_returns_empty_json(self):
        """
        [3,2,2] RED TEST: Empty game_state → return "{}"
        """
        # Arrange: Empty game_state
        game_state_json = "{}"
        max_chars = 1000

        # Act: Compact game_state
        result = _compact_game_state(game_state_json, max_chars)

        # Assert: Should return valid empty JSON
        self.assertEqual(result, "{}")
        parsed = json.loads(result)
        self.assertEqual(parsed, {})

    def test_minimal_critical_fields_preserved(self):
        """
        [3,2,3] RED TEST: Minimal critical fields compacted successfully.
        """
        # Arrange: Game state with CRITICAL and non-critical fields
        game_state = {
            "current_location": "village",  # CRITICAL
            "current_hp": 50,  # CRITICAL
            "max_hp": 50,  # CRITICAL
            "armor_class": 15,  # CRITICAL
            "quest_history": "Long quest description "
            * 100,  # LOW priority - droppable
        }
        game_state_json = json.dumps(game_state)
        max_chars = 200  # Tight budget

        # Act: Compact game_state
        result = _compact_game_state(game_state_json, max_chars)

        # Assert: Should return valid JSON with critical fields
        parsed = json.loads(result)
        # Critical fields should be preserved
        self.assertIn("current_location", parsed)
        self.assertIn("current_hp", parsed)
        self.assertIn("max_hp", parsed)

    def test_nested_critical_fields_preserved(self):
        """
        [3,2,5] RED TEST: Nested critical fields should be preserved during compaction.

        Ensures world_data.current_location_name, combat_state, and player_character_data
        remain in compacted output even when trimming large payloads.
        """
        # Arrange: Nested critical fields + large low-priority payload
        game_state = {
            "world_data": {
                "current_location_name": "Dockside",
                "extra_lore": "X" * 8000,
            },
            "combat_state": {"in_combat": True, "initiative_order": [1, 2, 3]},
            "player_character_data": {"name": "Aria", "hp": 12},
            "quest_history": "Long quest log " * 2000,
        }
        game_state_json = json.dumps(game_state)
        max_tokens = 50  # Force compaction

        # Act: Compact game_state
        result = _compact_game_state(game_state_json, max_tokens)

        # Assert: Nested critical fields should still exist
        parsed = json.loads(result)
        self.assertIn("world_data", parsed)
        self.assertEqual(parsed["world_data"].get("current_location_name"), "Dockside")
        self.assertIn("combat_state", parsed)
        self.assertTrue(parsed["combat_state"].get("in_combat"))
        self.assertIn("player_character_data", parsed)
        self.assertEqual(parsed["player_character_data"].get("name"), "Aria")

    def test_all_fields_critical_returns_original(self):
        """
        [3,2,4] RED TEST: All fields critical, can't compact → return original.

        When all fields are CRITICAL and total exceeds budget, compaction is
        impossible. Should return original valid JSON, not truncated garbage.
        """
        # Arrange: All CRITICAL fields exceeding budget using actual priority fields
        game_state = {
            "current_location": "X" * 5000,  # CRITICAL but huge
            "current_hp": 50,  # CRITICAL
            "max_hp": 50,  # CRITICAL
            "combat_participants": [{"name": "Y" * 5000}],  # CRITICAL but huge
        }
        game_state_json = json.dumps(game_state)
        max_chars = 1000  # Can't fit even critical fields

        # Act: Compact game_state
        result = _compact_game_state(game_state_json, max_chars)

        # Assert: Should return original (valid JSON)
        parsed = json.loads(result)
        self.assertIsInstance(parsed, dict)
        # Should have original massive critical data
        self.assertIn("current_location", parsed)
        self.assertIn("combat_participants", parsed)
        self.assertTrue(len(parsed["current_location"]) > 4000)


if __name__ == "__main__":
    unittest.main()
