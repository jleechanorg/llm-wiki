---
title: "TDD: Test duplicate critical memories in _compact_core_memories()"
type: source
tags: [python, testing, tdd, context-compaction, memory, deduplication, bug-fix]
source_file: "raw/test_compact_core_memories_dedup.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD test suite for a bug in the `_compact_core_memories()` function in `mvp_site/context_compaction.py`. The tests verify that critical memories are not duplicated when they appear in both the critical memories list and the last 3 entries of the fallback path.

## Key Claims
- **Bug Location**: Line 802 in `context_compaction.py` uses `critical_memories + memory_lines[-3:]` which can create duplicates
- **Duplicate Scenario**: When a critical memory is ALREADY in the last 3 entries, it would appear twice in the compacted output
- **Expected Fix**: Deduplicate the combined result to ensure each critical memory appears exactly once

## Key Test Cases
- `test_no_duplicate_critical_memories_in_fallback`: RED test verifying no duplication when critical memory in last 3
- `test_critical_memories_preserved`: Verifies critical memories preserved when not in last 3
- `test_no_duplication_with_multiple_criticals_in_recent`: Verifies no duplication with multiple criticals

## Connections
- [[ContextCompaction]] — the module containing the buggy function
- [[TestDrivenDevelopment]] — the methodology used for this test-first approach
- [[MemoryDeduplication]] — the specific pattern/concept being tested
