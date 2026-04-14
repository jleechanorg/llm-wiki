---
title: "jleechanclaw-human-channel-bridge"
type: source
tags: [jleechanclaw, slack, ao, session-mirror]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/human_channel_bridge.py
---

## Summary
AO session lifecycle events mirrored to Slack channel C0ANK6HFW66. Polls AO session metadata files (~/.agent-orchestrator/{hash}-{project}/sessions/{session-id}), detects spawn/finish transitions, posts human-readable Slack messages with thread support. Includes watchdog for silent sessions and terminal status guarantee (every session gets a terminal message even if it errored before spawn). Reads incoming channel messages and replies contextually.

## Key Claims
- AO session dirs: ~/.agent-orchestrator/{hash}-{project}/sessions/
- Session metadata: flat key=value files (worktree, branch, status, agent, createdAt)
- Token resolution: OPENCLAW_SLACK_BOT_TOKEN → SLACK_BOT_TOKEN → openclaw.json
- Spawn/finish messages use randomized personality phrases
- Watchdog: posts nudge if active session hasn't posted in > 5 minutes (configurable)
- Terminal status guarantee: sessions that error before spawn still get an exit message
- Loop guard: only replies to non-bot users
- Rate limit: max 3 contextual replies per run

## Connections
- [[jleechanclaw-slack-catchup]] — different Slack integration pattern
- [[jleechanclaw-pr-reviewer]] — different Slack integration pattern

## Contradictions
- None identified