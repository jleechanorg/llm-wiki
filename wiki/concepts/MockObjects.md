---
title: "MockObjects"
type: concept
tags: [testing, mocks, test-doubles]
sources: []
last_updated: 2026-04-08
---

## Description
Test doubles that simulate external dependencies (databases, APIs, services) allowing tests to run in isolation without network calls or external dependencies.

## Key Mock Classes in This Project
- [[FakeFirestoreClient]] — mocks Firestore database
- [[FakeLLMResponse]] — mocks LLM provider responses

## Related Patterns
- [[StubObjects]]
- [[FakeObjects]]
- [[TestIsolation]]
