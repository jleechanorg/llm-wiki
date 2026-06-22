---
name: cancelled-workflow-stuck-in-pr-checks
description: "Cancelled PR-event workflow runs show as 'fail' in `gh pr checks` and block mergeStateStatus from CLEAN; a successful workflow_dispatch run for the same check name does NOT supersede them. Fix: push an empty commit to re-trigger the pull_request event and produce a fresh success run that overwrites the entry."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 79a12801-6187-4144-846a-f1b1d003e14d
  bead: rev-2odam
---

PR #7789 reached `mergeable: MERGEABLE` + `reviewDecision: APPROVED` after the CR round-2 port-aware fix, but `mergeStateStatus: UNSTABLE` because `gh pr checks` listed **Mobile Auth Same-Origin Regression: fail** even though two runs existed: run `27978606006` (pull_request, **cancelled** because I dispatched a duplicate) and run `27978617125` (workflow_dispatch, **success**). The successful workflow_dispatch run did NOT appear in `gh pr checks` at all; the cancelled PR-event run was the only entry shown, and GitHub labels cancelled runs as `fail` for PR purposes.

**Why**: `gh pr checks` prefers the **PR-event run** for each check name when the workflow has a `pull_request:` trigger (the check is "required" for the PR). `workflow_dispatch` runs do NOT write to the PR's required statusCheckRollup even when they target the same head SHA — they're separate. Cancelling the PR-event run leaves a permanent "fail" entry that only a new PR-event run (from a push) can overwrite.

**How to apply**:
- NEVER dispatch a `workflow run` for the same workflow while a `pull_request` event run is still in flight on the same head — the race will leave whichever finishes first as the PR check, and cancellation makes the "fail" permanent.
- If you already cancelled a PR-event run, the recovery is: `git commit --allow-empty -m "ci: re-trigger <workflow>" && git push` — the push fires the `pull_request` event and the new success run supersedes the cancelled entry. Verified on PR #7789 (head `f9d3a6113b` after empty commit on `dff79097e3`).
- Detect: `gh pr checks <PR>` shows the same check name with `fail` and the run URL matches a `conclusion=cancelled` run (`gh run view <ID> --json conclusion`). The statusCheckRollup accumulates forever and won't auto-clear.
- Distinct from `project_2026-06-19_pr_monitor_stuck_statuscheckrollup.md` (that one is Bugbot-poll-timeout FAILURE in Green Gate; this one is any cancelled PR-event workflow).
- Related: `feedback_2026-06-22_green_gate_workflow_dispatch_ref_pitfall.md` — workflow_dispatch cannot populate PR-required statusCheckRollup, so for PR-required checks you must push.