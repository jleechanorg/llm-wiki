---
title: "No Worktree Isolation"
type: concept
tags: [pairv2, refactor-pattern, automation]
sources: []
last_updated: 2026-04-13
---

## Description

The no-worktree isolation pattern executes benchmark coder and verifier in `/tmp` workspace when worktrees are disabled. This provides isolation without requiring git worktree operations, suitable for benchmarking scenarios.

## Why It Matters

Benchmarking pair-v2 should default to no-worktree mode for speed. When no-worktree is active, coder and verifier should execute in `/tmp` workspace instead of the active repository checkout to avoid polluting the user's working directory.

## Key Technical Details

- **Workspace root**: `/tmp` when worktrees disabled
- **Scope**: `.claude/pair/benchmark_pair_executors.py`, `.claude/pair/pair_execute_v2.py`
- **Pattern**: Check worktree availability, route to `/tmp` fallback

## Related Beads

- BD-pairv2-no-worktree-tmp-dir
