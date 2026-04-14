---
title: "Migration Examples"
type: source
tags: [testing, migration, patterns]
sources: [mvp-site-migration-examples]
last_updated: 2025-01-15
---

## Summary

Examples showing how to update existing tests to support dual modes (mock and real services). Demonstrates before/after patterns for common test scenarios.

## Key Claims

- **Before/After patterns**: Shows mock-only to dual-mode migration
- **BaseTestCase usage**: Modern test class with service provider
- **Gradual migration**: Step-by-step migration approach
- **Compatibility helpers**: MockCompatibilityMixin for legacy tests
- **Real mode safety**: Resource limits and isolation patterns

## Migration Pattern

1. Add service provider fixture
2. Replace manual patches with service provider
3. Add cleanup in finally block
4. Use compatibility mixin for minimal changes

## Connections

- [[mvp-site-fixtures]] - Service provider fixtures
- [[mvp-site-testing-framework]] - Testing framework
