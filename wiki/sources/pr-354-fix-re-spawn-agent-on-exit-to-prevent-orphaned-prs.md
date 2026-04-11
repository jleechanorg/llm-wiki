---
title: "PR #354: fix: re-spawn agent on exit to prevent orphaned PRs"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-354.md
sources: []
last_updated: 2026-03-21
---

## Summary
When an agent session ends mid-flight (timeout, crash, or early exit), the PR is left orphaned — no active session, no respawn, no forward progress. The `agent-exited` reaction was `action: notify` only, so the orchestrator just sent a notification and moved on.

This is the primary blocker for full autonomy: PRs with CI failures, CR CHANGES_REQUESTED, or unresolved Bugbot findings would sit forever without a human manually re-triggering an agent.

## Metadata
- **PR**: #354
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +2/-1 in 1 files
- **Labels**: none

## Connections
