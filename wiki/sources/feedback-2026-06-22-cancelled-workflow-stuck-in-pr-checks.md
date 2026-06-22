---
title: "Cancelled PR-event workflow run stuck as 'fail' in gh pr checks — empty-commit re-trigger"
type: source
tags: [ci, github-actions, gh-cli, workflow-race, worldarchitect, pr-7789, statuscheckrollup, green-gate]
date: 2026-06-22
source_file: ~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-22_cancelled_workflow_run_stuck_in_pr_checks.md
---

## Summary

While driving PR #7789 (jleechanorg/worldarchitect.ai — Mobile Auth Same-Origin Regression CI test, merge commit `8b6456a774`) to 7-green, `gh pr checks` showed **Mobile Auth Same-Origin Regression: fail** with a `conclusion=cancelled` PR-event run, even though a `workflow_dispatch` run for the same check name completed successfully on the same head SHA. `mergeStateStatus: UNSTABLE` blocked merge despite `mergeable: MERGEABLE` and `reviewDecision: APPROVED`. Fix: push an empty commit to re-fire the `pull_request` event; the new PR-event success run overwrites the cancelled entry and `mergeStateStatus` flips to `CLEAN`.

## Key Claims

- `gh pr checks` prefers the **PR-event run** for each check name when the workflow has a `pull_request:` trigger — `workflow_dispatch` runs do NOT populate the PR's required `statusCheckRollup` even when they target the same head SHA.
- Cancelling a `pull_request`-event run labels it `fail` (not `cancelled`) in `gh pr checks` output. The successful `workflow_dispatch` run is invisible to PR checks.
- `gh run rerun --failed` does not re-run `cancelled` runs; the recovery is a fresh push.
- Empty-commit push is safe in this context: it does NOT invalidate CodeRabbit's existing APPROVED review (CR's re-review on a no-diff head typically produces a "no changes" pass-through).
- Distinct from the Bugbot-poll-timeout FAILURE case (`project_2026-06-19_pr_monitor_stuck_statuscheckrollup.md`): that one is a stuck `failure` conclusion in `statusCheckRollup`; this one is `cancelled` at run level + missing PR-event successor.

## Key Quotes

> A successful `workflow_dispatch` run for the same check name did NOT appear in `gh pr checks` at all; the cancelled PR-event run was the only entry shown, and GitHub labels cancelled runs as `fail` for PR purposes.

## Triage pattern (reusable)

1. Detect: `gh pr checks <PR>` shows a check name with `fail` whose run URL matches `gh run view <ID> --json conclusion` returning `cancelled`.
2. NEVER dispatch a `gh workflow run` for the same workflow while a `pull_request`-event run is still in flight on the same head — the race guarantees whichever finishes first becomes the PR check, and cancellation locks it.
3. Recovery: `git commit --allow-empty -m "ci: re-trigger <workflow>" && git push origin <branch>` — the push fires the `pull_request` event and the new success run overwrites the cancelled entry.
4. Verify with `gh pr checks <PR>` (the check name should flip to `pass`) and `gh pr view <PR> --json mergeStateStatus` (`UNSTABLE` → `CLEAN`).

## Connections

- [[PR7789]] — the PR driven to green
- [[WorldArchitectAI]] — host repo
- [[SelfHostedRunnerInfraFlakeVsRealFailure]] — parent concept (cancel-rerun family)
- [[GreenGateWorkflow]] — uses the same `pull_request:` PR-event pattern
- [[feedback-2026-06-20-gh-pr-checks-cancelled-shows-fail]] — sibling lesson (cancelled at job level, not run level)
- [[feedback-2026-06-19-pr-monitor-stuck-statuscheckrollup]] — sibling lesson (Bugbot-timeout stuck FAILURE)
- [[feedback-2026-06-22-green-gate-workflow-dispatch-ref-pitfall]] — same root cause family (workflow_dispatch can't satisfy PR-required status)