---
title: "Framework Validation Tests"
type: source
tags: [python, testing, service-provider, mock-framework, integration-tests]
source_file: "raw/framework-validation-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Framework validation script demonstrating all TestServiceProvider components working together. Tests validate MockServiceProvider functionality, RealServiceProvider configuration validation, factory mode switching between mock/real/capture modes, and global provider state management.

## Key Claims
- **MockServiceProvider provides mock Firestore, Gemini, and Auth services** for isolated testing
- **RealServiceProvider validates configuration** — raises ValueError if required API keys are missing
- **Factory switching supports multiple modes**: mock, real, capture, and invalid mode rejection
- **Global provider state management**: get_current_provider() returns singleton, set_service_provider() overrides, reset_global_provider() clears

## Key Test Cases
1. validate_mock_provider() — Tests mock service creation and operations
2. validate_real_provider_validation() — Tests config validation raises ValueError without API key
3. validate_factory_switching() — Tests mode switching between mock/real/capture
4. validate_global_provider_management() — Tests singleton pattern and state management

## Connections
- [[TestServiceProvider]] — core testing framework
- [[ServiceProviderFactory]] — factory pattern implementation
