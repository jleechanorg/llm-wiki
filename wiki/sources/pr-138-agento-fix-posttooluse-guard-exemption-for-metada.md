---
title: "PR #138: [agento] fix: PostToolUse guard exemption for metadata-updater"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-138.md
sources: []
last_updated: 2026-03-24
---

## Summary
The `metadata-updater.sh` hook is registered on both PreToolUse and PostToolUse hooks, but had no way to distinguish between them. This caused the merge guard to fire on PostToolUse events (blocking legitimate metadata updates), and could mark `status=merged` before the merge command actually succeeded.

## Metadata
- **PR**: #138
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +12/-5 in 1 files
- **Labels**: none

## Connections
