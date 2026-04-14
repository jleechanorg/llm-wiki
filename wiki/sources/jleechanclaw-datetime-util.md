---
title: "jleechanclaw-datetime-util"
type: source
tags: [jleechanclaw, datetime, utilities]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/datetime_util.py
---

## Summary
Datetime utilities for timezone-aware timestamp handling across jleechanclaw. Provides helpers for UTC normalization, timezone conversions, and Slack timestamp formatting.

## Key Claims
- UTC normalization for all timestamps
- Slack ts formatting (Unix timestamp strings)
- Timezone-aware comparisons

## Connections
- [[jleechanclaw-slack-catchup]] — uses datetime formatting for Slack ts
- [[jleechanclaw-human-channel-bridge]] — uses datetime for timestamp handling

## Contradictions
- None identified