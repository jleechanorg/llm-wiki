---
title: "TestServiceProvider"
type: concept
tags: [testing, framework, service-provider, mock-mode]
sources: ["service-provider-framework-integration-tests", "framework-validation-tests"]
last_updated: 2026-04-08
---

## Definition
A testing framework that provides unified access to services (Firestore, Gemini, Auth) with switchable mock/real modes through a single provider interface.

## Key Methods
- `get_current_provider()` — returns the appropriate provider based on TEST_MODE
- `reset_global_provider()` — resets global state between tests
- `provider.get_firestore()` / `provider.get_gemini()` / `provider.get_auth()` — service accessors
- `provider.is_real_service` — boolean indicating current mode

## Use Cases
- CI environments requiring isolated tests without external APIs
- Development testing with realistic service behavior
- Migration path for existing tests to use the framework

## Related Concepts
- [[MockModeTesting]]
- [[FirebaseMocking]]
- [[ServiceProviderPattern]]
