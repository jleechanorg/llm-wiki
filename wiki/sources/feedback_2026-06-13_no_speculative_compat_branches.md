---
title: "No Speculative Compatibility Branches in Agent Routing"
type: source
tags: [feedback, agent-routing, code-quality, zfc, worldarchitect, pr-7516]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_no_speculative_compat_branches.md
---

## Summary
Never add `isinstance(game_state, dict)`-style compatibility branches to agent routing methods without (a) a test that exercises the dict path AND (b) a production call site that actually passes a dict. In PR #7516, commit `31b1623f7f` added such a branch to `CampaignUpgradeAgent.matches_game_state()` and imported `campaign_divine` at module level, justified as "routing compatibility for E2E and API tests" — but both production call sites always pass a `GameState` object, no test exercised the dict path, and `campaign_divine` was not previously imported. The branch was speculative and was reverted in commit `1fe0159c4e`.

## Key Claims
- Speculative compatibility code written "for future tests" accumulates as dead code and can mask real issues when CI runs different routing paths
- Before adding any `isinstance(game_state, dict)` branch or new import to an agent method: find all call sites with `grep -rn "ClassName.matches_game_state"` and verify at least one passes a dict
- The branch was added speculatively "just in case" during a commit titled "Fix: Resolve unit test failures" — the actual test failures were in `rewards_engine.py`, not `agents.py`
- Revert commit: `1fe0159c4e` on `fix/rev-toavb-orphaned-ccs-flag-repro`

## Key Quotes
> "**Do not add compatibility branches (`isinstance(game_state, dict)`) to agent routing methods without (a) a test that exercises the dict path AND (b) a production call site that actually passes a dict.**"

> "Both production call sites (`agents.py:3393`, `agents.py:3815`) always pass a `GameState` object; `campaign_divine` was not previously imported by `agents.py` on main; no test exercised the dict path; no E2E test was ever written that required it."

## Connections
- [[ZeroFrameworkCognition]] — broader principle of not adding speculative logic
- [[CampaignUpgradeAgent]] — the agent where the speculative branch was added
- [[PR_7516]] — the PR that added the speculative branch and was reverted
- [[agents.py]] — file containing the routing methods
- [[campaign_divine]] — the module imported speculatively
- [[GameState]] — the object type that production call sites actually pass
- [[rev-toavb-orphaned-ccs-flag-repro]] — branch where the revert commit lives
