---
title: "jleechanclaw-failure-budget"
type: source
tags: [jleechanclaw, failure, budget]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/failure_budget.py
---

## Summary
Failure budget tracking for subtask and session budgets. Tracks how many failures are allowed before escalation, managing retry budgets and budget exhaustion detection.

## Key Claims
- Budget tracking per subtask/session
- Budget exhaustion detection
- Escalation on budget exceeded

## Connections
- [[jleechanclaw-task-tracker]] — uses failure budgets for subtasks

## Contradictions
- None identified