---
title: "Scaffold Calculation"
type: concept
tags: [prompt-engineering, token-management, context-budgeting]
sources: [entity-tracking-budget-fix-end2end-test]
last_updated: 2026-04-08
---

## Definition

The process of calculating token budgets for all prompt components (system prompt, game state, entity tracking, narrative history) BEFORE generating the final prompt sent to the LLM.

## Key Components

1. **System prompt** - Base instructions
2. **Game state** - Current NPC data, resources, locations
3. **Entity tracking** - EntityPreloader output, entity instructions
4. **Narrative history** - Prior turns

## Budget Calculation

```
available_tokens = (max_context * 0.8) - system_prompt - entity_tracking_reserve
narrative_budget = available_tokens - game_state_tokens
```

The ENTITY_TRACKING_TOKEN_RESERVE is subtracted BEFORE narrative allocation, ensuring entity overhead never causes overflow.

## Related Concepts
- [[EntityTrackingBudget]] — the reserved portion
- [[ContextBudgeting]] — overall token management
- [[TokenEstimation]] — measurement method
