---
name: no-speculative-compat-branches
description: Never add dict-shaped compat branches to agent routing methods without a test requiring it and a real call site that passes a dict
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: cc529d80-6799-46a8-9cd4-e0efc53d964b
---

## Rule

**Do not add compatibility branches (`isinstance(game_state, dict)`) to agent routing methods
without (a) a test that exercises the dict path AND (b) a production call site that actually
passes a dict.**

## Why

In PR #7516, commit `31b1623f7f` added a `if isinstance(game_state, dict):` branch to
`CampaignUpgradeAgent.matches_game_state()` and imported `campaign_divine` at module level,
justified in the PR description as "routing compatibility for E2E and API tests." However:

- Both production call sites (`agents.py:3393`, `agents.py:3815`) always pass a `GameState` object
- `campaign_divine` was not previously imported by `agents.py` on main
- No test exercised the dict path
- No E2E test was ever written that required it

The branch was added speculatively "just in case" during a commit titled "Fix: Resolve unit test
failures" — the actual test failures were in `rewards_engine.py`, not `agents.py`.

**Revert commit**: `1fe0159c4e` on `fix/rev-toavb-orphaned-ccs-flag-repro`

## How to Apply

Before adding any `isinstance(game_state, dict)` branch or new import to an agent method:
1. Find all call sites: `grep -rn "ClassName.matches_game_state"` — verify at least one passes a dict
2. Find or write the test that exercises the dict path
3. If neither exists, do not add the branch

Speculative compatibility code written "for future tests" accumulates as dead code and can mask
real issues when CI runs different routing paths.
