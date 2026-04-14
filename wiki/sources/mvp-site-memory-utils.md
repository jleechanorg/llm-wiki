---
title: "mvp_site memory_utils"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/memory_utils.py
---

## Summary
Utility functions for memory selection and formatting. Functions for detecting duplicate memories, budget-based selection, and prompt formatting.

## Key Claims
- is_similar_memory() checks if new memory is semantically similar to existing ones
- is_duplicate_memory() checks for exact or near-duplicate memories
- select_memories_by_budget() selects memories within token budget allocation
- format_memories_for_prompt() formats memories into prompt-ready text

## Connections
- [[MemoryManagement]] — memory utilities for selection and formatting
- [[ContextCompaction]] — core_memories processing