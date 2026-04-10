---
title: "Mock Service Pattern"
type: concept
tags: [testing, mock, service-wrapper, interface-parity]
sources: [mock-firestore-service-wrapper, test-migration-examples-mock-to-dual-mode]
last_updated: 2026-04-08
---

Testing pattern where a mock implementation provides the same interface as a production service. Allows tests to run against in-memory fake objects instead of real external dependencies (databases, APIs). Critical for [[RealModeTestingFramework]] dual-mode operation.

## Key Principles
- **Interface Parity**: Mock must match real service's function signatures exactly
- **Drop-in Replacement**: Code should not need to know it's using a mock
- **State Management**: Module-level singletons ensure consistent test state
