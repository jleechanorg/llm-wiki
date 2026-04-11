---
title: "Firestore Mocking in Unit Tests"
type: source
tags: [python, testing, firestore, mocking, unit-tests, magicmock]
source_file: "raw/test_firestore_mocking.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Demonstrates proper Firestore client mocking in unit tests using MagicMock and unittest.patch. Validates that get_db() can be mocked at the function level to provide controlled Firestore behavior for isolated testing without external dependencies.

## Key Claims
- **get_db() mocking works**: The get_db() function in firestore_service can be properly mocked using @patch decorator for isolated tests
- **Mock chain setup**: Mock Firestore operations require chaining client → collection → document → get()
- **Mock preserves interface**: MagicMock provides the expected Firestore interface (collection, batch methods)
- **Context manager isolation**: Using patch as context manager provides test isolation

## Key Quotes
> "Firebase is now always enabled, so we mock get_db() directly"

## Connections
- [[Firestore]] — the Firebase database being mocked
- [[FirestoreService]] — module containing get_db() function
- [[UnitTesting]] — the testing methodology used

## Contradictions
- None identified
