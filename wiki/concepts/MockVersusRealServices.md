---
title: "Mock vs Real Services in Testing"
type: concept
tags: [testing, mocking, integration-testing, service-abstraction, test-isolation]
sources: [test-service-provider-abstract-base-class, integration-test-runner-real-api-calls]
last_updated: 2026-04-08
---

## Summary
Testing strategy that supports both mocked (fake) and real service implementations. The mock version ensures test isolation and speed, while the real version validates actual API integration.

## Trade-offs

| Aspect | Mock Services | Real Services |
|--------|--------------|---------------|
| Speed | Fast (in-memory) | Slow (network I/O) |
| Reliability | Deterministic | Depends on external APIs |
| Coverage | Limited to mocked behavior | Full integration coverage |
| Isolation | Complete | May have side effects |
| Debugging | Easy | Harder (network issues) |

## Best Practices
- **Unit tests**: use mocks for speed and isolation
- **Integration tests**: use real services for accurate validation
- **Hybrid approach**: mock for setup/isolation, real for final validation
- **Cleanup**: always clean up real service state between tests

## Connection to TestServiceProvider
The TestServiceProvider ABC encapsulates both modes:
- is_real_service property indicates current mode
- cleanup() method ensures test isolation with real services
- Same interface works for both mock and real implementations

## Related Concepts
- [[Test Service Provider Abstract Base Class]] — the interface definition
- [[Real Service Provider Implementation]] — real service concrete implementation
- [[Integration Testing]] — testing with real external dependencies
