---
title: "jleechanclaw-auto-review-trigger"
type: source
tags: [jleechanclaw, auto-review, trigger]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/auto_review_trigger.py
---

## Summary
Automatic review triggering based on PR events. Monitors for PR events that should trigger review and dispatches the appropriate review workflow. Part of the automated PR review pipeline that ensures all PRs get reviewed without manual intervention.

## Key Claims
- Triggers on PR events: opened, synchronize, reopened
- Dispatches to appropriate review handler based on PR characteristics
- Coordinates with pr_reviewer and pr_review_decision

## Connections
- [[jleechanclaw-pr-reviewer]] — builds context for triggered reviews
- [[jleechanclaw-pr-review-decision]] — executes review decision

## Contradictions
- None identified