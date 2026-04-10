---
title: "Global Provider Management"
type: concept
tags: [testing, singleton, architecture]
sources: ["real-mode-testing-framework-integration-tests"]
last_updated: 2026-04-08
---

Pattern for managing a singleton TestServiceProvider instance across test execution. Implemented via get_current_provider() and reset_global_provider() functions.

## Behavior
- **get_current_provider()**: Returns the global singleton provider instance
- **reset_global_provider()**: Clears global state and allows new instance creation
- **Same instance**: Multiple calls to get_current_provider() return identical object
- **Different after reset**: After reset, new calls return different instance

## Use Cases
- Sharing provider across multiple test functions
- Ensuring clean state between test runs
- Backward compatibility via get_test_client_for_mode() helper

## Related
- [[TestingFramework]]
- [[TestServiceProvider]]
