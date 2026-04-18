# S10 Repro — Missing Rewards Box (gufBO3, KtKlU0, 3JM2) — 2026-04-18

**Bead:** rev-7vyc (streaming fix family)
**Branch at repro time:** `fix/streaming-rewards-canonicalization` (commit 12bfbdba5)
**Server:** `mvp-site-app-s10-i6xf2p72ka-uc.a.run.app`

## Campaign Analysis (Firestore game_states/current_state)

### Campaign gufBO3EVc0GAp5LmVzWG — Class A + Class C

**State at repro time:**
- `level=1, experience.current=700` (no `to_next_level` field)
- `level_up_pending=False`, `level_up_in_progress=absent`, `level_up_complete=absent`
- `rewards_box=None` (top-level and ccs)
- `planning_block` present with normal (non-level-up) choices

**Analysis:**
- `level_from_xp(700) = 2` (threshold 300 crossed), stored level = 1 → `level_up_available=True`
- But `level_up_pending=False` and `rewards_box=None` → XP threshold crossing NOT propagated
- Earlier repro (Wave 4/5) showed `level_up_in_progress={}` (truthy empty map, Bug Pattern B) blocking detection; current state shows it cleared, but `rewards_box` was never re-emitted
- Root cause: `_extract_xp_robust` was returning 0 for `experience.current` field (reading only `xp` key), causing `resolve_level_up_signal` to see XP=0 and report no threshold crossing

**Fix required:** `_extract_xp_robust` fallback to `experience.current` (committed in 12bfbdba5)

### Campaign KtKlU0rOV6MmG3b6cOxd — Class D + Class E

**State at repro time:**
- `level=1, experience.current=400`
- `level_up_pending=False`, all flags absent
- `rewards_box=None` (top-level and ccs)
- `planning_block` present AND contains **"Level Up to Level 2" choice**

**Analysis:**
- `level_from_xp(400) = 2` (threshold 300 crossed), stored level = 1 → level-up due
- planning_block injection DID detect the level-up (correct level-up choice present)
- BUT `rewards_box=None` — passthrough canonicalization path did not persist `rewards_box`
- Root cause: `normalize_rewards_box_for_ui()` not called on streaming path when `_has_level_up_ui_signal=False` (the `lua` was stripped at line 430 of `_canonicalize_core` because `level_up_detected=False` due to XP format mismatch)

**Fix required:** Both `_extract_xp_robust` XP format fix AND `normalize_rewards_box_for_ui()` on all paths

### Campaign 3JM2gKc3eTFZHQnBtO8m — No Active Bug (State Advanced)

**State at repro time:**
- `level=2, experience.current=350, to_next_level=900`
- All level_up flags False/absent, `rewards_box=None`
- `planning_block` present with normal choices

**Analysis:**
- `level_from_xp(350) = 2` matches stored level=2 → `progression.level_up_available=False`
- `rewards_box=None` is CORRECT (no level-up due)
- Bug reported at time of screenshot was Class B (lua=True leaking in `_canonicalize_core`); state has since advanced (character was promoted to 2, XP 350 < threshold 900 for level 3)
- No active bug at current state

## Root Causes Summary

| Class | Mechanism | Fixed by |
|---|---|---|
| Class A | `_extract_xp_robust` returned 0 for `experience.current` field; XP threshold crossing missed | `_extract_xp_robust` fallback fix (commit 12bfbdba5) |
| Class C | `level_up_pending` never set True; `resolve_level_up_signal` returned False | `resolve_level_up_signal` level_up_pending check (commit 12bfbdba5) |
| Class D | `normalize_rewards_box_for_ui()` not called on streaming passthrough path | Streaming canonicalization fix (PR #6361) |
| Class E | planning_block injection reached level-up choice, but `rewards_box` not emitted | Same as Class D |

## Caveat — Historical Campaigns Cannot Be Retroactively Fixed

These campaigns' broken state (rewards_box=None, level_up_pending=False) will persist in Firestore unless the user triggers a new action that re-runs the rewards computation. The fix branch prevents this for NEW campaigns.
