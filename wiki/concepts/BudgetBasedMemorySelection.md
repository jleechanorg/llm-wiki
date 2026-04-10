---
title: "Budget-Based Memory Selection"
type: concept
tags: [memory, budget, selection, token-management]
sources: ["memory-utils-tests"]
last_updated: 2026-04-08
---

Algorithm for selecting which memories to include when token budget is exceeded.

## Behavior
1. Always includes most recent N memories (MIN_RECENT_MEMORIES)
2. When over budget, drops oldest memories first (LRU eviction)
3. Preserves original order of selected memories

## Token Estimation
~40 characters ≈ 10 tokens for estimation purposes.

## Constraints
- `max_tokens` — maximum tokens allowed for memories
- `min_recent` — minimum recent memories to always preserve

## Connected To
- [[MemoryUtils]] — implements select_memories_by_budget()
- [[Memory Budget Alignment]] — ensures budget selection respects BUDGET_CORE_MEMORIES_MIN/MAX bounds
