---
title: "Token Budget Selection"
type: concept
tags: [tokens, budget, memory, context-window]
sources: [memory-utilities-core-memories]
last_updated: 2026-04-08
---

## Definition
Token budget selection is a memory management strategy that ensures memories fit within the LLM's input token limit (typically 240k tokens) to prevent context overflow.

## Implementation
The `select_memories_by_budget()` function:
1. Always includes the most recent N memories (MIN_RECENT_MEMORIES = 10) for continuity
2. Adds older memories from newest to oldest until token budget exhausted
3. Uses ceiling division: `(chars + CHARS_PER_TOKEN - 1) // CHARS_PER_TOKEN` to avoid undercounting

## Usage
```python
from mvp_site.memory_utils import select_memories_by_budget

selected = select_memories_by_budget(
    all_memories,
    max_tokens=50000,  # Optional, defaults to MAX_CORE_MEMORY_TOKENS
    min_recent=10      # Optional, defaults to MIN_RECENT_MEMORIES
)
```

## Related
- [[Deduplication]] - removes duplicate memories before budgeting
- [[ContextCompaction]] - provides BUDGET_CORE_MEMORIES_MAX constant
