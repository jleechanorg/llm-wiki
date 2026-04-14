---
title: "jleechanclaw-openclaw-notifier"
type: source
tags: [jleechanclaw, openclaw, notifications]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/openclaw_notifier.py
---

## Summary
OpenClaw notification system for sending messages via the OpenClaw gateway. Sends notifications to Slack channels through the gateway using the configured bot token. Part of the notification system that keeps stakeholders informed about PR and session events.

## Key Claims
- Uses OpenClaw gateway for Slack message delivery
- Token sourced from openclaw.json configuration
- Supports thread replies via thread_ts parameter

## Connections
- [[jleechanclaw-slack-util]] — related Slack notification utilities

## Contradictions
- None identified