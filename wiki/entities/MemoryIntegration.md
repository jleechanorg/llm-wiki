---
title: "MemoryIntegration"
type: entity
tags: [python, class, mcp, memory, integration]
sources: [memory-mcp-integration]
last_updated: 2026-04-08
---

## Description
Core memory integration class for automatic context enhancement in LLM responses.

## Attributes
- `hot_cache` — TTL: 5 minutes
- `warm_cache` — TTL: 30 minutes  
- `entity_cache` — TTL: 1 hour
- `cache_timestamps` — tracking cache entry timing
- `metrics` — MemoryMetrics instance

## Methods
- `extract_query_terms(user_input)` — Extracts up to 5 key terms from user input
- `calculate_relevance_score(entity, query_context)` — Calculates entity relevance (0.0-1.0)

## Source
[[memory-mcp-integration]]
