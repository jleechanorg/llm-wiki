---
title: "pytest_integration.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Pytest integration for the Real-Mode Testing Framework. Provides fixtures, markers, and utilities for running tests in either mock or real service modes.

## Key Claims
- Main fixtures: `service_provider` (shared), `isolated_service_provider` (fresh state), `firestore_client`, `gemini_client`, `auth_service`
- Custom markers: `@mock_only`, `@real_only`, `@expensive`, `@integration`, `@unit`
- Auto-skips tests based on mode: mock-only tests skipped in real mode, real-only skipped in mock mode
- Parametrized fixture `all_modes_service_provider` runs tests in both mock and real modes (skips real if no API keys)
- `skip_if_real_mode()` and `skip_if_mock_mode()` helper functions
- Session-level validation of test environment
- Example test functions demonstrating patterns

## Connections
- [[test_memory_integration]] — uses these fixtures