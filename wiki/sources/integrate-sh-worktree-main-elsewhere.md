# Source: integrate.sh fails in worktree when main is checked out elsewhere

- **Date ingested**: 2026-06-12
- **Type**: feedback / operational learning
- **Origin**: worldarchitect.ai `/integrate` + `/learn` session (worktree `worktree_level_quick`)
- **Bead**: rev-d6qgj
- **Raw**: `raw/feedback_2026-06-12_integrate_sh_worktree_main_elsewhere.md`

## Summary

`./integrate.sh` assumes a single-repo layout and breaks in a `git worktree`
fleet two ways:

1. **Local-only commits → HARD STOP.** Push the current branch to its own
   remote (`git push origin HEAD:<branch>`) before re-running.
2. **`git checkout main` fatal** when `main` is checked out in another worktree
   (`fatal: 'main' is already checked out at <path>`).

**Worktree-correct equivalent of `/integrate`:**

```bash
git fetch origin main --quiet
git checkout -b "dev$(date +%s)" origin/main
git status --short --branch   # clean, tracking origin/main
```

Branching directly off `origin/main` sidesteps the worktree ref conflict. Do
NOT reach for `integrate.sh --force` — it does not resolve the cross-worktree
checkout conflict.

See concept: [[GitWorkflow]].
