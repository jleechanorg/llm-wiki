---
title: "Context Compaction"
type: source
tags: [token-budget, memory-management, llm-optimization]
sources: [mvp-site-context-compaction]
last_updated: 2025-01-15
---

## Summary

Token budget allocation and component compaction system for LLM requests. Ensures story context quality while preventing any single component from consuming excessive tokens. Implements a min-first, fill-to-max allocation strategy.

## Key Claims

- **Min-first allocation**: 68% of budget allocated to minimums across components
- **Priority fill-to-max**: Remaining 32% distributed by priority (system_instruction > game_state > core_memories > entity_tracking > story_context)
- **Guaranteed story minimum**: Story context gets at least 30% (15% absolute floor in emergencies)
- **Component-specific compaction**: Different strategies for system instruction, game state, core memories, entity tracking
- **Budget warnings**: Generates UI warnings for budget warnings (persisted to avoid repeat displays)

## Budget Percentages

| Component | Min | Max | Notes |
|-----------|-----|-----|-------|
| system_instruction | 10% | 50% | No compact unless >100k tokens |
| game_state | 5% | 20% | Compact by dropping low-priority fields |
| core_memories | 20% | 30% | Keep CRITICAL + recent entries |
| entity_tracking | 3% | 15% | Uses tiering (active/present/dormant) |
| story_context | 30% | 60% | Gets leftover budget, can expand |

## Connections

- [[mvp-site-llm-service]] - Main LLM orchestration
- [[mvp-site-token-utils]] - Token estimation
- [[mvp-site-memory-utils]] - Memory formatting for prompts
