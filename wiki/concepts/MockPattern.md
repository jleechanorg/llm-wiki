---
title: "Mock Pattern"
type: concept
tags: [testing, design-pattern, mocks]
sources: [mock-service-provider-tests]
last_updated: 2026-04-08
---

Testing technique where mock objects simulate real dependencies. Enables isolated unit testing without external services (databases, APIs).

## Benefits
- Fast test execution (no network calls)
- Deterministic results
- No external dependencies for CI

## Related Concepts
- [[Service Provider Pattern]] — dependency injection for services
- [[Test Fixture]] — setup code for tests
