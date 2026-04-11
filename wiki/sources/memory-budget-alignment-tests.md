---
title: "Memory Budget Alignment Tests"
type: source
tags: [python, testing, memory, tdd, budget]
source_file: "raw/test_memory_budget_alignment.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD test suite validating alignment between memory_utils and context_compaction memory budget systems. Tests ensure the two budget allocation mechanisms don't cause aggressive compaction that loses campaign context. Uses RED-GREEN methodology where tests define expected behavior before implementation.

## Key Claims
- **MAX_CORE_MEMORY_TOKENS alignment**: memory_utils constant should not exceed budget allocator's maximum to prevent aggressive re-compaction
- **Minimum budget usability**: MAX_CORE_MEMORY_TOKENS should remain usable even at minimum budget allocation (BUDGET_CORE_MEMORIES_MIN)
- **Campaign context preservation**: Core memories minimum budget must preserve at least 20k tokens for long-running campaigns (1000+ turns)
- **Constant documentation**: BUDGET_CORE_MEMORIES constants should have explanatory comments about campaign/memory rationale

## Key Quotes
> "memory_utils.MAX_CORE_MEMORY_TOKENS (X) exceeds context_compaction max (Y). This causes aggressive re-compaction that loses campaign context."

## Connections
- [[MemoryUtils]] — provides MAX_CORE_MEMORY_TOKENS constant
- [[ContextCompaction]] — provides BUDGET_CORE_MEMORIES_MIN/MAX percentages
- [[MemoryBudgetAlignment]] — concept for aligning two budget systems

## Contradictions
- None detected — this test validates alignment, not conflicting behavior
