---
title: "PR #434: [agento] fix(monitor): standardize PR report output format"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-434.md
sources: []
last_updated: 2026-03-29
---

## Summary
- Standardize `scripts/ao6green-pr-monitor.sh` output to `PR #<n> — age: <Xh Ym> — status: concerning|ok`
- Add `age` field showing hours+minutes (Xh Ym)
- Map trajectory to standard status: on-track → ok, at-risk/off-track → concerning
- Add CLAUDE.md rule enforcing this format for all automation and sessions

## Metadata
- **PR**: #434
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +55/-12 in 2 files
- **Labels**: none

## Connections
