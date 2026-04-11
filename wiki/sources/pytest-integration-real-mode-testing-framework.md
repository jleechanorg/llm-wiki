---
title: "Pytest Integration for Real-Mode Testing Framework"
type: source
tags: [pytest, testing, fixtures, mock-mode, real-mode, integration]
source_file: "raw/pytest_integration.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Pytest-specific fixtures, markers, and utilities for the Real-Mode Testing Framework. Provides seamless switching between mock and real service backends via TEST_MODE environment variable, with parametrized fixtures for running tests in both modes.

## Key Claims
- **Environment-Based Mode Switching** — Tests run in mock or real mode based on TEST_MODE env var (defaults to "mock")
- **Service Provider Abstraction** — get_service_provider() returns appropriate provider (mock or real) based on mode
- **Parametrized Dual-Mode Testing** — all_modes_service_provider fixture runs each test in both mock and real modes
- **Marker-Based Test Filtering** — Custom markers (mock_only, real_only, expensive, integration, unit) control test execution

## Key Fixtures
| Fixture | Purpose |
|---------|---------|
| test_mode | Returns TEST_MODE env var value |
| service_provider | Main fixture providing TestServiceProvider |
| isolated_service_provider | Fresh state for critical isolation |
| firestore_client | Firestore client (mock or real) |
| gemini_client | Gemini client (mock or real) |
| auth_service | Auth service (mock or real) |
| is_real_service | Boolean check for real mode |
| all_modes_service_provider | Parametrized fixture for dual-mode |

## Key Markers
- **mock_only** — Skip in real mode
- **real_only** — Skip in mock mode
- **expensive** — Flag expensive real-mode tests
- **integration** — Integration test marker
- **unit** — Unit test marker

## Configuration Check
Real mode requires both GOOGLE_APPLICATION_CREDENTIALS and GEMINI_API_KEY environment variables.

## Connections
- [[Real-Mode Testing Framework Migration]] — Framework this pytest integration supports
- [[Mock Service Provider Implementation]] — Underlying service provider abstraction
- [[Mock Firestore Service Wrapper]] — Firestore mock implementation
- [[Mock Gemini Service wrapper]] — Gemini mock implementation
