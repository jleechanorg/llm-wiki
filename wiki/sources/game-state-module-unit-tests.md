---
title: "GameState Module Unit Tests"
type: source
tags: [python, testing, unit-tests, game-state, mocking, firebase]
source_file: "raw/test_game_state.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Comprehensive unit tests for the GameState class and related functions in mvp_site.game_state module. Tests cover checkpoint validation, HP handling, and various calculation functions. Implements extensive mocking to handle CI environments lacking Firebase dependencies.

## Key Claims
- **Comprehensive mocking**: Uses MagicMock and module patching to simulate firebase_admin, pydantic, cachetools, google, and other optional dependencies
- **Test environment setup**: Sets TESTING_AUTH_BYPASS, USE_MOCKS, and GEMINI_API_KEY environment variables before imports
- **Module imports**: Tests import from mvp_site.game_state, mvp_site.firestore_service, mvp_site.dice, mvp_site.world_logic
- **Test class structure**: Contains TestGameState class with test methods like test_validate_checkpoint_consistency_dict_location_bug

## Key Quotes
> "CRITICAL FIX: Mock firebase_admin completely to avoid google.auth namespace conflicts"

## Connections
- [[GameState]] — main class being tested
- [[FirestoreService]] — mocked module under mvp_site.firestore_service
- [[WorldLogic]] — module being tested alongside game_state

## Contradictions
- None identified
