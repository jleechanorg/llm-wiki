---
title: "Global Pytest Configuration for MVP Site Tests"
type: source
tags: [pytest, testing, configuration, mocks, dev-mode]
source_file: "raw/global-pytest-configuration-mvp-site-tests.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python configuration file that ensures mvp_site tests run with mock services and dev-mode-safe settings. Prevents real network calls to Gemini/Firebase and avoids clock-skew validation errors during test execution.

## Key Claims
- **Environment Force-Setting**: Sets TESTING_AUTH_BYPASS, USE_MOCKS, MOCK_SERVICES_MODE, and WORLDAI_DEV_MODE to true for all tests
- **API Key Mocking**: Provides dummy API keys (test-api-key) to satisfy libraries that check for presence
- **Flask Module Loading**: Ensures the real Flask module is loaded, not a mock, for tests that monkeypatch sys.modules
- **Network Call Prevention**: Blocks real Gemini and Firebase calls during test execution

## Key Quotes
- "Ensures test runs use mock services and dev-mode-safe settings, preventing real network calls"

## Connections
- [[TestConfigurationManagement]] — related test configuration approach
- [[CaptureFrameworkDocumentation]] — related testing framework for capturing real service interactions

## Contradictions
- None
