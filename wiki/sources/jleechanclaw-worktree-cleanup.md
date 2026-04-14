---
title: "jleechanclaw-worktree-cleanup"
type: source
tags: [jleechanclaw, worktree, cleanup]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/worktree_cleanup.py
---

## Summary
Worktree cleanup for removing stale Git worktrees. Identifies and removes worktrees that are no longer needed (merged sessions, abandoned branches, etc.). Part of the resource management system.

## Key Claims
- Stale worktree detection
- Safe cleanup with branch checks
- Resource leak prevention

## Connections
- [[jleechanclaw-session-reaper]] — related resource cleanup

## Contradictions
- None identified