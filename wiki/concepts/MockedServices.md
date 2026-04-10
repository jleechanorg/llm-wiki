---
title: "Mocked Services"
type: concept
tags: [testing, mocking, firebase, test-doubles]
sources: ["common-test-utilities"]
last_updated: 2026-04-08
---

## Definition
Mocked services are test doubles that replace real external dependencies (like Firebase) with fake implementations during testing.

## Why Use Mocked Services
- **Isolation**: Tests run independently of external services
- **Speed**: No network calls or rate limits
- **Reliability**: No flakiness from external service outages
- **Repeatability**: Consistent, deterministic test results

## Implementation Pattern
The project uses complete mocking for end-to-end tests, ensuring `has_firebase_credentials()` returns `False` so tests never accidentally call real Firebase APIs.

## Related Concepts
- [[FirebaseCredentials]] — What gets mocked
- [[UnitTests]] — Test type that commonly uses mocks
- [[IntegrationTests]] — Tests that may use real services

## Sources
- [[CommonTestUtilities]]
