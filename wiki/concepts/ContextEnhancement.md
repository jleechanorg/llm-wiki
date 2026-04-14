---
title: "ContextEnhancement"
type: concept
tags: [memory, context, prompt-augmentation, llm]
sources: [mvp-site-memory-utils, mvp-site-memory-mcp-real]
last_updated: 2026-04-14
---

## Summary

The process of augmenting LLM prompts with relevant historical memories to improve response quality and consistency. In WorldAI, `format_memories_for_prompt()` converts selected memories into prompt-ready text, and `MemoryMCPInterface` documents the architectural constraint that MCP tools cannot be called from Python, requiring the LLM to handle memory searches directly.

## Key Claims

### Memory Formatting Pipeline
- `format_memories_for_prompt()` converts selected memories into prompt-ready text
- Input: list of Memory objects from `select_memories_by_budget()`
- Output: formatted text block ready for injection into LLM prompt

### Architectural Constraint
- MCP tools NOT callable from Python runtime
- `MemoryMCPInterface` returns empty list or False as fallback
- Correct pattern: LLM handles memory searches via behavioral protocol in CLAUDE.md

### Semantic Search Integration
- `is_similar_memory()` for deduplication before formatting
- Budget-based selection ensures memories fit within token allocation

## Connections

- [[MemoryManagement]] — broader memory selection and formatting system
- [[MemoryIntegration]] — MCP integration pattern and its limitations
- [[ContextCompaction]] — token budget management for memory integration
- [[mvp-site-memory-utils]] — implementation of context enhancement utilities