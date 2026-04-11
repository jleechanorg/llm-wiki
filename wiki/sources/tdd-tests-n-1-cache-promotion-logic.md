---
title: "TDD Tests for N-1 Cache Promotion Logic"
type: source
tags: [python, testing, unittest, tdd, cache, gemini, deferred-promotion]
source_file: "raw/tdd-tests-n-1-cache-promotion-logic.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest suite validating N-1 cache promotion logic in CampaignCacheManager. When a cache rebuild occurs, the NEW cache has Gemini propagation delay (cached_tokens=0 for ~30-60s). The N-1 logic defers switching to the new cache: the current request uses the OLD cache, and the new cache is promoted on the NEXT request. Layer 1 unit test — no server required.

## Key Claims
- **First Cache Deferred**: First-ever cache applies N-1 deferral, caller gets None (no old cache to use)
- **Rebuild Returns Old Cache Name**: On rebuild, create_cache returns the OLD cache name (N-1 logic)
- **Promote Switches to New Cache**: promote_pending_cache() switches active cache to the new one, deletes old cache
- **Should Rebuild False When Pending**: should_rebuild() returns False when a pending cache exists

## Connections
- [[CampaignCacheManager]] — class being tested
- [[GeminiCacheManager]] — module under test (mvp_site.gemini_cache_manager)
- [[N-1 Cache Promotion]] — the core concept being validated


## Contradictions
- None detected
