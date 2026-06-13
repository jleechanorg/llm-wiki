---
name: venv-sharing-across-git-worktrees-pr-7522
description: worktree venv symlinks to main instead of 700MB reinstall
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 29688ac9-ba1e-4f51-923c-b2ab3f5a8a45
---

**PR #7522**: Share Python venv across git worktrees via symlink

## Problem
Each git worktree was creating its own 700 MB Python venv, wasting disk space and setup time.

## Solution
`scripts/venv_utils.sh` now detects linked worktrees and symlinks instead of reinstalling:

1. **New functions**:
   - `is_git_worktree()` — returns 0 when cwd is inside a linked git worktree (`git-dir != git-common-dir`)
   - `get_git_main_project_root()` — resolves main checkout from `git-common-dir`

2. **Symlink path in `setup_venv()`**:
   - When `VENV_NO_SYMLINK` and `GITHUB_ACTIONS` are unset AND worktree detected
   - Validates main venv exists and has Python 3.10-3.12 + pip
   - `ln -sfn main/venv worktree/venv` (idempotent, safe to re-run)
   - Falls back to local venv creation on any failure

3. **Escape hatches**:
   - `VENV_NO_SYMLINK=1` — skip symlink, always create local venv
   - `GITHUB_ACTIONS=true` — skip symlink (auto-set in GitHub Actions)

## Technical notes
- macOS `/var` is a symlink to `/private/var` — use `cd && pwd -P` for path normalization
- Test suite: `scripts/tests/test_venv_utils.sh` — 8 tests, all passing
- PR merged 2026-06-13 22:42Z

## Gotchas
- `block-merge.sh` hook blocks agent merge attempts — human must run `! gh pr merge`
- Fresh worktrees get symlinks; existing worktrees keep their real venvs until re-run

## References
- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/7522
- Commit: c404436a51
- Evidence: https://gist.github.com/jleechan2015/487e707cc5d25d7504bb3e7076d91650