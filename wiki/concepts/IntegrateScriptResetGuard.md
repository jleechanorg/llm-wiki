---
title: "Integrate Script Reset Guard"
type: concept
tags: [git, integrate, safety-guard, recurring-bug, harness-fix]
sources:
  - sources/feedback-2026-06-16-git-reset-wrong-branch.md
  - sources/feedback-2026-05-05-integrate-reset-lost-pr-work.md
last_updated: 2026-06-16
---

# Integrate Script Reset Guard

A harness-level safety check that **prevents `git reset --hard` from running on the wrong branch**. Required because the same anti-pattern has been the root cause of two separate lost-PR incidents in 2026.

## The pattern (and why it's recurring)

The `/integrate` skill has a documented "align main with origin/main" step. The script (or the agent invoking it) does:

```bash
git reset --hard origin/main
```

This is **safe ONLY when the current branch IS `main`**. When the script runs in a worktree or after an interrupted integrate, the current branch may be a feature branch instead. `git reset --hard` does not check whether the target ref matches the current branch — it just mutates the current branch's HEAD. The result: a feature branch with 2-3 unpushed commits is reset to origin/main's tip, and the unpushed commits become orphans (still in object store + reflog, but no longer reachable from any branch).

## Two recorded occurrences

1. **2026-05-05** (worldarchitect.ai): `/integrate` on `expfix` branch orphaned PR #6790's commits. Restored in PR #6814. Source: `sources/feedback-2026-05-05-integrate-reset-lost-pr-work.md`.
2. **2026-06-16** (user_scope): `/integrate` flow on `feat/hooks-and-disk-magician-scopes` orphaned 7763aeb20 (original hooks commit) and 93a979dfb (self-exemption). Recovered via `git branch -f` + reflog BEFORE any `git gc`.

A recurring bug with this profile is a **harness defect**, not a "user error to document around." The fix is in the script, not in a memory entry that future agents might miss.

## Required fix (≤10 lines, applies to any integrate.sh wrapper)

Add a branch-mismatch check immediately before any `git reset --hard <ref>` call:

```bash
# integrate.sh — insert before every `git reset --hard`:
current=$(git -C "$REPO_ROOT" symbolic-ref --short HEAD 2>/dev/null || echo "")
expected="$INTEGRATE_TARGET_BRANCH"   # default: main
if [ -n "$current" ] && [ "$current" != "$expected" ]; then
  echo "BLOCKED: integrate.sh requires current branch to be '$expected', got '$current'." >&2
  echo "  Hint: if main is checked out in another worktree, run from that worktree or use" >&2
  echo "  'git -C \"$REPO_ROOT\" branch -f $expected origin/$expected' to move the pointer only." >&2
  exit 2
fi
```

Alternative for non-main targets (e.g. worktree rebase targets): parameterize `$INTEGRATE_TARGET_BRANCH` from a CLI arg or env var. Default to `main`.

## Recovery procedure (when the bug has already fired)

```bash
# Step 1: Do NOT run git gc / git prune (they destroy unreachable objects)
# Step 2: Find the lost SHA
git -C <repo> reflog --all | grep -E "<partial-sha>"
# Step 3: Verify the commit object exists
git -C <repo> cat-file -t <sha>
# Step 4: Restore the branch pointer
git -C <repo> branch -f <branch-name> <sha>
# Step 5: Verify the working tree matches expectations
git -C <repo> log <branch-name> --oneline -5
```

The recovery window is bounded by the gc.pruneExpire default of 14 days for unreachable objects. After that, the commits are gone.

## Why this is a concept (not just a source note)

The pattern is general: **any script that mutates a branch via `git reset --hard` or `git push --force` must check that the current branch is the intended target before mutating.** This applies to:

- integrate.sh (reset to origin/main)
- branch-rebase.sh (reset to base ref)
- any auto-deploy script (push to deploy branch)

All three need the same guard, generalized as a small helper function (`assert_current_branch_matches <expected>`) that can be sourced into each.

## Related

- [[PostMergeFollowupWorkflow]] — adjacent concept; covers fetching main + verifying merge is ancestor before writing follow-up work
- [[WorktreeWorkflow]] — the worktree case is the most common trigger for the wrong-branch reset (worktree has feat branch checked out, integrate.sh tries to reset main from inside the worktree)
- [[feedback-2026-06-16-git-reset-wrong-branch]] — the most recent occurrence
- [[feedback-2026-05-05-integrate-reset-lost-pr-work]] — the prior occurrence (note the "Workaround" framing in the original; this concept page promotes it to a required harness fix)
