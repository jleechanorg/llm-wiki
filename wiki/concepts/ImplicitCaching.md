---
title: "Implicit Caching"
type: concept
tags: [gemini, caching, optimization]
sources: []
last_updated: 2026-04-08
---

Gemini API feature that automatically caches repeated content in prompts. Usage metadata allows verification of cache hit rates.

## How It Works
When prompts contain repeated content, Gemini can reuse cached tokens instead of reprocessing. The usage_metadata response field shows:
- prompt_token_count: total tokens in request
- cached_content_token_count: tokens served from cache
- cache_hit_rate: percentage of cache reuse

## Related Pages
- [[GeminiUsageMetadataLoggingTests]] — tests for logging this metadata
- [[GeminiAPI]] — provider with implicit caching support

## Connections
- [[GeminiAPI]] — provides implicit caching
- [[UsageMetadata]] — the metadata that enables verification
