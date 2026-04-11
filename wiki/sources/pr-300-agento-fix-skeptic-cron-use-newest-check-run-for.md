---
title: "PR #300: [agento] fix(skeptic-cron): use newest check-run for gate pass detection (bd-xyxg)"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-300.md
sources: []
last_updated: 2026-03-29
---

## Summary
skeptic-cron has **never successfully auto-merged a PR**. All 30+ recent merges show `merged_by=null` (manual `--admin` or `--auto`). The merge path in skeptic-cron has never been exercised.

## Metadata
- **PR**: #300
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +7/-10 in 2 files
- **Labels**: none

## Connections
