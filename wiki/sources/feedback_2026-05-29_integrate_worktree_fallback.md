# integrate.sh Worktree Fallback

**Date**: 2026-05-29
**Type**: feedback
**Source**: `~/.claude/projects/-Users-jleechan-projects-worktree-autolvl-coder/memory/feedback_2026-05-29_integrate_worktree_fallback.md`

## Rule

When `integrate.sh` fails with "Fatal: main is already checked out at …", use direct fallback:

```bash
git fetch origin main --quiet
git checkout -b dev$(date +%s) origin/main
git branch --set-upstream-to=origin/main <new-branch>
```

## Context

`integrate.sh` tries `git checkout main` as an intermediate step. In a worktree layout where `main` is checked out in another worktree, Git refuses with:
```
fatal: 'main' is already checked out at '/Users/jleechan/projects/worktree_root_cause'
❌ ERROR: Failed to switch to main
```

## References

- Session 2026-05-29, `worktree_autolvl_coder`
- Also see: `raw/feedback_2026-05-05_integrate_reset_lost_pr_work.md` (different integrate failure mode)
