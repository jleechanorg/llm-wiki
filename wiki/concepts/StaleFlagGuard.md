---
title: "StaleFlagGuard"
type: concept
tags: [state-management, guards, anti-pattern, stale-state]
sources: ["rev-0g1y-level-up-active-state-inconsistency"]
last_updated: 2026-04-08
---

## Definition
A defensive programming pattern where explicit `false` values in game state flags are treated as intentional stale guards, preventing leftover values from triggering incorrect behavior.

## Application in Level-Up
- `level_up_in_progress: false` — explicitly cleared, should prevent modal injection
- `level_up_pending: false` — explicitly cleared, should prevent finish choice injection
- `rewards_pending.level_up_available: true` — leftover stale value should be ignored when guards are false

## Why It Matters
Without stale flag guards, old state values (e.g., from previous sessions) can incorrectly trigger behaviors. The guard ensures that explicit `false` takes precedence over stale `true` values.

## Related
- [[LevelUpActiveStateLogic]] — uses stale flag guards
- [[ModalStateManagement]] — related state clearing patterns


## 2026-06-13 — Positive Evidence Rule (PR #7516)

Suppression predicates must use **positive evidence** of advancement, not field absence.
- ✅ `rewards_box_level > player_level` — model wrote a higher level into rewards_box
- ❌ `not rewards_box` — absent field means "not written yet", not "already advanced"

Absent `rewards_box` is valid for the hybrid CC+LevelUp modal (no rewards_box until processed).
See [[feedback-2026-06-13-suppress-requires-positive-evidence]].
