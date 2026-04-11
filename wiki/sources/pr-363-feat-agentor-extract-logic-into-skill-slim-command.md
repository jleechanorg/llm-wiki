---
title: "PR #363: feat(agentor): extract logic into skill, slim commands to thin layers"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-363.md
sources: []
last_updated: 2026-03-23
---

## Summary
`/agentor` and `/agento_report` had all their logic buried in a shell script (`agento-report.sh`). The commands were fat layers that called `bash ~/.claude/scripts/agento-report.sh` with no inline display and Slack posting via curl.

## Metadata
- **PR**: #363
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +156/-33 in 4 files
- **Labels**: none

## Connections
