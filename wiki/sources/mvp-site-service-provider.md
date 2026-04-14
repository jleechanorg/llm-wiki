---
title: "Service Provider"
type: source
tags: [testing, service-provider, abstraction, mock-real]
sources: [mvp-site-service-provider]
last_updated: 2025-01-15
---

## Summary

Abstract base class for test service providers using ABC pattern. Defines the interface for mock and real service providers in the Real-Mode Testing Framework.

## Key Claims

- **ABC pattern**: Abstract base class with abstractmethod decorators
- **Service interface**: Defines firestore_client, gemini_client, auth_service
- **Mode-agnostic**: Works with both mock and real implementations
- **Test isolation**: Each provider can manage its own test data cleanup
- **Capture support**: Optional client wrapping for interaction capture

## Abstract Methods

- `get_firestore_client()` - Returns Firestore client
- `get_gemini_client()` - Returns Gemini client
- `get_auth_service()` - Returns auth service
- `cleanup()` - Cleanup test data

## Implementations

- [[mvp-site-mock-provider]] - Mock implementation for fast unit tests
- [[mvp-site-real-provider]] - Real implementation with actual APIs

## Connections

- [[mvp-site-fixtures]] - Fixture integration
- [[mvp-site-pytest-integration]] - Pytest configuration
