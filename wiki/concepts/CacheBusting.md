---
title: "Cache Busting"
type: concept
tags: [caching, deployment, versioning]
sources: ["shared-constants-configuration"]
last_updated: 2026-04-08
---

Technique using Git commit hash to force browsers to load fresh assets on each deploy. APP_VERSION uses subprocess to get git short hash at import time, defaults to "dev" when git unavailable.

## Implementation
- Git short hash (CACHE_BUST_HASH_LENGTH = 8)
- Shared between scripts/cache_busting.py and mvp_site/main.py
- Appended to asset URLs for cache invalidation

## Related
- [[Shared Constants Configuration]] — defines APP_VERSION and CACHE_BUST_HASH_LENGTH
