---
title: "PR #2308: fix: add explicit entity tracking token reserve to prevent context overflow"
type: source
tags: []
date: 2025-12-03
source_file: raw/prs-worldarchitect-ai/pr-2308.md
sources: []
last_updated: 2025-12-03
---

## Summary
- Fix ContextTooLargeError caused by entity tracking tokens not being budgeted in scaffold calculation
- Add `ENTITY_TRACKING_TOKEN_RESERVE` constant (10,500 tokens) for explicit reserve
- Replace insufficient 15% buffer (~2,700 tokens) with explicit entity tracking reserve

## Metadata
- **PR**: #2308
- **Merged**: 2025-12-03
- **Author**: jleechan2015
- **Stats**: +381/-4 in 3 files
- **Labels**: none

## Connections
