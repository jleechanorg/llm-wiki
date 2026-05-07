---
title: "Squash-Merge Branch Evaluation — Two-Dot Diff Pattern"
type: source
tags: [git, squash-merge, branch-evaluation, integrate]
date: 2026-05-05
raw: raw/feedback_2026-05-05_squash_merge_branch_evaluation.md
---

After a squash merge, `git log origin/main..HEAD` and `git diff origin/main...HEAD` (three-dot) are misleading — they show the full branch delta from the merge base (before divergence), not from the squash commit on main.

## Correct Three-Step Evaluation

1. `git show --stat <squash-sha>` — confirm what files/lines the squash commit contained
2. `git diff --stat origin/main HEAD -- <files>` (two-dot) — actual content difference
3. `gh pr view <N> --json state,mergedAt` — confirm merge status

If step 1 and step 2 match file lists → branch work is DONE, run `/integrate`.

## Session Evidence

- Branch `investigate-duplicate-xp-rewards` had PR [#6797](https://github.com/jleechanorg/worldarchitect.ai/pull/6797) squash-merged
- `git log origin/main..HEAD` showed 17 commits ahead — all misleading
- `git show --stat 634bf11c9` confirmed all 10 files were in squash commit
- Ran `./integrate.sh --force` → new branch `dev1778010685`

## Related Concepts

- [[SquashMerge]] — detection and merge strategy
- [[integrate-sh]] — script for fresh branch creation
