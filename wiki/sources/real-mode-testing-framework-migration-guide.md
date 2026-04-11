---
title: "Real-Mode Testing Framework Migration Guide"
type: source
tags: [testing, migration, pytest, mock, real-services, dual-mode]
source_file: "raw/real-mode-testing-framework-migration-guide.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Guide for updating existing tests to support dual-mode operation, enabling tests to run with either mock or real services. Uses TEST_MODE environment variable to switch between mock (default), real, and capture modes.

## Key Claims
- **Minimal Migration**: Single import pattern with DualModeTestMixin for backward compatibility
- **Three Test Modes**: mock (default), real, and capture controlled via TEST_MODE env var
- **Service Provider Pattern**: Unified access to Firestore, Gemini, and Auth services across modes
- **Automatic Mode Detection**: smart_patch() automatically handles mock/real patching logic
- **Safety Limits**: Real mode includes automatic resource limits to prevent excessive API calls

## Key Concepts
- **DualModeTestMixin**: Mixin class enabling dual-mode support with single import
- **smart_patch()**: Context manager that auto-selects patching strategy based on mode
- **Capture Mode**: Records real service responses for analysis while maintaining test isolation

## Migration Patterns
1. **Class-Level**: Add DualModeTestMixin to existing test class
2. **Method-Level**: Use @dual_mode_test decorator with smart_patch
3. **Gradual Migration**: Progressive adoption with is_real flag for conditional logic

## Connections
- [[DualModeTesting]] — core testing paradigm
- [[TestServiceProvider]] — service abstraction layer
- [[BaseTestCase]] — pytest fixture providing service access
