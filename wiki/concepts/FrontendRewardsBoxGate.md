---
title: "FrontendRewardsBoxGate"
type: concept
tags: [frontend, rewards-box, xp, level-up, visibility, worldarchitect-ai, bug-chain]
sources: [rev-qcax, pr-6192, pr-6261, level-up-bugs-and-streaming-unification-2026-04-14]
last_updated: 2026-04-14
---

## Summary

`FrontendRewardsBoxGate` is the frontend logic at `app.js:924` that hides the `rewards_box` when `xp_gained=0`. This gate blocks level-up display even when `level_up_available=true`. **Bug confirmed live 2026-04-14** despite bead `jleechan-o34j` being closed as "done" on 2026-04-12.

## The Bug

```javascript
// raw/mvp_site_all/app.js line 924 — BUGGY
if (fullData.rewards_box && fullData.rewards_box.xp_gained > 0) {
```

The outer gate at line 924 prevents the entire rewards box from rendering — including the `level_up_available` check at line 959 that would show "LEVEL UP AVAILABLE!". The fix:

```javascript
// CORRECT
if (fullData.rewards_box && (fullData.rewards_box.xp_gained > 0 || fullData.rewards_box.level_up_available)) {
```

## Why PR #6192 Didn't Fix It

PR #6192 claims the fix was applied in #6161 (commit `a872098d7c`) and added regression tests. The `raw/mvp_site_all/app.js` snapshot still has the buggy gate. Two possibilities:
1. The fix was deployed then regressed
2. The snapshot predates the fix

## PR #6261 (Backend, OPEN)

PR #6261 adds `_extract_reward_value()` helper for robust XP/gold parsing from messy LLM payloads ("500 XP", booleans, NaN, fallback keys). **Does NOT fix frontend gate** — separate fix needed.

## Problem Scenario

1. Player earns 0 XP on a narrative turn
2. But `rewards_pending.level_up_available=true` (level-up IS available)
3. Frontend gate `xp_gained === 0` hides the rewards_box entirely
4. Player never sees the level-up prompt

## Related

- [[LevelUpModalRouting]] — Modal routing for level-up
- [[LevelUpStateManagement]] — Level-up state management
- [[RewardsBoxAtomicity]] — Rewards box atomicity invariants
- [[LevelUpBugInvestigation]] — file:line references, sentinel contracts
- [[StructureDriftPattern]] — root cause: structure drift from checkpoint PR #2162
