---
title: "service_provider.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Abstract base class for test service providers. Defines the interface for switching between mock and real services during testing.

## Key Claims
- ABC with abstract methods: `get_firestore()`, `get_gemini()`, `get_auth()`, `cleanup()`
- `is_real_service` property must be implemented by subclasses
- Enables the Real-Mode Testing Framework pattern for tests that can run against either mock or real services

## Connections
- [[real_provider]] — concrete implementation using real services
- [[pytest_integration]] — uses these providers for test fixtures