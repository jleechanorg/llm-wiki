---
title: "TestServiceProvider"
type: entity
tags: [python, testing, interface]
sources: ["real-service-provider-tests"]
last_updated: 2026-04-08
---

Interface/base class for test service providers. Defines contract for is_real_service, get_firestore, get_gemini, get_auth, and cleanup methods.

## Implementations
- [[RealServiceProvider]] — real implementation creating actual Google clients
- Mock test provider — mocked implementation for isolated testing

## Related
- [[RealServiceProvider]] — implements this interface
