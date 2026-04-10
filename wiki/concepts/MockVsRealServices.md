---
title: "Mock vs Real Services Pattern"
type: concept
tags: [testing, mocking, integration-testing]
sources: [test-fixtures-pytest-unittest]
last_updated: 2026-04-08
---

A testing pattern where tests can run against either mock (fake) service implementations or real service implementations based on environment configuration. The TEST_MODE environment variable controls which implementation is used.

Benefits:
- **Fast feedback**: Mock mode runs quickly without external dependencies
- **Integration validation**: Real mode catches issues with actual service implementations
- **CI/CD flexibility**: Run mocks in PR checks, real services in nightly builds

Implementation in [[Test Fixtures for Pytest and Unittest]] uses TestServiceProvider to abstract the switch.
