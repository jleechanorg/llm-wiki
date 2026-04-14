---
title: "HotWarmColdCache"
type: concept
tags: [memory, cache, hot-warm-cold, tiered-access]
sources: [mvp-site-memory-utils]
last_updated: 2026-04-14
---

## Summary

A tiered memory caching pattern where memories are classified by access frequency and relevance. Although WorldAI does not implement a formal three-tier (hot/warm/cold) cache, the entity tiering system (ACTIVE/PRESENT/DORMANT) and memory selection utilities (`is_duplicate_memory()`, `is_similar_memory()`) serve a similar function of prioritizing high-value memories within token budget constraints.

## Key Claims

### Memory Deduplication
- `is_duplicate_memory()` — detects exact or near-duplicate memories
- `is_similar_memory()` — detects semantically similar memories
- Prevents redundant memory injection into prompts

### Budget-Constrained Selection
- `select_memories_by_budget()` — selects memories within token allocation
- Memory formatting transforms selected memories into prompt-ready text
- Tiering prevents low-priority memories from consuming budget

### Entity Tiering Analogy
- ACTIVE entities: current scene, high priority
- PRESENT entities: referenced but not active
- DORMANT entities: archived, lowest priority

## Connections

- [[MemoryManagement]] — memory selection and deduplication
- [[ContextCompaction]] — budget allocation for memory tiers
- [[mvp-site-memory-utils]] — utility functions implementing tiered memory selection