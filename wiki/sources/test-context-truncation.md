---
title: "Context Truncation Behavior Tests"
type: source
tags: [python, testing, context-compaction, truncation, llm-service]
source_file: "raw/test_context_truncation.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating the context truncation behavior in `llm_service._truncate_context()`. Tests verify that when context is under the character limit, no truncation occurs, and when over the limit with few turns, adaptive truncation with hard-trimming is applied to fit the budget. NEW BEHAVIOR (PR #2311): With extremely low token budgets, adaptive truncation aggressively reduces turns and hard-trims content to guarantee budget fit.

## Key Claims
- **No Truncation Under Limit**: Context under max_chars remains unchanged
- **Adaptive Truncation**: Very low budgets trigger aggressive hard-trimming
- **Turn Prioritization**: Recent turns (60% of budget) prioritized over older turns (25%)
- **Budget Guarantee**: Result always fits within specified character budget

## Key Quotes
> "With a very low token budget (120 chars ≈ 30 tokens), adaptive truncation aggressively reduces turns and hard-trims text to fit." — PR #2311

## Connections
- [[PR2311]] — introduces the adaptive truncation behavior
- [[GameState]] — mock game state used for context construction
- [[ContextTruncation]] — the function being tested

## Contradictions
- None identified
