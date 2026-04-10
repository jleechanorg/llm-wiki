---
title: "Mock Gemini Service"
type: concept
tags: [mock, testing, interface-parity, fixture]
sources: ["mock-gemini-service-wrapper"]
last_updated: 2026-04-08
---

## Description
Testing pattern that provides a mock implementation of an LLM service with identical interface to the production service. Enables tests to run without making actual API calls while maintaining the same code paths.

## Benefits
- **Isolation**: Tests run without external dependencies
- **Speed**: No network latency or API rate limits
- **Determinism**: Predefined responses enable repeatable test scenarios
- **Interface Parity**: Same function signatures allow seamless swapping

## Related Concepts
- [[StructuredFieldsFixtures]] — predefined test response data
- [[DualModeTesting]] — pattern for switching between mock and real backends
