---
title: "Post-Merge Follow-Up Workflow"
type: concept
tags: [git, worktree, post-merge, follow-up]
sources: [sources/post-merge-followup-fresh-origin-main-2026-05-06.md]
last_updated: 2026-05-06
---

Post-merge follow-up work starts from the actual merged main tree, not from the pre-merge review branch or a cached local remote-tracking ref.

## Rule

Before writing cleanup tasks, fetch `refs/heads/main` directly into `refs/remotes/origin/main` and verify the merge commit is an ancestor of that ref.

```bash
git fetch origin '+refs/heads/main:refs/remotes/origin/main'
git merge-base --is-ancestor <merge_commit_sha> refs/remotes/origin/main
```

Only then create or reset the follow-up branch from `refs/remotes/origin/main`.

## Why

A stale local `origin/main` can invert the evidence: landed files look absent, fixed assertions look unfixed, and pre-merge review concerns get copied into incorrect follow-up beads.

## Related

- [[SquashMerge]]
- [[PRRecreatePipeline]]
