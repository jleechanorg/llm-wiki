---
title: "DualModeTestMixin"
type: entity
tags: [python, testing, mixin]
sources: ["real-mode-testing-framework-integration-validation"]
last_updated: 2026-04-08
---

A unittest mixin enabling tests to execute in both mock and real modes. When combined with test classes, allows the same test logic to validate behavior against both mocked dependencies and real external APIs.

## Usage
```python
class TestBackwardsCompatibility(DualModeTestMixin, unittest.TestCase):
    def test_something(self):
        # Runs twice: once in mock mode, once in real mode
        pass
```
