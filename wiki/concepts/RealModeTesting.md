---
title: "Real-Mode Testing"
type: concept
tags: [testing, integration, mock-vs-real]
sources: ["real-mode-testing-framework-integration-validation"]
last_updated: 2026-04-08
---

A testing approach where tests execute against actual external APIs (Firestore, Gemini, Auth) rather than mocked dependencies. Enabled via TEST_MODE=real environment variable. Provides higher confidence in integration correctness but requires valid API credentials.

## Key Properties
- **Requires credentials**: Real API keys must be configured
- **Slower execution**: Network calls add latency
- **Higher fidelity**: Tests the actual service integration
- **Fallback to mock**: Tests gracefully skip when credentials unavailable

## Use Cases
- End-to-end integration validation
- Regression testing against live APIs
- Verifying mock implementations match real behavior
