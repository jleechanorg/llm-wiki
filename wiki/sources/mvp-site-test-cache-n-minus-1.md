---
title: "test_cache_n_minus_1.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
TDD tests for N-1 cache promotion logic in CampaignCacheManager. When a cache rebuild happens, the new cache has Gemini propagation delay. The N-1 logic defers switching - current request uses old cache, new cache is promoted on next request.

## Key Claims
- First cache: N-1 applied, caller gets None (no old cache)
- Rebuild returns OLD cache name (N-1 logic), deferred=True
- `promote_pending_cache()` switches to new cache and deletes old
- `should_rebuild()` returns False when pending cache exists
- `reset_cache()` clears both active and pending state
- Tool upgrade (old cache lacks code_execution) skips N-1 deferral - immediate switch

## Connections
- [[gemini_cache_manager]] — the module being tested