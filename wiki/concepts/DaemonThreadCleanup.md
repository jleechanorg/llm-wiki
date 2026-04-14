---
title: "Daemon Thread Cleanup"
type: concept
tags: [pairv2, bug-pattern, automation]
sources: []
last_updated: 2026-04-13
---

## Description

The daemon thread cleanup pattern ensures background threads are properly terminated using try/finally blocks. This prevents thread leaks when daemon threads are spawned for file watching or monitoring tasks.

## Why It Matters

`_wait_for_live_completion` spawns a daemon `_file_watcher` thread for monitoring. Cleanup (`stop_watcher.set()` + `watcher_thread.join()`) was only called on the timeout path. All successful return paths exited without stopping the watcher thread, causing resource leaks.

## Key Technical Details

- **Cleanup mechanism**: Use try/finally to guarantee cleanup on all exit paths
- **Scope**: `.claude/pair/pair_execute_v2.py` — `_wait_for_live_completion()`
- **Pattern**: Always pair thread start with cleanup in finally block

## Related Beads

- BD-pairv2-watcher-thread-leak
