---
title: "Service Provider Pattern"
type: concept
tags: [design-pattern, dependency-injection, architecture]
sources: [mock-service-provider-tests]
last_updated: 2026-04-08
---

Design pattern providing a way to obtain service instances. Allows swapping between real and mock implementations for testing.

## Implementation
- Abstract interface defines service contract
- Concrete providers (real/mock) implement interface
- Consumer code receives provider via injection


## Related Concepts
- [[Mock Pattern]] — using mocks for testing
- [[Dependency Injection]] — broader inversion of control pattern
