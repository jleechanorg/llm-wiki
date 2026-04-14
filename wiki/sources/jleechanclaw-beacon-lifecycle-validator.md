---
title: "jleechanclaw-beacon-lifecycle-validator"
type: source
tags: [jleechanclaw, lifecycle, validation]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/bead_lifecycle_validator.py
---

## Summary
Bead lifecycle validation for task tracking. Validates that bead (task) state transitions are legal and consistent. Part of the lifecycle management system ensuring tasks move through valid states (pending → in_progress → completed/failed).

## Key Claims
- Validates state transitions against allowed transitions
- Ensures consistency between parent task and subtask states

## Connections
- [[jleechanclaw-task-tracker]] — validates lifecycle of tasks tracked by task_tracker

## Contradictions
- None identified