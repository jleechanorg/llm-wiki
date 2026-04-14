---
title: "MemGPT"
type: concept
tags: [MemGPT, memory-augmented-llm, context-management, retrieval]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

MemGPT is a memory-augmented large language model that uses a hierarchical memory system with different tiers of storage and retrieval. It is referenced in the Meta-Harness paper as related work in the area of adaptive retrieval and context management. MemGPT and similar systems explore how to manage limited context windows through intelligent memory management.

## Key Claims

- MemGPT uses a tiered memory system to extend effective context beyond fixed window limits
- Employs retrieval mechanisms to fetch relevant information from longer-term storage
- Related to Meta-Harness in that both address context management challenges
- RecursiveLM is another related system mentioned for adaptive retrieval

## Relationship to Meta-Harness

| Aspect | MemGPT | Meta-Harness |
|--------|--------|--------------|
| Goal | Extend context via memory tiers | Optimize harness code that manages context |
| Mechanism | Hierarchical memory retrieval | Filesystem-based history + agentic proposer |
| What is optimized | Retrieval strategy | What information to store, retrieve, and present |
| Novel contribution | Memory tiers | Full harness code search with 10M tokens |

## Connections

- [[MetaHarness]] — related by shared goal of managing context effectively
- [[MemoryAugmentedLLM]] — broader concept that MemGPT exemplifies
- [[ContextManagement]] — both MemGPT and Meta-Harness address context challenges
- [[FilesystemHistory]] — Meta-Harness uses filesystem rather than hierarchical memory
