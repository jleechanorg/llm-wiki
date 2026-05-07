---
name: Directory tests (.claude) CI vs local parity
description: CI collects 29 tests in .claude/ via run_tests.sh with testmon; local pytest direct invocation fails due to testmon baseline mismatch and pytest rootdir configuration
type: feedback
bead: none
---

## Context
Following PR 6795 merge, needed to verify local `.claude/` directory tests matched CI run 25460653021/job 74703744367 which passed 29 tests.

## Technical Details
- **CI test discovery**: `run_tests.sh --test-dirs=".claude" --testmon` runs 1203 files but testmon skips unchanged ones; CI had testmon baseline so only 29 affected tests ran
- **Local pytest direct invocation fails**: `python -m pytest .claude/ -v` produces "No tests collected" because:
  1. pytest uses `pyproject.toml` which has `testpaths = ["mvp_site"]` — overrides `.claude/` as root
  2. testmon `.testmondata` baseline doesn't match local state
  3. Individual directories work: `.claude/commands/_copilot_modules/tests/` → 47 passed, `.claude/scripts/tests/` → 34 passed, etc.
- **Root cause**: The `pyproject.toml` `testpaths = ["mvp_site"]` setting redirects pytest discovery to `mvp_site/tests/` when running from project root, unless explicitly overridden
- **Cerebras tests**: 9 failures are `initially_fails` red-phase TDD tests (expected to fail before implementation)
- **Hooks tests**: 12 failures in `test_multi_player_composition.py` due to git worktree path resolution (`subprocess.check_output(['git', 'rev-parse', '--show-toplevel'])` returns worktree path not current dir)

## Resolution
- Use `run_tests.sh` with exact CI env vars to match CI behavior locally
- Or run individual test directories directly with explicit paths
- Don't rely on `pytest .claude/` from project root due to pyproject.toml testpaths override

## Verification
CI run 25460653021 passed: 29 tests across 25 test files in `.claude/`
Local with run_tests.sh: matched CI behavior (testmon skipping + parallel execution)

## References
- CI run: https://github.com/jleechanorg/worldarchitect.ai/actions/runs/25460653021/job/74703744367
- `run_tests.sh` line 583: `PYTHONPATH="${PYTHONPATH}:${PWD}:${PWD}/testing_utils:${PWD}/mvp_site:${PWD}/automation"`
- `pyproject.toml` testpaths override: `testpaths = ["mvp_site"]`