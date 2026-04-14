---
title: "test_cache_prompt_structure.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Unit tests validating that LLMRequest.to_explicit_cache_parts() correctly splits content for caching without requiring real campaigns or API calls.

## Key Claims
- `to_explicit_cache_parts()` merge equals `to_json()` - content, field ordering, and JSON payloads must be byte-for-byte identical
- Validates field ordering for prefix-based caching
- Tests split cases: zero cached, partial cached, all cached
- campaign_id in game_state triggers explicit caching condition (BEAD-3qy)
- `build_full_content_for_retry` centralized function produces correct output

## Key Quotes
> "Field ordering must be identical for prefix-based caching!"
> "JSON payloads must be byte-for-byte identical!"

## Connections
- [[llm_request]] — provides to_explicit_cache_parts
- [[llm_service]] — provides build_full_content_for_retry