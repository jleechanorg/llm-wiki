# Post-Merge Follow-Up Branches Need Verified Fresh origin/main

- **Date**: 2026-05-06
- **Type**: feedback
- **Beads referenced**: rev-7s7ja, rev-v2xbn, rev-rhfuz, rev-7nxgn
- **PR context**: https://github.com/jleechanorg/worldarchitect.ai/pull/6795

After a PR merges, do not trust a cached local `origin/main` snapshot when creating follow-up work. Fetch the exact remote main ref, verify the merge commit is reachable from `refs/remotes/origin/main`, and only then inspect the landed tree.

In the PR 6795 post-merge cleanup pass, stale local main initially made the branch look like it was missing merged files and fixes. A direct fetch advanced `origin/main` to merge commit `a80e21e596d29fd788603d7ed75d2807e44a7536`; after reset, the actual landed tree showed the true cleanup targets: combat metadata model gap, committed scratch/false-pass evidence scripts, and action-resolution/dice contract reconciliation.

## Apply This

Use this sequence for post-merge cleanup branches:

```bash
git fetch origin '+refs/heads/main:refs/remotes/origin/main'
git merge-base --is-ancestor <merge_commit_sha> refs/remotes/origin/main
git checkout -B <followup_branch> refs/remotes/origin/main
```

Then inspect the merged tree before creating beads. Do not convert pre-merge evidence concerns into follow-up tasks until the exact merged tree has been checked.
