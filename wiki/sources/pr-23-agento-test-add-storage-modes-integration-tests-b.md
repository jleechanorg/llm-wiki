---
title: "PR #23: [agento] test: add storage modes integration tests (bead jleechan-1kbf)"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-/pr-23.md
sources: []
last_updated: 2026-03-29
---

## Summary
- Add `tests/blog/storage-modes.test.ts` with 4 Vitest integration tests covering storage mode behavior
- **file storage is default**: verifies `blog-data.json` created in `process.cwd()` after posting
- **file storage persists**: verifies posts survive across `createBlogApp()` restarts when `FILE_STORAGE_PATH` is shared
- **memory mode is ephemeral**: verifies `list_posts` returns empty after app restart (no file persistence)
- **custom FILE_STORAGE_PATH**: verifies data stored at env-specified

## Metadata
- **PR**: #23
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +178/-0 in 1 files
- **Labels**: none

## Connections
