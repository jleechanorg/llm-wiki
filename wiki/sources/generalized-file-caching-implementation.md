---
title: "Generalized File Caching Implementation"
type: source
tags: [caching, performance, optimization, python]
source_file: "raw/generalized-file-caching-implementation.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Implementation of generalized file caching using the `cachetools` library to eliminate repeated file I/O operations, achieving ~11x speedup (file I/O ~0.022ms → cache hit ~0.002ms). Uses TTLCache with 1000-file limit and 1-hour TTL for automatic expiration and size management.

## Key Claims
- **Performance improvement**: ~11x speedup over direct file I/O (0.022ms → 0.002ms per read)
- **Library-based approach**: Uses `cachetools.TTLCache` for automatic TTL expiration and size limits
- **Thread-safe**: Built-in thread safety with manual locks for statistics
- **Per-session savings**: ~1ms with typical 50-file access patterns

## Key Quotes
> "This optimization improves **performance**, not token usage. The same content is still sent to Gemini - caching eliminates file I/O latency."

## Implementation Details
- **Storage**: TTLCache(maxsize=1000, ttl=3600) - 1000 files max, 1-hour expiration
- **Keys**: Normalized absolute file paths
- **Values**: Raw file content as strings
- **Threading**: threading.Lock around cache operations

## Usage Pattern
```python
from file_cache import read_file_cached, clear_file_cache, get_cache_stats

# Replace open(file).read() with cached version
content = read_file_cached('/path/to/file.txt')

# Cache management
stats = get_cache_stats()  # Returns hit rate, misses, etc.
clear_file_cache()         # For testing
```

## Benefits Over Custom Implementation
- 170 lines → 20 lines using library
- Automatic TTL, size management, thread safety
- Battle-tested library maintenance

## Connections
- Related to [[GameStateSchemaFieldConstants]] — cached file reads for schema constants
- Related to [[RuntimeGeneratedPydanticModels]] — performance optimization for model generation
- Related to [[ThreadSafeFileCachingWithTTLCache]] — alternative/implementation


## Contradictions
- None identified
