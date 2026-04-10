---
title: "TestingFramework"
type: entity
tags: [python, testing, framework]
sources: ["real-mode-testing-framework-integration-validation"]
last_updated: 2026-04-08
---

A unified testing framework providing mock and real service modes for integration testing. Enables tests to run against either mocked dependencies or real external APIs by setting the TEST_MODE environment variable.

## Key Features
- **Service Provider Interface**: get_current_provider() returns mock or real services
- **Mode Switching**: Toggle between mock and real modes via environment variables
- **Service Isolation**: reset_global_provider() ensures clean state between tests
- **Backward Compatibility**: Legacy test attributes (test_firestore, test_gemini, test_auth) preserved

## Usage
```python
from testing_framework.fixtures import BaseTestCase
from testing_framework.integration_utils import dual_mode_test

class MyTest(BaseTestCase):
    @dual_mode_test
    def test_something(self):
        # Runs in both mock and real modes
        pass
```
