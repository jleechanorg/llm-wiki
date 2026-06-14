---
title: "Phantom Revert (Stale Branch Tip Re-introduces Removed Code)"
type: concept
tags: [git-workflow, branch-hygiene, post-merge-cleanup, anti-pattern, worldarchitect]
sources: [sources/feedback-2026-06-14-pre-push-diff-check-phantom-revert.md]
last_updated: 2026-06-14
---

## Definition

A **phantom revert** is a local feature branch whose diff against `origin/main` *re-introduces* code or tests that a *later* `main` commit has explicitly removed. The branch's own title and commit message claim the work was merged (e.g., "merged via #X"). The branch's own gate runs (CodeRabbit, Green Gate, Skeptic) all evaluate only the branch's own diff and see a clean feature PR. But the branch's tip is *behind* current main on the relevant files, and the diff against current main re-adds dead code.

## Why It's Invisible to Local Gates

CodeRabbit, Green Gate, and Skeptic all evaluate the branch's diff against its base (often an older `origin/main` SHA, the PR's merge-base, or the branch's parent). They do NOT compare the branch's tip against the *current* `origin/main`. If the branch was forked from main at SHA `A`, a main cleanup landed at SHA `B > A`, and the branch's tip is at `A + chore-work`, the gates see only the chore-work diff against `A`-base and report PASS — even though the branch tip now re-adds code that `B` deleted.

The supersede relationship is only visible by running `git diff origin/main..HEAD` from the branch tip.

## Detection Workflow

**Before pushing any branch that the user describes as "stale," "looks merged," or "should I PR this?":**

```bash
git fetch origin main
git diff origin/main..HEAD --stat
git diff origin/main..HEAD -- <files-touched-by-recent-main-cleanups>
```

Then for each `+` line in the diff, check `git log origin/main -- <file>` for recent delete commits. If a recent main commit's body or `git show` lists the lines as explicitly removed, the branch is a phantom revert.

## Recovery

Three options, in order of preference:

1. **Delete the branch** (if work is fully on main and no follow-up is needed): `git branch -D <name>`.
2. **Rebase onto current main** and re-evaluate: `git rebase origin/main`. If the diff is now empty or trivially different, the branch is dead. If the diff shows a real new feature on top of the post-cleanup main, it can be pushed.
3. **Cherry-pick the unique work** (if the branch has one or two commits not in main) onto a fresh branch off `origin/main`: `git checkout -b new-branch origin/main && git cherry-pick <sha>...`.

## Anti-Pattern: Push First, Review After

Pushing the branch and opening a PR before checking the diff against current main is the failure mode. The PR will:
- Pass the branch's own gates (CodeRabbit, Green Gate) which only evaluate the branch's own diff.
- Get reviewed by humans or post-merge CI runners.
- Cause real harm when merged: re-introduces dead code, dead tests, or dead no-op entries.

## Related Concepts

- [[PostMergeFollowupWorkflow]] — inverse pattern: a follow-up branch starting from a *stale* view of main, rather than a pre-merge branch lagging behind current main.
- [[MergeReadinessContract]] — phantom reverts bypass merge-readiness checks because the local branch's *own* diff appears clean to its own gates.
- [[agent-pr-sprawl]] — branch sprawl includes zombie branches that linger after their work is superseded by main cleanups.
- [[StaleFlag]] — a different kind of "stale state" (boolean flag, not git branch), but the same root cause: state that was correct in an older snapshot but stale in the current one.

## Concrete Example (2026-06-14)

Branch `chore/disable-block-merge-hook` at local `01fbab4dc7`:
- `git diff origin/main..HEAD --stat` showed:
  ```
   .claude/settings.json              |   6 +
   mvp_site/tests/test_world_logic.py | 493 +++++++++++++++++++++++++++++++++++++
  ```
- Both files were cleanup targets of PR [#7563](https://github.com/jleechanorg/worldarchitect.ai/pull/7563), which removed the no-op `echo` entry and 9 orphaned `TestSpellcasterInitialization` tests.
- The local branch's tip predated the cleanup; pulling `origin/main` brought in #7563 but the local branch still carried the pre-#7563 versions of the same files.
- Recovery: spotted before any push; user chose `git branch -D chore/disable-block-merge-hook` + `git checkout -b dev$(date +%s) origin/main`.

## How to Prevent

- **After every `git fetch origin main` on a feature branch**, run `git diff origin/main..HEAD --stat` as a routine check.
- **In `integrate.sh` or similar workflow tools**, add a post-reset check that flags "branch's own commit is now in main" + "branch's tip is behind current main on a file changed by a recent main commit" as a "phantom revert risk."
- **In CLAUDE.md or harness rules**, add an agent rule: "Before opening any PR from a branch not currently in main, run `git diff origin/main..HEAD --stat` and verify the diff is not a re-add of recently-removed code."
