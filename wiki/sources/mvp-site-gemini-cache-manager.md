---
title: "mvp_site gemini_cache_manager"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/gemini_cache_manager.py
---

## Summary
Gemini Explicit Cache Manager for WorldArchitect.AI campaigns. Manages explicit caching to cache system prompts + old story entries while keeping recent entries uncached. Rebuilds cache every 5 new entries with N-1 propagation delay handling.

## Key Claims
- CampaignCacheManager manages explicit cache for a single campaign
- should_rebuild() checks if cache needs rebuilding (REBUILD_THRESHOLD=5 entries)
- CACHE_TTL = "3600s" (1 hour) with CACHE_EXPIRY_BUFFER of 300s
- N-1 logic: keeps old cache name for first request after rebuild to handle propagation delay
- Expected savings: 70-80% cost reduction with 100% cache hit frequency

## Connections
- [[LLMIntegration]] — explicit caching for cost optimization
- [[ContextCompaction]] — cache strategy for story entries
