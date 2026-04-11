---
title: "PR #404: [P2] fix: remove redundant empty-string guards from review-requested and session-killed reminders"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-worldai_claw/pr-404.md
sources: []
last_updated: 2026-03-27
---

## Summary
- Remove redundant  guard from  and  lifecycle reminders in 
- The  and  reminders already carry this guard (added in af2c2ff2b) — the guard on  and  was redundant since those reminders fire only in PR-context workflows
- Non-PR sessions now correctly receive the full message (no early exit), which is the intended behavior since these reminders are PR-specific

## Metadata
- **PR**: #404
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +0/-0 in 0 files
- **Labels**: none

## Connections
