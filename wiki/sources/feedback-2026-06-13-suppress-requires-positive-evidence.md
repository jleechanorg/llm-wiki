# Suppression Requires Positive Evidence (2026-06-13)

**Type**: feedback | **Classification**: Critical
**Bead**: rev-jw8e4 | **PR**: [#7516](https://github.com/jleechanorg/worldarchitect.ai/pull/7516)

## Summary

Stale-flag suppression in `_compute_stale_level_up_suppression` (rewards_engine.py) must require
positive evidence of advancement (`rewards_box_level > player_level`), not absence of data
(`or (not rewards_box)`). Absence means "not written yet", not "already advanced".

## Failure Pattern

`or (not rewards_box)` fired on the hybrid CC+LevelUp modal where `rewards_box=None` is valid
(level-up not yet processed). This caused `is_level_up_active()` to return `False`, which
broke `test_character_creation_finish_clears_hybrid_level_up_approval_flags` when
`ENABLE_SEMANTIC_ROUTING=false` (CI env).

## Fix

Removed `or (not rewards_box)` from `rewards_box_already_advanced` computation.
Commit: `e652898218` on `fix/rev-toavb-orphaned-ccs-flag-repro`.

## Rule

When writing suppression predicates: require positive evidence, never absence-as-evidence.
