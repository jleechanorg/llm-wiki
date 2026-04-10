---
title: "Memory Deduplication"
type: concept
tags: [memory, deduplication, algorithm]
sources: ["memory-utils-tests"]
last_updated: 2026-04-08
---

Process of detecting and filtering duplicate or near-duplicate memories from campaign history.

## Mechanism
Uses sliding window approach (DEDUPE_WINDOW_SIZE, default 20) to check only recent memories, avoiding O(n²) comparison on large campaigns. Supports:
- Exact duplicate detection
- Case-insensitive matching
- Near-duplicate detection via similarity threshold (default 0.85)

## Use Cases
- Preventing redundant memory entries
- Maintaining memory diversity
- Supporting long-running campaigns (800+ memories)

## Connected To
- [[MemoryUtils]] — implements deduplication functions
- [[Memory Budget Alignment]] — deduplication works within token budget constraints
