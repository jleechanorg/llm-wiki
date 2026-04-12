---
title: "FrontendRewardsBoxGate"
type: concept
tags: [frontend, rewards-box, xp, level-up, visibility]
sources: [rev-qcax]
last_updated: 2026-04-12
---

## Summary

`FrontendRewardsBoxGate` is the frontend logic at `app.js:924` that hides the `rewards_box` when `xp_gained=0`. This gate can block level-up display even when `level_up_available=true` and `xp_gained=0`.

## The Bug

```javascript
// app.js line ~924
if (xp_gained === 0) {
    rewards_box.style.display = 'none';  // Hides box even when level_up_available=true
}
```

## Problem Scenario

1. Player earns 0 XP on a narrative turn
2. But `rewards_pending.level_up_available=true` (level-up IS available)
3. Frontend gate `xp_gained === 0` hides the rewards_box entirely
4. Player never sees the level-up prompt

## Correct Pattern

The gate should check `level_up_available` OR `xp_gained > 0`, not just `xp_gained > 0`.

## Related

- [[LevelUpModalRouting]] — Modal routing for level-up
- [[LevelUpStateManagement]] — Level-up state management
- [[RewardsBoxAtomicity]] — Rewards box atomicity invariants
