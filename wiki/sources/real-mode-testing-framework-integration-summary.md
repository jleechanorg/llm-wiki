---
title: "Real-Mode Testing Framework Integration Summary"
type: source
tags: [testing, integration, pytest, unittest, fixtures, migration, quality-assurance]
source_file: "raw/real-mode-testing-framework-integration-summary.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Comprehensive integration framework enabling existing tests to run in both mock and real service modes. Provides pytest fixtures, unittest base classes, migration patterns, and safety features for seamless transition between testing environments without breaking existing test behavior.

## Key Claims
- **Dual-mode testing**: Tests run with mock services or real Firebase/Gemini services via environment variable
- **Zero breaking changes**: Existing tests work unchanged in mock mode with backwards compatibility
- **Resource management**: Automatic cleanup, test isolation, and cost protection for real-mode operations
- **Multiple integration patterns**: Mixins, decorators, fixtures, and base classes for different test styles
- **Migration documentation**: Comprehensive guides and examples for gradual test migration

## Key Components

### Test Fixtures (`fixtures.py`)
- Pytest fixtures for service providers, Firestore, Gemini client, Auth service
- unittest base classes (BaseTestCase, IsolatedTestCase)
- Manual setup functions for non-fixture usage

### unittest Integration (`integration_utils.py`)
- DualModeTestMixin for existing test classes
- @dual_mode_test decorator for individual methods
- SmartPatcher context manager for conditional patching
- Resource management helpers

### Pytest Integration (`pytest_integration.py`)
- Custom markers (@mock_only, @real_only, @expensive)
- Parametrized fixtures for cross-mode testing
- Automatic test skipping based on mode

## Safety Features
- Automatic cleanup after test runs
- Test isolation with unique collection names in real mode
- Resource limits for expensive operations
- Global provider state management
- Cost protection with configurable call limits

## Migration Approaches
- **Minimal**: Add DualModeTestMixin, existing methods unchanged
- **Gradual**: Conditional service selection per test method
- **Full**: Migrate to BaseTestCase with full framework features

## Connections
- [[Test Fixtures for Pytest and Unittest]] — related testing infrastructure
- [[Service Provider Factory for Tests]] — factory pattern for test providers
- [[Unified Fake Service Manager]] — consolidated fake services
- [[Fake Firestore Implementation]] — Firestore test double
- [[Realistic LLM test doubles]] — LLM test doubles

## Contradictions
- None identified
