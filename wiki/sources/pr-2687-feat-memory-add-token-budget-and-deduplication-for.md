---
title: "PR #2687: feat(memory): Add token budget and deduplication for core memories"
type: source
tags: []
date: 2025-12-28
source_file: raw/prs-worldarchitect-ai/pr-2687.md
sources: []
last_updated: 2025-12-28
---

## Summary
Implements token budget and deduplication for core memories to prevent context overflow in long-running campaigns.

### Problem
- Core memories grow unbounded (800+ observed in production campaigns)
- ALL memories sent to LLM every turn, consuming entire context window
- Near-duplicate memories waste tokens
- Previous 180-char truncation was too aggressive

### Solution

| Feature | Implementation | Benefit |
|---------|----------------|---------|
| Token budget | `select_memories_by_budget()` -

## Metadata
- **PR**: #2687
- **Merged**: 2025-12-28
- **Author**: jleechan2015
- **Stats**: +971/-11 in 5 files
- **Labels**: none

## Connections
