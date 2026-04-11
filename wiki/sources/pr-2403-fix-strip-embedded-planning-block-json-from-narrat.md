---
title: "PR #2403: Fix: Strip embedded planning block JSON from narrative text"
type: source
tags: [bug]
date: 2025-12-11
source_file: raw/prs-worldarchitect-ai/pr-2403.md
sources: []
last_updated: 2025-12-11
---

## Summary
- Fixes bug where raw planning block JSON (`{"thinking": ..., "choices": ...}`) appeared in campaign narrative display
- Adds robust JSON stripping from narrative text to prevent raw JSON from being shown to users
- Planning block data is properly separated into the `planning_block` structured field

## Metadata
- **PR**: #2403
- **Merged**: 2025-12-11
- **Author**: jleechan2015
- **Stats**: +996/-19 in 6 files
- **Labels**: bug

## Connections
