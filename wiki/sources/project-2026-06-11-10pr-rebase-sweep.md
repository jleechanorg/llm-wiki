---
title: "10 PR rebase sweep (2026-06-11)"
type: source
tags: [rebase, conflict-resolution, sweep, force-push, theirs-strategy, worktree-detached]
date: 2026-06-11
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/project_2026-06-11_10pr_rebase_sweep.md
---

## Summary
On 2026-06-11 16:00 PDT, 10 CONFLICTING PRs were rebased onto `origin/main` to clear conflict state — all transitioned to MERGEABLE with 0 failing checks each. PRs cleared: #7397, #7372, #7422, #7424, #7253, #7213, #7236, #7377, #7329, #7434. Patterns learned about `git rebase -X theirs`, the import-standards gate, the Bugbot-defensive-code rule, the detached-HEAD force-push recipe, and large-stack rebase (#7377: 27 commits, #7329: 6 commits, #7434: 18 commits across `world_logic.py` + `rewards_engine.py`).

## Key Claims
- `git rebase -X theirs` is the correct hammer for branches with 100+ file conflicts when the branch's overall direction is right (used successfully on #7329 — XP alias partial-restore — 6 commits).
- Import standards gate: `from x import y` inside function bodies is FORBIDDEN by `import-validation` CI gate. When rebasing, always prefer ours for this pattern.
- Bugbot-style defensive code in HEAD wins: when HEAD has `_local_meta.pop("canonical_signal", None)` style safety lines that the branch lacks, take ours. The HEAD version incorporates more Cursor Bugbot fixes.
- `git push --force-with-lease` does NOT work from a detached HEAD worktree. Use `git push origin <sha>:refs/heads/<branch> --force` to push a specific SHA to a branch.
- Detached HEAD after rebase: when `git checkout -b <branch> <sha>` says "already exists" because the branch is checked out elsewhere, you end up with detached HEAD. Must use `git push <sha>:refs/heads/<branch> --force` to update the remote branch.
- #7434 took ours (HEAD) for Bugbot-aligned safety fixes (e.g. `_local_meta.pop("canonical_signal", None)`), took theirs when branch added new code (e.g. `_snapshot_canonical_pair` helper). ALWAYS take ours for the import-standards issue (no inline `from x import` inside functions).
- Remaining CONFLICTING PRs after sweep (low priority): #7374 (level-up observability, deep conflicts), #7380 (large stacked), #7354 (already 7-green per prior memory).

## Key Quotes
> "for each, took ours (HEAD) when it had Bugbot-aligned safety fix (e.g. `_local_meta.pop("canonical_signal", None)`), took theirs when branch added new code (e.g. `_snapshot_canonical_pair` helper). ALWAYS take ours for the import-standards issue" — decision rule

> "**`git push --force-with-lease` does NOT work from a detached HEAD worktree**: use `git push origin <sha>:refs/heads/<branch> --force` to push a specific SHA to a branch." — gotcha

## Connections
- [[PRRebaseSweep]] — this sweep
- [[GitRebaseXTheirs]] — strategy for 100+ file conflicts
- [[ImportStandardsGate]] — CI gate that affects rebase decisions
- [[BugbotDefensiveCode]] — HEAD-wins rule for safety lines
- [[DetachedHeadForcePush]] — recipe for force-pushing from detached worktrees
- [[NoOpRefreshSweep]] — the 12-PR successor sweep that continues this work
