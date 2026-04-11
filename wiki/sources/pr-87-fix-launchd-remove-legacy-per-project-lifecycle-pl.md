---
title: "PR #87: fix(launchd): remove legacy per-project lifecycle plists, raise ThrottleInterval to 60s"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-87.md
sources: []
last_updated: 2026-03-21
---

## Summary
The /auton diagnostic revealed 10+ concurrent lifecycle-worker processes running simultaneously (expected ≤3, one per project). The root cause: legacy `com.agentorchestrator.lifecycle-*.plist` files in `~/Library/LaunchAgents/` use `KeepAlive: true`, which causes launchd to respawn every 30s unconditionally — even when a worker is already running for that project. Since the worker exits with code 0 when it detects a duplicate, launchd keeps retrying forever.

## Metadata
- **PR**: #87
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +12/-1 in 2 files
- **Labels**: none

## Connections
