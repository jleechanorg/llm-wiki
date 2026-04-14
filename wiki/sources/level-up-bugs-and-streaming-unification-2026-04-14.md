---
title: "Level-Up Bugs and Streaming Unification (2026-04-14)"
type: source
tags: [worldarchitect-ai, level-up, rewards-box, streaming, atomicity, frontend, bug-chain]
date: 2026-04-14
source_file: roadmap/level-up-bugs-and-streaming-unification-2026-04-14.md
---

## Summary

The level-up bug is not a single bug — it is a multi-month cascade of regressions across **backend emission logic**, **frontend visibility gates**, and **streaming vs non-streaming code path divergence**. The fundamental reason it remains unfixed despite 15+ PRs is that each PR introduces a fix that creates a new regression in a different layer, and the fix + regression are rarely shipped in the same PR.

**The 2026-04-14 live report (no rewards box after XP gain) traces to `app.js:924`:**
```javascript
// BUGGY — hides entire rewards_box including level_up_available when xp_gained=0
if (fullData.rewards_box && fullData.rewards_box.xp_gained > 0) {
```
PR #6192 claimed this was fixed in #6161 and added regression tests. The `raw/mvp_site_all/app.js` snapshot still has the buggy gate — either the fix was not deployed or it regressed post-deployment.

---

## Why This Is Hard: Three Compounding Factors

### 1. Fix/regression coupling across layers

When backend PR #6161, #6193, #6195, #6204 fixed `rewards_box` emission, they did NOT include frontend visibility gate fixes. Each backend fix exposed a new scenario where:
- Backend correctly emits `rewards_box.level_up_available=true`
- Frontend silently hides it because `xp_gained=0`

The dice rolls regression is the same pattern: backend #6179 fixed emission, but frontend `app.js:868` still gates dice on `debugMode`.

### 2. Two code paths with divergent postconditions

| Concern | Non-streaming | Streaming |
|---------|---------------|-----------|
| Entry | `process_action_unified` | `streaming_orchestrator` done block |
| Rewards postcondition | `_enforce_primary_rewards_box_postcondition` | Not called |
| `ensure_level_up_rewards_pending` | Called with pre/post snapshots | Not called |

The streaming path (`/api/campaigns/<id>/interaction/stream`) is what real players use. It bypasses the same postcondition enforcement that the unified path runs. Beads `rev-ippc.1` and `rev-ippc.2` track this.

### 3. Canonicalizer self-undo in same persistence path

`_canonicalize_level_from_xp_in_place` (game_state.py ~639) preserves narrative-only level bumps (e.g. `level=3, XP=0`). Then `validate_and_correct_state` calls `validate_xp_level(strict=False)` which auto-corrects `stored_level > expected_level` back down. The validator always wins — canonicalizer self-undoes in the same persistence path.

---

## Bug Chain: PRs That Fixed It

| PR | What it fixed | Status |
|----|---------------|--------|
| #6233 | **Centralization** — inlined rewards/ package into game_state.py + world_logic.py; ONE `_is_state_flag_true` | Merged 2026-04-13 |
| #6254 | `has_visible_content` now includes `current_xp > 0 and next_level_xp > 0` — backend is single source of truth for visibility | Merged 2026-04-14 |
| #6259 | [antig] fixes missed serious PR audit findings including rewards bug | Merged 2026-04-14 |
| #6261 | `_extract_reward_value()` for messy LLM payloads (strings, NaN, fallback keys) — backend robustness | OPEN |

## Architecture After #6254: Backend is Single Source of Truth

With PR #6254, `normalize_rewards_box_for_ui()` `has_visible_content` correctly returns True for:
- `xp_gained > 0` ✅
- `current_xp > 0 and next_level_xp > 0` ✅ (PR #6254 fix)
- `level_up_available=true` ✅ (test case in PR #6261)

**Frontend should just `if (fullData.rewards_box)` — if backend returned it, render it.**

The `xp_gained > 0` double-gate in frontend `app.js:924` was redundant and wrong once #6254 landed. **Fix applied to wiki snapshot.**

### Bug Chain: Historical PRs (pre-centralization)

| PR | What it fixed | What it broke/regressed |
|----|---------------|------------------------|
| #6161 | rewards_box/planning_block atomicity, added normalize_rewards_box_for_ui | Over-aggressive `has_visible_content → None` gate dropped rewards_box for level-up-only payloads |
| #6179 | Living world debug gate removed (debug_info emits for non-debug) | — |
| #6193 | Removed `has_visible_content → None` gate, rewards_box no longer dropped | Broke `_process_rewards_followup` sentinel contract |
| #6195 | Restored sentinel gate with `progress_percent > 0` added | — |
| #6196 | Dragon knight template bypass dropped FIELD_REWARDS_BOX | — |
| #6197 | `debug_info` moved outside rewards_box gate | — |
| #6201 | `social_hp_challenge`, `recommend_spicy_mode`, `god_mode_response` un-nested | — |
| #6204 | `action_resolution`, `dice_rolls`, `dice_audit_events`, `resources`, `tool_requests` hoisted out of rewards_box gate | Primary fix for dice regression |
| #6192 | Added regression tests for `xp_gained=0` gate | Tests claimed fix was in #6161 but snapshot had buggy gate |
| #6165 | Wizard CTA hidden, stale level-up choices during polling | — |
| #6198 | Computed `@property level` redesign (OPEN — 7 CHANGES_REQUESTED) | Canonicalizer self-undo bug still present |

---

## FrontendRewardsBoxGate: The Bug + The Fix

**File:** `raw/mvp_site_all/app.js:924`
**Root cause:** Double-gate — backend `has_visible_content` was too restrictive, so frontend added its own gate. After PR #6254 fixes backend, frontend gate is now redundant and wrong.

**After PR #6254:** Backend `normalize_rewards_box_for_ui` is the single source of truth. Frontend should just `if (fullData.rewards_box)`.

```javascript
// BEFORE (double-gate, wrong): app.js:924
if (fullData.rewards_box && fullData.rewards_box.xp_gained > 0) {

// AFTER (single source of truth): FIXED in wiki snapshot
if (fullData.rewards_box) {
```

**Note:** PR #6254 specifically fixed `current_xp > 0 and next_level_xp > 0` in `has_visible_content`. Test case 7 in PR #6261 confirmed `level_up_available=true` also returns non-None. The frontend gate is now purely redundant.

---

## Key Beads

| ID | Priority | Focus | Status |
|----|----------|-------|--------|
| `jleechan-vcrc` | P0 | Fix FrontendRewardsBoxGate `xp_gained=0` gate (2026-04-14) | Open |
| `rev-ippc.1` | Epic | Streaming done: call primary rewards postcondition | Open |
| `rev-ippc.2` | Epic | Streaming done: call `ensure_level_up_rewards_pending` | Open |
| `rev-6twjz` | P0 | `level_up_complete` without `rewards_box` | Open |
| `rev-kyuqw` | — | `current_xp` wrong, `level_up_available` stuck | Open |
| `rev-ezqiy` | — | `projected_level_up_button_text` missing | Open |
| `rev-6j269` | — | Multi-level progression no modal | Open |
| `rev-5mivk` | — | `atomicity_contract` planning suppression | Open |
| `REV-dl8xu` | Epic | Level/XP centralization — delete rewards/ package | Approved design |

---

## Connections

- [[LevelUpBug]] — 8+ PR bug chain, 3 root causes
- [[FrontendRewardsBoxGate]] — specific frontend gate bug concept page
- [[LevelUpBugInvestigation]] — investigation with file:line references
- [[LevelUpBugEvidence]] — evidence map: beads, memory files, roadmap
- [[StructureDriftPattern]] — root cause of field nesting (checkpoint PR #2162)
- [[RewardsBoxAtomicity]] — 6 atomicity violations in rewards_box/planning_block
- [[DiceRollDebugRegression]] — same pattern as FrontendRewardsBoxGate
- [[LevelUpStateManagement]] — stale flags: `level_up_in_progress`, `rewards_pending`

## Contradictions

- PR #6192 source page claims `xp_gained > 0` gate was fixed in #6161 (commit `a872098d7c`), but `raw/mvp_site_all/app.js` snapshot still shows the buggy gate at line 924. Either the fix regressed post-deployment or the snapshot predates the fix.
- Bead `jleechan-o34j` (FrontendRewardsBoxGate) was **closed as "done" on 2026-04-12** but the bug is live as of 2026-04-14.
