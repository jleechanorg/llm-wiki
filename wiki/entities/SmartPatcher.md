---
title: "SmartPatcher"
type: entity
tags: [testing, mocking, utility]
sources: [real-mode-testing-framework-integration-summary]
last_updated: 2026-04-08
---

Context manager for conditional patching that only applies mocks in mock mode. Enables tests to use real services in real mode while maintaining mock behavior in mock mode.

## Usage
```python
def test_method(self):
    with SmartPatcher('module.Class', mock_object):
        # Patched in mock mode, real in real mode
```

## Related
- [[DualModeTestMixin]] — often used together
- [[MockServiceProvider]] — default mock provider
