# PR #1: docs: update README to reflect actual implementation status

**Repo:** jleechanorg/agent_bridge
**Merged:** 2026-03-02
**Author:** app/kilo-code-bot
**Stats:** +64/-36 in 1 files

## Summary
- Added Feature Status section classifying real/partial/stub/not-done features
- Fixed API endpoints to match actual routes in server.ts (cron endpoints changed from `/api/cron` to `/api/cron/jobs`)
- Corrected default port from 19876 to 18789
- Corrected default host from 127.0.0.1 to 0.0.0.0
- Marked AUTH_TOKEN as optional (API open if unset)
- Clarified only claude/codex runners are actually wired (gemini/cursor are stubs)
- Marked Discord/Telegram/Webhook channels as stubs
- Added note about

## Raw Body
## Summary
- Added Feature Status section classifying real/partial/stub/not-done features
- Fixed API endpoints to match actual routes in server.ts (cron endpoints changed from `/api/cron` to `/api/cron/jobs`)
- Corrected default port from 19876 to 18789
- Corrected default host from 127.0.0.1 to 0.0.0.0
- Marked AUTH_TOKEN as optional (API open if unset)
- Clarified only claude/codex runners are actually wired (gemini/cursor are stubs)
- Marked Discord/Telegram/Webhook channels as stubs
- Added note about in-memory sessions (SQLite exists but not wired)
- Noted Prometheus metrics class exists but no /metrics route is mounted
- Labeled architecture diagram as target-state

Built for [jleechan](https://jleechanai.slack.com/archives/C0AJQ5M0A0Y/p1772439131850379) by [Kilo for Slack](https://kilo.ai/features/slack-integration)
