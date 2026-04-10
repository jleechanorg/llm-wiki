---
title: "Staging Worktree"
type: entity
tags: [openclaw, git, worktree, staging, pipeline]
sources: [staging-pipeline]
last_updated: 2026-04-09
---

## Summary
Git worktree at `~/.smartclaw-staging/` on the `staging` branch, used as the staging environment for the OpenClaw 3-stage dev pipeline. Separate from prod (`~/.smartclaw/` on `main`, port 18789), runs on port 18790.

## Details
- **Location**: `~/.smartclaw-staging/`
- **Branch**: `staging`
- **Port**: 18790 (vs prod port 18789)
- **Purpose**: Isolated staging gateway for pre-production config validation

## Sync Invariant
Staging must never be behind main. Verify with:
```bash
git rev-list staging..main --count
```
If non-zero, fast-forward staging: `git checkout staging && git merge --ff-only origin/main && git push origin staging`

## Connections
- [[Smartclaw]] — parent project
- [[StagingPipeline]] — 3-stage pipeline using this worktree
- [[GitWorktreePruning]] — worktree lifecycle management
