# Source: Worktree-safe integrate pattern

**File**: `~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-05-22_integrate_worktree_safe_pattern.md`
**Ingested**: 2026-05-22
**Type**: feedback / workflow

## Summary

When running `/integrate` inside a git worktree, `integrate.sh` fails because it tries to switch to `main`, which may be checked out in another worktree. Use `git checkout -b <branch> origin/main` directly.

## Safe pattern

```bash
git fetch origin main
git reset --hard origin/main
git clean -fd
git checkout -b dev<timestamp> origin/main
git branch --set-upstream-to=origin/main
```

## Reference

- Branch `dev1779437181` created 2026-05-22 at `b230333c5f`
- `.claude/hooks/pre-commit-detached-guard.sh` prevents detached HEAD commits