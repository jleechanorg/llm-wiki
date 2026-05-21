---
name: auto-docs-push-race
description: worldarchitect.ai auto-docs workflow pushes immediately after any branch push; rebase before re-pushing local commits
type: feedback
bead: none
---

## Context

When working on WA PR branches, the `Generate PR Design Docs` workflow fires on every push and pushes a new commit to the branch within seconds.

## Problem

After pushing local commits, any subsequent local commits fail to push with "non-fast-forward" because the remote tip moved ahead.

## Rule

**Always `git fetch origin <branch> && git rebase origin/<branch>` before pushing new local commits to any WA PR branch.**

```bash
git fetch origin chore/trim-claude-md
git rebase origin/chore/trim-claude-md
git push origin chore/trim-claude-md
```

## Why

Auto-docs fires on push, adds a commit, and the local branch tip is now behind remote. A plain `git push` gets rejected. This is not a conflict — a rebase is sufficient (no merge needed).

## Observed in

PR #6942 (`chore/trim-claude-md`), 2026-05-16. Happened 3 times during the PR lifecycle.

**How to apply:** Before every second+ push to a WA branch, run the rebase pattern above.
