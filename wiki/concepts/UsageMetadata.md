---
title: "Usage Metadata"
type: concept
tags: [logging, metrics, gemini, api]
sources: []
last_updated: 2026-04-08
---

Response metadata from Gemini API showing token usage and caching statistics.

## Fields
- prompt_token_count: total tokens in the prompt
- cached_content_token_count: tokens served from cache
- candidates_token_count: tokens in the response
- cache_hit_rate: calculated percentage


## Related Pages
- [[GeminiUsageMetadataLoggingTests]] — tests for this metadata
- [ImplicitCaching](ImplicitCaching.md) — feature this metadata verifies

## Connections
- [GeminiAPI](../entities/GeminiAPI.md) — source of usage metadata
- [ImplicitCaching](ImplicitCaching.md) — feature it verifies
