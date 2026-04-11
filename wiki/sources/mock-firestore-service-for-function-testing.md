---
title: "Mock Firestore Service for Function Testing"
type: source
tags: [python, firestore, mock, testing, in-memory]
source_file: "raw/mock-firestore-service-for-function-testing.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing in-memory Firestore simulation for testing without making actual Firestore calls. Implements MockFirestoreDocument and MockFirestoreClient classes that replicate the real Firestore API behavior, enabling tests to run in isolation from external services.

## Key Claims
- **Interface Parity**: MockFirestoreClient mimics the real Firestore client API for seamless swapping in tests
- **In-Memory Storage**: Uses dictionaries to store campaigns, game_states, and story_logs
- **Operation Tracking**: Tracks operation_count and last_operation for test verification
- **Sample Data Initialization**: Automatically initializes with SAMPLE_CAMPAIGN, SAMPLE_GAME_STATE, and SAMPLE_STORY_CONTEXT
- **Nested Field Support**: MockFirestoreDocument.get() handles dot-notation paths like "player.name"

## Key Classes
- **MockFirestoreDocument**: Simulates DocumentSnapshot with to_dict(), get(), exists, and id properties
- **MockFirestoreClient**: Main client with campaigns, game_states, and story_logs storage

## Key Methods
- **get_campaigns_for_user()**: Retrieves all campaigns for a user with operation tracking
- **get_campaign_by_id()**: Fetches campaign and story context by ID
- **get_campaign_game_state()**: Returns game state document for a campaign

## Connections
- Related to [[Mock Firestore Service Wrapper]] — provides the underlying mock implementation
- Used by [[Real-Mode Testing Framework]] — enables dual-mode testing with mock/real switching
- Follows pattern from [[Test Fixtures for Pytest and Unittest]] — uses sample data fixtures

## Contradictions
- None identified
