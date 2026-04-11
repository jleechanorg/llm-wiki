---
title: "PR #940: feat: add DAU/WAU analysis to user activity script"
type: source
tags: []
date: 2025-12-24
source_file: raw/prs-/pr-940.md
sources: []
last_updated: 2025-12-24
---

## Summary
- Add DAU/WAU metrics (avg and p50) to `scripts/query-user-activity.mjs`
- Query last 4 weeks of Firestore data with efficient batched processing
- Fix Firestore project: use `ai-universe-2025` for data vs `ai-universe-b3551` for auth
- Add progress indicator and daily ASCII chart

## Metadata
- **PR**: #940
- **Merged**: 2025-12-24
- **Author**: jleechan2015
- **Stats**: +1884/-183 in 4 files
- **Labels**: none

## Connections
