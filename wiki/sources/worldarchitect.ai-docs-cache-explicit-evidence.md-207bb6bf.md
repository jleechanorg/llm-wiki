---
title: "Explicit Cache Evidence — fix/cache-context-reclassification"
type: source
tags: [cache, gemini, mvp, provably-fair, testing]
sources: []
last_updated: 2026-04-07
---

## Summary

This PR fixes explicit caching in the Gemini provider with three key fixes: (1) double-billing fix — concatenates full `story_history` in merged payload instead of sending it twice (cache prefix + live JSON), (2) provably-fair compatibility — moves seed from dynamic `system_instruction` to static prepend content part, and (3) never-disable-cache — removes all `effective_cache_name = None` patterns. Achieved 89-93% cache hit rate across 12 test requests.

## Key Claims

- **Test Results**: Cache Prompt Equivalence: PASS, Explicit Cache Verification: 89-93% hit rate
- **Double-billing fix**: `story_history` now concatenated in merged payload, eliminating duplicate billing
- **Provably-fair compatibility**: Seed moved to prepended Content part — system_instruction stays static and cacheable
- **N-1 cache promotion**: New caches staged as "pending" and promoted on next request to avoid Gemini propagation delay
- **Before vs After**: `CACHE_REFERENCE` went from 0 log entries to 12, effective_cache_name went from None to cache name passed through, hit rate went from 0% to 89-93%

## Key Quotes

> "CACHE_REFERENCE log entries — 12 (every request used cache)"
> "PROVABLY_FAIR commitments — 12 (every request had unique seed)"
> "CACHE_NOT_HIT warnings — 0"
> "Cache rebuilds occur at threshold=5 with N-1 promotion"

## Connections

- [[Testing MCP]] — testing framework used for TDD guards
- [[Gemini Provider]] — the provider being fixed for explicit caching

## Contradictions

- None identified
