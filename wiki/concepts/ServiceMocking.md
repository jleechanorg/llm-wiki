---
title: "Mocking Pattern"
type: concept
tags: [testing, mocking, isolation]
sources: ["god-mode-end-to-end-integration-tests"]
last_updated: 2026-04-08
---

## Description
Testing pattern where external dependencies are replaced with controlled mock implementations. This test file uses:

- [FakeFirestoreClient](../entities/FakeFirestoreClient.md) — mocks Firestore database operations
- [FakeLLMResponse](../entities/FakeLLMResponse.md) — mocks LLM API responses

## Benefits
- Fast test execution (no network calls)
- Deterministic results
- Test isolation from external services

## Related Concepts
- [TestIsolation](TestIsolation.md)
- [DependencyInjection](DependencyInjection.md)
- [[ServiceVirtualization]]
