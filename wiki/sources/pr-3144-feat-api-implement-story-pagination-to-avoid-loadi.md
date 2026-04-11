---
title: "PR #3144: feat(api): Implement story pagination to avoid loading all entries into memory"
type: source
tags: []
date: 2026-01-06
source_file: raw/prs-worldarchitect-ai/pr-3144.md
sources: []
last_updated: 2026-01-06
---

## Summary
- **Root cause**: Campaign kuXKa6vrYY6P99MfhWBn had 1620 story entries = 34.7MB response, exceeding Cloud Run 32MB limit
- Implements query-level pagination using Firestore DESCENDING + LIMIT to avoid loading all entries into memory
- Adds Load older entries UI button for accessing full story history
- Default fetches last 300 entries (configurable via story_limit param, clamped 10-500)

## Metadata
- **PR**: #3144
- **Merged**: 2026-01-06
- **Author**: jleechan2015
- **Stats**: +1894/-133 in 15 files
- **Labels**: none

## Connections
