---
title: "N-1 Cache Promotion"
type: concept
tags: [cache, gemini, deferred-promotion, performance]
sources: ["tdd-tests-n-1-cache-promotion-logic"]
last_updated: 2026-04-08
---

## Description
Cache promotion strategy where when a cache rebuild occurs, the NEW cache has Gemini propagation delay (cached_tokens=0 for ~30-60s). The N-1 logic defers switching to the new cache: the current request uses the OLD cache, and the new cache is promoted on the NEXT request.

## How It Works
1. **First Cache**: Cache is created but deferred (caller gets None, no old cache to use)
2. **Promote Before Next Request**: First cache promoted to active before next user request
3. **Rebuild**: New cache created but returns OLD cache name for current request (deferred=True)
4. **Next Request**: promote_pending_cache() switches active to new, deletes old

## Why It Matters
Without N-1 deferral, users would experience ~30-60s of cache misses while Gemini propagates the new cache. This pattern ensures zero perceived downtime during cache rebuilds.

## Related
- [[CampaignCacheManager]] — Implements this pattern
- [[GeminiCacheManager]] — Module providing cache management
