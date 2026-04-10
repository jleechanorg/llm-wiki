---
title: "Component Compaction"
type: concept
tags: [llm, optimization, token-reduction]
sources: ["context-compaction-token-budget-allocation"]
last_updated: 2026-04-08
---

## Definition
The process of reducing oversized LLM request components to fit within allocated token budgets while preserving the most critical information.

## Compaction Strategies by Component
- **System Instruction**: No compaction unless exceeds 100k tokens, then emergency compression
- **Game State**: Priority-based dropping — low priority fields dropped first (completed_quests, quest_history, dialogue_history)
- **Core Memories**: Summarization and key fact extraction
- **Entity Tracking**: Scene-relevant NPC context only
- **Story Context**: Recent history truncation with key narrative beats preserved

## Priority Tiers for Game State
1. **Critical**: current_hp, max_hp, temp_hp, armor_class, current_location, in_combat, combat_participants, turn_order
2. **High**: inventory, active_quests, character_name, abilities, skills
3. **Medium**: world_data, world_events, reputation
4. **Low**: completed_quests, quest_history, dialogue_history

## Related Concepts
- [[TokenBudgetAllocation]]
- [[TokenEstimation]]
- [[ContextManagement]]
