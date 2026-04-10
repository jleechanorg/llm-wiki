---
title: "RealServiceProvider"
type: entity
tags: [python, testing, service-provider]
sources: ["real-service-provider-tests"]
last_updated: 2026-04-08
---

Real service provider implementation that creates actual Google Cloud clients for Firestore and Gemini, as opposed to mocked test providers.

## Test Coverage
- Interface implementation via [[TestServiceProvider]]
- Real service flag (is_real_service = True)
- Capture mode support for test data recording
- Firestore client creation with auth handling
- Gemini client creation with API key validation
- Test collection tracking and cleanup

## Related
- [[TestServiceProvider]] — test interface
- [[RealServiceProviderTests]] — unit tests for this class
