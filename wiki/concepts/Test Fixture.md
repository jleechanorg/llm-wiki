---
title: "Test Fixture"
type: concept
tags: [testing, pytest, fixtures]
sources: [real-mode-testing-framework-integration-summary]
last_updated: 2026-04-08
---

Pre-configured test resources (service providers, clients, mock objects) injected into tests via pytest fixtures. The framework provides fixtures for service_provider, firestore_client, gemini_client, and auth_service.

## Provided Fixtures
- `service_provider`: Main TestServiceProvider instance
- `firestore_client`: Firestore client (mock or real)
- `gemini_client`: Gemini client (mock or real)
- `auth_service`: Auth service (mock or real)

## Usage
```python
def test_something(service_provider):
    firestore = service_provider.get_firestore()
    # Works in both mock and real modes
```

## Related
- [[Pytest Integration]] — pytest-specific fixture system
- [[TestServiceProvider]] — underlying abstraction
