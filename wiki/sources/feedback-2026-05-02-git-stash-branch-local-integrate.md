---
created: 2026-05-02
type: source
tags: [git, workflow, integration]
parent: [[learnings-2026-05]]
---

# git stash is branch-local during cross-branch integration

## Summary

`git stash` does not follow `git checkout` — stash is associated with the branch where it was created, not a global clipboard. When integrating changes across branches, use `git checkout source-branch -- path` instead of relying on stash.

## Key Rule

> **Use `git checkout source -- path` for cross-branch file transfer. Never rely on stash to follow across branches.**

## Pattern

```bash
# WRONG — stash stays on source branch, not global
git stash
git checkout new-branch
git stash pop  # applies against new-branch HEAD — often "nothing to commit"

# RIGHT — direct file checkout
git checkout source-branch -- file1 file2 file3
```

## Context

Integration from `fix/gemini-api-key-auth` (7 commits ahead of origin/main) to `dev1777768605`: stash showed "nothing to commit" on target branch because the stash was tied to source branch's commit context, not the target's.

## Does not affect [[jeffrey-oracle]]

Pure git workflow learning — no product psychology or system behavior update.
