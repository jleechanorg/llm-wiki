---
title: "Agent Routing Tests with Schema Validation"
type: source
tags: [python, testing, unittest, agent-routing, schema-validation]
source_file: "raw/agent-routing-schema-validation-tests.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest file testing agent routing based on schema-validated state updates. Uses CharacterCreationAgent and RewardsAgent with GameState and sanitize_state_updates_overlay for overlay sanitization.

## Key Claims
- **Rewards Agent Matching**: RewardsAgent.matches_game_state correctly identifies when combat/rewards state is ready after overlay sanitization
- **Encounter Fields**: Validates encounter_completed, rewards_processed, and rewards_pending fields work together
- **Character Creation**: CharacterCreationAgent.matches_game_state validates level_up_pending and character_creation_completed flags
- **Overlay Sanitization**: sanitize_state_updates_overlay processes updates without errors for routing logic

## Key Quotes
> "Test rewards agent matches after overlay sanitization" — validates RewardsAgent matching
> "Test character creation agent matches level_up flags after sanitization" — validates CharacterCreationAgent matching

## Connections
- [[RewardsAgent]] — the agent being tested
- [[CharacterCreationAgent]] — the agent being tested
- [[GameState]] — the state object being validated
- [[SchemaValidation]] — the sanitization process being tested

## Contradictions
- None identified
