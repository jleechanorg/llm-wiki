---
title: "Pytest Integration"
type: source
tags: [testing, pytest, fixtures, markers]
sources: [mvp-site-pytest-integration]
last_updated: 2025-01-15
---

## Summary

Pytest-specific fixtures, markers, and utilities for the Real-Mode Testing Framework. Enables test filtering and parametrized mode testing.

## Key Claims

- **Mode-specific fixtures**: service_provider, firestore_client, gemini_client, auth_service
- **all_modes_service_provider**: Parametrized fixture for running tests in both mock and real modes
- **Custom markers**: mock_only, real_only, expensive, integration, unit
- **Auto-skip**: Tests automatically skipped based on TEST_MODE and markers
- **Session validation**: Validates test environment at session start

## Markers

| Marker | Purpose |
|--------|---------|
| mock_only | Skip in real mode |
| real_only | Skip in mock mode |
| expensive | Filter expensive tests |
| integration | Integration test |
| unit | Unit test |

## Connections

- [[mvp-site-fixtures]] - Core fixtures module
- [[mvp-site-testing-framework]] - Testing framework overview
