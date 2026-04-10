---
title: "Prefix-Based Caching"
type: concept
tags: [caching, gemini, performance, optimization]
sources: []
last_updated: 2026-04-08
---

Prefix-based caching is a Gemini API caching strategy where the first part of a prompt (cacheable prefix) is cached and reused across requests, while the unique conversation portion (uncacheable) is sent fresh each time.

## Key Requirements
- **Field Ordering Must Match**: Cache key depends on exact field ordering
- **Byte-for-Byte Equivalence**: Merged explicit parts must equal implicit JSON
- **Split Cacheable/Uncacheable**: story_history entries split at configured boundary

## Implementation
- `LLMRequest.to_explicit_cache_parts()` splits content at entry count boundary
- Cacheable portion sent with cache_token in subsequent requests
- Uncacheable portion sent fresh each time

## Related
- [[CachePromptStructureEquivalenceTests]] — validates the implementation
- [[ExplicitCaching]] — explicit splitting approach
- [[ImplicitCaching]] — single-JSON-blob approach
