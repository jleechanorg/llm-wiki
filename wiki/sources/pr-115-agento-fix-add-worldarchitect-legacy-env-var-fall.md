---
title: "PR #115: [agento] fix: add WORLDARCHITECT_ legacy env var fallback for worldSchedulerEnabled (worldai_claw-371)"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-worldai_claw/pr-115.md
sources: []
last_updated: 2026-03-27
---

## Summary
`worldSchedulerEnabled()` in `server.ts` and `schedulingEnabled` in `faction_store.ts` only checked `WORLDCLAW_*` env vars, ignoring the legacy `WORLDARCHITECT_*` names.

## Metadata
- **PR**: #115
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +689/-876 in 8 files
- **Labels**: none

## Connections
