---
title: "In-Memory Database Simulation"
type: concept
tags: [testing, in-memory, database, simulation]
sources: ["mock-firestore-service-for-function-testing"]
last_updated: 2026-04-08
---

## Definition
Testing technique that uses in-memory data structures (dictionaries, lists) to simulate database behavior. Provides fast, reproducible test execution without external dependencies.

## Characteristics
- **Storage**: Uses dict for collections (campaigns, game_states, story_logs)
- **Operation Tracking**: Counts operations and records last_operation for verification
- **Sample Data**: Pre-initializes with realistic test fixtures

## Advantages
- No network calls = fast tests
- No Firebase project required
- Deterministic results
- Easy state reset between tests

## Related
- [[MockFirestore]] — specific implementation for Firestore
- [[Test Fixtures]] — SAMPLE_CAMPAIGN, SAMPLE_GAME_STATE constants
