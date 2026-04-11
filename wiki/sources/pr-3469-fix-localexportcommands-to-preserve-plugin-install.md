---
title: "PR #3469: Fix localexportcommands to preserve plugin-installed files"
type: source
tags: []
date: 2026-01-11
source_file: raw/prs-worldarchitect-ai/pr-3469.md
sources: []
last_updated: 2026-01-11
---

## Summary
- Remove `--delete` flag from rsync in `/localexportcommands`
- Remove `rm -rf` from fallback path
- Command now **merges** files instead of **replacing** them

## Metadata
- **PR**: #3469
- **Merged**: 2026-01-11
- **Author**: jleechan2015
- **Stats**: +8/-6 in 1 files
- **Labels**: none

## Connections
