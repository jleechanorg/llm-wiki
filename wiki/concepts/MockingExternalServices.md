---
title: "Mocking External Services"
type: concept
tags: [testing, mocking, integration]
sources: ["campaign-creation-end2end-tests"]
last_updated: 2026-04-08
---

Testing technique where external dependencies (APIs, databases, third-party services) are replaced with test doubles that return controlled responses. Allows testing without network calls or external credentials.

## Implementation
In the campaign creation tests, mocking is done via:
- `@patch` decorators on `mvp_site.firestore_service.get_db`
- `@patch` decorators on `mvp_site.llm_service._call_llm_api_with_llm_request`
- Fake implementations like `FakeFirestoreClient` and `FakeLLMResponse`

## Benefits
- Fast test execution (no network I/O)
- Deterministic results
- No external credentials required
- Can simulate error conditions

## Related
- [[TestFixtures]] — reusable test data and helpers
- [[ServiceLayerTesting]] — testing service integration points
