---
title: "Real-Mode Testing Framework Integration Tests"
type: source
tags: [python, testing, unittest, framework, integration, service-provider]
source_file: "raw/real-mode-testing-framework-integration-tests.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest suite validating core functionality of the Real-Mode Testing Framework without external dependencies. Tests service provider creation, mode switching (mock/real), global provider management, and backward compatibility helpers.

## Key Claims
- **Service Provider Creation**: get_service_provider("mock") creates TestServiceProvider with all services (Firestore, Gemini, Auth)
- **Mode Switching**: Framework supports switching between mock and real service modes
- **Global Provider Management**: get_current_provider returns singleton instance; reset_global_provider creates new instance
- **Backward Compatibility**: get_test_client_for_mode helper provides all expected service keys

## Key Code Patterns
```python
provider = get_service_provider("mock")
firestore = provider.get_firestore()
gemini = provider.get_gemini()
auth = provider.get_auth()
```

## Connections
- [[TestServiceProvider]] — core service provider class
- [[TestingFramework]] — the framework under test
- [[ServiceProviderPattern]] — architectural pattern being tested

## Contradictions
- None identified
