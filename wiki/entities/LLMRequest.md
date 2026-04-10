---
title: "LLMRequest"
type: entity
tags: [class, mvp-site, caching]
sources: []
last_updated: 2026-04-08
---

LLMRequest is a Python class in mvp_site.llm_request that handles request data for LLM calls. It provides two methods for preparing cached content:

## Methods
- `to_json()` — returns implicit caching prompt as single JSON blob
- `to_explicit_cache_parts(cached_entry_count)` — splits content into cacheable and uncacheable parts

## Usage
Used by llm_service.py for prefix-based caching with Gemini API. The to_explicit_cache_parts() method enables deferred caching where story_history entries can be split between cacheable (prefix) and uncacheable (conversation) segments.

## Related
- [[CachePromptStructureEquivalenceTests]] — validates equivalence between implicit and explicit cache approaches
- [[PrefixBasedCaching]] — the caching strategy using this class
