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

- [[InstallScriptIdempotency]] — install.sh must not corrupt .env with duplicate entries
- [[Launchd]] — launchd plist management for runner auto-restart