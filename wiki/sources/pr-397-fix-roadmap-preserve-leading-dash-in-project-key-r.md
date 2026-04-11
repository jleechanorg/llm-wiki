---
title: "PR #397: fix(roadmap): preserve leading dash in project_key (remove .lstrip)"
type: source
tags: []
date: 2026-03-25
source_file: raw/prs-worldai_claw/pr-397.md
sources: []
last_updated: 2026-03-25
---

## Summary
PR #391 introduced Claude auto-memory read/write into `/roadmap` and `/r` commands. During review of PR #390, CodeRabbit identified that `.lstrip('-')` incorrectly strips the leading dash from Claude project directory paths.

Claude project dirs are named `-Users-jleechan-...` (WITH leading dash). The `.lstrip('-')` call strips it, causing memory writes to go to `~/.claude/projects/Users-jleechan-...` instead of `~/.claude/projects/-Users-jleechan-...`.

This fix was applied to the 5 other comma

## Metadata
- **PR**: #397
- **Merged**: 2026-03-25
- **Author**: jleechan2015
- **Stats**: +2/-2 in 1 files
- **Labels**: none

## Connections
