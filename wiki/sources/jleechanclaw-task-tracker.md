---
title: "jleechanclaw-task-tracker"
type: source
tags: [jleechanclaw, tasks, subtasks, persistence]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/task_tracker.py
---

## Summary
Cross-session task and subtask state management. Tracks tasks with subtasks, links subtasks to AO session IDs, marks subtasks complete when AO session reaches "merged", aggregates task status from subtask states, handles failure propagation when budget exhausts. Persists to JSON with atomic write pattern (write to temp then rename) and file locking (fcntl.LOCK_EX).

## Key Claims
- TaskStatus: pending, in_progress, completed, failed
- SubtaskStatus: pending, in_progress, completed, failed
- Subtasks inherit budget from parent task; AO event "merged" → COMPLETED; "failed"/"budget_exhausted" → FAILED
- Atomic write: tempfile.mkstemp + os.replace for crash safety
- Session-to-subtask mapping rebuilt on load for crash recovery
- Emits SubtaskEventType events (STARTED, COMPLETED, FAILED, PROGRESS) via subtask_events module

## Connections
- [[jleechanclaw-subtask-events]] — event emission for task state changes

## Contradictions
- None identified