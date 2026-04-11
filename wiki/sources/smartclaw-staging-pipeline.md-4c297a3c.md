---
title: "Smartclaw Staging Pipeline"
type: source
tags: ["openclaw", "ci-cd", "staging", "deployment", "git-worktree"]
date: 2026-04-07
source_file: "raw/llm_wiki-raw-staging_pipeline.md"
sources: []
last_updated: 2026-04-07
---

## Summary
A 3-stage development pipeline for OpenClaw that adds automated safety gates between configuration changes and production. The pipeline consists of: (1) staging branch where changes land first, (2) automated canary health checks against staging gateway, and (3) CI gate with portable checks running on every PR to block merges on failure.

## Key Claims
- **Stage 1**: Staging branch + worktree ensures changes never go directly to production
- **Stage 2**: Auto-promote script runs 6/6 canary checks before merging staging to main
- **Stage 3**: CI gate runs 2/6 portable checks on every PR targeting staging branch
- **Fail-closed**: Any canary failure prevents promotion entirely

## Architecture Components

### Staging Branch & Worktree
- Long-lived `staging` branch in `jleechanorg/smartclaw`
- `~/.smartclaw-staging/` is a git worktree checked out to staging branch (port 18790)
- `~/.smartclaw/` is production worktree on main branch (port 18789)
- Worktree over plain directory: changes can be committed back to staging branch

### Auto-Promote Script (`staging-promote.sh`)
1. Verifies staging is a valid worktree on staging branch
2. Runs `staging-canary.sh --port 18790` against staging gateway
3. If 6/6 checks pass: merges staging → main and pushes to origin
4. If any check fails: exits with error, no promotion

### CI Gate (`.github/workflows/staging-canary-gate.yml`)
- Fires on every PR targeting staging branch
- Runs 2/6 portable checks as a gate before merge

## Key Guards
- Refuses to promote if staging is not a worktree
- Refuses to promote if staging worktree is not on staging branch
- Aborts any in-progress merge before starting (idempotent)
- Stashes uncommitted local changes before merging

## Staging Sync Invariant
After any staging branch creation or reset, verify staging is at or ahead of main:
```bash
git rev-list staging..main --count
```
If non-zero, staging is behind main and must be fast-forwarded.

## Connections
- [[SmartclawOrchestrationSystemDesign]] — orchestration design this pipeline supports
- [[SmartclawHarnessEngineering]] — 4-layer harness layer above this pipeline
- [[SmartclawPostmortem20260319]] — past incident that motivated staging discipline
- [[GitHub]] — hosts the PR workflow and CI gates