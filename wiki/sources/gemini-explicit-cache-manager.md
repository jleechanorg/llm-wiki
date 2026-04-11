---
title: "Gemini Explicit Cache Manager"
type: source
tags: [gemini-api, caching, optimization, cost-reduction]
source_file: "raw/gemini-explicit-cache-manager.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Manages explicit caching for WorldArchitect.AI campaigns to leverage unchanging story entries and system prompts. Uses a split strategy: cache system prompts + old story entries (1-N) that never change, while keeping recent entries (N+1 to current) + dynamic game state uncached. Rebuilds every 5 new entries with ~1s overhead amortized to 200ms per request. Expected to achieve 70-80% cost reduction with 100% cache hit frequency.

## Key Claims
- **Split Cache Strategy**: System prompts and historical story entries (1-N) are cached; recent entries (N+1 to current) and dynamic game state remain uncached
- **Rebuild Threshold**: Cache rebuilds every 5 new entries — ~1s rebuild cost divided by 5 requests = 200ms amortized overhead
- **Proactive TTL Management**: 5-minute buffer before 1-hour TTL triggers proactive rebuild to avoid FAILED_PRECONDITION errors
- **N-1 Propagation Handling**: After rebuild, keeps old cache name for first request to avoid propagation delay on new cache
- **Model Compatibility**: Forces rebuild on model mismatch to avoid FAILED_PRECONDITION from Gemini API

## Key Technical Details
- REBUILD_THRESHOLD = 5 entries
- CACHE_TTL = 3600s (1 hour)
- CACHE_EXPIRY_BUFFER = 300s (5 minutes)
- Supports tools via CachedContentConfig

## Connections
- Related to: [[RuntimeGeneratedPydanticModels]] — both optimize LLM interaction efficiency
- Related to: [[GameStateManagementProtocol]] — game state is part of uncached dynamic content

## Contradictions
- None identified
