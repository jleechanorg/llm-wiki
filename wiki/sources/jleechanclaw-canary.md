---
title: "jleechanclaw-canary"
type: source
tags: [jleechanclaw, slack, health-check, heartbeat]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/canary.py
---

## Summary
Canary sender that posts health check messages to Slack via the second bot. Uses MCP mail creds (~/.mcp_mail/credentials.json SLACK_BOT_TOKEN) or SECOND_BOT_SLACK_TOKEN env var. The second bot's user ID (U0A4G7LDJ4R) is configured in openclaw.json channels.slack.ignoredUsers so OpenClaw gateway drops these messages silently (no loop risk).

## Key Claims
- Token priority: SECOND_BOT_SLACK_TOKEN env var → ~/.mcp_mail/credentials.json SLACK_BOT_TOKEN
- Uses curl --config - (stdin) to pass token without leaking in ps aux
- Thread support: optional thread_ts for in-thread replies
- Returns True only when Slack API response ok=true (not just curl exit code)

## Connections
- [[jleechanclaw-pr-review-decision]] — both send Slack DMs but different bots/channels

## Contradictions
- None identified