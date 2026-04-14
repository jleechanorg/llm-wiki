---
title: "FrontendRewardsBoxGate"
type: concept
tags: [frontend, rewards-box, xp, level-up, visibility, worldarchitect-ai, bug-chain]
sources: [rev-qcax, pr-6192, pr-6254, pr-6261, level-up-bugs-and-streaming-unification-2026-04-14]
last_updated: 2026-04-14
---

## Summary

`FrontendRewardsBoxGate` was a double-gate at `app.js:924` where the frontend duplicated the backend's `has_visible_content` check. After PR #6254 (centralization + `has_visible_content` fix), the frontend gate is now **redundant and wrong** — backend `normalize_rewards_box_for_ui` is the single source of truth.

**Fix applied:** `app.js:924` changed from `if (fullData.rewards_box && fullData.rewards_box.xp_gained > 0)` to `if (fullData.rewards_box)`.

## The Bug (Historical)

```javascript
// app.js line 924 — BEFORE PR #6254 (double-gate, wrong)
if (fullData.rewards_box && fullData.rewards_box.xp_gained > 0) {
```

## The Fix (After PR #6254 Centralization)

```javascript
// app.js line 924 — AFTER (single source of truth, correct)
if (fullData.rewards_box) {
```

## Why the Gate Was Wrong After #6254

PR #6254 fixed `has_visible_content` in `normalize_rewards_box_for_ui` to return True for:
- `xp_gained > 0` ✅
- `current_xp > 0 and next_level_xp > 0` ✅ (PR #6254 fix)
- `level_up_available=true` ✅ (confirmed via test case 7 in PR #6261)

Backend is now the **single source of truth**. Frontend double-gate would suppress what backend correctly emitted.

## Key PRs

| PR | Date | What it did |
|----|------|-------------|
| #6233 | 2026-04-13 | **Centralization** — inlined rewards/ into game_state.py + world_logic.py |
| #6254 | 2026-04-14 | Fixed `has_visible_content` to include XP progress tracking |
| #6259 | 2026-04-14 | [antig] missed serious PR audit findings + rewards bug |
| #6261 | OPEN | `_extract_reward_value()` for messy LLM payloads |

## Related

- [[LevelUpBugInvestigation]] — file:line references, sentinel contracts
- [[StructureDriftPattern]] — root cause: structure drift from checkpoint PR #2162
- [[LevelUpStateManagement]] — stale flag management
- [[RewardsBoxAtomicity]] — rewards_box atomicity invariants
