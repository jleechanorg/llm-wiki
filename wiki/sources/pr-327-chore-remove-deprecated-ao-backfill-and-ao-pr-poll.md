---
title: "PR #327: chore: remove deprecated ao-backfill and ao-pr-poller scripts"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-327.md
sources: []
last_updated: 2026-03-21
---

## Summary
PR #326 disabled auto-merge in these scripts, raising the question of whether they are needed at all. Investigation confirmed AO lifecycle workers now handle all spawn, cleanup, review-check, and PR monitoring natively. Both scripts were partially broken:
- ao-backfill.sh crashed every run due to declare -A (bash 3 on macOS /bin/bash)
- ao-pr-poller.sh had spawn failures (ao spawn without project context) and was redundant with lifecycle workers

## Metadata
- **PR**: #327
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +4/-1730 in 9 files
- **Labels**: none

## Connections
