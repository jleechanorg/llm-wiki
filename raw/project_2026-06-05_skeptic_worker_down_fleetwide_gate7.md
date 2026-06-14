---
name: skeptic-verdict-worker-down-fleet-wide-gate-7-unreachable-pr
description: "Gate 7 needs an external AO worker (not skeptic-cron) to post VERDICT; it was down across all 11 open PRs on 2026-06-05, parking PR"
metadata: 
  node_type: memory
  type: project
  originSessionId: 15c06163-394b-4d82-97e5-d551f8fa1350
---

PR [#7262](https://github.com/jleechanorg/worldarchitect.ai/pull/7262) ("single-home modal flags in nested `custom_campaign_state`", branch `fix/stale-top-level-levelup-pending`) was *believed* **6/7 green** and **parked by owner** on Gate 7. Passing: CI per statusCheckRollup; mergeable=MERGEABLE; CodeRabbit APPROVED; Bugbot clean; 0 unresolved comment threads; Evidence Gate + real-LLM e2e 2/2 PASS (twin campaign, original `MfM8TFz73DUeFFmt0mDb` never touched). reviewDecision="" (no blocking required reviewer).

**CORRECTION (2026-06-05, later):** the "6/7 green" claim was WRONG at parked head `5aecd9fd`. External review found 3 `TestXPLevelValidation` assertions in `mvp_site/tests/test_game_state.py` (lines 2640/2669/3182) still read TOP-LEVEL `result["level_up_pending"]` while the one-flag refactor (commit `cac39e273c`) moved `validate_xp_level`'s write to nested `custom_campaign_state.level_up_pending` (game_state_mixins.py:1499/1505). The level-up + scalar-mismatch tests FAILED deterministically (pure logic, 0.57s). **TEST-ONLY** — no production caller reads `level_up_pending` from the validate_xp_level result dict (game_state.py:2215, world_logic.py:4436 read only corrected/computed_level/clamped_*/epic_level/expected_/provided_level). Fixed by updating the 3 assertions to the nested canonical home (NOT restoring top-level). New head **`f20d810d350d724d04bd9d2f4478f011a331c889`**; full file 216 passed. CR re-approval + a new skeptic trigger now needed (head changed). **CI false-green caveat:** Self-Hosted MVP Shards reported `test_game_state.py` ✓ at `5aecd9fd` despite the deterministic failure → bead **rev-6o3nb** (P1) tracks the shard coverage/checkout gap.

**Gate 7 mechanism (KEY):** The skeptic pipeline is TWO stages, and `skeptic-cron.yml` is only the first.
1. `skeptic-cron.yml` — `workflow_dispatch` ONLY (no `schedule:`), `auto_merge="false"`, calls reusable `jleechanorg/agent-orchestrator/.github/workflows/skeptic-cron-reusable.yml@main`. Steps: list PRs → **Post skeptic triggers for 6-green eligible PRs** → Check 7-green and merge. It only POSTS a `SKEPTIC_CRON_TRIGGER` comment (markers `skeptic-request-id-cron-<runid>-1-<pr>-<sha>`, `skeptic-head-sha-<full>`, `skeptic-cron-trigger-<full>`). It does NOT post the verdict.
2. **External agent-orchestrator skeptic worker** consumes that trigger and posts the actual `VERDICT:` comment, authored by `jleechan2015`, matching the exact HEAD_SHA. THIS is what Gate 7 needs.
3. `green-gate.yml` "Poll for VERDICT" step polls 30× (~1/min, ~30 min) for a VERDICT on the exact HEAD_SHA by `SKEPTIC_BOT_AUTHOR=jleechan2015`, else **fails closed** (exit 1).

**2026-06-05 finding:** the consumer worker was **down fleet-wide** — scanned all 11 open PRs (7271,7268,7264,7263,7259,7255,7253,7252,7247,7242,7241) + #7262 = **zero VERDICT comments anywhere**. No open PR could reach 7-green. Trigger for `5aecd9fd` was enqueued (skeptic-cron run 27006863859, 09:25:47Z) and remains unconsumed; it will drain when the worker comes up. The fix is infra (bring up the AO skeptic lifecycle/launchd worker, respecting AO spawn-safety: hard cap 20, max_spawn 8, batch ≤5) — NOT `gh`-controllable, NOT a #7262 code defect.

The `/green` skill still references a stale `skeptic-gate.yml` (no longer exists); the live workflow is `skeptic-cron.yml`.

Governing bead `rev-x7pug` (code work) is CLOSED/completed. New tracking bead `rev-97y3l` (P1) covers the outage. Merge remains human-gated (`MERGE APPROVED`). See [[project_2026-06-04_mfm8tfz_stale_levelup_openrouter_verdict]] for the underlying stale-flag root cause that #7262 fixes.

**Why:** future sessions will see "Green Gate failed" on a code-complete PR and waste time hunting a code defect; the real cause is the out-of-band verdict worker, and `skeptic-cron` dispatch alone never produces a verdict.

**How to apply:** when a PR is 6/7 with Gate 7 the only red and "Poll for VERDICT … failing closed" in the Green Gate log, check `gh pr view <PR> --json comments` for ANY VERDICT by jleechan2015; if zero across multiple PRs, the worker is down fleet-wide — escalate to infra, don't debug the PR.
