---
title: "Watcher Thread Leak"
type: concept
tags: [pairv2, resource-leak, threading]
sources: []
last_updated: 2026-02-23
---

## Definition

A Watcher Thread Leak occurs when a daemon thread spawned for file watching (mtime stat-polling) is not cleaned up on successful completion paths. The thread continues polling files after the session is done, wasting CPU. In fan-out mode with multiple attempts, leaked watcher threads accumulate.

## Problem

`_wait_for_live_completion` spawns a `_file_watcher` daemon thread that monitors result files. The cleanup (`stop_watcher.set()` + `watcher_thread.join()`) was only called on the timeout path. All successful return paths (session report found, coder outbox ready, both agents ended) exited without stopping the watcher thread.

## Solution

Wrap the completion wait loop in `try/finally` to guarantee cleanup on all exit paths:

```python
try:
    while not done:
        # wait loop
finally:
    stop_watcher.set()
    watcher_thread.join(timeout=2.0)
```

## Prevention

Always use `try/finally` when spawning threads that need cleanup. Never rely on all return paths being enumerated explicitly.

## Sources

- BD-pairv2-watcher-thread-leak: cleanup guaranteed via try/finally
