---
title: "Test Decorators"
type: concept
tags: [python, testing, decorators]
sources: ["real-mode-testing-framework-integration-validation"]
last_updated: 2026-04-08
---

Decorators provided by the Testing Framework for controlling test execution across mock and real modes.


## Available Decorators
- **@dual_mode_test**: Test runs in both mock and real modes
- **@real_mode_only**: Test runs only in real mode (skips in mock)
- **@skip_in_real_mode**: Test skipped in real mode (runs in mock only)
- **@smart_patch**: Context manager for patching services conditionally

## Example
```python
@dual_mode_test
def test_api_call(self):
    # Executes in both modes
    result = self.gemini.generate_content("Hello")
    assert result is not None
```
