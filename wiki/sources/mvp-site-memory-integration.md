---
title: "Memory Integration"
type: source
tags: [memory, mcp, context-enhancement]
sources: [mvp-site-memory-integration]
last_updated: 2025-01-15
---

## Summary

Automatic memory context enhancement for LLM responses. Integrates with Memory MCP to retrieve relevant memories based on user input.

## Key Claims

- **MemoryIntegration class**: Core memory integration with hot/warm/entity caching
- **Query term extraction**: Extracts entities, technical terms, PR references from input
- **Relevance scoring**: Calculates relevance based on name match (0.4), type match (0.2), observations (0.05/match), recency bonus
- **enhance_slash_command()**: Memory enhancement for /learn, /debug, /think, /analyze, /fix commands
- **Three-tier caching**: Hot (5 min), warm (30 min), entity (1 hour) TTLs

## Connections

- [[mvp-site-memory-mcp-real]] - Real MCP implementation
- [[mvp-site-memory-utils]] - Memory formatting for prompts
