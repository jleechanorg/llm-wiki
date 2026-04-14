---
title: "jleechanclaw-jsonfile-util"
type: source
tags: [jleechanclaw, json, utilities]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/jsonfile_util.py
---

## Summary
JSON file utilities for atomic writes and file locking. Provides helpers for safely writing JSON files with atomic write patterns and file locking for concurrent access.

## Key Claims
- Atomic write pattern (temp file + rename)
- File locking with fcntl
- JSON serialization helpers

## Connections
- [[jleechanclaw-task-tracker]] — uses JSON file utilities for persistence

## Contradictions
- None identified