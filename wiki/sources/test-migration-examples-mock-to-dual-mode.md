---
title: "Test Migration Examples - Mock to Dual-Mode"
type: source
tags: [testing, pytest, migration, mock, service-provider]
source_file: "raw/test-migration-examples-mock-to-dual-mode.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Documentation showing how to update existing tests from traditional mock-only approach to dual-mode testing that supports both mock and real service backends. Demonstrates before/after patterns using BaseTestCase and service provider injection.

## Key Claims
- **Service Provider Pattern**: BaseTestCase provides `self.gemini`, `self.firestore`, `self.auth` that work in both mock and real modes
- **Mode Detection**: `self.is_real` flag allows conditional logic to skip patching in real mode
- **Pytest Compatibility**: Both unittest-style and pytest-style migration examples provided
- **Backward Compatibility**: Original mock-only tests continue to work; dual-mode is additive
- **Environment Variable Control**: Uses TEST_MODE env var to switch between mock/real backends

## Key Quotes
> "BEFORE: Hardcoded mocks, only works in mock mode"
> "AFTER: Use service provider - works with mock OR real services"

## Connections
- [[BaseTestCase]] — base class enabling dual-mode testing
- [[TestServiceProvider]] — abstraction layer for service switching
- [[RealModeTestingFramework]] — framework this migration pattern supports
- [[TestFixtures]] — fixtures module providing mode selection

## Contradictions
- None identified
