---
title: "PR #5766: Fix PR fetching: keep per-window search to avoid 1000-result cap"
type: source
tags: []
date: 2026-02-25
source_file: raw/prs-worldarchitect-ai/pr-5766.md
sources: []
last_updated: 2026-02-25
---

## Summary
Restores per-window `gh pr list --search` calls in `fetch_merged_prs_by_date_range()` to avoid silently truncating results when an author has more than 1000 merged PRs in the date range.

## Metadata
- **PR**: #5766
- **Merged**: 2026-02-25
- **Author**: jleechan2015
- **Stats**: +156/-3 in 2 files
- **Labels**: none

## Connections
