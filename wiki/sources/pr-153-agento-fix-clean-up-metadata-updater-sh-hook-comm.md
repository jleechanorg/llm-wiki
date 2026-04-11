---
title: "PR #153: [agento] fix: clean up metadata-updater.sh hook comments and dead code"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-153.md
sources: []
last_updated: 2026-03-24
---

## Summary
- Removes stale PreToolUse/merge-policy enforcement comments from `.claude/metadata-updater.sh` — this is a PostToolUse-only hook
- Removes dead `AO_HOOK_EVENT_NAME` env-var fallback since the JSON `hook_event_name` field is always present

## Metadata
- **PR**: #153
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +4/-14 in 1 files
- **Labels**: none

## Connections
