# PR #7522: Share Python venv Across Git Worktrees

**Source**: https://github.com/jleechanorg/worldarchitect.ai/pull/7522
**Merged**: 2026-06-13 22:42Z

## What
Each git worktree was creating its own 700 MB Python venv. Now they symlink to the main project's venv instead.

## Implementation

### New Functions in `scripts/venv_utils.sh`

```bash
# Detect linked worktree: git-dir != git-common-dir
is_git_worktree() {
    git_dir="$(git rev-parse --git-dir)"
    common_dir="$(git rev-parse --git-common-dir)"
    [[ "$(cd "$git_dir" && pwd)" != "$(cd "$common_dir" && pwd)" ]]
}

# Resolve main checkout from worktree
get_git_main_project_root() {
    dirname "$(cd "$(git rev-parse --git-common-dir)" && pwd)"
}
```

### Symlink Logic in `setup_venv()`

```bash
if [ -z "$VENV_NO_SYMLINK" ] && [ -z "$GITHUB_ACTIONS" ] && is_git_worktree; then
    main_root="$(get_git_main_project_root)"
    if validate_existing_venv "$main_root/venv"; then
        ln -sfn "$main_venv" "$link_target"
    fi
fi
```

### Escape Hatches
- `VENV_NO_SYMLINK=1` — always create local venv
- `GITHUB_ACTIONS=true` — auto-enabled in GitHub Actions

## Test Suite
`scripts/tests/test_venv_utils.sh` — 8 tests covering:
- is_git_worktree (main vs worktree)
- get_git_main_project_root path resolution
- setup_venv symlink creation
- symlink target correctness
- VENV_NO_SYMLINK=1 escape
- fallback when main venv absent
- idempotency of re-runs

## Key Gotchas
1. macOS `/var` → `/private/var` — use `pwd -P` for path normalization
2. `block-merge.sh` hook blocks agent merge — human must run `! gh pr merge`
3. Existing worktrees keep real venvs until re-run

## Results
Fresh worktrees now get symlinks → saves ~700 MB per worktree