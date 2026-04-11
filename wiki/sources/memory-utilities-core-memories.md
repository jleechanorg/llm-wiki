---
title: "Memory Management Utilities for Core Memories"
type: source
tags: [python, memory, token-budget, deduplication, utilities]
source_file: "raw/memory-utilities-core-memories.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Centralized memory management utilities providing token budget selection, deduplication logic, and memory constants for core memories in an LLM-powered application.

## Key Claims
- **Token Budget Selection**: `select_memories_by_budget()` ensures memories fit within token limits to prevent context overflow
- **Deduplication**: Fuzzy similarity detection (0.85 threshold) removes near-duplicate memories using SequenceMatcher
- **Automatic Memory Prefixing**: `[auto]` prefix marks auto-generated memories for tracking
- **Minimum Recent Memories**: Always includes at least 10 recent memories regardless of budget for continuity
- **Window-based Deduping**: Only checks recent 20 memories (O(n) for performance) instead of all memories (O(n²))

## Key Functions
- `select_memories_by_budget()` - Select memories fitting within token budget
- `is_duplicate_memory()` - Check if memory exists in recent memories (exact or near-duplicate)
- `is_similar_memory()` - Fuzzy similarity comparison using SequenceMatcher

## Constants
- `AUTO_MEMORY_PREFIX = "[auto]"` - Prefix for auto-generated memories
- `AUTO_MEMORY_MAX_LENGTH = 500` - Max chars per auto-generated memory (~100 words)
- `MEMORY_SIMILARITY_THRESHOLD = 0.85` - Similarity threshold for deduplication
- `MIN_RECENT_MEMORIES = 10` - Minimum recent memories to always include
- `DEDUPE_WINDOW_SIZE = 20` - Number of recent memories checked for duplicates

## Connections
- [[TokenBudgetSelection]] —token budget selection concept
- [[Deduplication]] — deduplication concept
- [[ContextCompaction]] — related module (BUDGET_CORE_MEMORIES_MAX constant)

## Contradictions
- None identified
