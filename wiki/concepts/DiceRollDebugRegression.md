---
title: "DiceRollDebugRegression"
type: concept
tags: [worldarchitect-ai, dice, debug, regression, debug-mode]
sources: [pr-6194-investigate-dice-rolls-debug-messages-regression-p]
last_updated: 2026-04-11
---

## Summary

On current main, the game UI does not render dice roll entries or debug messages (debug_info) even when `debug_mode=true`. This regression predates PR #6161 (merged Apr 11) — it existed before that PR merged.

**Status:** Investigation open. PR #6194 is an investigation-only PR documenting findings.

## Regression Window

- **Working:** ~Mar 21 2026, commit `02a6e5fb3` (mvp-stable production)
- **Broken:** commit `8f95edde2` → current main (~3 week window)
- **PR #6161 is NOT the root cause** — proven by git merge-base ancestry checks

## Ruled Out

| Hypothesis | Evidence |
|------------|----------|
| Frontend render code changed | `diff` of `app.js` lines 869-886, 896-905, 1184-1222 — identical to stable |
| PR #6161 introduced regression | merge-base ancestor checks show #6161 is not in the regression window |
| Frontend debug-gating | render code identical stable ↔ main |

## Leading Hypothesis

Backend payload emission: `debug_info` and dice rolls under `action_resolution.mechanics.rolls` are present in streaming `done` payloads but not being emitted in `unified_response` for narrative-only turns.

This is related to [[StructureDriftPattern]] — `debug_info` was nested inside `if hasattr(structured_response, "rewards_box"):` block (PR #6204 fixed this), but the regression predates the checkpoint that introduced that nesting.

## Key Files to Check

- `mvp_site/world_logic.py` — `debug_info` emission logic (now fixed by PR #6204)
- `mvp_site/world_logic.py` — `action_resolution.mechanics.rolls` extraction
- `mvp_site/world_logic.py:6707-6738` — Former location of nested fields

## Connections

- [[StructureDriftPattern]] — Related structural issue
- [[dice_rolls]] — Dice roll display
- [[LevelUpBug]] — Related bug chain
