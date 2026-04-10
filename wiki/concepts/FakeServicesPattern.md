---
title: "Fake Services Pattern"
type: concept
tags: [testing, mocking, design-pattern, integration-testing]
sources: [fake-services-unit-tests]
last_updated: 2026-04-08
---

A testing methodology where fake implementations of external services (databases, APIs, authentication) are created to enable isolated unit and integration testing without external dependencies.

## Why Use It
- **Speed**: No network calls or external service dependencies
- **Reliability**: Tests don't fail due to service outages or rate limits
- **Isolation**: Each test runs independently without shared state
- **CI/CD**: Works in environments without access to production services

## Implementation Requirements
- Match real service API surface
- Produce JSON-serializable output (no Mock objects)
- Support realistic data patterns
- Enable integration testing across services

## Connected Concepts
- [[FakeFirestoreClient]] — example implementation
- [[FakeFirebaseAuth]] — example implementation
- [[FakeLLMClient]] — example implementation
- [[IntegrationTesting]] — where this pattern is most valuable
- [[TestIsolation]] — principle this enables
