---
title: "Post-merge follow-up branches require verified fresh remote main"
type: feedback
date: 2026-05-06
tags: [git, worktree, post-merge, follow-up]
---

## Summary

After a PR merges, fetch the exact remote main ref and verify the merge commit is reachable before creating a follow-up branch or cleanup beads.

## Lesson

Stale local `origin/main` can make the merged tree look different from reality. During the PR 6795 post-merge cleanup pass, a stale main snapshot made some merged files/fixes appear absent. Directly fetching `+refs/heads/main:refs/remotes/origin/main` advanced local `origin/main` to merge commit `a80e21e596d29fd788603d7ed75d2807e44a7536`, after which the actual cleanup targets were clear.

## Procedure

```bash
git fetch origin '+refs/heads/main:refs/remotes/origin/main'
git merge-base --is-ancestor <merge_commit_sha> refs/remotes/origin/main
git checkout -B <followup_branch> refs/remotes/origin/main
```

Then inspect the merged tree and create beads only for defects that truly landed.

## PR 6795 Concrete Outcome

The valid post-merge cleanup targets were:

- Combat metadata prompt/schema proof for missing `unit_category` and `resistance`.
- Removal or quarantine of committed scratch evidence files and false-pass scripts.
- Reconciliation of the action-resolution/dice compatibility contract.

## See Also

- [[SquashMerge]]
- [[PRRecreatePipeline]]
- [[PostMergeFollowupWorkflow]]
