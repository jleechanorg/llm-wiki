---
title: "Cache/Caching"
type: concept
tags: [cache, performance, optimization, gemini, prefix-caching]
sources: []
last_updated: 2026-04-08
---

## Summary
Caching mechanism in Gemini API that reduces costs and latency by reusing previously computed context. Prefix-based caching keeps the beginning of a conversation (system instructions, recent turns) in context while processing new requests. Critical for maintaining cache compatibility with additional features like provably fair seed injection.

## Key Aspects
- **cache_name**: Identifier for cached content (e.g., "cachedContents/test-cache-abc")
- **Prefix Caching**: First N story_history entries are cacheable, remaining are uncacheable
- **Field Ordering**: Implicit and explicit approaches must maintain identical key ordering for cache hits
- **Deferral Logic**: N-1 logic defers switching to new cache until next request

## Related Pages
- [[TDDTestsCacheProvablyFairCompatibility]] — validates cache flow-through
- [[TDDTestsN1CachePromotionLogic]] — validates N-1 deferral
- [[CachePromptStructureEquivalenceTests]] — validates structure equivalence
