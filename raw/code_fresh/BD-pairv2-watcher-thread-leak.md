# BD-pairv2-watcher-thread-leak

## ID
BD-pairv2-watcher-thread-leak

## Title
pair_execute_v2: file watcher thread not cleaned up on successful completion paths

## Status
closed

## Type
bug

## Priority
high

## Created
2026-02-23

## Description
`_wait_for_live_completion` spawns a daemon `_file_watcher` thread that monitors result files via mtime stat-polling. The cleanup (`stop_watcher.set()` + `watcher_thread.join()`) is only called on the **timeout** path. All successful return paths (session report found, coder outbox ready, both agents ended) exit the function without stopping the watcher thread.

While the thread is a daemon (so it won't prevent process exit), it continues stat-polling files after the session is done, wasting CPU. In fan-out mode with multiple attempts, leaked watcher threads accumulate.

## Scope
- `.claude/pair/pair_execute_v2.py` — `_wait_for_live_completion()`

## Acceptance
- `stop_watcher.set()` + `watcher_thread.join(timeout=2.0)` called before every `return` in `_wait_for_live_completion`
- Alternatively, refactor to use `try/finally` to guarantee cleanup on all exit paths
- No change in completion behavior or timing

## Close Reason
Fixed in e7314be3b. `_wait_for_live_completion` while-loop wrapped in `try/finally`; `stop_watcher.set()` + `watcher_thread.join(timeout=2.0)` now guaranteed on all exit paths. 159/159 tests pass.

## Related
- `BD-pair-wait-event-driven` (parent implementation)
