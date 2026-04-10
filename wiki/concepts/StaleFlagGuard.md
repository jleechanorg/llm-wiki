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
