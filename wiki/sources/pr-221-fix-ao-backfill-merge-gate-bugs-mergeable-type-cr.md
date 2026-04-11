---
title: "PR #221: fix(ao-backfill): merge gate bugs — MERGEABLE type, CR bot login, CI fail-closed, flock continue"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldai_claw/pr-221.md
sources: []
last_updated: 2026-03-16
---

## Summary
Fix 4 bugs in the ao-backfill.sh merge gate logic:

1. **MERGEABLE check**: Changed != 'MERGEABLE' to != 'true' — GitHub REST API returns boolean, not the GraphQL enum string

2. **CR bot login**: Changed coderabbit[bot] to coderabbitai[bot] in the reviews jq select

3. **no-required-checks logic**: When length == 0 (no required checks), now returns 'fail' instead of 'pass' (fail-closed)

4. **flock subshell continue**: Replaced continue inside subshell with SKIP_POKE flag variable (continue doe

## Metadata
- **PR**: #221
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +612/-11 in 6 files
- **Labels**: none

## Connections
