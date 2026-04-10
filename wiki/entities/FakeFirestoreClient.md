---
title: "FakeFirestoreClient"
type: entity
tags: [testing, firestore, mocking]
sources: []
last_updated: 2026-04-08
---

## Description
Test utility from tests.fake_firestore that provides in-memory Firestore emulation for end-to-end tests without requiring real Firebase credentials.

## Usage
Used to mock Firestore database operations in integration tests, allowing tests to run in CI/CD without actual Firebase dependency.

## Related
- [[End2EndBaseTestCase]] - test base class using this mock
- [[FirestoreService]] - the real service being mocked
