---
title: "Context Compaction - Token Budget Allocation and Component Compaction"
type: source
tags: [llm, token-budget, context-management, performance-optimization]
source_file: "raw/context-compaction-token-budget-allocation.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module implementing component-level token budget allocation for LLM requests in WorldArchitect.AI, ensuring story context quality while preventing any single component from consuming excessive tokens. Uses a min-first, fill-to-max allocation strategy that guarantees story context gets at least 30% of the token budget.

## Key Claims
- **Token Budget Strategy**: Min-first, fill-to-max allocation ensuring guaranteed minimums (68% total) before discretionary allocation (32%)
- **Story Context Guarantee**: Story context receives guaranteed 30% minimum, can expand to 60% if other components are small
- **Component Compaction**: Oversized components compacted using component-specific strategies, except system instruction (unless >100k tokens)
- **Priority-Based Fill**: Fill-to-max allocates remaining budget in priority order: system_instruction > game_state > core_memories > entity_tracking > story_context
- **Game State Priority Tiers**: Critical, high, medium, and low priority fields determine what gets dropped first during compaction

## Key Budget Percentages
| Component | Min | Max | Notes |
|-----------|-----|-----|-------|
| System Instruction | 10% | 50% | No compaction unless >100k tokens |
| Game State | 5% | 20% | Compact if over |
| Core Memories | 20% | 30% | Compact if over |
| Entity Tracking | 3% | 15% | Compact if over |
| Story Context | 30% | 60% | Guaranteed 30% min, gets leftovers |

## Key Quotes
- "The functions here implement a min-first, fill-to-max allocation strategy that guarantees story context gets at least 30% of the token budget"
- "Allocate token budgets across LLM request components (min/max constraints)"
- "Compact oversized components using component-specific strategies"

## Connections
- [[Token Estimation]] — token_utils module for measuring component sizes
- [[LLM Service Architecture]] — extracted from llm_service.py to isolate budget logic
- [[Game State Management]] — priority tiers determine what gets dropped during compaction

## Contradictions
- []
