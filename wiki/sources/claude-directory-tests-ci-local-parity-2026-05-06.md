# Directory Tests CI vs Local Parity

## Source
Claude auto-memory: `feedback_2026_05_06_claude_directory_tests_ci_local_parity.md`

## Summary
CI collects 29 tests in `.claude/` via `run_tests.sh` with testmon; local pytest direct invocation fails due to `pyproject.toml` testpaths override and testmon baseline mismatch.

## Key Findings
- CI uses `run_tests.sh --test-dirs=".claude" --testmon` with testmon baseline
- Local `python -m pytest .claude/ -v` fails because `pyproject.toml` sets `testpaths = ["mvp_site"]`
- Individual test directories work: `_copilot_modules/tests/` (47), `scripts/tests/` (34), etc.
- Cerebras tests: 9 failures are `initially_fails` red-phase TDD tests (expected)
- Hooks tests: 12 failures in `test_multi_player_composition.py` due to git worktree path resolution

## Resolution
Use `run_tests.sh` with exact CI env vars to match CI behavior locally, or run individual test directories directly.

## References
- CI run: https://github.com/jleechanorg/worldarchitect.ai/actions/runs/25460653021/job/74703744367
