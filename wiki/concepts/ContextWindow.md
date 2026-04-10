---
title: "Context Window"
type: concept
tags: [llm, token-limit, context]
sources: ["context-components-reference", "context-budget-design-document"]
last_updated: 2026-04-08
---

## Description
The maximum number of tokens an LLM can process in a single request, determining how much context (system instructions, game state, story turns) can be included.

## Key Parameters
- **Safe Budget**: 90% of context window (20% reserved for output)
- **Model-specific limits**: Different models have different context windows

## WorldArchitect Implementation
- Uses 90% safety margin to reserve 20% for output generation
- Allocates remaining 80% across scaffold, entity tracking, and story budget
- Story budget further split: 25% start, 10% middle, 60% end

## Related Concepts
- [[Token Budget Allocation]] — how context window is divided
- [[Context Truncation]] — managing when context exceeds window
- [[Context Components Reference]] — detailed breakdown
