---
title: "git reset --hard on wrong branch orphans commits (recurrence #2)"
type: source
tags: [git, anti-pattern, recurring, worktree, recovery, reflog, integrate]
date: 2026-06-16
source_file: ../../raw/feedback_2026-06-16_git_reset_wrong_branch.md
---

## Summary

`git reset --hard origin/main` was run while the current branch was `feat/hooks-and-disk-magician-scopes`, not `main`. The reset moved feat's HEAD to origin/main's tip, orphaning 2 unpushed commits (7763aeb20 + 93a979dfb). This is the **second** recorded occurrence of this anti-pattern in 2026 — the first was 2026-05-05 on the `expfix` branch (PR #6790 lost work, restored in #6814).

## Key Claims

- `git reset --hard <ref>` mutates the **current** branch's HEAD; `<ref>` is just the destination tip.
- A branch's unpushed commits become orphans (still in `.git/objects/`, still in reflog) when its HEAD is reset to a different SHA.
- Recovery is possible ONLY before `git gc`/`git prune` runs; default 14-day retention for unreachable objects.
- The recovery command is `git branch -f <branch> <lost-sha>` after locating the SHA via `git reflog --all | grep <sha>` or `git fsck --no-reflogs --lost-found`.

## Key Quotes

> "ALWAYS `git checkout <target>` first, OR use `git branch -f` to move pointer only."

> "Do NOT run `git gc` or `git prune` — they destroy unreachable objects."

## Connections

- [[feedback-2026-05-05-integrate-reset-lost-pr-work]] — prior occurrence of the same anti-pattern (PR #6790 → #6814 recovery). The 2026-05-05 fix was partial; this 2026-06-16 incident confirms the fix did not stick.
- [[WorktreeWorkflow]] — covers the `git checkout -b <branch> origin/main` workaround used to avoid touching main from a non-main worktree. The reset mistake is a separate failure mode.
- [[PostMergeFollowupWorkflow]] — requires fetching `refs/heads/main` and verifying merge commit is ancestor; the reset error happens BEFORE merge.
- [[jleechan]] — the user who experienced this; integration sessions in user_scope repo.
- [[user-scope-backup-repo]] (implied entity) — the user_scope repo on the local machine where the incident occurred; recover via `git -C /Users/jleechan/projects_other/user_scope ...`.

## Required update to integrate / harness

The `/integrate` skill has been the trigger in BOTH occurrences (2026-05-05 and 2026-06-16). The skill description says it runs `git reset --hard origin/main` as part of the integration. This is a recurrent bug, not a one-off.

Fix-on-discovery: a guard in `integrate.sh` (or the skill's wrapper) that **explicitly checks the current branch matches the target** before invoking reset. Pseudocode:

```bash
current=$(git symbolic-ref --short HEAD)
target=main
if [ "$current" != "$target" ]; then
  echo "BLOCKED: integrate.sh requires current branch to be '$target', got '$current'." >&2
  echo "  If main is checked out in another worktree, use './integrate.sh --worktree-mode' instead." >&2
  exit 2
fi
```

This is a 5-line fix to a class of bugs that has already cost 2 PR-recovery cycles. Workaround-as-memory is INSUFFICIENT here.
