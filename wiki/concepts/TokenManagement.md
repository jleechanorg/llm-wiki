---
title: "Token Management"
type: concept
tags: [tokens, context-window, budget, backstory]
sources: [llm-service-ai-integration-response-processing, context-compaction]
last_updated: 2026-04-08
---

System for managing token limits to prevent backstory cutoffs in LLM responses. Includes context compaction, budget allocation, and filtering mechanisms.

## Key Components
- **Context Compaction**: Reduces context size while preserving essential information
- **Budget Allocation**: Distributes available tokens across story context, system prompts, and other components
- **Token Counting**: Tracks token usage across different prompt sections
- **Backstory Protection**: FIXED token limit management specifically to prevent backstory cutoffs

## Related Systems
- [[Context Compaction]] — reduces context size
- [[Game State Schema]] — state representation for token estimation
