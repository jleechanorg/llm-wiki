---
title: "PR #142: [agento] fix(metadata-updater): add hook_event guard to merge block"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-142.md
sources: []
last_updated: 2026-03-24
---

## Summary
Extract `hook_event_name` from the PostToolUse hook JSON to distinguish PreToolUse vs PostToolUse invocations. Re-introduce gh pr merge policy enforcement in PreToolUse (block when `AO_ALLOW_GH_PR_MERGE != 1`), allow PostToolUse to fall through for metadata updates, and only mark `status=merged` in PostToolUse.

## Metadata
- **PR**: #142
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +11/-4 in 1 files
- **Labels**: none

## Connections
