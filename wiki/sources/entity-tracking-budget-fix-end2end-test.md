---
title: "Entity Tracking Budget Fix End-to-End Test"
type: source
tags: [python, testing, e2e, context-budgeting, entity-tracking]
source_file: "raw/test_entity_tracking_budget.py"
last_updated: 2026-04-08
---

## Summary
End-to-end test validating that story continuation with large context + many NPCs does not cause ContextTooLargeError. Tests the ENTITY_TRACKING_TOKEN_RESERVE fix which budgets entity tracking tokens (~3,500+) in scaffold calculation rather than adding them after truncation.

## Key Claims
- **ENTITY_TRACKING_TOKEN_RESERVE Fix**: Entity tracking tokens now budgeted in scaffold calculation, preventing overflow when context is near limit
- **Large Context Handling**: Tests 50-turn story context with 15 NPCs without triggering ContextTooLargeError
- **Bug Reproduction**: Original bug: qwen-3-235b received 97,923 tokens when max was 94,372 — entity tracking added AFTER truncation but not budgeted

## Connections
- [[EntityTrackingBudget]] — the fix being validated
- [[Qwen3-235b]] — model that encountered the bug
