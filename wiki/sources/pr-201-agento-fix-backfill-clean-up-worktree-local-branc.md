---
title: "PR #201: [agento] fix(backfill): clean up worktree + local branch on claim_failed to prevent cascading poison"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-201.md
sources: []
last_updated: 2026-03-26
---

## Summary
When `backfillUncoveredPRs()` fails to claim a PR (e.g. branch already checked out in another worktree), the session's `kill()` call fails silently because the session isn't fully registered yet. The worktree and its local branch are left behind, permanently blocking every subsequent backfill attempt for that PR.

Real-world impact: 55 dead worktrees accumulated in `~/.worktrees/jleechanclaw/`, blocking lifecycle-worker from claiming PRs #393 and #383 for over 13 hours.

## Metadata
- **PR**: #201
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +351/-161 in 7 files
- **Labels**: none

## Connections
