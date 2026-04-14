---
title: "Level-Up Bugs and Streaming Parity — Root Cause Synthesis"
type: synthesis
tags: [worldarchitect-ai, level-up, streaming, bug-chain, atomicity]
sources: [level-up-bugs-and-streaming-unification-2026-04-14]
last_updated: 2026-04-14
---

## Summary

The level-up bug is not a single bug — it is a multi-month cascade of regressions across **backend emission logic**, **frontend visibility gates**, and **streaming vs non-streaming code path divergence**. Each PR introduces a fix that creates a new regression in a different layer, and fix + regression are rarely shipped in the same PR.

## Key Insights

### 1. Fix/Regression Coupling Across Layers

When backend PRs #6161, #6193, #6195, #6204 fixed `rewards_box` emission, they did NOT include frontend visibility gate fixes. Each backend fix exposed a new scenario where:
- Backend correctly emits `rewards_box.level_up_available=true`
- Frontend silently hides it because `xp_gained=0`

The dice rolls regression is the same pattern: backend #6179 fixed emission, but frontend `app.js:868` still gates dice on `debugMode`.

**Pattern:** Backend team and frontend team ship fixes independently → invisible regressions at integration points.

### 2. Two Code Paths With Divergent Postconditions

| Concern | Non-streaming | Streaming |
|---------|---------------|-----------|
| Entry | `process_action_unified` | `streaming_orchestrator` done block |
| Rewards postcondition | `_enforce_primary_rewards_box_postcondition` | **Not called** |
| `ensure_level_up_rewards_pending` | Called with pre/post snapshots | **Not called** |

The streaming path (`/api/campaigns/<id>/interaction/stream`) bypasses the same postcondition enforcement that the unified path runs. This means players on the real (streaming) code path get different behavior than test scenarios.

**Pattern:** Streaming was built as an optimization but never fully parity-checked against the canonical path.

### 3. Canonicalizer Self-Undo in Same Persistence Path

`_canonicalize_level_from_xp_in_place` (game_state.py ~639) preserves narrative-only level bumps (e.g. `level=3, XP=0`). Then `validate_and_correct_state` calls `validate_xp_level(strict=False)` which auto-corrects `stored_level > expected_level` back down. The validator always wins — canonicalizer self-undoes in the same persistence path.

**Pattern:** Two state-mutating operations that should be ordered differently are running back-to-back, with the second always winning.

### 4. Double-Gate Architecture That Degrades

After PR #6254, `normalize_rewards_box_for_ui()` `has_visible_content` correctly handles:
- `xp_gained > 0` ✅
- `current_xp > 0 and next_level_xp > 0` ✅ (PR #6254 fix)
- `level_up_available=true` ✅

Frontend `app.js:924` had its own redundant gate (`xp_gained > 0`) that became wrong once backend was fixed. The architecture degraded from "two gates for safety" to "two gates where one is now wrong."

**Fix:** Frontend should just `if (fullData.rewards_box)` — if backend returned it, render it. Backend is now the single source of truth.

### 5. Bug Chain Complexity Obscures Root Cause

15+ PRs over months, with each fix breaking something different. The bug chain table shows PRs going forward and backward in time — PR #6192 claimed the fix was in #6161, but the snapshot still had the buggy gate. Bead `jleechan-o34j` was closed as "done" on 2026-04-12 but the bug was live on 2026-04-14.

**Pattern:** Evidence of fix != proof of fix deployment. Snapshots can predate fixes, and regression tests can pass for the wrong reason.

## Connections

- [[FrontendRewardsBoxGate]] — the specific frontend gate that became redundant after #6254
- [[StreamingParity]] — the overarching theme: streaming path lacks postcondition enforcement
- [[RewardsBoxAtomicity]] — 6 atomicity violations in rewards_box/planning_block
- [[DiceRollDebugRegression]] — same pattern, different field
- [[StructureDriftPattern]] — root cause of field nesting from checkpoint PR #2162
- [[LevelUpStateManagement]] — stale flags: `level_up_in_progress`, `rewards_pending`
