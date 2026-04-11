---
title: "Test Fixtures for Pytest and Unittest"
type: source
tags: [python, testing, pytest, unittest, fixtures]
source_file: "raw/test-fixtures-pytest-unittest.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Provides test fixtures and base classes for seamless switching between mock and real services in the Real-Mode Testing Framework. Enables tests to run against either fake or live service implementations based on TEST_MODE environment variable.

## Key Claims
- **Pytest Fixtures**: `service_provider`, `firestore_client`, `gemini_client`, `auth_service`, `test_mode`, `is_real_service` fixtures for dependency injection
- **Unittest Base Classes**: `BaseTestCase` and `IsolatedTestCase` with automatic provider setup/teardown
- **Environment-Based Switching**: Tests automatically use mock or real services based on TEST_MODE env var
- **Isolation Support**: `IsolatedTestCase` provides fresh provider per test for complete isolation
- **Migration Helpers**: `get_test_client_for_mode()` supports gradual migration of existing tests

## Key Functions
### pytest fixtures
- `service_provider()` — yields TestServiceProvider based on TEST_MODE
- `firestore_client()` — provides Firestore client (mock or real)
- `gemini_client()` — provides Gemini client (mock or real)
- `auth_service()` — provides auth service (mock or real)
- `test_mode()` — returns current TEST_MODE value
- `is_real_service()` — boolean check for real service usage

### unittest base classes
- `BaseTestCase.setUp()` — initializes service provider, firestore, gemini, auth
- `BaseTestCase.tearDown()` — cleanup provider
- `IsolatedTestCase` — resets global provider before each test

### helper functions
- `setup_test_services(test_mode)` — manual service setup
- `cleanup_test_services(provider)` — manual cleanup
- `get_test_client_for_mode(test_mode)` — get dict with provider and clients

## Connections
- [[Service Provider Factory for Tests]] — factory pattern this builds on
- [[Fake Firestore Implementation]] — mock Firestore service
- [[Realistic Firebase Auth test doubles]] — mock Auth service
- [[Realistic LLM test doubles with response templates]] — mock LLM service
