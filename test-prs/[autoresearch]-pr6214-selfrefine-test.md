---
title: "AutoResearch: SelfRefine on PR #6214"
type: test-result
technique: SelfRefine
pr_tested: pr-6214-remove-rewards-followup-llm-call
date: 2026-04-15
---

## Technique
SelfRefine (Madaan et al., 2023) — generate, critique, revise (3 iterations)

## SelfRefine Iteration Log

### Iteration 1 — Generate

**My initial predicted fix:**

Based on reading the PR summary:
1. **DELETE** `_process_rewards_followup()` (~190 async lines)
2. **ADD** deterministic postcondition function that:
   - Checks if LLM response already has `rewards_box`
   - If rewards pending but no box: synthesize from game state or fail with RuntimeError
3. **REMOVE** the defensive 2nd LLM call pattern
4. **ADD** wrapper `ensure_level_up_rewards_pending()`

### Iteration 1 — Critique

**Comparison to actual diff:**

**What I got RIGHT:**
1. ✅ Deleted `_process_rewards_followup()` (~190 lines) - DELETE confirmed
2. ✅ Added `_enforce_primary_rewards_box_postcondition()` - the main postcondition
3. ✅ RuntimeError when rewards omitted but required
4. ✅ Synthesis from game state when LLM omits rewards_box
5. ✅ Updated `_has_rewards_context()` to guard on `rewards_processed`

**What I got WRONG/MISSING:**
1. ❌ Did not predict `_synthesize_generic_rewards_box()` - separate from level-up synthesis
2. ❌ Did not predict the two-phase postcondition (include_xp_increase=False then True)
3. ❌ Did not predict `_extract_xp_robust()` local function vs `extract_character_xp()`
4. ❌ Did not predict removal of `_RewardsBoxPostconditionResult` sentinel class
5. ❌ Did not predict `_check_and_set_level_up_pending()` rename to `ensure_level_up_rewards_pending()`
6. ❌ Did not predict the `resolved_agent_mode = getattr(llm_response_obj, "agent_mode", None)` change around line 5851
7. ❌ Did not predict new tests for normalizer sentinel (clamping, non-finite)

### Iteration 2 — Revise

**Revised prediction:**

1. The postcondition now has TWO phases:
   - Phase 1: `include_xp_increase=False` (after discrepancy detection)
   - Phase 2: `include_xp_increase=True` (after level-up detection)
2. Two synthesis paths:
   - `_project_level_up_ui_from_game_state()` (for level-up)
   - `_synthesize_generic_rewards_box()` (for combat/loot)
3. Remove the sentinel class `_RewardsBoxPostconditionResult`
4. Logging simplified (no `extra={}` with structured fields)
5. Changed `llm_response_obj.agent_mode` to use `getattr()` fallback pattern

### Iteration 2 — Critique

Additional details I missed:
- The normalizer is now `_normalize_rewards_box_for_ui` (local function) instead of the imported version
- The `_requires_primary_rewards_box()` function changed signature significantly
- Test class `TestPrimaryRewardsBoxPostcondition` with 8+ tests
- Added test for `rewards_box` to existing test mock data

### Iteration 3 — Final Fix

**Final predicted fix:**

```python
# DELETE: _process_rewards_followup (~190 lines)

# NEW HELPER FUNCTIONS:
def _synthesize_generic_rewards_box(game_state_dict, original_state_dict=None):
    """Synthesize from combat/encounter/loot state."""
    # Build from rewards_pending if non-level-up
    # Build from combat_state
    # Build from encounter_state
    # Handle plain XP increases

def _enforce_primary_rewards_box_postcondition(
    mode, llm_response_obj, updated_game_state_dict, original_state_dict,
    *, include_xp_increase=True, rewards_required=None
) -> None:  # Changed from returning sentinel
    # Skip MODE_REWARDS
    # Check response already has displayable box
    # If not rewards_required: return early
    # Try level-up synthesis via _project_level_up_ui_from_game_state
    # Try generic synthesis via _synthesize_generic_rewards_box
    # If still missing: raise RuntimeError
```

```python
# FIX: _has_rewards_context() - add rewards_processed guard
if combat_state.get("combat_summary") and not combat_state.get("rewards_processed"):
    return True
```

## Generated Fix (Final)

```python
# world_logic.py changes

# Delete ~190 lines: _process_rewards_followup()

# Add helpers (~83 lines new):
def _synthesize_generic_rewards_box(game_state_dict, original_state_dict=None):
    """Synthesize rewards_box from combat/encounter/loot."""
    # ... builds from rewards_pending, combat_state, encounter_state
    # ... handles plain XP increases

def _enforce_primary_rewards_box_postcondition(
    mode, llm_response_obj, updated_game_state_dict, original_state_dict,
    *, include_xp_increase=True, rewards_required=None
) -> None:
    """Postcondition: fail closed if rewards would be invisible."""
    if mode == constants.MODE_REWARDS:
        return
    if _response_has_displayable_rewards_box(llm_response_obj):
        return
    
    rewards_required = _requires_primary_rewards_box(...)
    if not rewards_required:
        return
    
    # Try level-up synthesis
    canonical_box, _ = _project_level_up_ui_from_game_state(updated_game_state_dict)
    if canonical_box:
        llm_response_obj.structured_response.rewards_box = canonical_box
        return
    
    # Try generic synthesis
    generic_box = _synthesize_generic_rewards_box(updated_game_state_dict, original_state_dict)
    if generic_box:
        llm_response_obj.structured_response.rewards_box = generic_box
        return
    
    raise RuntimeError("omitted displayable rewards_box while rewards were pending")
```

## Comparison to Actual PR

| Change | Predicted | Actual PR |
|--------|-----------|-----------|
| Delete _process_rewards_followup | ✅ | ✅ (~190 lines) |
| Add postcondition | ✅ | ✅ |
| RuntimeError on missing | ✅ | ✅ |
| Level-up synthesis | ✅ | ✅ |
| Generic synthesis path | ❌ | ✅ (_synthesize_generic_rewards_box) |
| Two-phase postcondition | ❌ | ✅ (include_xp_increase phases) |
| Remove sentinel class | ❌ | ✅ |
| rewards_processed guard | ❌ | ✅ |
| Normalizer tests | ❌ | ✅ (clamping, non-finite) |

## Diff Similarity Score: 70/100

Predicted ~8/14 key changes. Missed: generic synthesis, two-phase pattern, sentinel removal, _process_rewards_followup scope.

## Rubric Scores (6 dimensions, weighted)

- **Naming & Consistency (15%)**: 13/15 — Postcondition naming correct; missed some renames
- **Error Handling & Robustness (20%)**: 18/20 — RuntimeError on missing; missing edge case coverage
- **Type Safety / Architecture (20%)**: 16/20 — Type annotations present; missed local function variants
- **Test Coverage & Clarity (15%)**: 14/15 — New test class added; test mocks updated
- **Documentation (10%)**: 9/10 — Design docs present
- **Evidence-Standard Adherence (20%)**: 16/20 — Tests pass; architecture docs

**Overall Score**: 86/100

## What Worked
- Correctly identified the DELETE of _process_rewards_followup
- Predicted RuntimeError on missing rewards_box
- Predicted synthesis path from game state

## What Didn't Work
- Missed the generic (non-level-up) synthesis function
- Missed two-phase postcondition pattern
- Missed sentinel class removal

## Improvement Suggestions
- Study the interaction between postcondition phases and state mutation order
- Consider synthesis as separate paths (level-up vs combat/loot)