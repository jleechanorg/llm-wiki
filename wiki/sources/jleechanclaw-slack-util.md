---
title: "jleechanclaw-slack-util"
type: source
tags: [jleechanclaw, slack, utilities]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/slack_util.py
---

## Summary
Slack utility functions for sending messages and normalizing Slack-related values. CurlSlackNotifier posts via chat.postMessage API using OPENCLAW_SLACK_BOT_TOKEN. Includes normalization helpers for thread_ts and channel_id that treat None-like values as empty strings.

## Key Claims
- CurlSlackNotifier uses curl --config - pattern to avoid token leaking in ps
- Only returns True when Slack API response ok=true (not just curl exit code)
- normalize_slack_trigger_ts and normalize_slack_channel treat None/"None"/"null" as empty string
- Backward compatibility aliases: _normalize_slack_trigger_ts, _normalize_slack_trigger_channel

## Connections
- [[jleechanclaw-slack-catchup]] — both use similar curl + Slack API patterns
- [[jleechanclaw-canary]] — different token sources and use cases

## Contradictions
- None identified