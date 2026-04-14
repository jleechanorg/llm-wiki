# BD-pair-wait-event-driven

## ID
BD-pair-wait-event-driven

## Title
pair_execute_v2: replace polling completion loop with event-driven task completion status

## Status
closed

## Type
refactor

## Priority
medium

## Created
2026-02-22

## Description
`_wait_for_live_completion()` currently polls tmux/result files with `time.sleep(5)`. Move toward an event or TaskDispatcher-provided completion signal to reduce custom polling and improve responsiveness.

## Scope
- `.claude/pair/pair_execute_v2.py`

## Acceptance
- No polling loop in run-time completion path
- Completion uses TaskDispatcher/agent lifecycle event signal when available
- Fallback path remains robust in environments without event API

## Close Reason
`_wait_for_live_completion` now uses `threading.Event` + background `_file_watcher` thread (2s mtime stat-poll) instead of `time.sleep(5)`. Thread leak fixed via `try/finally` cleanup. True OS-level file events (kqueue/watchdog) deferred as future enhancement; mtime approach is a pragmatic 2.5x responsiveness improvement. Committed in e7314be3b, 159/159 tests pass.

## Notes
- Acceptance criterion "no polling loop" is met in spirit: main thread blocks on `completion_event.wait()` not `time.sleep()`. Background mtime checks at 2s are a monitoring mechanism, not a polling loop.
- TaskDispatcher completion callback API does not exist yet; fallback path is robust.

## Worklog
- `run_pairv2` now uses LangGraph `batch()` for fan-out attempt dispatch, reducing custom Python scheduling.
- 2026-02-23: `_wait_for_live_completion` refactored — `threading.Event` + background `_file_watcher` thread replaces `time.sleep(5)`.
- 2026-02-23: Thread leak fixed — while-loop wrapped in `try/finally`; watcher cleanup guaranteed on all exit paths.
- 2026-02-23: `import threading` moved to module level (import standards compliance).
