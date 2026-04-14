---
title: "Test Fixtures"
type: source
tags: [testing, pytest, fixtures, unittest]
sources: [mvp-site-fixtures]
last_updated: 2025-01-15
---

## Summary

Pytest and unittest fixtures for the Real-Mode Testing Framework. Provides seamless switching between mock and real services based on TEST_MODE.

## Key Claims

- **Service provider fixtures**: firestore_client, gemini_client, auth_service
- **Dual-mode support**: Automatically switches based on TEST_MODE env var
- **BaseTestCase**: Unittest base class with service provider integration
- **IsolatedTestCase**: Fresh provider per test for isolation
- **Compatibility mixin**: Helps migrate existing mock-based tests

## Pytest Fixtures

- service_provider: Provides appropriate provider based on TEST_MODE
- firestore_client: Firestore (mock or real)
- gemini_client: Gemini (mock or real)
- auth_service: Auth service (mock or real)
- test_mode: Current test mode string
- is_real_service: Boolean for real mode check

## Connections

- [[mvp-site-service-provider]] - Service provider implementation
- [[mvp-site-factory]] - Provider factory
