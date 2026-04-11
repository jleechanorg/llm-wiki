---
title: "End-to-End Visit Campaign Integration Test"
type: source
tags: [testing, end2end, integration, firestore, game-state, tdd]
source_file: "raw/end2end_visit_campaign_test.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end integration test for visiting an existing campaign. Uses complete mocking for external services (Firestore DB) and tests the full flow from API endpoint through all service layers. Only mocks external services - does not require real Firebase credentials.

## Key Claims
- **Test Target**: Visit/read existing campaign through full application stack
- **Mocking Strategy**: Complete Firestore mocking, no real credentials required
- **Test Framework**: unittest with unittest.mock.patch
- **Auth Bypass**: Uses TESTING_AUTH_BYPASS environment variable

## Test Setup Details
- Test campaign ID: test-campaign-789
- Test user ID: test-user-123
- Mock campaign: "Epic Dragon Quest"
- Mock game state includes Thorin the Bold (player character) and Gandalf (NPC companion)

## Mock Data Structure
- Campaign data with title, created_at, initial_prompt, selected_prompts
- GameState with player_character_data, npc_data, world_data, combat_state
- Story entries with sequence_id, mode, dice_rolls, resources, session_header, planning_block

## Connections
- Related to [[GameState]] - core game state object being tested
- Related to [[FirestoreService]] - mocked external service
- Related to [[End-to-End Testing]] - testing methodology used
