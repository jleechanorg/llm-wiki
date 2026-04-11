---
title: "3-Stage OpenClaw Dev Pipeline"
type: source
tags: [openclaw, staging, pipeline, ci, git, worktree]
date: 2026-03-31
source_file: raw/STAGING_PIPELINE.md
---

## Summary
Three-stage automated safety pipeline for `~/.smartclaw/` (live OpenClaw gateway config): (1) staging branch + worktree, (2) auto-promote via canary checks, (3) CI gate on PRs. Prevents bad config edits from crashing the production gateway or dropping Slack messages.

## Key Claims
- **Stage 1**: Changes land on `staging` branch first (not `main`), with `~/.smartclaw-staging/` as a git worktree on branch `staging`
- **Stage 2**: `staging-promote.sh` runs 6-point canary against staging gateway (port 18790), only merges staging → main if all pass
- **Stage 3**: CI gate `.github/workflows/staging-canary-gate.yml` fires on every PR, runs 2/6 checks (config schema + SDK protocol version), blocks merge on failure
- Canary checks: Gateway health, config schema, native module ABI, Slack token validity, SDK protocol version, heartbeat latency (2/6 run in CI, 4/6 require local gateway)
- **orch-1ps.4** (git hooks for auto-restart) is P1 and not yet implemented — staging gateway requires manual restart after promotion
- Staging sync invariant: staging must never be behind main — verify with `git rev-list staging..main --count`

## Architecture
```
~/.smartclaw/ (PROD, port 18789, main branch)
    ↑ promote (staging-promote.sh)
~/.smartclaw-staging/ (STAGING, port 18790, staging branch)
    ↑ PR merges
.github/workflows/staging-canary-gate.yml (CI gate, 2/6 checks)
```

## Connections
- [[Smartclaw]] — target application: OpenClaw gateway config management
- [[HealthCheck]] — canary health endpoint verification
- [[GitHooks]] — post-merge hooks for auto-restart (orch-1ps.4, not yet implemented)
- [[CanaryTesting]] — 6-point staging canary before production promotion
