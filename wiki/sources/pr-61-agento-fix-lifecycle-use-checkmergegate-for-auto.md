---
title: "PR #61: [agento] fix(lifecycle): use checkMergeGate() for auto-merge instead of getMergeability()"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-61.md
sources: []
last_updated: 2026-03-21
---

## Summary
- replace auto-merge precheck in lifecycle manager to use `checkMergeGate()` (full 6-condition gate) instead of `scm.getMergeability()`
- source merge gate config from `project.mergeGate` with default `{ enabled: true }`
- update lifecycle-manager tests to assert full merge gate inputs are queried and auto-merge still executes when gate passes

## Metadata
- **PR**: #61
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +144/-179 in 6 files
- **Labels**: none

## Connections
