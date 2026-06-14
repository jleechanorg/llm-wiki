---
name: repo-runner-label-variable-can-silently-break-ci-dispatch
description: "SELF_HOSTED_RUNNER_LABELS repo variable was set out-of-band (gh api) to [\"self-hosted-mikey\",\"ARM64\"]; 10 X64 Colima runners were idle and 6 mac Docker runners were OOMKilled. PR"
metadata: 
  node_type: memory
  type: feedback
  bead: rev-z3881
  originSessionId: 85f321ae-5eaa-498c-b2fb-57383f2f2804
---

## Context

Green Gate dispatches for PRs #7278, #7382, #7473, #7524 sat in `queued` indefinitely. Investigation:

- Repo variable `SELF_HOSTED_RUNNER_LABELS = ["self-hosted-mikey","ARM64"]` (created `2026-06-13T20:44:29Z`, updated `21:40:18Z` by `jleechan2015` via `gh api PATCH .../actions/variables/SELF_HOSTED_RUNNER_LABELS`).
- 9 X64 Colima runners (label set: `self-hosted, Linux, self-hosted-mikey, X64`) **do not** carry `ARM64` → no label match → idle.
- 6 mac Docker runners (`org-runner-mac-1..6`) were OOMKilled + containerd metadata corruption → can't run jobs.
- The variable was set out-of-band: no PR, no commit, no `git log` evidence. `gh api .../actions/variables` is the only inspection path.
- `wa-oss-runner-local` (host-level mac ARM64) was stuck in `SessionConflictException` for 6+ hours; the listener log shows "registration has been deleted from the server, please re-configure".

## Symptom signature

- `gh pr view <N> --json statusCheckRollup` shows "queued" / "in_progress" for hours with `runner_id: null, runner_name: null`.
- `gh api .../actions/runners/9911` returns `status: online, busy: true` (or `offline, busy: true` after the listener dies) — busy is sticky after a job is cancelled.
- New dispatches after the variable fix **do** pick up runners, so any in-flight `queued` jobs that pre-date the fix will stay stuck and need a re-dispatch.

## Solution (reusable pattern)

1. **Query the variable first** when GG dispatches stall: `gh api repos/<org>/<repo>/actions/variables/SELF_HOSTED_RUNNER_LABELS` (or any custom var the workflow reads).
2. **Patch out-of-band via gh api** if drift is the cause: `gh api -X PATCH repos/<org>/<repo>/actions/variables/SELF_HOSTED_RUNNER_LABELS -f 'value=["self-hosted-mikey"]'`. This is a runtime fix, doesn't need a PR.
3. **Make the workflow self-consistent via PR**: change `green-gate.yml` line 35 fallback to a minimal label set so the file is correct even if the variable is unset or unset-by-mistake. PR #7548 is the canonical example.
4. **Re-dispatch stuck jobs** (cancelling an existing `queued` run does not auto-dispatch a new one): `gh api -X POST repos/<org>/<repo>/actions/workflows/green-gate.yml/dispatches -f "ref=<branch>" -f "inputs[pr_number]=<N>" -f "inputs[head_sha]=<sha>"`.
5. **Removing a broken runner**: cannot delete a runner via `gh api DELETE .../runners/<id>` while `busy: true`. Steps to clear it: (a) cancel the run, (b) `kill <listener_pid>` if process still around, (c) `launchctl bootout gui/$(id -u)/<service-label>` to release the registration, (d) wait for GH heartbeat timeout (~5 min) for the busy flag to clear, (e) re-issue the DELETE.

## Why this is feedback (not just project)

- The `SELF_HOSTED_RUNNER_LABELS` variable is **out-of-band config** — not committed, not in any PR, not visible in `git log` or `git diff origin/main`. Future drift can happen the same way and the same symptom will recur.
- The workflow file had a defensive default `["self-hosted","self-hosted-mikey"]` (no ARM64) — but `vars.X || 'default'` uses the var when set, so the variable override silently won.
- Going forward: any new repo-level Actions variable that influences job scheduling should be either (a) added to a tracking doc, or (b) replaced with a hardcoded workflow file value.

## Verification

- PR #7548 (HEAD `8afb5b9094`, merged `2026-06-14T00:28:46Z` by `jleechan2015`) made the workflow file self-consistent.
- After var patch + workflow merge: PR #7278 dispatch `27483284097` and PR #7382 dispatch `27483319025` both reached `in_progress` with runners (X64 Colima pool) within 1 minute.
- `wa-oss-runner-local` (id 9911) successfully deleted at 00:21Z after the busy flag cleared.

## Files

- `.github/workflows/green-gate.yml` line 35 — PR #7548 changed the hardcoded fallback to `["self-hosted-mikey"]` and added an explanatory comment.
- `~/Library/LaunchAgents/actions.runner.jleechanorg.wa-oss-runner-local.plist` — still on disk, **unloaded**; can be re-installed on reboot. To fully disable: `launchctl bootout` is already done; remove the plist file to prevent re-install.

## References

- PR #7548: https://github.com/jleechanorg/worldarchitect.ai/pull/7548 (MERGED)
- Commit: `fbe4c2f6e638d0f0a278a958c7767e6594d33d34` on `main`
- Related: `project_2026-06-13_green_gate_gate8_smoke_workflow_removed.md` (Gate 8 deadlock)
- Related: `feedback_2026-06-13_self_hosted_mikey_label_means_routing_not_environment.md` (label semantics)
- Related: `project_2026-06-13_org_runner_pool_expansion_and_sentinel_audit.md` (pool 6→15)
- Related: `project_2026-06-13_colima_migration_completed.md` (X64 Colima setup)
