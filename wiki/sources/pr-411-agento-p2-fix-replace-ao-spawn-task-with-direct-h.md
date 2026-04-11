---
title: "PR #411: [agento][P2] fix: replace ao spawn --task with direct headless CLI invocations in bug-hunt"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-worldai_claw/pr-411.md
sources: []
last_updated: 2026-03-27
---

## Summary
- `ao spawn` has no `--task` flag; all 5 agents in `bug-hunt-daily.sh` were silently producing empty JSON output files, causing the script to always report "0 bugs found"
- Replaced both `ao spawn --task` invocations (lines ~142 and ~253) with verified direct headless CLI calls per agent type

## Metadata
- **PR**: #411
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +33/-15 in 1 files
- **Labels**: none

## Connections
