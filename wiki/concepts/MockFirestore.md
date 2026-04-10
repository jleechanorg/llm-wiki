---
title: "MockFirestore"
type: concept
tags: [testing, mock, firestore, database]
sources: ["mock-firestore-service-for-function-testing"]
last_updated: 2026-04-08
---

## Definition
Testing pattern that provides in-memory simulation of Firestore database operations without making actual API calls. Enables tests to run in isolation from external Firebase services.

## Implementation
- MockFirestoreDocument: mimics DocumentSnapshot with to_dict(), get(), exists, id
- MockFirestoreClient: provides get_campaigns_for_user, get_campaign_by_id, get_campaign_game_state

## Use Cases
- Unit testing Flask routes without Firebase dependency
- Integration testing with realistic data shapes
- CI/CD pipelines that cannot access real Firestore

## Related
- [[Test Fixtures]] — sample data (SAMPLE_CAMPAIGN, SAMPLE_GAME_STATE) used with mocks
- [[Dual-Mode Testing]] — switching between mock and real backends
