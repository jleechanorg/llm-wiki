---
title: "Real-Mode Testing Framework Integration Validation Tests"
type: source
tags: [python, testing, integration, framework, dual-mode]
source_file: "raw/test_real_mode_framework_integration.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Validation test suite ensuring the Real-Mode Testing Framework integrates correctly with existing tests and maintains backwards compatibility. Tests verify service access (Firestore, Gemini, Auth), dual-mode operations, and decorator compatibility across mock and real execution modes.

## Key Claims
- **Framework provides unified interface**: get_current_provider() returns either mock or real services based on TEST_MODE environment variable
- **Mock mode is default for testing**: Tests run safely without external dependencies by setting TEST_MODE=mock
- **Seamless mode switching**: Same test code works with both mock and real services by changing environment variables
- **Service isolation**: reset_global_provider() ensures clean state between tests
- **Backward compatibility attributes**: test_firestore, test_gemini, test_auth available for legacy test patterns
- **DualModeTestMixin enables dual execution**: Tests can run in both mock and real modes via decorator

## Key Quotes
> "All services should be accessible through the framework" — validates service availability in both modes

> "Same test code works with both mock and real services by changing environment variables" — demonstrates seamless mode switching

## Connections
- [[TestingFramework]] — the overarching framework this test validates
- [[DualModeTestMixin]] — mixin class enabling dual-mode test execution
- [[BaseTestCase]] — base test case class providing service fixtures
- [[RealModeTesting]] — concept of running tests against actual APIs vs mocks

## Contradictions
- None identified
