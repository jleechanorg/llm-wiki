# GitWorkflow

Operational rules for git branch creation, tracking, and lifecycle management in agent-driven development.

## Upstream Tracking (2026-05-14)

After creating any branch (`git checkout -b`, `git switch -c`) or entering any worktree, immediately set upstream tracking:

```bash
git branch --set-upstream-to=origin/<branch> <branch>
```

Do not wait for the first `git push -u`. Worktree branches never get upstream set automatically. This is a mechanical step — always do it.

**Why**: Every worktree/new branch session required manual upstream tracking fix. `git checkout -b` and worktree creation don't set upstream by default.

**Bead**: br-befe0

## `/integrate` in a worktree fleet (2026-06-12)

`./integrate.sh` (the `/integrate` command) assumes a single-repo layout and
breaks two ways when run from a `git worktree`:

1. **Local-only commits → HARD STOP.** The script refuses if the current branch
   is ahead of its remote. Fix: `git push origin HEAD:<branch>` (non-destructive
   fast-forward) first, then re-run.
2. **`git checkout main` fatal** when `main` is checked out in another worktree
   (`fatal: 'main' is already checked out at <path>`). A ref can only be checked
   out in one worktree at a time.

**Worktree-correct equivalent** — branch directly off `origin/main`:

```bash
git fetch origin main --quiet
git checkout -b "dev$(date +%s)" origin/main   # matches integrate.sh dev{epoch} naming
git status --short --branch                      # clean, tracking origin/main
```

Do NOT reach for `integrate.sh --force` — it does not resolve the cross-worktree
checkout conflict. Source: `sources/integrate-sh-worktree-main-elsewhere.md`
(bead rev-d6qgj).

## Related

- [[WorktreeDiscipline]] — worktree-specific operational rules
- [NoWorktreeIsolation](NoWorktreeIsolation.md) — worktree ref-exclusivity constraint
- [[BranchUpstreamTracking]] — source learning page
