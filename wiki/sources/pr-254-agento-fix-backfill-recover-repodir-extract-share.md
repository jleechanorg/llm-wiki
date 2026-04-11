---
title: "PR #254: [agento] fix(backfill): recover repoDir, extract shared util, fix CR nits"
type: source
tags: []
date: 2026-03-28
source_file: raw/prs-worldai_claw/pr-254.md
sources: []
last_updated: 2026-03-28
---

## Summary
When claimPR fails in backfillUncoveredPRs, the cascade cleanup falls back to inline worktree removal. The recovery chain (worktree dir, project.path, sibling scan) can leave repoDir=null when the worktree directory was already deleted from disk. In that case, the if(repoDir) guard skipped branch deletion, leaving the local branch entry in the owning repo. Subsequent backfill attempts for the same PR permanently fail because git refuses to worktree add -b when the branch already exists locally.

## Metadata
- **PR**: #254
- **Merged**: 2026-03-28
- **Author**: jleechan2015
- **Stats**: +349/-66 in 6 files
- **Labels**: none

## Connections
