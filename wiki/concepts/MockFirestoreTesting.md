---
title: "Mock Firestore Testing"
type: concept
tags: [testing, firestore, mocking, unit-tests, integration-tests]
sources: []
last_updated: 2026-04-08
---

## Description
Testing pattern using Firestore's mock client (`MOCK_SERVICES_MODE=true`) to run tests without connecting to actual Firebase/Firestore services. Enables fast, isolated testing of database operations.

## Key Patterns
- **Singleton behavior**: Mock `get_db()` returns same instance
- **Document persistence**: Documents persist across get_db() calls within same test
- **Reset capability**: `reset_mock_firestore()` clears state for clean test isolation

## Advantages
- No Firebase project required
- No network calls (instant tests)
- No authentication setup needed
- Full Firestore API coverage

## Related
- [[FirestoreService]] — module being tested
- [[UpdateCampaign]] — function tested with mocks
