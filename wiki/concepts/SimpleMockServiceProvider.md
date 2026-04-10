---
title: "SimpleMockServiceProvider"
type: concept
tags: [testing, mock, service-provider, python]
sources: [simplified-mock-service-provider-implementation, test-service-provider-abstract-base-class]
last_updated: 2026-04-08
---

## Definition
A lightweight mock service provider implementation that provides stub implementations for Firestore, Gemini, and Auth services without complex external dependencies. Used for testing the service provider interface pattern.

## Key Components
- **SimpleMockFirestore** — In-memory mock with collection/document API
- **SimpleMockGemini** — Call-count tracking for LLM mock
- **SimpleMockAuth** — Token verification mock

## Usage
```python
provider = SimpleMockServiceProvider()
firestore = provider.get_firestore()
```

## Related Concepts
- [[TestServiceProvider]] — Abstract base interface
- [[RealServiceProvider]] — Production implementation
- [[MockObject]] — Testing pattern for external dependencies
