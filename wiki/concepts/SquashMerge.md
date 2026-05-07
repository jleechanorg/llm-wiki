---
title: "Squash-Merge"
type: concept
tags: [git, merge-strategy, pull-request]
sources: []
last_updated: 2026-05-05
sources: [sources/squash-merge-branch-evaluation-2026-05-05.md]
---

A Git merge strategy where all commits from a feature branch are squashed into a single commit when merging into the target branch. The commit message typically includes the PR reference in the format `Description (#123)`.

## Detection Challenge
Squash-merge detection in scripts must correctly identify PR references while avoiding false positives:
- Must require at least one digit: `(#123)` vs `(#)` or `(#abc)`
- Must handle edge cases like spaces: `(# 123)` should not match
- Must use fixed-strings mode to prevent regex interpretation

## Branch Evaluation After Squash Merge

After a squash merge, `git log origin/main..HEAD` and `git diff origin/main...HEAD` (three-dot) are misleading — they compute from the pre-divergence merge base, making the branch appear to have unmerged work even when the squash commit captured everything.

**Authoritative three-step check:**
1. `git show --stat <squash-sha>` — verify what files the squash commit contained
2. `git diff --stat origin/main HEAD -- <files>` (two-dot, no dots space) — actual content delta
3. `gh pr view <N> --json state,mergedAt` — confirm merged status

If steps 1 and 2 produce the same file list → branch is done, run `/integrate`.

Evidence: PR [#6797](https://github.com/jleechanorg/worldarchitect.ai/pull/6797) squash commit `634bf11c9` contained all 10 files; three-dot diff still showed 1741 lines changed on the branch — misleading.

## Related
- [[integrate-sh]] — script implementing detection
- [[squash-merge-detection-tests]] — tests for the detection logic
