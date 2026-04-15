---
title: "Six Regression Fixes"
type: concept
tags: [regression, fixes, worldai]
last_updated: 2026-04-14
---

## Summary

Six Regression Fixes documents the six targeted bug fixes applied to resolve specific regressions introduced during a major refactor. Each fix addresses a distinct failure mode.

## The Six Fixes

### CR #1: Level Up Choice Projection
**Problem**: Modal was not appearing on level-up because projection flag wasn't set.
**Fix**: Set `has_level_up_ui_signal = true` in the rewards box when level-up detected.

### CR #2: Stale Suppression Path
**Problem**: Stale level-up flags suppressing new level-ups.
**Fix**: Clear stale flags before computing new level-up state.

### CR #3: Rewards Box Normalization
**Problem**: Rewards values exceeding MAX_REWARDS causing Firestore write failures.
**Fix**: All rewards boxes pass through `normalize_rewards_box_for_ui()` before persistence.

### CR #4: Streaming Passthrough
**Problem**: Passthrough path returning raw LLM output without normalization.
**Fix**: Passthrough now calls normalization before returning.

### CR #5: Postcondition Enforcement
**Problem**: Rewards box postcondition not checked after updates.
**Fix**: `_enforce_primary_rewards_box_postcondition` returns the validated rewards box.

### CR #6: Test Coverage Gap
**Problem**: No test coverage for stale flag suppression.
**Fix**: Added `test_level_up_stale_flags.py` with specific stale-suppression cases.

## Connections
- [[PRRegressionResolution]] — General regression resolution
- [[LevelUpBug]] — Level-up specific bugs
- [[LevelUpRegressionFix]] — Regression fix documentation
