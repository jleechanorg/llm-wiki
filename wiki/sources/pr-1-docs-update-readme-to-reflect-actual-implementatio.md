---
title: "PR #1: docs: update README to reflect actual implementation status"
type: source
tags: []
date: 2026-03-02
source_file: raw/prs-/pr-1.md
sources: []
last_updated: 2026-03-02
---

## Summary
- Added Feature Status section classifying real/partial/stub/not-done features
- Fixed API endpoints to match actual routes in server.ts (cron endpoints changed from `/api/cron` to `/api/cron/jobs`)
- Corrected default port from 19876 to 18789
- Corrected default host from 127.0.0.1 to 0.0.0.0
- Marked AUTH_TOKEN as optional (API open if unset)
- Clarified only claude/codex runners are actually wired (gemini/cursor are stubs)
- Marked Discord/Telegram/Webhook channels as stubs
- Added note about

## Metadata
- **PR**: #1
- **Merged**: 2026-03-02
- **Author**: app/kilo-code-bot
- **Stats**: +64/-36 in 1 files
- **Labels**: none

## Connections
