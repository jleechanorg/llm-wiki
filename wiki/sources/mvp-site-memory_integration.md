---
title: "memory_integration.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Automatically enhances LLM responses with relevant memory context extracted via Memory MCP. Provides search, relevance scoring, and context injection for slash commands.

## Key Claims
- Three-tier caching: hot cache (5 min TTL), warm cache (30 min), entity cache (1 hour)
- `extract_query_terms()` extracts up to 5 unique terms: capitalized entity names, technical terms (filtered by stop words), PR references
- Relevance scoring algorithm: name match (0.4), type match (0.2), observation relevance (0.05 per match, max 0.3), recency bonus (0.1 max)
- Search limits to top 3 terms to prevent timeout, deduplicates by entity name, filters by score >= 0.4, returns top 5
- Enhances context by injecting memory section with entity name, type, and observations (limited to 3)
- Supports slash commands: `/learn`, `/debug`, `/think`, `/analyze`, `/fix`
- MemoryMetrics tracks cache hits/misses and query latency

## Connections
- [[mcp_memory_real]] — provides the underlying MCP functions
- [[test_memory_integration]] — tests this module