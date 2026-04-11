---
title: "NPC Death State Persistence E2E Tests"
type: source
tags: [python, testing, e2e, npc, death-state, firestore, integration]
source_file: "raw/test_npc_death_state_e2e.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end integration test for NPC death state persistence. Tests verify that when a user kills an NPC (e.g., Marcus), the death state is properly synced between combat_state and npc_data across the full application stack from API endpoint through service layers.

## Key Claims
- **Death state synchronization**: When NPC is killed (hp_current: 0), they are removed from combat but preserved in npc_data with dead status
- **Subsequent turn behavior**: Dead NPCs should not be offered as targets in subsequent turns
- **Full stack coverage**: Tests the complete flow from /api/campaigns/{id}/interaction endpoint through all service layers
- **Low-level mocking**: Only mocks external services (LLM provider APIs and Firestore DB) at the lowest level

## Key Test Structure
- `TestNPCDeathStateEnd2End`: Main test class extending End2EndBaseTestCase
- `_setup_campaign_with_combat()`: Sets up campaign with active combat and named NPC "Marcus"
- Verifies NPC is removed from combat but preserved in npc_data

## Connections
- [[End2EndBaseTestCase]] — base test class providing Flask test client setup
- [[FakeFirestoreClient]] — mock Firestore for campaign/game state persistence
- [[FakeLLMResponse]] — mock LLM provider for AI response generation
- [[NPC Death State Persistence]] — concept for death state synchronization between combat and npc_data

## Contradictions
- None identified
