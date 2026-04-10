---
title: "Mock vs Real Mode Testing"
type: concept
tags: [testing, mock, integration-testing]
sources: ["real-mode-testing-framework-integration-tests"]
last_updated: 2026-04-08
---

Testing methodology allowing tests to run against either mock implementations or real external services. The TestingFramework supports mode switching via get_service_provider("mock") or get_service_provider("real").

## Mode Comparison
| Aspect | Mock Mode | Real Mode |
|-------|-----------|-----------|
| Services | In-memory implementations | Actual Firebase/Gemini |
| Dependencies | None | Requires credentials |
| Speed | Fast | Slower |
| Reliability | High | Variable |

## Usage
```python
# Mock mode (default for tests)
mock_provider = get_service_provider("mock")

# Real mode (requires credentials)
real_provider = get_service_provider("real")
```

## Related
- [[TestingFramework]]
- [[TestServiceProvider]]
