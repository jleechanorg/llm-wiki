---
title: "jleechanclaw-subtask-events"
type: source
tags: [jleechanclaw, events, task-tracking]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/subtask_events.py
---

## Summary
Subtask event emission system for cross-component communication. Emits events when subtask state changes (STARTED, COMPLETED, FAILED, PROGRESS) to allow other components to react without tight coupling. Used by task_tracker to notify about subtask lifecycle transitions.

## Key Claims
- SubtaskEventType enum: STARTED, COMPLETED, FAILED, PROGRESS
- emit_subtask_event function with event_type, task_id, subtask_id, session_id, message
- Events written to ~/.openclaw/state/subtask_events.jsonl
- Each line is a JSON object with all event fields plus timestamp

## Connections
- [[jleechanclaw-task-tracker]] — uses subtask_events for state change notifications

## Contradictions
- None identified