---
title: "PR #166: feat(lifecycle-worker): add sweepOrphanWorktrees to prevent ghost-worktree claim failures"
type: source
tags: []
date: 2026-03-25
source_file: raw/prs-worldai_claw/pr-166.md
sources: []
last_updated: 2026-03-25
---

## Summary
Ghost git worktrees accumulate when AO sessions die without proper cleanup, blocking `backfillUncoveredPRs` with:
```
fatal: refusing to fetch into branch checked out at ~/.worktrees/agent-orchestrator/ao-NNN
```
After 3 consecutive failures the backfill aborts. Manually cleaned twice in 2026-03-24 session — mandatory /harness invocation.

## Metadata
- **PR**: #166
- **Merged**: 2026-03-25
- **Author**: jleechan2015
- **Stats**: +744/-33 in 6 files
- **Labels**: none

## Connections
