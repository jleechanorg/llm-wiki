---
title: "Staging Branch"
type: entity
tags: [openclaw, git, staging, pipeline]
sources: [staging-pipeline]
last_updated: 2026-04-09
---

## Summary
Long-lived git branch for the OpenClaw staging pipeline. All config changes land here first (not `main`), get CI-gated and canaried, then promoted to `main`.

## Details
- **Repo**: jleechanorg/smartclaw
- **Purpose**: Pre-production branch for `~/.smartclaw/` gateway config changes
- **Promotion**: `staging → main` only via `staging-promote.sh` after canary passes

## Sync Caveat
A bug in initial implementation created staging from a stale Saturday commit instead of current main. This caused 3 days of staging lag. After any staging branch creation or reset, must verify staging is at or ahead of main.

## Connections
- [[Smartclaw]] — parent project
- [[StagingWorktree]] — worktree checked out to this branch
- [[StagingPipeline]] — pipeline that uses this branch
