---
title: "TestVisitCampaignEnd2End"
type: entity
tags: [testing, integration-test, campaign]
sources: []
last_updated: 2026-04-08
---

## Description
Test class verifying the full flow of visiting/reading an existing campaign through the application stack. Tests API endpoint behavior with mocked Firestore and authentication.

## Test Coverage
- Campaign retrieval from Firestore
- Game state loading
- Story entry persistence
- Auth bypass via TESTING_AUTH_BYPASS

## Related
- [End2EndBaseTestCase](End2EndBaseTestCase.md) - parent test class
- [GameState](GameState.md) - tested object
- [EpicDragonQuest](EpicDragonQuest.md) - sample campaign used in tests
