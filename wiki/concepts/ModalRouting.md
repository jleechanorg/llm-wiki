---
title: "Modal Routing"
type: concept
tags: [modal, routing, game-logic]
sources: ["modal-routing-fixtures", "modal-state-management-integration-tests"]
last_updated: 2026-04-08
---

## Definition
The process of determining which agent (LevelUpAgent or CharacterCreationAgent) should handle user input based on current game state.

## Key Mechanisms
- `get_agent_for_input()` function routes input to appropriate modal agent
- Considers custom_campaign_state, rewards_pending, and player_character_data
- Returns agent class and metadata tuple

## Invariants
- Routing and finish-choice injection must agree on modal active state
- Only one modal should be active at a time (mutual exclusion)
- Stale flags must be cleared on state transitions

## Related Concepts
- [[ModalInjection]] — finish choice injection logic
- [[ModalStateManagement]] — overall modal state handling
