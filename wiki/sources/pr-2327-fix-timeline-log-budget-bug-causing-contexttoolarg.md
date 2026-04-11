---
title: "PR #2327: Fix timeline log budget bug causing ContextTooLargeError"
type: source
tags: []
date: 2025-12-09
source_file: raw/prs-worldarchitect-ai/pr-2327.md
sources: []
last_updated: 2025-12-09
---

## Summary
- Fix timeline log budget calculation that was causing `ContextTooLargeError` in production
- The scaffold calculation did not account for timeline_log duplicating story content (~2x tokens)
- Add `TIMELINE_LOG_DUPLICATION_FACTOR = 2.05` to correctly budget for timeline log
- Delete obsolete model cycling task file and update docs with "No Model Switching" policy

## Metadata
- **PR**: #2327
- **Merged**: 2025-12-09
- **Author**: jleechan2015
- **Stats**: +731/-207 in 12 files
- **Labels**: none

## Connections
