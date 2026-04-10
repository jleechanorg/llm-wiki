---
title: "TokenBudgetAllocation"
type: concept
tags: [context-management, tokens, allocation]
sources: ["context-budgeting-allocation-tdd-tests"]
last_updated: 2026-04-08
---

## Description
System for distributing available token budget across context components with guaranteed minimums:
- System instruction: 10% minimum
- Game state: 5% minimum
- Core memories: 20% minimum
- Entity tracking: 3% minimum
- Story context: 30% minimum

## Key Behavior
- Normal-sized components receive allocated budget without compaction
- Components exceeding 40% of budget generate warnings
- Components exceeding 100k tokens trigger emergency compaction
- Story context receives remaining budget after minimums are satisfied
