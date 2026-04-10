---
title: "Budget Allocation"
type: concept
tags: [token-budget, resource-management, context-compaction]
sources: ["tdd-test-fixed-size-component-overflow-crash"]
last_updated: 2026-04-08
---

## Summary
Budget allocation in the context compaction system divides a maximum token budget across multiple components (system_instruction, game_state_json, core_memories, story_context, checkpoint_block, sequence_id, entity_tracking). Some components are fixed-size while others can be reduced.

## Fixed-Size Components
- checkpoint_block: Preserved at original measured size
- sequence_id: Preserved at original measured size

## Flexible Components
- story_context: Can be reduced when other components exceed budget

## Overflow Handling
When total minimums exceed max_input_allowed, the system reduces flexible components (story_context) before reducing fixed-size components. This prevents crashes and allows the request to proceed.

## Related Concepts
- [[GracefulDegradation]]
- [[ContextCompaction]]
- [[TokenBudgetManagement]]
