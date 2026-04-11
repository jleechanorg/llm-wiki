---
title: "PR #234: [agento] fix: dedup send-to-agent reactions by PR head SHA (bd-1178)"
type: source
tags: []
date: 2026-03-28
source_file: raw/prs-worldai_claw/pr-234.md
sources: []
last_updated: 2026-03-28
---

## Summary
This PR fixes reaction dedup in `lifecycle-manager.ts` so the `send-to-agent` reaction doesn't fire repeatedly for unchanged PRs. Previously, `changes_requested` reactions would re-send to agents on every poll cycle even when nothing changed, burning agent context windows.

The fix introduces a `DedupHeadShaStore` (`dedup-head-sha-store.ts`) that persists the last-sent PR head SHA per session, independent of `ReactionTracker`. This survives status transitions that clear the tracker.

## Metadata
- **PR**: #234
- **Merged**: 2026-03-28
- **Author**: jleechan2015
- **Stats**: +665/-6 in 8 files
- **Labels**: none

## Connections
