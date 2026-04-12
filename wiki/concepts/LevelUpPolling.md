---
title: "LevelUpPolling"
type: concept
tags: [level-up, polling, worldarchitect, game-state, rewards-pending]
sources: [rev-ldfd]
last_updated: 2026-04-12
---

## Summary

`LevelUpPolling` is the pattern where the frontend polls to detect when a level-up is available. The critical invariant: polling must project from the canonical `game_state.rewards_pending` field, NOT from story-entry snapshots.

## The Problem

If the polling logic reads level-up availability from story-entry snapshots (which may be stale or incomplete), it can miss genuine level-up events or display stale UI state. The canonical source is `game_state.rewards_pending.level_up_available`.

## Correct Pattern

```python
# Polling reads from canonical game_state, not story entry
rewards_pending = game_state.get("rewards_pending", {})
if rewards_pending.get("level_up_available"):
    # Show level-up modal
```

## Related

- [[LevelUpStateManagement]] — Level-up flag management
- [[RewardsBoxAtomicity]] — rewards_box and planning_block consistency
- [[LevelUpBug]] — Full bug chain context
