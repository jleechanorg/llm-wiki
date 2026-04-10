---
title: "Thread-Safe Caching"
type: concept
tags: [caching, concurrency, python]
sources: [generalized-file-caching-module]
last_updated: 2026-04-08
---

## Summary
Caching pattern that maintains correctness under concurrent access from multiple threads. Requires synchronization primitives to prevent race conditions.

## Implementation Pattern
```python
import threading
cache = {}
lock = threading.Lock()

def get_or_compute(key, compute):
    with lock:
        if key in cache:
            return cache[key]
    result = compute()
    with lock:
        cache[key] = result
    return result
```

## Alternatives
- `asyncio.Lock` for async code
- `threading.RLock` for reentrant locking
- Lock-free designs using atomic operations

## Related Concepts
- [[TTLCache]] — TTL expiration with size limits
- [[CacheInvalidation]] — manual cache updates
