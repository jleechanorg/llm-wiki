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

## Related

- [[WorktreeDiscipline]] — worktree-specific operational rules
- [[BranchUpstreamTracking]] — source learning page
