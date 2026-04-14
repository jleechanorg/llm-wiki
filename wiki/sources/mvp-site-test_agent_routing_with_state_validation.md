---
title: "test_agent_routing_with_state_validation.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Tests for agent routing with schema-validated state updates using overlay sanitization. Verifies that RewardsAgent and CharacterCreationAgent correctly match game state after overlay sanitization transforms raw updates into validated schema-conforming data.

## Key Claims
- sanitize_state_updates_overlay validates and transforms state updates before agent matching
- RewardsAgent matches when combat/encounter state shows encounter_completed with rewards_processed=false, or rewards_pending exists with level_up_available=true
- CharacterCreationAgent matches when character_creation_completed=false with level_up_pending/in_progress flags alongside rewards_pending.level_up_available

## Connections
- [[mvp-site-validation]] — defines sanitize_state_updates_overlay function
- [[mvp-site-agents]] — defines RewardsAgent and CharacterCreationAgent
- [[mvp-site-GameState]] — game state model for agent matching