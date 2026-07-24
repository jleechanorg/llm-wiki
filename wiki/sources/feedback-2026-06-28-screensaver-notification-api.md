---
title: "macos-screensaver-detection-api-gotchas-nsworkspace-vs-darwin-distributed-notifications-class-rename"
type: source
tags: [cmux, macos, tcc, dev-workflow]
date: 2026-06-28
source_file: ~/.claude/projects/-Users-jleechan-projects-reference-cmux/memory/feedback_2026-06-28_screensaver-notification-api.md
---

## Summary



## Key Claims

- 1. `NSWorkspace` does NOT have `screensaverDidStart/DidStop` notifications
- 2. `NSDistributedNotificationCenter` was renamed to `DistributedNotificationCenter`
- 3. Default to `false` on cold start
- Reusable pattern
- References

## Source

`feedback_2026-06-28_screensaver-notification-api.md` — full content at `~/.claude/projects/-Users-jleechan-projects-reference-cmux/memory/feedback_2026-06-28_screensaver-notification-api.md`
