---
name: pre-push-git-diff-origin-main-head-stat-catches-phantom-reverts-of-post-merge-cleanup-work
description: "When a branch's work is already on main via a merged PR, but the local branch tip predates subsequent main cleanups, the branch's diff against current main can be a REVERT of those cleanups. Always check before pushing or opening a new PR."
metadata: 
  node_type: memory
  type: feedback
  bead: none (br sync conflict; on feature branch dev1781426388)
  originSessionId: e5eecccc-5918-42a1-a26d-fe53192cafd0
---

# Pre-push diff check catches phantom reverts of post-merge cleanup work

## The pattern

A local feature branch's work was merged into `main` via PR #X. The user pulls
`origin/main` into the branch and the working tree is clean. The local branch
tip is now strictly behind `origin/main` (or one fast-forward ahead). It
**looks** like the work is done. But the local branch's diff against the
*current* `origin/main` may not be empty — and the lines it adds may undo
work that a *later* PR did against `main`.

## Concrete instance (2026-06-14)

- Branch `chore/disable-block-merge-hook` had commit `4763ac3ef4` (the
  pre-CI-fix version of the block-merge.sh removal).
- PR [#7555](https://github.com/jleechanorg/worldarchitect.ai/pull/7555) merged
  the chore into `main` as `8d4586d02d` (post-CI-fix). Work "done."
- PR [#7563](https://github.com/jleechanorg/worldarchitect.ai/pull/7563) later
  cleaned up #7555's leftovers: removed the no-op `echo` entry from
  `.claude/settings.json` AND removed 9 orphaned `TestSpellcasterInitialization`
  tests in `mvp_site/tests/test_world_logic.py`.
- The local branch tip was still based on `4763ac3ef4` (pre-#7555's CI fixes),
  so after a `git pull origin main` it carried the **older** settings.json
  with the no-op echo still present.
- `git diff origin/main..HEAD --stat` showed:
  ```
   .claude/settings.json              |   6 +
   mvp_site/tests/test_world_logic.py | 493 +++++++++++++++++++++++++++++++++++++
  ```
  Both lines **re-added** what #7563 had just removed. The branch was a
  *phantom revert* of the cleanup work. Pushing and opening a PR would have
  reintroduced 9 dead tests + a dead no-op entry.

## Why this is dangerous

- The branch's own title and commit message read "merged via #7555." There's
  no local signal that the work has been *superseded*.
- CodeRabbit, Green Gate, and Skeptic all run against the branch's own diff.
  A phantom revert looks like a valid feature PR from the agent's perspective.
- The only place the supersede relationship is visible is in
  `git diff origin/main..HEAD` — the agent must look there before acting.

## The fix (workflow rule)

**Before pushing any branch or opening any PR from a stale-looking branch,
run:**

```bash
git diff origin/main..HEAD --stat
git diff origin/main..HEAD -- <files-touched-by-recent-main-cleanups>
```

If the diff:
- Re-adds code that a recent main commit explicitly deleted (check
  `git log origin/main -- <file>` for the deletion commit's SHA), OR
- Re-adds tests/config that a recent main commit's body lists as removed

→ The branch is dead. Either delete it or rebase onto the current main
and confirm the new diff is empty/intentional before pushing.

## How to apply

- **First action on a "looks merged" branch**: `git fetch origin main` + read
  the diff, not just the local `git log`.
- **When the user says "reset to origin main" or "is this branch safe to push?"**:
  always run `git diff origin/main..HEAD --stat` first. Report the result
  before any push.
- **When the diff shows re-adds of recently-deleted code**: surface the
  supersede relationship with the originating PR (cite SHA + PR number) and
  ask whether to delete the branch, rebase, or pivot.
- **When using `./integrate.sh`**: it hard-stops on unsynced commits and
  has a squash-merge detector, but does NOT detect "merged but
  post-superseded." Manual diff check is still required.

## Verification

Recovered 2026-06-14: spotted the 499-line phantom revert before any push;
user chose to delete the local `chore/disable-block-merge-hook` branch
(`git branch -D`) and create a fresh `dev1781426388` off `origin/main`
(`git checkout -b dev$(date +%s) origin/main`). Origin's stale branch
remains on the remote — not deleted (would need separate `git push origin
--delete` + explicit approval).

## References

- PRs: [#7555](https://github.com/jleechanorg/worldarchitect.ai/pull/7555) (merged chore), [#7563](https://github.com/jleechanorg/worldarchitect.ai/pull/7563) (cleanup that the stale branch was reverting)
- Local: `git diff origin/main..HEAD --stat` on `chore/disable-block-merge-hook` at `01fbab4dc7`
- Reusable pattern: same as the 2026-06-11 "10 CONFLICTING PRs rebased onto origin/main" sweep, but applied at the per-branch level pre-push.
