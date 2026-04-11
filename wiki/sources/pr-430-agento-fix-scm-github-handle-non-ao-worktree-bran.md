---
title: "PR #430: [agento] fix(scm-github): handle non-AO worktree branch conflicts via ref-based recovery"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldai_claw/pr-430.md
sources: []
last_updated: 2026-04-11
---

## Summary
- Fix `checkoutPR` to handle "already checked out at" conflicts from non-AO worktrees
- Use `git update-ref` to redirect the shared branch to the PR head, then `git reset --hard` to update the AO worktree
- Verify by SHA comparison (not branch name) since the branch is shared with non-AO worktree
- Fix workspace-worktree TypeScript error (`cfg.branchNumber` doesn't exist)

## Metadata
- **PR**: #430
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +74/-9 in 2 files
- **Labels**: none

## Connections
