---
title: "Service Provider Factory"
type: concept
tags: [testing, factory, architecture]
sources: [real-mode-testing-framework-integration-summary]
last_updated: 2026-04-08
---

Factory pattern implementation (get_service_provider) that instantiates the appropriate TestServiceProvider based on TEST_MODE environment variable or explicit parameter.

## Factory Behavior
```python
# Auto-detect from TEST_MODE
provider = get_service_provider()

# Explicit mode selection
provider = get_service_provider('mock')    # MockServiceProvider
provider = get_service_provider('real')     # RealServiceProvider
provider = get_service_provider('capture') # Capture mode
```

## Related
- [[TestServiceProvider]] — produced abstract type
- [[MockServiceProvider]] — mock product
- [[RealServiceProvider]] — real product
