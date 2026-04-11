---
title: "PR #4181: Homepage latency: parallelize load and trim campaigns list"
type: source
tags: []
date: 2026-01-29
source_file: raw/prs-worldarchitect-ai/pr-4181.md
sources: []
last_updated: 2026-01-29
---

## Summary
- Parallelize campaign page load Firestore calls via shared async loader (4 concurrent queries)
- Field selection optimization: campaigns list fetches only `title`, `created_at`, `last_played`, `initial_prompt` fields
- Truncate `initial_prompt` to 100 chars for payload reduction in list view
- Default campaigns list limit: 50 (full list display)

## Metadata
- **PR**: #4181
- **Merged**: 2026-01-29
- **Author**: jleechan2015
- **Stats**: +1239/-223 in 18 files
- **Labels**: none

## Connections
