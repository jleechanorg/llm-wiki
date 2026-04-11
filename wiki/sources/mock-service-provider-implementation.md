---
title: "Mock Service Provider Implementation"
type: source
tags: [python, mock, testing, service-provider, firestore, gemini]
source_file: "raw/mock-service-provider-implementation.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python implementation of a mock service provider that uses existing mock services (MockFirestoreClient, MockLLMClient) for testing without external dependencies. Provides an abstraction layer enabling seamless switching between mock and real service backends.

## Key Claims
- **Interface Compliance**: Implements TestServiceProvider interface for consistent testing API
- **Dual-Mode Support**: Property is_real_service returns False indicating mock mode
- **Service Composition**: Combines MockFirestoreClient and MockLLMClient into unified provider
- **Cleanup Support**: Reset method returns services to initial state for test isolation

## Key Classes
- **MockServiceProvider**: Main provider class implementing TestServiceProvider
- **MockFirestoreClient**: Existing mock for Firestore operations (from mvp_site.mocks)
- **MockLLMClient**: Existing mock for Gemini/LLM operations (from mvp_site.mocks)

## Connections
- Related to [[TestServiceProvider Implementation]] - this is the mock implementation
- Uses [[Mock Firestore Service for Function Testing]] for Firestore mocking
- Uses [[Mock Gemini API Service for Function Testing]] for LLM mocking
