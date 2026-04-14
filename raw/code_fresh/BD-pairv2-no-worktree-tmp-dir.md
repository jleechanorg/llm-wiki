# BD-pairv2-no-worktree-tmp-dir

## ID
BD-pairv2-no-worktree-tmp-dir

## Title
pair_execute_v2: run benchmark coder/verifier in /tmp when worktrees are disabled

## Status
closed

## Type
refactor

## Priority
medium

## Created
2026-02-22

## Description
Benchmarking pair-v2 should default to no-worktree mode and avoid creating git worktrees for each run. When no-worktree is active, coder and verifier should execute in a `/tmp` workspace instead of the active repository checkout.

## Scope
- `.claude/pair/benchmark_pair_executors.py`
- `.claude/pair/pair_execute_v2.py`
- `orchestration/task_dispatcher.py`

## Acceptance
- [x] `benchmark_pair_executors.py` defaults pair-v2 benchmark runs to `--no-worktree` with new `--pairv2-worktree` opt-in flag.
- [x] pair-v2 launch path sets a `/tmp` workspace root when `state["no_worktree"]` is true.
- [x] `TaskDispatcher.create_dynamic_agent` honors `workspace_config["workspace_root"]`/`workspace_name` in no-worktree mode instead of hardcoding `os.getcwd()`.
- [x] Existing worktree mode behavior remains unchanged.

## Close Reason
All acceptance criteria met and committed in e7314be3b. Test assertions updated to expect `/tmp` workspace root. 159/159 tests pass.

## Worklog
- 2026-02-22: Created bead. Identified benchmark and pair_execute_v2 as targets.
- 2026-02-23: `benchmark_pair_executors.py` — `pairv2_no_worktree` defaults `True` across all runner functions; `--pairv2-worktree` opt-in flag added to CLI.
- 2026-02-23: `pair_execute_v2.py` — `_launch_coder_only` routes to `/tmp/<repo_name>/pairv2/<session_id>` when `state["no_worktree"]` is true; `run_pairv2` defaults `no_worktree=True`; new `--worktree` CLI flag overrides.
- 2026-02-23: `TaskDispatcher.create_dynamic_agent` already honors `workspace_config["workspace_root"]` (lines 1928-1936, 2300-2303) — no changes needed.
- 2026-02-23: Two test assertions updated for `/tmp` workspace root expectation. Committed e7314be3b.
