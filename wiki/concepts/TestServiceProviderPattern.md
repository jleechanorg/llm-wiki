---
title: "Test Service Provider Pattern"
type: concept
tags: [testing, pattern, service-provider]
sources: ["real-service-provider-tests"]
last_updated: 2026-04-08
---

Testing pattern using service provider abstraction to switch between real and mocked implementations. RealServiceProvider creates actual Google Cloud clients while test mocks provide isolated behavior.

## Interface Contract
- is_real_service: Boolean flag indicating real vs mocked
- get_firestore(): Returns Firestore client
- get_gemini(): Returns LLM client
- get_auth(): Returns auth context
- track_test_collection(name): Register collection for cleanup
- cleanup(): Remove test data from tracked collections

## Benefits
- Unified interface for real/test providers
- Capture mode for recording test fixtures
- Automatic cleanup of test data
- Graceful auth failure handling

## Related
- [[TestServiceProvider]] — interface definition
- [[RealServiceProvider]] — implementation
