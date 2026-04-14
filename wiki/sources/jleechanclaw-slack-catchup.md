---
title: "jleechanclaw-slack-catchup"
type: source
tags: [jleechanclaw, slack, channel-reader]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/slack_catchup.py
---

## Summary
Slack catchup bot that synthesizes recent Slack activity into a handoff digest. Reads all allowed Slack channels from openclaw.json, fetches recent messages (default last 48h), groups by channel showing message count and latest ts, expands top threads and highlights. Posts structured digest back to triggering Slack thread. Persists per-channel cursor state for incremental sync.

## Key Claims
- Token resolution: OPENCLAW_SLACK_BOT_TOKEN → SLACK_BOT_TOKEN → SLACK_USER_TOKEN → openclaw.json
- Classifies messages into: threads, questions, announcements, noise
- Substantive content detection via regex keyword matching (http, github, fix, feat, pr, etc.)
- Thread root: ts == thread_ts with reply_count > 0
- Max 5 pages history, 20 thread roots per channel
- State file: ~/.openclaw/state/slack_catchup_state.json

## Connections
- [[jleechanclaw-slack-util]] — shares Slack API integration patterns
- [[jleechanclaw-human-channel-bridge]] — different Slack integration pattern

## Contradictions
- None identified