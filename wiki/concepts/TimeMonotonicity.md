---
title: "TimeMonotonicity"
type: concept
tags: [game-state, time, monotonicity, validation, temporal-regression]
sources: [mvp-site-game-state]
last_updated: 2026-04-14
---

## Summary

The principle that game time in WorldAI campaigns always moves forward — never backward. TimeMonotonicity enforcement prevents temporal regressions where campaign time, round counters, or turn sequences could be altered to re-execute already-resolved events. Implemented via `validate_xp_level(strict=False)` which auto-corrects `stored_level > expected_level` derived from XP thresholds.

## Key Claims

### Auto-Correction Pattern
- `validate_xp_level(strict=False)` corrects stored_level when it exceeds expected_level from XP
- Validator **always wins** over canonicalizer in the same persistence path (see [[LevelUpBug]] chain)
- `_canonicalize_level_from_xp_in_place` runs first, then `validate_and_correct_state` in same path

### XP → Level Mapping (D&D 5e Official)
| Level | XP Threshold |
|-------|-------------|
| 1→2 | 300 |
| 2→3 | 900 |
| 3→4 | 2,700 |

### Temporal Regression Prevention
- Any mechanism that could reduce campaign time, undo turn resolution, or re-execute decided events must be blocked
- Schema migration preserves temporal integrity for legacy campaigns

## Connections

- [[LevelUpMechanics]] — level progression with monotonic XP thresholds
- [[mvp-site-game-state]] — game state management with time validation
- [[LevelUpBug]] — canonicalizer self-undo pattern affecting monotonicity
- [[SchemaMigration]] — legacy campaign temporal integrity preservation