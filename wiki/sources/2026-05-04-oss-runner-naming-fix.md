---
title: "OSS Runner Naming Fix — PR #6791 Merged"
type: source
tags: [self-hosted-runner, org-runner, docker, github-actions, launchd, install-sh]
date: 2026-05-04
source_file: https://github.com/jleechanorg/worldarchitect.ai/pull/6791
---

## Summary

All 6 org-scoped ARM64 runners (`org-runner-mac-1` through `org-runner-mac-6`) are online on `jleechanorg`. PR #6791 fixed a naming mismatch between Docker container names and GitHub runner deregistration filters, and made `install.sh` idempotent for `.env` writes.

## Root Cause

`RUNNER_NAME_PREFIX` defaulted to `org-runner` while `RUNNER_CONTAINER_NAME` was set to `org-runner-mac` in `.env`. Docker container names (`org-runner-mac-N`) didn't match the GitHub runner deregister filter (`startswith(env.GH_RUNNER_PREFIX)`), so offline cleanup skipped them. The `myoung34/github-runner` container uses `RUNNER_NAME` for GitHub registration and Docker `--name` for container name — these two are independent.

## Fix

- `start-runner.sh` line 84: `RUNNER_NAME_PREFIX="${RUNNER_NAME_PREFIX:-${RUNNER_CONTAINER_NAME}}"` — ensures deregister filter always matches Docker container name prefix
- `install.sh` `_ensure_env()` function uses `grep -q` + `sed -i ''` to update `.env` entries in-place rather than appending on every run
- Bootout errors now report `WARN` instead of being silently suppressed with `|| true`

## Stray Runner Removed

`org-runner-mac-fec58f214615` (orphaned legacy runner with `org-scope` label) was deregistered via `gh api orgs/jleechanorg/actions/runners/76066 --method DELETE`.

## Verification

```bash
gh api orgs/jleechanorg/actions/runners --jq '.runners[] | {name, status}'
# all 6 org-runner-mac-* → online
```

## Connections

- [[SelfHostedRunnerNaming]] — core concept: RUNNER_NAME_PREFIX must match RUNNER_CONTAINER_NAME
- [[InstallScriptIdempotency]] — install.sh must not append duplicate .env entries on re-run