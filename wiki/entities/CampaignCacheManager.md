---
title: "CampaignCacheManager"
type: entity
tags: [class, cache, gemini]
sources: ["tdd-tests-n-1-cache-promotion-logic"]
last_updated: 2026-04-08
---

## Description
Python class managing Gemini cache lifecycle for campaign story entries. Handles cache creation, deferred promotion (N-1 logic), and cache rebuilding with propagation delay awareness.

## Key Methods
- `create_cache()` — Creates new cache, applies N-1 deferral logic
- `promote_pending_cache()` — Promotes staged cache to active, deletes old cache
- `should_rebuild()` — Returns False when pending cache exists
- `has_pending_cache()` — Checks if cache is staged as pending

## Related
- [[N-1 Cache Promotion]] — Core logic pattern
- [[GeminiCacheManager]] — Module containing this class
