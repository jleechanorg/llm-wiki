---
title: "Pre-push diff check catches phantom reverts of post-merge cleanup work"
type: source
tags: [feedback, git-workflow, branch-hygiene, post-merge-cleanup, integrate.sh, worldarchitect]
date: 2026-06-14
source_file: ~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-14_pre_push_diff_check_phantom_revert.md
bead: none (br sync conflict on feature branch)
---

## Summary

A local feature branch's work was merged into `main` via PR #X. The user pulls `origin/main` into the branch and the working tree is clean. The local branch tip looks fine, the commit message says "merged via #X." But the local branch's diff against the *current* `origin/main` may not be empty — and the lines it adds may undo work that a *later* main PR did. Pushing and opening a new PR in this state is a **phantom revert**: a regression that looks like a valid feature PR from the agent's perspective and would re-introduce dead code/dead tests that main has already removed.

## Concrete Instance (2026-06-14)

- Branch `chore/disable-block-merge-hook` had commit `4763ac3ef4` (pre-CI-fix version of block-merge.sh removal).
- PR [#7555](https://github.com/jleechanorg/worldarchitect.ai/pull/7555) merged the chore into `main` as `8d4586d02d`. Work "done."
- PR [#7563](https://github.com/jleechanorg/worldarchitect.ai/pull/7563) later cleaned up #7555's leftovers: removed the no-op `echo` from `.claude/settings.json` AND removed 9 orphaned `TestSpellcasterInitialization` tests.
- The local branch tip was still based on `4763ac3ef4` (pre-#7555's CI fixes), so after `git pull origin main` it carried the **older** settings.json with the no-op echo still present.
- `git diff origin/main..HEAD --stat` showed +499 lines / 2 files — both **re-adding** what #7563 had just removed. Branch was a phantom revert.

## Decision Rule

**Before pushing any branch that the user calls "stale" or "looks done," or before any "make a PR" prompt, run:**

```bash
git diff origin/main..HEAD --stat
git diff origin/main..HEAD -- <files-touched-by-recent-main-cleanups>
```

If the diff:
- Re-adds code that a recent main commit explicitly deleted (verify with `git log origin/main -- <file>` for the deletion commit's SHA), OR
- Re-adds tests/config that a recent main commit's body lists as removed,

→ The branch is dead. Either delete it, rebase onto current main, or pivot to fresh work. **Do not push.**

## Why This Is Dangerous

- The branch's own title and commit message read "merged via #X." No local signal that the work has been *superseded*.
- CodeRabbit, Green Gate, and Skeptic all run against the branch's own diff. A phantom revert looks like a valid feature PR.
- The supersede relationship is only visible in `git diff origin/main..HEAD` — the agent must look there before acting.
- `./integrate.sh --force` will hard-reset to origin/main and create a fresh `dev{timestamp}` branch, but the `dev` branch is a different ref and the original chore branch is still locally pre-supersession until explicitly deleted.

## How to Apply

- **First action on a "looks merged" branch**: `git fetch origin main` + read the diff, not just the local `git log`.
- **When the user says "reset to origin main" or "is this branch safe to push?"**: always run `git diff origin/main..HEAD --stat` first. Report the result before any push.
- **When the diff shows re-adds of recently-deleted code**: surface the supersede relationship with the originating PR (cite SHA + PR number) and ask whether to delete the branch, rebase, or pivot.
- **When using `./integrate.sh`**: it hard-stops on unsynced commits and has a squash-merge detector, but does NOT detect "merged but post-superseded." Manual diff check is still required.

## Connections

- [[PostMergeFollowupWorkflow]] — related: starts cleanup from actual merged main, not from pre-merge review branch. The phantom-revert pattern is the inverse: a *pre*-merge branch that has been left behind by *post*-merge main cleanups.
- [[MergeReadinessContract]] — phantom reverts bypass merge-readiness checks because the local branch's *own* diff appears clean to its own gates.
- [[agent-pr-sprawl]] — branch sprawl includes zombie branches that linger after their work is superseded.

## Recovery Pattern

In this instance: spotted the 499-line phantom revert before any push; user chose to delete the local `chore/disable-block-merge-hook` branch (`git branch -D`) and create a fresh `dev1781426388` off `origin/main` (`git checkout -b dev$(date +%s) origin/main`). Origin's stale branch remains on the remote — not deleted (would need separate `git push origin --delete` + explicit approval).

## Provenance

2026-06-14, ~01:30Z — recovered before any push on the `chore/disable-block-merge-hook` branch at local `01fbab4dc7`. PRs [#7555](https://github.com/jleechanorg/worldarchitect.ai/pull/7555) and [#7563](https://github.com/jleechanorg/worldarchitect.ai/pull/7563) cited as the supersede chain.
