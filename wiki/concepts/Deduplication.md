---
title: "Deduplication"
type: concept
tags: [memory, duplicates, similarity, dedup]
sources: [memory-utilities-core-memories]
last_updated: 2026-04-08
---

## Definition
Deduplication is the process of removing near-duplicate memories from the LLM's context to avoid redundancy and maximize information density.

## Implementation
Uses fuzzy matching with SequenceMatcher:
1. **Exact match first**: Quick check `new_entry == existing`
2. **Fuzzy similarity**: `SequenceMatcher(None, a.lower(), b.lower()).ratio()`
3. **Threshold**: 0.85 (85% similarity) — catches near-duplicates while allowing meaningfully different content

## Performance Optimization
Only checks the most recent 20 memories (DEDUPE_WINDOW_SIZE) rather than all memories:
- Duplicates are most likely to occur in recent context
- Full O(n²) check is expensive for large memory sets
- Window-based deduping is O(n) for each new entry

## Usage
```python
from mvp_site.memory_utils import is_duplicate_memory

if is_duplicate_memory(new_memory, existing_memories, threshold=0.85, window_size=20):
    skip  # Memory already exists
```

## Related
- [[TokenBudgetSelection]] - often runs after deduplication
- [[MemoryManagement]] - broader concept this is part of
