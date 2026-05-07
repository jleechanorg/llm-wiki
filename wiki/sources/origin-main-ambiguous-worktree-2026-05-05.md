---
title: "origin/main ambiguous ref in worktrees breaks integrate"
type: feedback
date: 2026-05-05
tags: [git, worktree, integration]
---

## Summary

A local branch `refs/heads/origin/main` shadowed the remote tracking ref `refs/remotes/origin/main`, causing `./integrate.sh` to fail. Solution: use `git ls-remote origin main` to get the actual remote SHA, then checkout by SHA directly.

## Problem

```
fatal: ambiguous object name: 'origin/main'
```

Two refs resolve to `origin/main`:
- `refs/heads/origin/main` (local branch)
- `refs/remotes/origin/main` (remote tracking)

## Fix (preferred — delete the offending local branch)

```bash
git for-each-ref --format='%(refname)' | grep "refs/heads/origin/"
# Verify no unique commits, then delete:
git branch -d "origin/main"
```

## Fix (workaround — checkout by SHA)

```bash
git ls-remote origin main
# f22bc0ad0c474fb79c699b843aec12fcdbcb6d1b  refs/heads/main
git checkout -b dev$(date +%s) f22bc0ad0c474fb79c699b843aec12fcdbcb6d1b
```

## Note on --force

`integrate.sh --force` does NOT bypass the 570-commit false-stop. It only overrides uncommitted-changes and squash-merge checks. The root fix is deleting the local branch.

## See Also

- [git stash is branch-local during integration](../learnings/2026-05-02-git-stash-branch-local.md)
- `/integrate` command in worldarchitect.ai
