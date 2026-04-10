---
title: "Resource Management"
type: concept
tags: [testing, infrastructure, safety]
sources: [real-mode-testing-framework-integration-summary]
last_updated: 2026-04-08
---

Safety mechanisms in the Real-Mode Testing Framework preventing resource exhaustion and controlling costs when testing against real services.

## Features
- **Automatic cleanup**: provider.cleanup() called after tests
- **Test isolation**: Unique collection names prevent conflicts
- **Resource limits**: Max operations per test
- **Cost protection**: Configurable call limits for API quotas

## Usage
```python
def test_expensive_operation(self):
    if self.is_real:
        max_calls = 3  # Limit in real mode
    else:
        max_calls = 100  # No limits in mock mode
```

## Related
- [[Real-Mode Testing]] — where resource management is critical
- [[TestServiceProvider]] — provides cleanup interface
