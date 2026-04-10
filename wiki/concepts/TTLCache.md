---
title: "TTLCache"
type: concept
tags: [caching, python, libraries]
sources: [generalized-file-caching-implementation]
last_updated: 2026-04-08
---

Time-To-Live cache from cachetools library that automatically expires entries after a set time.

## Characteristics
- **TTL**: Configurable time-based expiration (default: 1 hour)
- **Size limits**: Maximum number of entries (default: 1000)
- **Thread-safe**: Built-in locking for concurrent access

## Usage
```python
from cachetools import TTLCache
cache = TTLCache(maxsize=1000, ttl=3600)
```

## Related Concepts
- [[FileCaching]] — primary use case
- [[LRUCache]] — alternative eviction policy
