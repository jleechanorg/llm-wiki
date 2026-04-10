---
title: "Dual-Mode Testing"
type: concept
tags: [testing, mock, real-mode, integration]
sources: [pytest-integration-real-mode-testing-framework]
last_updated: 2026-04-08
---

## Definition
Testing approach where tests run in both mock and real service modes, ensuring compatibility with actual API backends. In WorldArchitect.AI, controlled by TEST_MODE environment variable.

## Key Patterns
- **Fixture-based mode selection** — service_provider fixture returns mock or real based on TEST_MODE
- **Parametrized execution** — all_modes_service_provider runs each test twice (mock + real)
- **Marker-based filtering** — mock_only/real_only markers skip tests inappropriate for certain modes
- **Configuration guards** — _has_real_service_config() checks for required API keys

## Related Concepts
- [[Test Isolation]] — Using isolated_service_provider for fresh state
- [[Integration Testing]] — integration marker for integration-level tests
- [[Mock Service Provider Implementation]] — Provides the abstraction layer
