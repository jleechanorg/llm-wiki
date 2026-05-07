---
name: git stash is branch-local during cross-branch integration
description: Stash does not follow checkout — use git checkout -- path instead
type: feedback
bead: none
originSessionId: c697dccc-f42a-4bfb-9027-2ba6d43f597d
---
## Context

During `/integrate` from `fix/gemini-api-key-auth` (6 modified files, 7 commits ahead of origin/main) to a fresh `dev1777768605` branch:

1. Ran `git stash` on `fix/gemini-api-key-auth` → stash@{0} saved with all changes
2. Ran `git checkout dev1777768605` → switched to new branch from origin/main
3. Ran `git stash pop` → reported "nothing to commit, working tree clean"

## Root Cause

`git stash` is **per-branch**, not a global clipboard. When a stash is created on branch A, it records the working tree state **of that branch**. Switching to branch B and running `git stash pop` applies stash@{0} against branch B's HEAD — if branch B's HEAD already matches the stash's base commit, there's nothing to apply and it reports "nothing to commit."

## Correct Integration Pattern

When integrating changes from one branch to another without carrying commits:

```bash
# Pattern: checkout files directly (not stash)
git checkout source-branch -- file1 file2 file3
# OR use git show to pipe diff to apply
git diff source-branch...HEAD -- file | git apply
```

**Never rely on stash to transfer changes across branches.** Stash is for temporarily suspending work on the current branch, not for cross-branch file transfer.

## Verification

Confirmed by:
- `git stash list` after checkout showed stash@{0} still present (not consumed)
- `git status` on new branch showed clean working tree after stash pop
- Manual `git checkout fix/gemini-api-key-auth -- <files>` recovered all 6 modified files on target branch

## References

- `fix/gemini-api-key-auth` branch, commit e8e338478
- `dev1777768605` integration branch
- Stash@{0} still in stash stack (not lost, just branch-local)
