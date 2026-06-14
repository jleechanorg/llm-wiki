---
title: "Cleanup commits must use provenance filter, not topic filter"
type: source
tags: [cleanup-commit, provenance, deletion-safety, worldarchitect-ai]
date: 2026-06-08
source_file: raw/feedback_2026-06-08_cleanup_commit_provenance_filter.md
---

## Summary
Never delete a file in a 'cleanup' commit because it's 'unrelated to the PR's topic.' Use provenance as the gate: before deleting any file, run 'git show origin/main:<file>'. If it returns content, the file exists on main → restore it, don't delete it. Only delete files that were introduced by messy merges and do NOT exist on origin/main. Incident (2026-06-07): PR #7280 commit a54557f366 'Dice audit: remove unrelated merge artifacts' deleted mvp_site/bq_logging.py (600 lines, PR #7331's production BQ sink module) — that file exists on main, so deletion would undo merged work.

## Key Claims
- Predicate for cleanup deletions: 'not on origin/main AND not from before the PR started', NOT 'not related to this PR's topic'
- Before deleting any file: git show origin/main:<file> — if content returned, restore it instead
- After staging: git diff --cached --stat | grep '^-' — audit every net deletion
- PR scope verification: use git diff origin/main --name-only, NOT gh pr view --json files (stale base issue)

## Connections
- [[pr-files-api-stale-base]]
- [[CleanupCommitProvenanceFilter]]
- [[DeletionSafety]]
