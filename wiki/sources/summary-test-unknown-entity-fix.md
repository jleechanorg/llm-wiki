---
title: "Summary test demonstrating the Unknown entity fix"
type: source
tags: [testing, entity-validation, tdd, mvp-site]
source_file: "raw/unknown_entity_filtering_test.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests demonstrating the Unknown entity filtering fix in EntityValidator. Shows the problem (Unknown treated as missing entity causing unnecessary retries), the fix (filtering Unknown from validation), and the result (no unnecessary retries for placeholder values).

## Key Claims
- **Problem**: When location defaults to 'Unknown', it gets added to expected entities and triggers false validation failures
- **Fix**: Entity validator filters out 'Unknown' placeholder before validation
- **Result**: No unnecessary retry triggered for placeholder entities
- **Real Entities Still Validated**: Real missing entities like 'Villain' are still properly detected

## Test Coverage
- `test_complete_fix_demonstration`: Shows Unknown filtered from missing entities
- `test_real_entities_still_validated`: Ensures real entities like 'Villain' are still validated

## Key Quotes
> "The problem: Unknown was treated as a missing entity" — Original bug behavior
> "The fix: Filter Unknown from validation" — Solution implemented
> "Entity validation no longer triggers unnecessary retries for 'Unknown'" — Fixed behavior
