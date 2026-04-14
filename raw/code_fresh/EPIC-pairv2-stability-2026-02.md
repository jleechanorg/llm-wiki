# EPIC-pairv2-stability-2026-02

## ID
EPIC-pairv2-stability-2026-02

## Title
Pairv2 Stability & Performance Round - February 2026

## Status
closed

## Type
epic

## Priority
high

## Created
2026-02-23

## Problem Statement
Pairv2 has completed thread pool removal, LangGraph batch fan-out, and process cleanup. Two stability improvements remain for production readiness: event-driven completion and centralized /tmp workspace for no-worktree mode.

## Scope
- `.claude/pair/pair_execute_v2.py`
- `.claude/pair/benchmark_pair_executors.py`
- `orchestration/task_dispatcher.py`

## Goals

### Goal 1: Event-Driven Completion
**Bead**: `BD-pair-wait-event-driven`
- Replace `time.sleep(5)` polling in `_wait_for_live_completion()`
- Implementation: background file watcher thread with `threading.Event` (mtime-based, 2s interval)
- **Status**: closed (e7314be3b)

### Goal 2: Centralized /tmp Workspace
**Bead**: `BD-pairv2-no-worktree-tmp-dir`
- Default benchmark and pairv2 runs to `--no-worktree` mode
- Route to `/tmp/<repo_name>/pairv2/<session_id>` workspace
- **Status**: closed (e7314be3b)

## Success Criteria
- [x] Event-driven wait replaces time.sleep(5)
- [x] Watcher thread cleanup on all exit paths (BD-pairv2-watcher-thread-leak)
- [x] Benchmark uses /tmp workspace by default
- [x] run_pairv2 defaults no_worktree=True with --worktree opt-in
- [x] Test coverage for /tmp routing and --worktree flag
- [x] All existing tests pass with changes (159/159)

## Related Beads
| Bead | Status | Notes |
|------|--------|-------|
| BD-pair-fanout-threadpool-remove | closed | ThreadPoolExecutor removed |
| BD-pair-attempt-selection-langgraph | closed | LangGraph batch fan-out |
| REV-kz9z-pairv2-process-cleanup | implemented | Session cleanup on failures |
| BD-pair-wait-event-driven | closed | File watcher + try/finally cleanup |
| BD-pairv2-no-worktree-tmp-dir | closed | /tmp routing, --worktree opt-in |
| BD-pairv2-watcher-thread-leak | closed | try/finally fix |

## Worklog
- 2026-02-23: Created epic with 2 in-progress beads
- 2026-02-23: All 3 beads fixed and committed (e7314be3b). 159/159 tests pass. Epic closed.
- CI: 4 failing checks are runner infrastructure (EACCES dotfiles_backup), not code — tracked separately.
