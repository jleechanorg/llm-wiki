---
title: "PR #53: feat(orch-qxw): DISPATCHING atomic state to prevent double-dispatch"
type: source
tags: []
date: 2026-03-05
source_file: raw/prs-worldai_claw/pr-53.md
sources: []
last_updated: 2026-03-05
---

## Summary
- Adds `TaskStatus.DISPATCHING` to `MCClient` StrEnum
- Updates `TaskPoller._dispatch_task()` to atomically claim a task via DISPATCHING before invoking the dispatch function
- If DISPATCHING update returns None/falsy (task already claimed), the task is skipped with a warning log

## Metadata
- **PR**: #53
- **Merged**: 2026-03-05
- **Author**: jleechan2015
- **Stats**: +236/-0 in 3 files
- **Labels**: none

## Connections
