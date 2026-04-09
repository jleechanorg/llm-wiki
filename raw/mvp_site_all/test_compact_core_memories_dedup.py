"""
TDD: Test duplicate critical memories in _compact_core_memories()

RED PHASE: This test should FAIL before the fix is applied.
The test verifies that critical memories are not duplicated when they
appear in the last 3 entries.

Bug: Line 802 uses `critical_memories + memory_lines[-3:]` which can
create duplicates if a critical memory is in the last 3 entries.
"""

import os
import sys
import unittest

# Add parent directory to path
sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from mvp_site.context_compaction import _compact_core_memories


class TestCompactCoreMemoriesDedup(unittest.TestCase):
    """Test deduplication logic in core memories compaction."""

    def test_no_duplicate_critical_memories_in_fallback(self):
        """
        RED TEST: Critical memory in last 3 entries should not be duplicated.

        When compaction uses the fallback `critical_memories + memory_lines[-3:]`,
        a critical memory that's ALREADY in the last 3 entries would appear twice.
        """
        # Create core memories where "Recent Y" is CRITICAL and in last 3
        core_memories = """CRITICAL: Old X
Normal1
Normal2
Normal3
Normal4
CRITICAL: Recent Y
Recent Z1
Recent Z2
"""

        # Trigger fallback compaction (small budget to force line 802 fallback)
        max_tokens = 15  # Triggers fallback at line 802

        result = _compact_core_memories(core_memories, max_tokens)

        # Count occurrences - "CRITICAL: Recent Y" is in last 3 AND in critical_memories
        occurrences_Y = result.count("CRITICAL: Recent Y")

        # ASSERTION: Should appear exactly once, not twice
        self.assertEqual(
            occurrences_Y,
            1,
            f"CRITICAL: Recent Y should appear exactly 1 time, found {occurrences_Y} times.\n"
            f"Result:\n{result}",
        )

    def test_critical_memories_preserved(self):
        """
        Verify critical memories are preserved even when not in last 3.
        """
        core_memories = """Memory 1: CRITICAL: The artifact is the Crown of Stars
Memory 2: Normal memory
Memory 3: Normal memory
Memory 4: Normal memory
Memory 5: Recent A
Memory 6: Recent B
Memory 7: Recent C
"""

        # Compact with budget that allows critical + recent
        max_tokens = 50

        result = _compact_core_memories(core_memories, max_tokens)

        # ASSERTION: Critical memory should be present
        self.assertIn("CRITICAL: The artifact is the Crown of Stars", result)

        # ASSERTION: Recent memories should be present
        self.assertIn("Recent C", result)

    def test_no_duplication_with_multiple_criticals_in_recent(self):
        """
        Verify no duplication when multiple critical memories are in recent entries.
        """
        core_memories = """Normal
CRITICAL: X
CRITICAL: Y
CRITICAL: Z
"""

        # Force fallback compaction (larger budget to include all)
        max_tokens = 20

        result = _compact_core_memories(core_memories, max_tokens)

        # Count each critical memory - should appear exactly once
        self.assertEqual(result.count("CRITICAL: X"), 1)
        self.assertEqual(result.count("CRITICAL: Y"), 1)
        self.assertEqual(result.count("CRITICAL: Z"), 1)


if __name__ == "__main__":
    unittest.main()
