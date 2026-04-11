---
title: "PR #444: [agento] [P2] fix: dropped-thread-followup stderr errors + 4h interval"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-444.md
sources: []
last_updated: 2026-03-30
---

## Summary
`~/.openclaw/scripts/dropped-thread-followup.sh` produces spurious stderr under launchd:
- `mkdir: command not found` on line 32
- `echo: write error: Broken pipe` on line 128 (SIGPIPE from python3 heredoc piping)
- `ne: command not found` on line 369 (corrupt cached version symptom)

Additionally, the launchd plist had `StartInterval: 300` (5 min) instead of the 4-hour cadence documented in the script header.

## Metadata
- **PR**: #444
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +9/-2 in 2 files
- **Labels**: none

## Connections
