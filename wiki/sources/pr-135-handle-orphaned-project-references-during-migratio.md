---
title: "PR #135: Handle orphaned project references during migrations"
type: source
tags: [codex]
date: 2025-12-18
source_file: raw/prs-/pr-135.md
sources: []
last_updated: 2025-12-18
---

## Summary
- Clean orphaned project references before recreating the agents and messages tables so new foreign key enforcement does not fail
- Log and normalize orphaned project_ids to NULL while raising explicit errors for orphaned sender references during migration
- Centralize a module logger for reuse in migration helpers

## Metadata
- **PR**: #135
- **Merged**: 2025-12-18
- **Author**: jleechan2015
- **Stats**: +70/-0 in 1 files
- **Labels**: codex

## Connections
