---
title: "Memory MCP Integration"
type: source
tags: [python, mcp, memory, integration, context, caching]
source_file: "raw/memory-mcp-integration.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Production MCP integration module providing automatic context enhancement for LLM responses. Features multi-tier caching (hot/warm/entity) with TTL-based expiration, query term extraction with stop word filtering, and relevance scoring for entity matching.

## Key Claims
- **Multi-Tier Caching**: Three cache layers (hot: 5min, warm: 30min, entity: 1hour) for optimized memory retrieval
- **Query Term Extraction**: Extracts entities, technical terms, and PR references from user input using regex patterns
- **Relevance Scoring**: Calculates entity relevance based on name match (0.4), type match (0.2), and observation relevance (0.3 max)
- **Stop Word Filtering**: Excludes common English words (the, is, at, which, on, etc.) from technical term extraction
- **Timestamp-based Recency**: Applies recency bonus based on entity timestamps for time-sensitive relevance

## Key Quotes
> "Extracts key terms from the user input for use in memory searches" — core purpose of term extraction

> "The scoring algorithm considers: name match, type match, and observation relevance" — relevance calculation breakdown

## Connections
- [[Memory MCP]] — the MCP integration this module implements
- [[Query Term Extraction]] — extracting key terms from user input
- [[Relevance Scoring]] — entity relevance calculation algorithm

## Contradictions
- None identified
