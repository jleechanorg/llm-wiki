---
title: "PR #191: [agento] fix(web): show EmptyState when all sessions are done"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-191.md
sources: []
last_updated: 2026-03-26
---

## Summary
Cherry-pick intent from ComposioHQ upstream commit `0fe63405`: show an EmptyState message when all sessions are in "done" status, instead of rendering a blank kanban board.

Our fork's `Dashboard.tsx` already had the core `hasKanbanSessions` logic (`KANBAN_LEVELS.some(...)`) — the missing piece was the `EmptyState` rendering call.

## Metadata
- **PR**: #191
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +136/-0 in 4 files
- **Labels**: none

## Connections
