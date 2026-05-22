---
name: integrate-worktree-safe-pattern
description: Use git checkout -b directly in worktrees; integrate.sh fails
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 77b8fa78-435c-4033-a0fc-524f6679b9ad
---

## Pattern: Worktree-safe branch creation

**Context**: Running `/integrate` inside a git worktree (`.git/worktrees/<name>`) causes `integrate.sh` to fail because it attempts to switch to `main` which another worktree may have checked out.

**Technical detail**: `integrate.sh` uses `git checkout main && git pull` which fails when `main` is not available in the current worktree context.

**Solution**: Use `git checkout -b <branch> origin/main` directly:
```bash
git fetch origin main
git reset --hard origin/main
git clean -fd
git checkout -b dev<timestamp> origin/main
git branch --set-upstream-to=origin/main
```

**Verification**: Branch `dev1779437181` created successfully at `b230333c5f`.

**References**:
- `git worktree list` — shows all worktrees and their checked-out branches
- `.claude/hooks/pre-commit-detached-guard.sh` — prevents detached HEAD commits