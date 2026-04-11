---
title: "Memory Utils Module Tests"
type: source
tags: [python, testing, memory, tdd, utilities]
source_file: "raw/test_memory_utils.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite for the memory_utils module validating similarity detection, duplicate filtering, and budget-based memory selection functions. Uses pytest-style assertions to verify memory management functionality critical for long-running campaigns with 800+ memories.

## Key Claims
- **Similarity detection**: is_similar_memory() uses configurable threshold to detect near-duplicate memories, case-insensitive matching
- **Duplicate detection**: is_duplicate_memory() checks recent window (default 20) to avoid redundant storage while preserving memory diversity
- **Budget selection**: select_memories_by_budget() ensures recent memories are always included while truncating oldest first
- **Token estimation**: Each ~40 character memory approximates 10 tokens for budget calculations

## Key Quotes
> "Should only check recent memories within window size" — deduplication only looks at most recent N memories

> "Most recent memories should always be included" — budget selection preserves recent memories even under tight limits

> "When over budget, oldest memories are dropped first" — LRU-style eviction for memory selection

## Connections
- [[Memory Budget Alignment]] — MAX_CORE_MEMORY_TOKENS constant that budget selection respects
- [[Memory Integration Test Suite]] — higher-level memory management with query extraction and relevance scoring

## Contradictions
- None identified
