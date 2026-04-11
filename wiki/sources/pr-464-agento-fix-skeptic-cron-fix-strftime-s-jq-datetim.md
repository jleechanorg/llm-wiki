---
title: "PR #464: [agento] fix(skeptic-cron): fix strftime("%s") jq datetime comparison"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-464.md
sources: []
last_updated: 2026-03-31
---

## Summary
- Fix `strftime("%s")` being called on a Unix timestamp integer, which jq parses as a broken-down time (year 1970), making the stale-check always fail and producing `CI: error` for ALL PRs
- Regression from `skeptic-cron` stale cursor[bot] check feature

## Metadata
- **PR**: #464
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +1/-1 in 1 files
- **Labels**: none

## Connections
