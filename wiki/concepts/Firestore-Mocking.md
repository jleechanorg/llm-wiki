---
title: "Firestore Mocking"
type: concept
tags: [testing, mocking, firestore, firebase]
sources: []
last_updated: 2026-04-08
---

## Description
Testing technique using FakeFirestoreClient to emulate Google Firestore database operations in tests without requiring real Firebase credentials or network access.

## Implementation
- Uses tests.fake_firestore.FakeFirestoreClient
- Patches firestore_service.get_db decorator
- Returns in-memory data matching Firestore API structure

## Related
- [[FakeFirestoreClient]] - the mock implementation
- [[FirestoreService]] - the real service being mocked
- [[End-to-End Testing]] - where this is used
