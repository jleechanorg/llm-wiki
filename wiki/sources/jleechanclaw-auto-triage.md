---
title: "jleechanclaw-auto-triage"
type: source
tags: [jleechanclaw, escalation, convergence, slack]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/auto_triage.py
---

## Summary
Proactive Slack DM when the same error_class escalates repeatedly. Scans outcomes.jsonl for NotifyJeffreyAction entries, detects when an error_class has escalated 2+ times within 7 days, and sends a convergence intelligence alert to Jeffrey. Helps catch systemic issues before they become persistent problems.

## Key Claims
- Escalation indicators: result="escalated" or action="NotifyJeffreyAction"
- Default window: 7 days, threshold: 2 escalations
- Reports error_class, escalation_count, PR list, first/last timestamps
- Sorted by escalation frequency (most frequent first)
- Sends to JEFFREY_DM_CHANNEL (D0AFTLEJGJU)

## Connections
- [[jleechanclaw-slack-catchup]] — also uses outcomes.jsonl scanning
- [[jleechanclaw-pr-review-decision]] — escalation destination is same JEFFREY_DM_CHANNEL

## Contradictions
- None identified