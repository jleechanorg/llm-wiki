---
title: "Generalized File Caching Module"
type: source
tags: [python, caching, performance, thread-safety]
source_file: "raw/generalized-file-caching-module.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Thread-safe file caching module using `cachetools.TTLCache` with 1-hour TTL expiration and automatic invalidation support. Replaces custom cache implementations with a battle-tested library.


## Key Claims
- **Cache Capacity**: 1000 files max with 3600-second (1 hour) TTL per entry
- **Thread Safety**: Uses `threading.Lock` for synchronized cache access across concurrent requests
- **TTL Expiration**: Entries automatically expire after 1 hour, preventing stale data
- **Invalidation API**: `invalidate_file()` removes specific files from cache on demand
- **Statistics Tracking**: Monitors hits, misses, hit rate percentage, total chars cached, and uptime

## Key Functions
### read_file_cached(filepath, encoding="utf-8")
Checks cache first, returns cached content on hit. On miss, reads from disk and caches. Thread-safe with locking.

### clear_file_cache()
Clears all cached entries and resets statistics. Useful for testing.

### get_cache_stats()
Returns: `{cache_hits, cache_misses, total_requests, hit_rate_percent, total_cached_chars, cached_files, uptime_seconds}`

### invalidate_file(filepath)
Removes specific file from cache. Returns True if file was cached and removed.

## Connections
- [[DefensiveNumericConverter]] — similar defensive wrapping pattern for uncertain data
- [[DataFixturesTesting]] — test fixtures may use cache clearing between tests
