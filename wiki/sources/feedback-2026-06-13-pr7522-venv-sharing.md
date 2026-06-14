---
title: "PR #7522 — Share Python venv Across Git Worktrees via Symlink"
type: source
tags: [venv, worktree, symlink, disk-usage, scripts, worldarchitect]
sources: [pr7522_venv_sharing.md]
last_updated: 2026-06-13
source_file: raw/feedback_2026-06-13_pr7522_venv_sharing.md
---

## Summary
PR #7522 fixed wasted disk space by sharing the main project's Python venv across git worktrees via symlink. Each worktree was creating its own 700 MB Python venv. `scripts/venv_utils.sh` now detects linked worktrees and symlinks `worktree/venv` → `main/venv` instead of reinstalling, with escape hatches (`VENV_NO_SYMLINK=1`, `GITHUB_ACTIONS=true`) and a validation fallback. PR merged 2026-06-13 22:42Z at commit c404436a51.

## Key Claims
- New functions in `scripts/venv_utils.sh`:
  - `is_git_worktree()` — returns 0 when cwd is inside a linked git worktree (`git-dir != git-common-dir`).
  - `get_git_main_project_root()` — resolves main checkout from `git-common-dir`.
- Symlink logic in `setup_venv()`: when `VENV_NO_SYMLINK` and `GITHUB_ACTIONS` are unset AND worktree detected, validates main venv exists and has Python 3.10-3.12 + pip, then runs `ln -sfn main/venv worktree/venv` (idempotent, safe to re-run). Falls back to local venv creation on any failure.
- Escape hatches: `VENV_NO_SYMLINK=1` (skip symlink, always create local venv) and `GITHUB_ACTIONS=true` (skip symlink, auto-set in GitHub Actions).
- Technical notes: macOS `/var` is a symlink to `/private/var` — use `cd && pwd -P` for path normalization.
- Test suite: `scripts/tests/test_venv_utils.sh` — 8 tests, all passing.
- Gotchas:
  - `block-merge.sh` hook blocks agent merge attempts — human must run `! gh pr merge`.
  - Fresh worktrees get symlinks; existing worktrees keep their real venvs until re-run.

## Key Quotes
> "Each git worktree was creating its own 700 MB Python venv, wasting disk space and setup time." — feedback_2026-06-13_pr7522_venv_sharing

> "macOS `/var` is a symlink to `/private/var` — use `cd && pwd -P` for path normalization" — feedback_2026-06-13_pr7522_venv_sharing

> "`block-merge.sh` hook blocks agent merge attempts — human must run `! gh pr merge`" — feedback_2026-06-13_pr7522_venv_sharing

## Connections
- [[pr7522_venv_sharing]] — the pre-existing source page (sibling)
- [[Worktree-Workflow]] — worktree conventions
- [[Block-Merge-Sh-Hook]] — agent-merge prevention hook
- [[Disk-Cleanup-Coverage]] — disk usage policies
