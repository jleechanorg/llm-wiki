---
title: "PR #384: fix: thread-reply-nudge covers all channels, not just one"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-384.md
sources: []
last_updated: 2026-03-24
---

## Summary
The thread-reply-nudge LaunchAgent (every 2 min) is the fallback for unanswered thread messages when the live WebSocket misses them. It was hardcoded to a single channel (C0AKYEY48GM). Messages in C0AJ3SD5C79 and all other channels were silently skipped — root cause of the 2026-03-24 miss where Jeffrey message at 08:30 UTC went 1.5h unanswered.

## Metadata
- **PR**: #384
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +259/-7 in 2 files
- **Labels**: none

## Connections
