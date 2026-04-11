---
title: "PR #3682: fix: Preserve mode for AI responses in story entries"
type: source
tags: []
date: 2026-01-16
source_file: raw/prs-worldarchitect-ai/pr-3682.md
sources: []
last_updated: 2026-01-16
---

## Summary
- Fix AI response mode not being preserved in story entries
- Think mode responses were appearing as regular "Scene #X" entries
- Root cause: `mode` was hardcoded to `None` for AI entries in `_persist_turn_to_firestore()`

## Metadata
- **PR**: #3682
- **Merged**: 2026-01-16
- **Author**: jleechan2015
- **Stats**: +148/-1 in 2 files
- **Labels**: none

## Connections
