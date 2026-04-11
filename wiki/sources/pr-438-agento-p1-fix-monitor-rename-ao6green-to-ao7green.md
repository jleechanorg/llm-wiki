---
title: "PR #438: [agento] [P1] fix(monitor): rename ao6green to ao7green — script and criteria now consistent"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-438.md
sources: []
last_updated: 2026-03-29
---

## Summary
- Rename `scripts/ao6green-pr-monitor.sh` → `scripts/ao7green-pr-monitor.sh` (and launchd wrapper)
- Fix stale trajectory threshold comment inside the script: `green_count >= 6` → `>= 7` (criteria were already 7-green; only the comment was wrong)
- Update log path from `ao6green-pr-monitor.log` → `ao7green-pr-monitor.log`
- Fix all CLAUDE.md PR Status Report Format references to use 7-green threshold and correct script name

## Metadata
- **PR**: #438
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +9/-9 in 4 files
- **Labels**: none

## Connections
