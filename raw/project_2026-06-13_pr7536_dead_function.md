# PR #7536 unmergeable: tested function removed by PR #7480

**Date:** 2026-06-13
**Status:** BLOCKED

## Finding

PR #7536 (`test(bq): cover Gemini usage_metadata path in _bq_log_spell_repair_interaction`) is **unmergeable as-is**.

The test it adds calls `world_logic._bq_log_spell_repair_interaction(...)` directly. That function:
- Existed in `b26a5eb1e9` (PR #7536's actual base) — 2 refs
- Was **removed** by `ed5a97b2c7` (PR #7480 "Remove deliberate second LLM calls") — landed on main
- Is **NOT present** on `origin/main` — 0 refs
- Is **NOT present** on any levelup v2 train branch:
  - `feat/levelup-v2-prompt-full-sheet` (PR-A) — 0
  - `feat/levelup-v2-routing` (PR-2) — 0
  - `feat/levelup-v2-rewards-engine` (PR-3) — 0
  - `feat/levelup-v2-godmode-fold` (PR-6) — 0 (lane revert undid it)

**The function is dead code in the entire train.**

## Rebase impact

`git rebase origin/main` (per the user instruction) RESOLVES the conflict in `mvp_site/tests/test_world_logic.py` (single conflict block, HEAD empty, theirs has the new test), but the resulting tree has main's `world_logic.py` which **lacks the function**. Running the test post-rebase:

```
AttributeError: module 'mvp_site.world_logic' has no attribute 'bq_logging'
```

Test cannot pass. PR is unmergeable.

## Other blockers

1. **CodeRabbit rate-limited** (no APPROVED review possible in 3h41m)
2. **Cursor Bugbot usage-limited** (skipped, no review)
3. **Org runner pool saturated** — presubmit, design-doc-gate, levelup-tests all queued for other PRs, none have started for `0365a7d`
4. **PR body references bead `rev-xe04r`** — that bead **does not exist** in `br list` (50 beads checked)
5. **PR-A (parent train) is OPEN with `baseRefOid: 5dc19a2706`** — PR #7536's recorded base is post-`ed5a97b2c7`, but the branch's actual merge base is `b26a5eb1e9` (pre-removal). Confusing provenance.

## Local test verification (on PR's own base)

```
$ TESTING_AUTH_BYPASS=true ./vpython -m pytest mvp_site/tests/test_world_logic.py -k "bq_log_spell_repair" -v
test_bq_log_spell_repair_gemini_usage_metadata_token_attribution PASSED [ 50%]
test_bq_log_spell_repair_openai_compat_token_attribution PASSED [100%]
2 passed
```

Tests pass on the PR's own branch. But that branch is in a state the rest of the world has moved past.

## Required fixes to make PR #7536 mergeable

One of:
- A. **Add `_bq_log_spell_repair_interaction` back to `world_logic.py` in this PR** — but PR body explicitly says "no production change" and the OpenAI-shape fallback was already supposed to be in main
- B. **Re-author the test** to target a function that exists on main (e.g. the new bq-logging path in `b8e7aa3fd9` lane revert — but that branch is also stuck)
- C. **Re-target base to PR-6's branch** — but PR-6 is also CONFLICTING and OPEN
- D. **Close the PR as superseded** — the function it tests no longer exists

## Recommendation for the user

Surface this gap and ask which path to take. Per the user instruction "If a fix exceeds 30 min on gate work, surface the gap and stop" — this is the gap.

**Local head:** `0365a7dd86ba9061ba7d1380dee781212f8b35c9` (on PR's own base, tests pass)
**Origin head:** `0365a7dd86ba9061ba7d1380dee781212f8b35c9` (matches local)
**7-green status:** NOT GREEN. 4 gates failing: (1) mergeable=dirty, (2) CodeRabbit=skipped/rate-limited, (3) Cursor Bugbot=skipped/usage-limited, (4) no unit-test CI run (queued, runner pool saturated).
