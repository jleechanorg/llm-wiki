---
title: "File Caching"
type: concept
tags: [caching, performance, python]
sources: ["file-cache-module-unit-tests"]
last_updated: 2026-04-08
---

## Description
A performance optimization technique using in-memory caching to reduce disk I/O. The file_cache.py module uses cachetools to implement LRU (Least Recently Used) caching for file reads, improving performance for repeated file access.

## Key Operations
- **read_file_cached()** - Reads file with caching, returns cached content on subsequent reads
- **get_cache_stats()** - Returns statistics: cache_hits, cache_misses, cached_files count
- **clear_file_cache()** - Clears all cached entries and resets statistics
- **invalidate_file()** - Removes specific file from cache

## Testing Coverage
- Basic read functionality
- Cache hit behavior (subsequent reads use cache)
- Cache miss behavior (first read populates cache)
- Error handling for missing files
- Cache clearing functionality
- Statistics tracking accuracy
- Thread safety for concurrent access
- Performance improvement validation
