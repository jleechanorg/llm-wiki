---
name: Level-Up Debugging Saga - 17 Days, Still Not Fixed
description: 30+ PRs across 17 days failed to fix FM1 (LLM derived level from XP), FM2 (XP monotonic decrease not blocked), stale level_up_pending modal lockout, streaming/polling divergence
type: feedback
bead: none
originSessionId: 78407be0-6864-42da-9926-4cd5bc97ad6f
---
## Context

**Duration**: 2026-04-14 to 2026-05-01 (~17 days)
**PRs attempted**: 30+
**Merged**: Small fraction
**Original failure modes** (unchanged across all attempts):

1. **FM1**: LLM derived `level` from `XP` instead of reading `player_character_data.level`
2. **FM2**: XP monotonic decrease not blocked (only warned, not prevented)
3. **FM3**: Stale `level_up_pending` flags causing modal lockout
4. **FM4**: Streaming vs polling path divergence
5. **FM5**: Signal-based vs XP-based level-up resolution conflicts
6. **FM6**: Normalization atomicity violations (raw LLM `rewards_box` persisted without canonicalization)

## Antipatterns Observed

| # | Antipattern | Manifestation | Root Cause |
|---|-------------|---------------|------------|
| 1 | PR proliferation without root cause fix | Same bugs fixed in different PRs repeatedly | No diagnosis before PR creation |
| 2 | CI/infrastructure consuming primary deliverable time | 6h lost to CI PRs with zero production code | Primary deliverable displaced |
| 3 | Same bugs fixed multiple times | FM1 appeared in at least 4 different PRs | No upstream fix, only downstream patches |
| 4 | Test harness ghost failures masking real bugs | Skipped tests, mock-related failures hiding actual behavior | Test infrastructure issues |
| 5 | Normalization atomicity violations | Raw LLM `rewards_box` persisted without `normalize_rewards_box_for_ui()` | Passthrough path didn't normalize |
| 6 | "Documenting a problem is not fixing it" | Docstrings added describing side effects instead of removing them | Commitment integrity violation |

## What the Code Actually Has Now

### FM1 Fix: LLM-level-from-XP Detection

**File**: `mvp_site/rewards_engine.py:1456-1461`
```python
# FALSE NEGATIVE: level_up=False, but xp_total >= threshold.
# TRANSITIONAL ZFC GUARD (Class 5 XP-overflow trigger).
# M3_DELETION_TARGET: remove once the model reliably emits level_up=True
# whenever XP crosses the next-level threshold.
if not is_level_up and xp_total >= threshold:
    logger.warning(
        "Contradiction: level_up=false but xp_total=%s >= threshold for "
        "level %s (%s). Overriding level_up to true.",
        xp_total, next_level, threshold,
    )
```

**Verdict**: PARTIAL. The backend override exists but is labeled TRANSITIONAL with M3_DELETION_TARGET. It overrides `level_up=false` to `true` when XP >= threshold, but the model still derives level from XP instead of reading `player_character_data.level`. The root cause (LLM prompt/prompt contract) was never fixed.

### FM2 Fix: XP Monotonicity Guard

**File**: `mvp_site/rewards_engine.py:1443-1450`
```python
# Enforce monotonicity: clamp LLM-provided xp_total to stored value to
# prevent downstream state regression and inconsistent XP math.
clamped = False
if xp_total < stored_xp:
    xp_total = stored_xp
    clamped = True
    if out_meta is not None:
        out_meta["monotonicity_clamped"] = True
```

**Verdict**: FIXED (guard exists). But it's clamped only in `_apply_explicit_signal_heuristic_override()`, which is a transitional formatter path. The upstream LLM prompt still doesn't prevent the model from deriving wrong XP values.

### FM3 Fix: Stale `level_up_pending` Detection

**File**: `mvp_site/agents.py:148-183`
```python
def _is_stale_level_up_pending(game_state):
    """True when level_up_pending is set but XP/rewards do not support level-up."""
    current_xp = rewards_engine._extract_xp_robust(player_data)
    next_level_xp = xp_needed_for_level(current_level + 1)
    return current_xp < next_level_xp
```

**Verdict**: EXISTS but has BUGS. Tests at `test_agents.py:2083`, `test_rev_439p_modal_bypass.py:16`, and `test_modal_agent_critical_bugs.py:143` are all SKIPPED with note: "Pre-existing branch bug: _is_stale_level_up_pending calls is_level_up_active which calls gs.get() on MagicMock". The stale flag detection itself has a pre-existing bug and was never fixed.

### FM6 Fix: Normalization Atomicity

**File**: `mvp_site/rewards_engine.py:1820` - `canonicalize_rewards()` is the canonical entry point
**But**: PR #6265 found the passthrough path bypassed normalization. The codebase now has the canonicalizer, but the streaming vs polling divergence (FM4) was never fully resolved.

## Design Doc: What Should Be There

**File**: `roadmap/zfc-level-up-model-computes-2026-04-19.md`

The design doc SPECIFIES:
- **Stage 0**: Delete duplicate legacy branches (NOT DONE - many still exist)
- **Stage 1**: Real-model compliance probe (NOT DONE - no evidence that model reliably emits `previous_turn_exp`/`current_turn_exp`)
- **Stage 2**: Formatter narrowing (PARTIAL - `format_model_level_up_signal()` still public)
- **Stage 3**: Transport parity streaming/non-streaming (NOT DONE - divergence remains)
- **Stage 4**: Delete legacy backend inference (NOT DONE - `resolve_level_up_signal()` still exists)

**M3 enforcement**: The doc requires net negative production LOC for the migration. Current evidence shows net positive - more code was added than deleted.

## The Specific Gap: What Is Still NOT Fixed

| Bug | Status | Gap |
|-----|--------|-----|
| FM1: LLM derives level from XP instead of reading `player_character_data.level` | PARTIAL - backend override exists but model prompt never fixed | Model still has wrong prompt contract; backend guard is transitional fallback |
| FM2: XP monotonic decrease not blocked | GUARD EXISTS - but only in formatter path | The LLM still produces wrong XP values; guard is downstream patch not upstream fix |
| FM3: Stale level_up_pending modal lockout | BUGGY - detection function has pre-existing bugs | Three tests skipped with note "Pre-existing branch bug: _is_stale_level_up_pending calls is_level_up_active which calls gs.get() on MagicMock" |
| FM4: Streaming/polling path divergence | NOT RESOLVED | `_build_early_metadata_payload()` vs `project_level_up_ui()` vs `canonicalize_rewards()` still multiple paths |

## Key File References

- `/Users/jleechan/projects/worktree_level4/mvp_site/rewards_engine.py` - monotonicity guard at 1443-1450, FM1 false-negative override at 1456-1504
- `/Users/jleechan/projects/worktree_level4/mvp_site/agents.py:148-183` - `_is_stale_level_up_pending()` (HAS BUGS - tests skipped)
- `/Users/jleechan/projects/worktree_level4/mvp_site/world_logic.py:2760-2792` - `_is_level_up_time_freeze_context()`
- `/Users/jleechan/projects/worktree_level4/roadmap/zfc-level-up-model-computes-2026-04-19.md` - full ZFC design spec

## Core Lesson

**The bugs weren't fixed because the approach was wrong from the start.** Instead of:
1. First fixing the upstream prompt contract (so the model outputs correct fields)
2. Then enforcing the formatter boundary (so only canonical paths format level-up)
3. Then deleting legacy branches (reducing attack surface)

The effort was scattered across:
- Adding downstream guards without fixing upstream
- Creating new PRs instead of building on merged work
- Fixing CI infrastructure before fixing production code
- Documenting problems instead of fixing them

**Net result**: 17 days, 30+ PRs, bugs still alive because no PR ever went upstream to fix the root cause (LLM prompt) and downstream to enforce the boundary (delete legacy paths).
