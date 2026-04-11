---
title: "PR #224: [agento] fix(backfill): clean up worktree + local branch on claim_failed to prevent cascading poison"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-worldai_claw/pr-224.md
sources: []
last_updated: 2026-03-27
---

## Summary
When `backfillUncoveredPRs()` fails to claim a PR (e.g. CONFLICTING), the worktree created during spawn is left behind with the PR branch checked out and locked. Every subsequent retry creates a NEW worktree, which also fails because git refuses to fetch into a branch checked out elsewhere. This cascading failure poisoned 55 worktrees over 13 hours, blocking lifecycle-worker backfill.

## Metadata
- **PR**: #224
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +0/-0 in 0 files
- **Labels**: none

## Connections
