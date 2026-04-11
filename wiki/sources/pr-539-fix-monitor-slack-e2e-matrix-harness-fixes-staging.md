---
title: "PR #539: fix(monitor): Slack E2E matrix harness fixes + staging config repair + skeptic webhook"
type: source
tags: []
date: 2026-04-10
source_file: raw/prs-worldai_claw/pr-539.md
sources: []
last_updated: 2026-04-10
---

## Summary
- **monitor-agent.sh**: Fix 4 bugs causing false-red STATUS=PROBLEM on every matrix run:
  1. Sender token precedence — `SLACK_USER_TOKEN` (human xoxp) now wins over `OPENCLAW_SLACK_USER_TOKEN` (bot-scoped)
  2. Timeout too short — `SLACK_E2E_TIMEOUT_SECONDS` now defaults to 180s (replies arrive 25-160s after probe)
  3. RUN_CANARY gate — matrix was gated behind `if [ "$RUN_CANARY" = "1" ]`, silently disabling it; gate removed
  4. Bot-authored sender detection — `slack_post_message_author_kind(

## Metadata
- **PR**: #539
- **Merged**: 2026-04-10
- **Author**: jleechan2015
- **Stats**: +389/-34 in 11 files
- **Labels**: none

## Connections
