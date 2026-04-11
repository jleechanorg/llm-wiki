---
title: "PR #82: fix(core): filter killed/merged sessions after repair in loadActiveSessionRecords"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-82.md
sources: []
last_updated: 2026-03-23
---

## Summary
`loadActiveSessionRecords()` in `session-manager.ts` was returning all session records including those with terminal statuses (killed, merged), causing stale data dir accumulation in the active session list.

## Metadata
- **PR**: #82
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +113/-7 in 3 files
- **Labels**: none

## Connections
