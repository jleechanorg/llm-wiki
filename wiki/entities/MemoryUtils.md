---
title: "MemoryUtils"
type: entity
tags: [module, memory, testing]
sources: ["memory-utils-tests", "memory-budget-alignment-tests", "memory-integration-test-suite"]
last_updated: 2026-04-08
---

Module for managing campaign memories with deduplication, similarity detection, and budget-based selection.

## Constants
- `AUTO_MEMORY_MAX_LENGTH` — maximum length for auto-generated memories
- `AUTO_MEMORY_PREFIX` — prefix for auto-generated memory entries
- `DEDUPE_WINDOW_SIZE` — sliding window for duplicate checking (default 20)
- `MAX_CORE_MEMORY_TOKENS` — maximum tokens allocated for core memories
- `MEMORY_SIMILARITY_THRESHOLD` — similarity threshold for near-duplicate detection (default 0.85)
- `MIN_RECENT_MEMORIES` — minimum recent memories to always preserve

## Functions
- `format_memories_for_prompt()` — formats memory list for LLM prompt injection
- `is_duplicate_memory()` — checks if memory is duplicate within sliding window
- `is_similar_memory()` — detects similar memories using configurable threshold
- `select_memories_by_budget()` — selects memories fitting within token budget

## Connected To
- [[Memory Budget Alignment]] — validates MAX_CORE_MEMORY_TOKENS stays within budget bounds
- [[Memory Integration Test Suite]] — higher-level integration with MCP and relevance scoring
