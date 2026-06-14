---
title: "Repo runner label variable can silently break CI dispatch (PR #7548)"
type: source
tags: [ci, runners, feedback, pr-7548, jleechanorg]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_repo_runner_label_variable_silent_drift.md
bead: rev-z3881
---

## Summary
`SELF_HOSTED_RUNNER_LABELS` repo variable was set out-of-band via `gh api PATCH` to `["self-hosted-mikey","ARM64"]`, which excluded the 10 X64 Colima runners from Green Gate dispatch while the 6 OOMKilled mac Docker runners held the only matching labels. PR #7548 (merged 2026-06-14T00:28:46Z) made the workflow self-consistent and `wa-oss-runner-local` was successfully deleted at 00:21Z.

## Key Claims
- Repo-level Actions variables that influence job scheduling are **out-of-band config** (not in any PR, not in `git log`) and can silently drift to label sets that exclude the entire available runner pool.
- The workflow file's hardcoded fallback `vars.X || 'default'` is only consulted when the variable is unset — set variables silently win.
- Symptom signature: `gh pr view <N>` shows "queued" or "in_progress" for hours with `runner_id: null, runner_name: null`.
- `busy: true` is **sticky** on a self-hosted runner even after the job is cancelled — to delete, you must cancel the run, kill/bootout the listener, then wait for GH heartbeat timeout (~5 min) for the busy flag to clear.

## Key Quotes
> `wa-oss-runner-local` (host-level mac ARM64) was stuck in `SessionConflictException` for 6+ hours; the listener log shows "registration has been deleted from the server, please re-configure".

> The variable was set out-of-band: no PR, no commit, no `git log` evidence. `gh api .../actions/variables` is the only inspection path.

## Connections
- [[self-hosted-mikey label is routing, not environment]] — `self-hosted-mikey` is the routing label, but the surrounding `SELF_HOSTED_RUNNER_LABELS` variable can narrow what counts.
- [[GitHub org runner registration vs group access]] — Default runner group with visibility:all is the dispatch pool; variable drift breaks the label match.
- [[Colima migration COMPLETED (2026-06-13)]] — X64 Colima runners (10 online) were idle because of this drift.
- [[Green Gate Gate 8 deadlocked: mcp-smoke-tests.yml removed]] — separate but adjacent: workflow gaps in CI.
- [[Org runner pool 6→15 + .ci-retrigger audit (2026-06-13)]] — pool expansion is moot when the variable excludes the entire pool.
- [[PR #7548]] — fix PR (MERGED)
- [[wa-oss-runner-local]] — broken host-level runner that was deleted
- [[SELF_HOSTED_RUNNER_LABELS]] — repo variable that drifted

## Reusable pattern (5 steps)
1. **Query** the variable when GG dispatches stall: `gh api repos/<org>/<repo>/actions/variables/SELF_HOSTED_RUNNER_LABELS`
2. **Patch** out-of-band via `gh api -X PATCH .../variables/SELF_HOSTED_RUNNER_LABELS -f 'value=["self-hosted-mikey"]'` if drift
3. **Make the workflow self-consistent** via PR (defensive fallback that doesn't require the variable)
4. **Re-dispatch** stuck jobs via `gh api -X POST .../workflows/green-gate.yml/dispatches` with `inputs[pr_number]` and `inputs[head_sha]`
5. **Remove broken runners** by clearing `busy: true` (cancel → kill listener → launchctl bootout → wait heartbeat → DELETE)
