# Level-Up Debugging Saga — 17 Days, Still Not Fixed

**Source file**: `feedback_2026-05-01_level-up-debugging-saga.md`
**Captured**: 2026-05-01
**Type**: feedback / Critical

## Summary

30+ PRs across 17 days (2026-04-14 to 2026-05-01) failed to fix the original level-up bugs. The root cause across all attempts: **upstream LLM prompt never corrected, downstream guards are patches not fixes**.

## Original Failure Modes

| ID | Failure | Status |
|----|---------|--------|
| FM1 | LLM derived `level` from `XP` instead of reading `player_character_data.level` | PARTIAL — backend override exists but model prompt never fixed |
| FM2 | XP monotonic decrease not blocked | GUARD EXISTS — but only in formatter path; upstream LLM still produces wrong XP |
| FM3 | Stale `level_up_pending` causing modal lockout | BUGGY — detection function has pre-existing bugs; 3 tests skipped |
| FM4 | Streaming vs polling path divergence | NOT RESOLVED — multiple projection paths still exist |
| FM5 | Signal-based vs XP-based level-up resolution conflicts | NOT RESOLVED |
| FM6 | Normalization atomicity violations (raw LLM rewards_box persisted without canonicalization) | PARTIALLY FIXED — canonicalizer exists but divergence remains |

## Key Code Evidence

### FM1: Backend Override (Not Upstream Fix)
**File**: `mvp_site/rewards_engine.py:1456-1461`
```python
# FALSE NEGATIVE: level_up=False, but xp_total >= threshold.
# TRANSITIONAL ZFC GUARD (Class 5 XP-overflow trigger).
# M3_DELETION_TARGET: remove once the model reliably emits level_up=True
if not is_level_up and xp_total >= threshold:
    logger.warning("Contradiction: level_up=false but xp_total=%s >= threshold...")
```
The override exists but is labeled TRANSITIONAL. The **upstream LLM prompt never corrected** so the model still derives level from XP.

### FM2: Monotonicity Guard
**File**: `mvp_site/rewards_engine.py:1443-1450`
```python
# Enforce monotonicity: clamp LLM-provided xp_total to stored value
if xp_total < stored_xp:
    xp_total = stored_xp
    clamped = True
```
Guard exists but is downstream patch, not upstream fix.

### FM3: Stale Flag Detection Has Bugs
**File**: `mvp_site/agents.py:148-183`
```python
def _is_stale_level_up_pending(game_state):
    """True when level_up_pending is set but XP/rewards do not support level-up."""
    # ... bug: calls is_level_up_active which calls gs.get() on MagicMock
```
**Three tests SKIPPED** with note: `"Pre-existing branch bug: _is_stale_level_up_pending calls is_level_up_active which calls gs.get() on MagicMock"`

- `test_agents.py:2083`
- `test_rev_439p_modal_bypass.py:16`
- `test_modal_agent_critical_bugs.py:143`

## Design Doc vs Reality

**File**: `roadmap/zfc-level-up-model-computes-2026-04-19.md`

The design doc specifies 4 stages. **None completed**:

| Stage | Target | Status |
|-------|--------|--------|
| M0 | Delete duplicate legacy branches | NOT DONE — many still exist |
| M1 | Real-model compliance probe | NOT DONE — no evidence model reliably emits `previous_turn_exp`/`current_turn_exp` |
| M2 | Formatter narrowing | PARTIAL |
| M3 | Transport parity + legacy deletion | NOT DONE — divergence remains |

## Core Lesson

**The bugs weren't fixed because the approach was wrong from the start:**

Instead of:
1. First fixing the upstream prompt contract (so the model outputs correct fields)
2. Then enforcing the formatter boundary (so only canonical paths format level-up)
3. Then deleting legacy branches (reducing attack surface)

The effort was scattered across:
- Adding downstream guards without fixing upstream
- Creating new PRs instead of building on merged work
- Fixing CI infrastructure before fixing production code
- Documenting problems instead of fixing them

**Net result**: 17 days, 30+ PRs, bugs still alive.

## Key File References

- `/Users/jleechan/projects/worktree_level4/mvp_site/rewards_engine.py` — monotonicity guard at 1443-1450, FM1 false-negative override at 1456-1504
- `/Users/jleechan/projects/worktree_level4/mvp_site/agents.py:148-183` — `_is_stale_level_up_pending()` (HAS BUGS - tests skipped)
- `/Users/jleechan/projects/worktree_level4/mvp_site/world_logic.py:2760-2792` — `_is_level_up_time_freeze_context()`
- `/Users/jleechan/projects/worktree_level4/roadmap/zfc-level-up-model-computes-2026-04-19.md` — full ZFC design spec
