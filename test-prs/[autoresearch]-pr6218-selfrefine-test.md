---
title: "AutoResearch: SelfRefine on PR #6218"
type: test-result
technique: SelfRefine
pr_tested: pr-6218-structured-gcp-logging-rewards-box
date: 2026-04-15
---

## Technique
SelfRefine (Madaan et al., 2023) — generate, critique, revise (3 iterations)

## SelfRefine Iteration Log

### Iteration 1 — Generate

**My initial predicted fix:**

Based on reading the PR summary:
1. Add structured GCP logging to `_enforce_primary_rewards_box_postcondition`
2. Log three distinct events:
   - LLM-provided rewards_box
   - LLM-omitted + server-synthesized
   - Failure case (RuntimeError)
3. Remove structured `extra={}` dicts from logging calls
4. Simplify postcondition by removing result class

### Iteration 1 — Critique

**Comparison to actual diff:**

**What I got RIGHT:**
1. ✅ Added structural logging to postcondition (various log lines)
2. ✅ Changed from sentinel class to early returns
3. ✅ Use `getattr()` for agent_mode fallback

**What I got WRONG/MISSING:**
1. ❌ This PR ADDS the functions (not just logging) - the diff shows adding `_response_has_displayable_rewards_box`, `_xp_increased`, `_requires_primary_rewards_box`, `_enforce_primary_rewards_box_postcondition`, `_RewardsBoxPostconditionResult`
2. ❌ Did not predict `_check_and_set_level_up_pending()` wrapper
3. ❌ Did not predict the test changes (removing AsyncMock patches)
4. ❌ Did not predict the import: `from types import SimpleNamespace`
5. ❌ Overlap with PR 6214 - this adds what that deletes

### Iteration 2 — Revise

**Revised prediction:**

This PR includes the base infrastructure that PR 6214 depends on. The diff shows:
1. Adding `_RewardsBoxPostconditionResult` sentinel class
2. Adding the 4 helper functions
3. Adding `_check_and_set_level_up_pending()` wrapper
4. Using `resolved_agent_mode = getattr(llm_response_obj, "agent_mode", None) or mode`
5. Removing AsyncMock patches from tests
6. Replacing `_process_rewards_followup` call with postcondition calls

### Iteration 2 — Critique

Additional observations:
- This is actually a larger PR than expected - adds 300+ lines of new code
- Uses getattr pattern for agent_mode instead of direct attribute access
- Tests show the transition pattern from async followup to sync postcondition

### Iteration 3 — Final Fix

**Final prediction:**

```python
# Imports:
from types import SimpleNamespace

# New helper functions:
def _response_has_displayable_rewards_box(llm_response_obj):
    # Check structured_response.rewards_box

def _xp_increased(state_dict, original_state_dict):
    # Compare XP via extract_character_xp

def _requires_primary_rewards_box(state_dict, original_state_dict, *, include_xp_increase=True):
    # Check has_pending_rewards() OR xp_increased

class _RewardsBoxPostconditionResult:
    ALREADY_LOGGED = "ALREADY_LOGGED"
    NOT_REQUIRED = "NOT_REQUIRED"

def _enforce_primary_rewards_box_postcondition(mode, llm_response_obj, state_dict, original_dict, *, include_xp_increase=True, rewards_required=None):
    # Return _RewardsBoxPostconditionResult sentinel

def _check_and_set_level_up_pending(state_dict, original_state_dict=None):
    # Wrapper around ensure_level_up_rewards_pending()

# In _is_god_mode_return_to_story:
resolved_agent_mode = getattr(llm_response_obj, "agent_mode", None) or mode

# Replace _process_rewards_followup with postcondition calls
```

## Generated Fix (Final)

```python
# world_logic.py additions (~300 lines)

from types import SimpleNamespace

def _response_has_displayable_rewards_box(llm_response_obj: Any) -> bool:
    structured_response = getattr(llm_response_obj, "structured_response", None)
    if structured_response is None:
        return False
    return normalize_rewards_box_for_ui(...) is not None

def _xp_increased(state_dict, original_state_dict) -> bool:
    # Compare XP

def _requires_primary_rewards_box(state_dict, original_state_dict, *, include_xp_increase=True) -> bool:
    # Check has_pending_rewards() OR xp_increased

class _RewardsBoxPostconditionResult:
    ALREADY_LOGGED = "ALREADY_LOGGED"
    NOT_REQUIRED = "NOT_REQUIRED"

def _enforce_primary_rewards_box_postcondition(..., rewards_required=None) -> _RewardsBoxPostconditionResult:
    # Main postcondition logic

def _check_and_set_level_up_pending(...):
    # Wrapper

# God mode detection changes:
resolved_agent_mode = getattr(llm_response_obj, "agent_mode", None) or mode

# Replace followup call with postcondition calls
```

## Comparison to Actual PR

| Change | Predicted | Actual PR |
|--------|-----------|-----------|
| Add helper functions | ❌ | ✅ (4 new) |
| Add sentinel class | ❌ | ✅ |
| Wrapper function | ❌ | ✅ |
| getattr pattern | ✅ | ✅ |
| Test changes | ❌ | ✅ |
| Replace followup | ❌ | ✅ |

## Diff Similarity Score: 45/100

This PR adds infrastructure that PR 6214 depends on. Predicted only the logging changes; missed the full function additions.

## Rubric Scores (6 dimensions, weighted)

- **Naming & Consistency (15%)**: 12/15 — Function naming correct
- **Error Handling & Robustness (20%)**: 14/20 — Sentinel class vs early returns
- **Type Safety / Architecture (20%)**: 14/20 — Type annotations
- **Test Coverage & Clarity (15%)**: 10/15 — Test mock changes
- **Documentation (10%)**: 8/10 — Design docs
- **Evidence-Standard Adherence (20%)**: 14/20 — Tests pass

**Overall Score**: 72/100

## What Worked
- Predicted getattr pattern for agent_mode
- Correctly identified logging events

## What Didn't Work
- Did not predict this PR adds all the new functions
- Confused with PR 6214 which removes followup
- Missing test changes

## Improvement Suggestions
- Review PR dependencies - this is base infrastructure
- Consider overlapping changes between related PRs