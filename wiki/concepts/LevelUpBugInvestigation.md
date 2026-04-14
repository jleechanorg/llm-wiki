---
title: "LevelUp Bug Investigation"
type: concept
tags: [worldarchitect, bug, level-up, dice-rolls, debug-info, structure-drift]
last_updated: 2026-04-11
---

## Summary

The dice-rolls/debug_info regression was caused by **structure drift**: `dice_rolls`, `action_resolution`, `debug_info`, and other fields were incorrectly nested inside an `if hasattr(structured_response, "rewards_box"):` block, so they only emitted on combat/XP turns. A parallel issue (rewards_box itself being dropped for level-up-only payloads) was introduced in PR #6161.

**The structure drift fix (PRs #6197/#6204) is now merged to origin/main.** All related fixes are on `origin/main` at commit `0f9191b71`.

---

## Bug Chain: PRs #6161 → #6179 → #6193 → #6194 → #6195 → #6196 → #6197 → #6200 → #6201 → #6204 → #6214

### PR #6161 (d868fec0c) — Root Cause Layer
Added `mvp_site/rewards/` module pipeline with `normalize_rewards_box_for_ui` that had an over-aggressive `has_visible_content → None` gate, causing `rewards_box` to be silently dropped for level-up-only payloads.

### PR #6193 (7facd239b) — rewards_box Fix Part 1
Removed the `has_visible_content → None` gate in `normalize_rewards_box_for_ui`. **Introduced a bug**: broke the None-sentinel contract used by `_process_rewards_followup` (the second-LLM-call defensive mechanism).

### PR #6194 (006a8de13) — INVESTIGATION ONLY
Confirmed dice_rolls and debug_info regression predates #6161 (root cause is commit `8f95edde2`, ~3 weeks before #6161). Ruled out frontend as cause. The dice rolls ARE present in `action_resolution.mechanics.rolls` in streaming `done` payloads. **No code change — investigation only.**

### PR #6195 (50310b5d0) — rewards_box Fix Part 2
Restored `has_visible_content → None` gate in `normalize_rewards_box_for_ui` but with `progress_percent > 0` added as displayable condition. Re-established None-sentinel for `_process_rewards_followup`.

### PR #6197 (e4c92ab54) — debug_info Structure Drift Fix
Moved `debug_info` emission outside the `rewards_box` gate. Was previously emitted inside `if hasattr(structured_response, "rewards_box"):` block, silently absent on most turns even when `debug_mode=True`.

### PR #6200 (401d1dfa6) — Frontend debug_info Rendering Fix
Added rendering of `debug_info.system_message` in debug mode in `app.js`. Previously captured but never displayed.

### PR #6201 (7e0ab4b65) — Additional Fields Fix
Un-nested `social_hp_challenge`, `recommend_spicy_mode`, `recommend_exit_spicy_mode`, and `god_mode_response` from rewards_box gate. Added tests including `test_dice_rolls_emitted_without_rewards_box`.

### PR #6204 (30ff7a7bf) — action_resolution + Final Structure Drift Fix
Hoisted 5 fields out of rewards_box block: `action_resolution`, `dice_rolls`, `dice_audit_events`, `resources`, `tool_requests`. **This is the primary fix for the dice regression** — `dice_rolls` and `action_resolution.mechanics.rolls` are now emitted on ALL turns, not just combat turns.

### PR #6214 — NOT YET MERGED
Removed the second LLM call (`_process_rewards_followup`). Single-call architecture where primary LLM handles rewards directly. **Still open / not in origin/main.**

### PR #6198 (level_not_clearing) — OPEN
Addresses 3 production bugs: sticky finish button (Class A), zero rewards_box on level-up (Class B/L), wrong XP threshold (Class F). **Introduces new file `game_state.py`** with canonicalizers. **Still open** — 1 APPROVED, 6 CHANGES_REQUESTED. Three blockers:
1. **CRITICAL**: `_canonicalize_level_from_xp_in_place` preservation undone by `validate_and_correct_state()` → `validate_xp_level(strict=False)` which auto-corrects `stored_level > expected_level` back down
2. **MEDIUM**: Stale finish button fix (`has_stale_finish`) requires `not other_choice_ids` — misses mixed-choices scenario
3. **CRITICAL**: Streaming E2E gap — evidence bundles use `GOD_MODE_UPDATE_STATE` which bypasses the `rewards_box` → `finish_level_up_return_to_game` pipeline where the bug lives

**Known limitation (self-reported)**: Integration bundle bypasses production rewards pipeline via `GOD_MODE_UPDATE_STATE` — does not prove end-to-end streaming path works.

---

## Current State (origin/main @ 0f9191b71)

### What is Fixed
- `action_resolution` emitted on all turns (line ~6706, outside rewards_box gate) ✅
- `dice_rolls` (top-level) emitted from `structured_response.dice_rolls` when present (line ~6920) ✅
- `dice_audit_events` emitted on all turns ✅
- `debug_info` emitted on all turns when `debug_mode=True` (line ~6731) ✅
- `resources`, `tool_requests` emitted on all turns ✅
- `social_hp_challenge`, `recommend_spicy_mode`, `recommend_exit_spicy_mode`, `god_mode_response` emitted without rewards_box gate ✅
- `rewards_box` not dropped for level-up-only payloads ✅
- Frontend renders `debug_info.system_message` in debug mode ✅

### What is NOT Fixed (PR #6214 not merged)
- `_process_rewards_followup` second-LLM-call defensive mechanism still exists (line ~1733 in origin/main)
- Single-call architecture not yet deployed

---

## Frontend Rendering: Dice Rolls Are Debug-Only

**Critical finding**: `app.js:868-884` shows dice rolls are **intentionally gated** on `debugMode`:

```javascript
// 4. Dice rolls (only show in debug mode)
if (debugMode) {
  const actionResolutionDice = getActionResolutionDiceRolls(fullData.action_resolution);
  const diceRollsToShow = actionResolutionDice.rolls.length > 0
    ? actionResolutionDice.rolls
    : (Array.isArray(fullData.dice_rolls) ? fullData.dice_rolls : []);
  // ...
}
```

This means:
- **Non-debug users were NEVER supposed to see dice rolls** (by design)
- **Debug users with `debug_mode=true`** should now see dice rolls after the #6204 fix
- The frontend shows dice rolls from TWO sources (preference order):
  1. `fullData.action_resolution.mechanics.rolls` (via `getActionResolutionDiceRolls`)
  2. `fullData.dice_rolls` (legacy fallback)

---

## Key File:Line References

### world_logic.py — Emission Site (origin/main @ 0f9191b71)
| Field | Location | Gate |
|-------|----------|------|
| `action_resolution` | ~6706 `add_action_resolution_to_response()` | `if structured_response:` (OUTSIDE rewards_box) |
| `dice_rolls` | ~6920 `if hasattr(structured_response, "dice_rolls")` | `if structured_response:` |
| `dice_audit_events` | ~6922 | `if structured_response:` |
| `debug_info` | ~6731 `if debug_mode and hasattr(...)` | `debug_mode` only |
| `rewards_box` | ~6707 `if hasattr(structured_response, "rewards_box")` | Independent conditional |
| `social_hp_challenge` | ~6712 | Independent conditional |
| `god_mode_response` | ~6735 | Independent conditional |

### app.js — Frontend Render (frontend_v1/app.js)
| Field | Location | Condition |
|-------|----------|-----------|
| `dice_rolls` | ~868-884 | `if (debugMode)` + non-empty rolls |
| `debug_info.system_message` | ~896+ | `if (debugMode)` |
| `getActionResolutionDiceRolls` | ~805-840 | Helper for formatting |

### action_resolution_utils.py
- `normalize_action_resolution_rolls()` at line ~179: Normalizes `action_resolution.mechanics.rolls` in place (maps `label` → `purpose`, populates `total`)
- `add_action_resolution_to_response()` at line ~272: Adds `action_resolution` to unified_response

### rewards/builder.py (NOT in local checkout)
- `normalize_rewards_box_for_ui()`: Sentinel function that gates rewards_box emission
- After PR #6193: removed `has_visible_content → None` gate
- After PR #6195: restored gate with `progress_percent > 0` condition

---

## Hypothesis: Is the Dice Regression Fixed?

**YES — for users with `debug_mode=true`.**

The root cause was: `dice_rolls` and `action_resolution.mechanics.rolls` were inside the `if hasattr(structured_response, "rewards_box"):` block (structure drift). They only emitted on combat/XP turns. On pure narrative turns (no rewards_box), dice rolls were silently absent.

After PR #6204 (hoisting), `add_action_resolution_to_response()` is called unconditionally for ALL turns, so `action_resolution.mechanics.rolls` is always present in the payload.

**For non-debug users**: Dice rolls are intentionally not shown (frontend `debugMode` gate). This is by design and unchanged.

**PR #6214 (single-call architecture)**: Still open. Removes `_process_rewards_followup` second LLM call. Not required for dice fix but eliminates redundant latency.

---

## Next Action Needed

1. **Verify production deployment** of origin/main @ 0f9191b71 (contains all fixes through #6204)
2. **Test with `debug_mode=true`** in a real game session: confirm dice rolls now appear on narrative turns
3. **Merge PR #6214** when ready: eliminates redundant second-LLM-call, reduces latency
4. **Complete PR #6194 investigation** (still open): runtime reproduction was not executed — confirm actual backend payload content in production after fix deployment
