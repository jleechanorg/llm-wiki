---
title: "jleechanclaw-decomposition-dispatcher"
type: source
tags: [jleechanclaw, decomposition, ao]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/decomposition_dispatcher.py
---

## Summary
Task decomposition and AO dispatching. Takes complex tasks and decomposes them into subtasks that can be dispatched to AO workers. Coordinates with task_tracker to create and track subtasks across multiple AO sessions.

## Key Claims
- Decomposes large tasks into smaller, parallelizable subtasks
- Creates subtasks in task_tracker with descriptions
- Links subtasks to AO session IDs for tracking

## Connections
- [[jleechanclaw-task-tracker]] — creates and tracks subtasks

## Contradictions
- None identified