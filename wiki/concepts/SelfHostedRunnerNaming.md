---
title: SelfHostedRunnerNaming
type: concept
tags: [self-hosted-runner, docker, github-actions, runner-naming]
date: 2026-05-04
---

## Definition

In `myoung34/github-runner` Docker containers, **Docker container name** (`--name` flag) and **GitHub runner name** (`RUNNER_NAME` env var) are independent. If they diverge, offline deregistration and container cleanup both break.

## Rule

`RUNNER_NAME_PREFIX` (used by the deregister filter) must equal `RUNNER_CONTAINER_NAME`.

In `start-runner.sh`:
```bash
RUNNER_NAME_PREFIX="${RUNNER_NAME_PREFIX:-${RUNNER_CONTAINER_NAME}}"
```

When setting `RUNNER_CONTAINER_NAME` in `.env`, always also set `RUNNER_NAME_PREFIX` to the same value.

## Verification

```bash
gh api orgs/jleechanorg/actions/runners --jq '.runners[] | {name, status}'
```

## Connected Concepts

- [InstallScriptIdempotency](InstallScriptIdempotency.md) — install.sh must not corrupt .env with duplicate entries
- [Launchd](Launchd.md) — launchd plist management for runner auto-restart

## Stable install path (2026-06-09)

Self-hosted runner scripts live in two places:

1. The main worktree: `/Users/jleechan/projects/worldarchitect.ai/self-hosted-oss/`
2. The stable install: `~/.local/share/worldarchitect-runners/` — this is what `launchd` actually runs.

**After editing any of `defaults.sh`, `launchd-start.sh`, `heal-runners.sh`, `start-runner.sh` in the worktree, `cp` to the stable install** or the launchd agent will continue running the OLD copy. If you forget this, `heal-runners.sh` exits with `exit=127` and the supervisor logs the error every 5 min, with no indication that the new code never ran.

```bash
cp self-hosted-oss/{defaults,launchd-start,heal-runners,start-runner}.sh \
   ~/.local/share/worldarchitect-runners/
```

See: [feedback-2026-06-09-runner-supervisor-and-ops](../sources/feedback-2026-06-09-runner-supervisor-and-ops.md) (PR #7271, bead rev-5ysuv)