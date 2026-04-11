---
title: "PR #256: [agento] fix(lifecycle): startup race -- isAlive probe bypasses grace period"
type: source
tags: []
date: 2026-03-28
source_file: raw/prs-worldai_claw/pr-256.md
sources: []
last_updated: 2026-03-28
---

## Summary
The bd-85r startup grace period was added to protect sessions during agent CLI initialization, but the `isAlive()` runtime probe runs *before* the grace period check fires — so a false-negative from `isAlive` during agent init would kill a spawning session before `determineStatus` ever reached the `getActivityState` path.

## Metadata
- **PR**: #256
- **Merged**: 2026-03-28
- **Author**: jleechan2015
- **Stats**: +40/-10 in 3 files
- **Labels**: none

## Connections
