---
name: Squash-merged branch evaluation — two-dot diff is authoritative
description: After a squash merge, git log shows 17+ diverging commits but content is already on main; use two-dot diff to confirm
type: feedback
bead: none
originSessionId: 96a04d61-d2fe-41e6-bc11-70bba53d0173
---
## Context

On 2026-05-05, branch `investigate-duplicate-xp-rewards` had PR [#6797](https://github.com/jleechanorg/worldarchitect.ai/pull/6797) squash-merged. Despite the merge, the branch still showed 17 commits ahead of origin/main via `git log origin/main..HEAD`, and `git diff --stat origin/main...HEAD` (three-dot) showed ~1741 lines changed.

## Root Cause

Three-dot `git diff A...B` finds the common merge base of A and B, then diffs B against that ancestor — NOT against A's current HEAD. After a squash merge:
- origin/main HEAD has the squash commit with all patch content
- The branch tip still has the original individual commits  
- Their common ancestor is the point BEFORE the branch diverged
- Three-dot diff shows the full branch delta from that old base — appears large even though content is identical to main

## Correct Evaluation Pattern

**Step 1**: Confirm the squash commit exists on main:
```bash
git log --oneline origin/main | grep "<PR title fragment>"
# → 634bf11c9 [antig] fix: prevent duplicate XP... (#6797)
```

**Step 2**: Show what the squash commit contained:
```bash
git show --stat <squash-sha>
# Shows: 10 files changed, 1748 insertions(+), 21 deletions(-)
```

**Step 3**: Use TWO-DOT diff (actual content difference, not graph-based):
```bash
git diff --stat origin/main HEAD -- <specific files>
# If squash covered everything: shows same files but main also has subsequent PRs
```

**Step 4**: Check subsequent main commits touching same files:
```bash
git log --oneline origin/main --not HEAD -- mvp_site/rewards_engine.py
# Shows PRs merged to main AFTER the squash that this branch lacks
```

If step 2 and step 3 produce nearly identical file lists and line counts → branch work is DONE. The remaining two-dot delta is from OTHER main commits since the squash.

## Rule

**Never use `git log origin/main..HEAD` or three-dot diff to evaluate whether a squash-merged branch has real work remaining.** These tools are graph-based and count the branch's original commits, not content differences.

Use:
1. `git show --stat <squash-commit-sha>` to verify what was merged  
2. `git diff --stat origin/main HEAD -- <files>` (two-dot) for actual content delta
3. `gh pr view <N> --json state,mergedAt` to confirm merge status

## Why

**How to apply**: Before deciding a branch needs a new PR, always run the three-step check above. A branch whose squash commit matches its full file list has no new work to contribute — run `/integrate` immediately.

## Verification

```bash
# This session: confirmed all branch work was in squash commit 634bf11c9
git show --stat 634bf11c9  # → 1748 insertions matching the branch
gh pr view 6797 --json state,mergedAt  # → MERGED 2026-05-05T07:24:57Z
```

## References

- Branch: `investigate-duplicate-xp-rewards`
- Squash commit: `634bf11c9` on origin/main
- PR: [#6797](https://github.com/jleechanorg/worldarchitect.ai/pull/6797) — merged 2026-05-05T07:24:57Z
- New branch created by `/integrate --force`: `dev1778010685`
