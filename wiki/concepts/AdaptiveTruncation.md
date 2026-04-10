---
title: "Adaptive Truncation"
type: concept
tags: [context-compaction, budget-management, llm-service]
sources: ["test-context-truncation"]
last_updated: 2026-04-08
---

## Summary
A truncation strategy introduced in PR #2311 that dynamically adjusts how conversation context is reduced based on available token budget. When budget is extremely limited, adaptive truncation employs hard-trimming to guarantee the result fits within budget.

## Behavior
1. Calculate percentage-based turn allocation (25% start / 60% end)
2. Hard-trim entries to fit within budget
3. Return truncation marker + minimal turns that fit

## Guarantees
- Result always fits within specified character budget
- At least one entry is always preserved
- Recent turns prioritized over older turns

## Related Pages
- [[TestContextTruncation]] — validates adaptive truncation behavior
- [[ContextTruncation]] — the function implementing this strategy
- [[CharacterLimit]] — the constraint being managed
