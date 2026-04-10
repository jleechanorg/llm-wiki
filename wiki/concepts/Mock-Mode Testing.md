---
title: "Mock-Mode Testing"
type: concept
tags: [testing, mocking, quality-assurance]
sources: [real-mode-testing-framework-integration-summary]
last_updated: 2026-04-08
---

Traditional testing approach using mock implementations (Fake Firestore, Fake LLM, Fake Auth) for fast, isolated unit and integration tests. Default mode for the testing framework.

## Key Characteristics
- Uses MockServiceProvider or SimpleMockServiceProvider
- Fast execution with no external API calls
- Deterministic behavior for reproducible tests
- Default when TEST_MODE is not set to 'real'

## Related
- [[Real-Mode Testing]] — alternative mode
- [[Dual-Mode Testing]] — framework supporting both
