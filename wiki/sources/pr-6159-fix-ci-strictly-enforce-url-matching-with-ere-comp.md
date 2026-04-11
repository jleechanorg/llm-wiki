---
title: "PR #6159: fix(ci): strictly enforce URL matching with ERE compatible regex"
type: source
tags: []
date: 2026-04-09
source_file: raw/prs-worldarchitect-ai/pr-6159.md
sources: []
last_updated: 2026-04-09
---

## Summary
In PR #6158, the skeptic-cron regex was updated to mandate valid video URL formats. However, the ERE bracket expression `[^[:space:)\]">]+` failed due to `grep -E` (POSIX ERE) syntax requirements, which demand the literal `]` to be positioned exactly immediately after the `[^` in order to represent literal bracket characters, resulting in a syntax error and a broken pipeline.

## Metadata
- **PR**: #6159
- **Merged**: 2026-04-09
- **Author**: jleechan2015
- **Stats**: +1/-1 in 1 files
- **Labels**: none

## Connections
