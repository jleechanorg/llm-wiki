# integrate reset lost PR work on expfix

**Date**: 2026-05-05
**Type**: Feedback / Anti-Pattern
**Source**: `~/.claude/projects/-Users-jleechan-worldarchitect-ai/memory/feedback_2026-05-05_integrate_reset_lost_pr_work.md`

## Summary

`/integrate` ran `git reset --hard origin/main` on the `expfix` branch, which moved the branch pointer to `origin/main` and made unmerged PR #6790 commits unreachable from the branch tip. The commits were recoverable via reflog.

## Key Pattern

**Before `/integrate` on a branch with open PRs, check for unmerged commits:**

```bash
git log --oneline <branch> | head -5  # identify unmerged commits
git cherry-pick <sha1> <sha2>           # copy to integration branch first
```

**Recovery after reset:**

```bash
git reflog <branch>                    # find pre-reset SHAs
git cherry-pick 4bbabed28 5506e9b23   # recover lost commits
```

## Related

- PR [#6814](https://github.com/jleechanorg/worldarchitect.ai/pull/6814) — restored PR #6790 fix on new branch
- `/integrate` skill
