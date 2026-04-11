---
title: "PR #1623: fix: Exclude slow UI tests from CI to prevent timeout"
type: source
tags: []
date: 2025-09-18
source_file: raw/prs-worldarchitect-ai/pr-1623.md
sources: []
last_updated: 2025-09-18
---

## Summary
- Exclude mvp_site/testing_ui/* tests containing 15-20 second sleeps
- Reduces CI runtime by ~100+ seconds of cumulative sleep time
- Prevents memory monitor timeout at 603 seconds

## Metadata
- **PR**: #1623
- **Merged**: 2025-09-18
- **Author**: jleechan2015
- **Stats**: +2/-2 in 1 files
- **Labels**: none

## Connections
