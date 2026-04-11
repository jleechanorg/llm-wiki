---
title: "TDD Test: Fixed-Size Component Overflow Crash"
type: source
tags: [python, testing, tdd, budget-allocation, overflow-handling, bug-fix]
source_file: "raw/test_fixed_size_overflow_crash.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD tests validating BEAD REV-2rt fix: ensures oversized checkpoint_block and sequence_id components cause graceful degradation instead of ValueError crash in budget allocation. Tests verify that story_context gets reduced to absorb overflow rather than truncating fixed-size components.

## Key Claims
- **Oversized checkpoint_block reduces story budget, not fixed-size**: When checkpoint_block exceeds budget, story_context minimum is reduced instead of crashing
- **Combined checkpoint + sequence overflow handled gracefully**: Both components can be oversized without crashing
- **Marginal overflow reduces story minimally**: Small overflows result in minimal story_context reduction to preserve quality
- **Fixed-size components preserved**: checkpoint_block and sequence_id allocations remain at measured size
- **Warning emission**: System emits warnings when story_context is reduced

## Test Cases Covered
- test_oversized_checkpoint_block_degrades_story_budget
- test_oversized_checkpoint_and_sequence_degrades_story_budget
- test_marginal_overflow_degrades_story_minimally

## Connections
- [[BudgetAllocation]] — the system being tested
- [[GracefulDegradation]] — the fix pattern applied
- [[ContextCompaction]] — the module containing _allocate_request_budget

## Contradictions
- None identified
