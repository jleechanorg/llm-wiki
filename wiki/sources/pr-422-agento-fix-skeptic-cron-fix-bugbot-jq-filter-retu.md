---
title: "PR #422: [agento] fix(skeptic-cron): fix bugbot jq filter returning -1 on every PR"
type: source
tags: []
date: 2026-03-28
source_file: raw/prs-worldai_claw/pr-422.md
sources: []
last_updated: 2026-03-28
---

## Summary
- Fix jq filter in Bugbot gate returning `-1` (crashing) on every PR
- Crashes silently suppressed by `|| echo "-1"`, blocking all PRs from merging

## Metadata
- **PR**: #422
- **Merged**: 2026-03-28
- **Author**: jleechan2015
- **Stats**: +4/-2 in 1 files
- **Labels**: none

## Connections
