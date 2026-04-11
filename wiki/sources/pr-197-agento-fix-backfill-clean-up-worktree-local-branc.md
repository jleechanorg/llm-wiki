---
title: "PR #197: [agento] fix(backfill): clean up worktree + local branch on claim_failed"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-197.md
sources: []
last_updated: 2026-03-26
---

## Summary
When `backfillUncoveredPRs()` fails to claim a PR (e.g. because the branch is already checked out elsewhere), the worktree created during `spawn()` was left behind with the PR branch locked. Every subsequent backfill retry created a NEW worktree that also failed because git refuses to fetch into a branch checked out in another worktree. This cascaded until dozens of ghost worktrees accumulated, permanently blocking the lifecycle-worker from claiming affected PRs.

Real-world impact: 55 dead work

## Metadata
- **PR**: #197
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +340/-33 in 4 files
- **Labels**: none

## Connections
