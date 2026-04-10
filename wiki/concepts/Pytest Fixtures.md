---
title: "Pytest Fixtures"
type: concept
tags: [pytest, testing, fixtures, python]
sources: [pytest-integration-real-mode-testing-framework]
last_updated: 2026-04-08
---

## Definition
Pytest fixtures are functions providing test setup and teardown logic. In the Real-Mode Testing Framework, fixtures abstract service provider selection and provide clients for Firestore, Gemini, and Auth services.

## Framework Fixtures
| Fixture | Scope | Purpose |
|---------|-------|---------|
| test_mode | session | Get TEST_MODE from environment |
| service_provider | function | Main service provider |
| isolated_service_provider | function | Fresh state provider |
| firestore_client | function | Firestore client |
| gemini_client | function | Gemini client |
| auth_service | function | Auth service |
| is_real_service | function | Real mode check |
| test_services | function | All services dict |
| all_modes_service_provider | function | Parametrized dual-mode |
