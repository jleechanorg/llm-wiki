---
title: "PR #281: fix: harness-analyzer crontab grep, weekday schedule, Red Lines, PR comments API"
type: source
tags: []
date: 2026-03-19
source_file: raw/prs-worldai_claw/pr-281.md
sources: []
last_updated: 2026-03-19
---

## Summary
- Fix broken crontab deprecation check (grep -rq produced no output for pipeline)
- Fix harness-analyzer-9am plist weekday schedule: 1-5 (Sun-Thu) → 2-6 (Mon-Fri)
- Fix AGENTS.md Red Lines detection: add to ISSUES_FOUND when missing
- Fix PR comment dedup: use `issues/{pr}/comments` instead of `pulls/{pr}/comments` for body comments

## Metadata
- **PR**: #281
- **Merged**: 2026-03-19
- **Author**: jleechan2015
- **Stats**: +383/-103 in 9 files
- **Labels**: none

## Connections
