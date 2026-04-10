---
title: "MockServiceProvider"
type: entity
tags: [testing, mock, service-provider]
sources: [mock-service-provider-tests]
last_updated: 2026-04-08
---

Mock service provider implementation used in testing. Provides mock instances of Firestore and LLM clients without connecting to real services.

## Used In
- Unit tests for service layer
- E2E test fixtures
- CI/CD test pipelines

## Related Entities
- [[MockFirestoreClient]] — mock Firestore implementation
- [[MockLLMClient]] — mock LLM client
- [[TestServiceProvider]] — interface being implemented
