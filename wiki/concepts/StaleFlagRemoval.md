---
title: "Stale Flag Removal"
type: concept
tags: [state-management, bug-fix]
sources: ["modal-state-lifecycle-tests", "level-up-stale-flag-clearing-tests"]
last_updated: 2026-04-08
---

## Summary
Bug fix pattern where stale level_up_in_progress=False should be REMOVED from state rather than preserved. Prevents stale flags from blocking future level-ups.

## Key Claims
- **BUG (9c9f93d4a)**: level_up_in_progress=False from previous level-up blocks new level-ups
- **Fix**: Remove the flag key entirely, don't preserve as False
- **Defense pattern**: Apply to all modal state flags
- **Test validation**: Modal lifecycle tests verify removal not preservation

## Connections
- [[Flag Clearing]] — broader clearing mechanism
- [[LevelUpAgent]] — affected by stale flags
- [[State Transitions]] — transitions must handle stale flags
- [[Level-up stale flag clearing]] — related bug fix tests
