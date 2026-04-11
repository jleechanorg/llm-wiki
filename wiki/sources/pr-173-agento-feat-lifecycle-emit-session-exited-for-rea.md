---
title: "PR #173: [agento] feat(lifecycle): emit session.exited for reaped co-workers (orch-s66)"
type: source
tags: []
date: 2026-03-25
source_file: raw/prs-worldai_claw/pr-173.md
sources: []
last_updated: 2026-03-25
---

## Summary
Reaped co-worker sessions (post-merge sweep) were not emitting `session.exited` notifications. When `reapPostMergeCoWorkers()` killed idle co-workers after a PR merge, the Slack thread terminal updates were silently skipped — only the primary merged session received the notification.

This caused stale-worker lifecycle noise: Slack would show merged workers as "still running" even after cleanup.

## Metadata
- **PR**: #173
- **Merged**: 2026-03-25
- **Author**: jleechan2015
- **Stats**: +271/-4 in 3 files
- **Labels**: none

## Connections
