---
title: "jleechanclaw-session-reaper"
type: source
tags: [jleechanclaw, session, cleanup]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/session_reaper.py
---

## Summary
Session cleanup and reaping for stale/orphaned AO sessions. Identifies sessions that are no longer active and cleans up their resources. Prevents resource leaks from abandoned sessions and keeps the session namespace manageable.

## Key Claims
- Identifies stale sessions based on last activity timestamp
- Cleans up session resources (worktrees, state files, etc.)
- Runs as part of periodic maintenance

## Connections
- [[jleechanclaw-human-channel-bridge]] — related session lifecycle management

## Contradictions
- None identified