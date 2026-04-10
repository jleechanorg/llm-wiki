---
title: "Backwards Compatibility"
type: concept
tags: [testing, migration, compatibility]
sources: [real-mode-testing-framework-integration-summary]
last_updated: 2026-04-08
---

Guarantee that existing tests continue to work unchanged when the Real-Mode Testing Framework is integrated. Zero breaking changes through mixins, decorators, and fallback mechanisms.

## Compatibility Strategies
- **Mixin inheritance**: DualModeTestMixin doesn't change test behavior
- **Decorator fallback**: @dual_mode_test works with existing tests
- **Environment detection**: TEST_MODE defaults to mock
- **Fallback mechanisms**: Handles missing dependencies gracefully

## Migration Options
1. **Minimal**: Add DualModeTestMixin, nothing else changes
2. **Gradual**: Conditional service selection per method
3. **Full**: Migrate to BaseTestCase with full features

## Related
- [[DualModeTestMixin]] — compatibility mechanism
- [[Migration Documentation]] — guidance for adoption
