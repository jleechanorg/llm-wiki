---
title: "Context Compaction"
type: concept
tags: [llm, optimization, token-budget, context-management]
sources: [story-context-tests-consolidated]
last_updated: 2026-04-08
---

## Definition
Process of managing LLM context windows by intelligently allocating token budgets across different context components (system instructions, game state, core memories, entity tracking, story context). The `_allocate_request_budget` function in context_compaction.py handles this allocation.

## Budget Components
- **system_instruction**: Base system prompt
- **game_state_json**: Current game state serialization
- **core_memories**: Persistent character/world memories
- **entity_tracking_estimate**: Active entities in scene
- **story_context**: Recent conversation turns

## Related Concepts
- [[TypeSafetyGuards]] — protects against malformed Firestore data
- [[WarningLogic]] — reports token reduction decisions
- [[TokenBudgetOptimization]] — maximizing useful context within limits
- [[MetaHarness]] — Meta-Harness searches over compaction strategies itself, optimizing WHAT to present rather than just making context fit
