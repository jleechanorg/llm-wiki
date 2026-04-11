---
title: "PR #113: [agento] fix: invalidate SessionStore cache after faction_simulator SQL UPDATE (worldai_claw-493)"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-worldai_claw/pr-113.md
sources: []
last_updated: 2026-03-27
---

## Summary
The faction_simulator offline player-action code writes session state directly to SQLite via `db.prepare('UPDATE sessions ...')` but never updates the SessionStore in-memory cache.

## Metadata
- **PR**: #113
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +835/-870 in 8 files
- **Labels**: none

## Connections
