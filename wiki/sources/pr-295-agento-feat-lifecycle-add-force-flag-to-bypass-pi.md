---
title: "PR #295: [agento] feat(lifecycle): add --force flag to bypass PID-file lock (orch-886k)"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-295.md
sources: []
last_updated: 2026-03-30
---

## Summary
The lifecycle-worker PID-file lock mechanism was already implemented (orch-886k) to prevent duplicate workers per project. However, there was no recovery path when the lock file is stale and an operator needs to force-restart the worker.

## Metadata
- **PR**: #295
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +280/-923 in 14 files
- **Labels**: none

## Connections
