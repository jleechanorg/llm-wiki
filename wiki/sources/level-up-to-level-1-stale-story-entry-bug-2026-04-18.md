# "Level Up to Level 1" Bug — Stale Story Entry Residue (2026-04-18)

**Bead:** rev-7vyc (streaming fix family)
**Campaign:** `wOhBvrJ0gYA2Ox9g1kLC` ("Stellaris - Nocturne V1")
**Bug Class:** Class 4 — Historical Stale-Flag Residue

## Root Cause

Pre-fix passthrough writes skipped `normalize_rewards_box_for_ui()` / `canonicalize_rewards()`, leaving two corrupted story entries in Firestore with `rewards_box.level_up_available=True` that were never cleared:

| Story Entry ID | Seq | `current_xp` | `next_level_xp` | Issue |
|---|---|---|---|---|
| `WZUsWv3sCZ7UGAXJ2Htq` | 28 | 300 | 900 | Self-inconsistent: 300 < 900, no level-up due |
| `e9itnNQ2dblpCKtTBqwJ` | 96 | 2850 | 2700 | Post-level-up residue: XP > threshold (2850 > 2700) but `new_level=None` |

## "Level Up to Level 1" Text Origin

`rewards_engine.py:206-211` — When `level_up_pending=True` and `current_level=1`, `resolve_level_up_signal` sets `target_level = current_level = 1`. This generates the planning choice "Level Up to Level 1" (meaningless — no actual level change). This occurred at an earlier campaign snapshot when `pc.level=1` and a stale `level_up_pending=True` persisted.

## Current State (Repro-Time)

| Field | Value |
|---|---|
| `pc.level` | 5 |
| `pc.experience.current` | 10150 |
| `pc.experience.to_next_level` | 14000 |
| `ccs.level_up_pending` | `False` |
| `rewards_box` (game_state) | `null` |

Current state is CLEAN. Bug was live at earlier session and captured in repro bundle at `/tmp/worldarchitect.ai/feat_level-up-atomicity-xp-signal-fix/repro_copy_campaign/20260417-060505/iteration_001/`.

## Fix Requirements

1. **Story entry migration**: Retroactively clear/canonicalize stale `rewards_box.level_up_available=True` on story entries where XP does not support the flag.
2. **Passthrough fix**: PR #6358 / PR #6361 atomicity fix prevents future occurrences but does not heal existing corrupted entries.

## Prevention

The fix in `_canonicalize_core` (line 430, `merged_rb.pop("level_up_available", None)` when `level_up_detected=False`) prevents future passthrough writes from leaving stale `lua=True`. But already-persisted story entries with stale flags require a migration.
