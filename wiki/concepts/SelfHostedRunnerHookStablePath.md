# Self-Hosted Runner: Pre-Job Hook + Stable-Path Install Convention

## Problem

Ephemeral self-hosted runner containers (both mac ARM64 via `self-hosted-oss` and Linux x64 via `self-hosted-colima`) accumulate disk from named Docker volumes (`runner-workdir-N:/_work`) and pip caches between cycles. This causes ENOSPC failures at the `scripts/ci/runner_preflight.sh` gate (threshold: 1 GB).

## Solution: Pre-Job Hook

The `ACTIONS_RUNNER_HOOK_JOB_STARTED` environment variable points to a script that fires inside the container BEFORE any workflow steps. This is the load-bearing fix — it runs on every job, before preflight checks. Periodic cleanup (launchd/cron) is supplemental.

**Hook behavior:**
1. Check available disk on `/_work`
2. If < 5 GB: delete `/root/.cache/pip`, `/_work/worldarchitect.ai`, `/_work/_temp`
3. Log before/after disk stats

## Stable-Path Install Convention (MANDATORY)

**Never** bind-mount the hook from a repo-relative path (`./scripts/pre-job-hook.sh`). The bind-mount path is resolved at container start time — if the branch changes or the worktree moves, the mount breaks silently.

**Correct pattern:**
```
repo source:         self-hosted-{fleet}/scripts/pre-job-hook.sh
install.sh installs: ~/.local/share/worldarchitect-{fleet}-runners/pre-job-hook.sh
compose bind-mount:  ${HOME}/.local/share/worldarchitect-{fleet}-runners/pre-job-hook.sh:/usr/local/bin/pre-job-hook.sh:ro
```

- **Mac runners** (`self-hosted-oss`): installed via `RUNTIME_SCRIPTS` array in `install.sh` → `~/.local/share/worldarchitect-runners/`
- **Linux colima runners** (`self-hosted-colima`): install step in `install.sh` → `~/.local/share/worldarchitect-colima-runners/`

## Merged PRs

| PR | Fleet | Date |
|----|-------|------|
| [#7770](https://github.com/jleechanorg/worldarchitect.ai/pull/7770) | Mac ARM64 (`self-hosted-oss`) | 2026-06-22 |
| [#7831](https://github.com/jleechanorg/worldarchitect.ai/pull/7831) | Linux x64 colima (`self-hosted-colima`) | 2026-06-23 |

## Related

- `~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-22_self_hosted_runner_disk_fill.md`
- `~/roadmap/learnings-2026-06.md` (2026-06-23 entry)
- Bead: `rev-c88ul` (closed)
