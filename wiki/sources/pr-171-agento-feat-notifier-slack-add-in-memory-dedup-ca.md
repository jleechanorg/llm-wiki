---
title: "PR #171: [agento] feat(notifier-slack): add in-memory dedup cache to suppress duplicate notifications"
type: source
tags: []
date: 2026-03-25
source_file: raw/prs-worldai_claw/pr-171.md
sources: []
last_updated: 2026-03-25
---

## Summary
- **Root cause**: `notifier-slack` POSTed directly to the webhook on every call with zero deduplication. Lifecycle polling retries or process restarts re-emitted the same session+eventType notification, spamming Slack.
- **Fix**: Added an in-memory dedup cache keyed on `sessionId:eventType` with a configurable TTL (default 60 s). Subsequent calls within the TTL window are silently suppressed; `post()` is exempt since it carries no event context.
- **Also fixed**: Pre-existing test bug where the

## Metadata
- **PR**: #171
- **Merged**: 2026-03-25
- **Author**: jleechan2015
- **Stats**: +150/-34 in 2 files
- **Labels**: none

## Connections
