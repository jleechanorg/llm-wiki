---
source: memory file
date: 2026-05-06
type: feedback
tags: [git, workflow, integrate, CLAUDE.md]
---

# integrate.sh Cleanup Behavior

## What is this?

When running `/integrate` on a branch that is both synced with its remote tracking branch AND has its PR merged to main, `integrate.sh`:

1. Creates a new timestamp-based branch (`dev{timestamp}`) from `origin/main`
2. **Deletes** the old branch (safe because it's synced and merged)
3. Uses `origin/main` directly when `main` is checked out in a worktree (skips local checkout)

## Key behaviors

### Branch deletion safety
A branch is only deleted if:
- It's synced with its remote tracking branch
- The PR is merged to main
- No unmerged commits

### Worktree constraint
If `main` is checked out in a worktree (`/Users/jleechan/projects/worktree_goal2`), the script skips `git checkout main` and uses `origin/main` directly as the base for the new branch.

### Artifact discipline rule
Before any push, always check for stray files not in `origin/main`:

```bash
git diff origin/main --name-only | head -20
```

A stray file like `specs/skeptic-report.json` (from a skeptic run) will pollute the branch and cause CI noise. Remove with `git rm` + `git commit --amend` before push.

## Usage
- `/integrate` → `dev{timestamp}` branch
- `/integrate fix/bug-123` → `fix/bug-123` branch
- `/integrate --force` → override safety checks

## Related
- `.claude/commands/integrate.md` — command definition
- `integrate.sh` — implementation script