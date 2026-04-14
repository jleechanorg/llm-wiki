---
title: "MemoryManagement"
type: concept
tags: [memory, selection, formatting, budget, token-allocation]
sources: [mvp-site-memory-utils, mvp-site-memory-mcp-real]
last_updated: 2026-04-14
---

## Summary

Utility system for memory selection, deduplication, and formatting in WorldAI's context management pipeline. Provides functions for semantic similarity detection, exact/近-duplicate identification, budget-constrained selection, and prompt formatting. Addresses the architectural limitation that MCP tools cannot be called from Python runtime.

## Key Claims

### Memory Selection
- `is_similar_memory()` — semantic similarity detection
- `is_duplicate_memory()` — exact or near-duplicate detection
- `select_memories_by_budget()` — budget-constrained memory selection

### Memory Formatting
- `format_memories_for_prompt()` — converts selected memories into prompt-ready text
- Handles token budget allocation for core_memories in context_compaction

### Architectural Constraint
- MCP tools (e.g., `mcp__memory-server__search_nodes`) NOT callable from Python
- MemoryMCPInterface returns empty list or False due to this limitation
- Correct approach: LLM handles memory searches directly via behavioral protocol

## Connections

- [[ContextCompaction]] — memory selection integrated with token budget management
- [[MemoryIntegration]] — broader memory integration pattern
- [[mvp-site-memory-utils]] — Python utility functions
- [[mvp-site-memory-mcp-real]] — architectural limitation documentation