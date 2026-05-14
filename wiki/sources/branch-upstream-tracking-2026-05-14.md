# Branch Upstream Tracking — Always Set After Creation

**Source**: feedback_2026-05-14_branch_upstream_tracking.md
**Date**: 2026-05-14
**Classification**: Mandatory
**Bead**: br-befe0

## Rule

After creating any branch (`git checkout -b`, `git switch -c`) or entering any worktree, immediately set upstream tracking:

```bash
git branch --set-upstream-to=origin/<branch> <branch>
```

Do not wait for the first `git push -u`. Worktree branches never get upstream set automatically.

## Why

Every worktree and new branch session required the user to manually ask for upstream tracking to be set. The agent never does it proactively because no instruction mandated it — `git checkout -b` and worktree creation don't set upstream by default.

## How to Apply

Immediately after `git checkout -b <branch>` or entering a worktree, set upstream. This is a mechanical step, not a judgment call — always do it.

## Harness Fix

- Added instruction to `~/.claude/CLAUDE.md` (global policy)
- Created feedback memory at `~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-05-14_branch_upstream_tracking.md`
- Roadmap entry in `~/roadmap/learnings-2026-05.md`
- Bead `br-befe0` in `.beads/issues.jsonl`

## Related Concepts

- [[GitWorkflow]] — branch creation and tracking
- [[WorktreeDiscipline]] — worktree-specific operational rules
