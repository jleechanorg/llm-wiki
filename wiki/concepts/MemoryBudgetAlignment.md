---
title: "Memory Budget Alignment"
type: concept
tags: [memory, budget, alignment, context-compaction]
sources: ["memory-budget-alignment-tests"]
last_updated: 2026-04-08
---

## Definition

The practice of ensuring memory_utils and context_compaction use compatible budget constants to prevent aggressive memory compaction that loses campaign context.

## Key Parameters

| Constant | Source | Purpose |
|----------|--------|---------|
| MAX_CORE_MEMORY_TOKENS | memory_utils | Maximum tokens allocated for core memories |
| BUDGET_CORE_MEMORIES_MIN | context_compaction | Minimum % of input budget for core memories |
| BUDGET_CORE_MEMORIES_MAX | context_compaction | Maximum % of input budget for core memories |

## Alignment Rules

1. MAX_CORE_MEMORY_TOKENS <= BUDGET_CORE_MEMORIES_MAX * max_input_tokens
2. MAX_CORE_MEMORY_TOKENS <= 2x * (BUDGET_CORE_MEMORIES_MIN * max_input_tokens)
3. BUDGET_CORE_MEMORIES_MIN * max_input_tokens >= 20,000 tokens for long campaigns

## Related Concepts

- [[ContextCompaction]] — the mechanism that enforces budget constraints
- [[CoreMemories]] — the content being budgeted
- [[REDGreenTDD]] — development methodology used in these tests
