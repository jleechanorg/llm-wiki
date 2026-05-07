---
name: OSS runner naming fix — all 6 ARM64 runners online, PR 6791 merged
description: RUNNER_NAME_PREFIX must mirror RUNNER_CONTAINER_NAME; install.sh idempotent .env writes
type: feedback
bead: none
---

All 6 org-scoped ARM64 runners (`org-runner-mac-1` through `org-runner-mac-6`) are online on `jleechanorg`. PR #6791 merged — `fix(org-runner): align RUNNER_NAME_PREFIX with RUNNER_CONTAINER_NAME`.

**Root cause**: `RUNNER_NAME_PREFIX` defaulted to `org-runner` while `RUNNER_CONTAINER_NAME` was set to `org-runner-mac` in `.env`. Docker container names (`org-runner-mac-N`) didn't match the GitHub runner deregister filter (`startswith(env.GH_RUNNER_PREFIX)`), so offline cleanup skipped them. GitHub runner names came from `RUNNER_NAME` env var which was `org-runner-N`, causing registration confusion.

**Fix**: `RUNNER_NAME_PREFIX="${RUNNER_NAME_PREFIX:-${RUNNER_CONTAINER_NAME}}"` in `start-runner.sh` line 84 — ensures the deregister filter always matches the Docker container name prefix.

**install.sh idempotency fix**: `_ensure_env()` function uses `grep -q` + `sed -i ''` to update `.env` entries in-place rather than appending, so re-running `install.sh` does not duplicate entries. Bootout errors now report `WARN` instead of being silenced with `|| true`.

**Stray runner removed**: `org-runner-mac-fec58f214615` (orphaned legacy runner with `org-scope` label) was deregistered via `gh api orgs/jleechanorg/actions/runners/76066 --method DELETE`.

**Files**: `self-hosted-oss/start-runner.sh`, `self-hosted-oss/install.sh`

**Verification**:
```bash
gh api orgs/jleechanorg/actions/runners --jq '.runners[] | {name, status}'
# all 6 org-runner-mac-* → online
```

**Why**: `myoung34/github-runner` uses `RUNNER_NAME` for GitHub registration and Docker `--name` for container name — these two are independent. When `.env` sets `RUNNER_CONTAINER_NAME` but not `RUNNER_NAME_PREFIX`, they diverge, breaking deregistration and container cleanup.

**How to apply**: When adding a new `RUNNER_CONTAINER_NAME` value to `.env`, also set `RUNNER_NAME_PREFIX` to the same value.