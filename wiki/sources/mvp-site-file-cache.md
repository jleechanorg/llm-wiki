---
title: "mvp_site file_cache"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/file_cache.py
---

## Summary
Generalized file caching module using cachetools TTLCache for thread-safe file content caching. Provides read_file_cached() with automatic TTL expiration (1 hour), cache statistics tracking (hits, misses, total chars cached).

## Key Claims
- read_file_cached() provides thread-safe file reading with 1-hour TTL cache
- TTLCache with CACHE_MAX_SIZE=1000 and CACHE_TTL_SECONDS=3600
- Cache statistics: hits, misses, total_chars_cached, start_time
- Normalizes paths for consistent cache keys

## Connections
- [[ContextCompaction]] — file caching for prompt loading
