---
title: "Real-Mode Testing"
type: concept
tags: [testing, integration, quality-assurance]
sources: [real-mode-testing-framework-integration-summary]
last_updated: 2026-04-08
---

Testing approach where tests execute against actual external services (Firebase Firestore, Gemini API, Firebase Auth) rather than mock implementations. Enables validation of integration behavior that mocks cannot fully simulate.

## Key Characteristics
- Uses RealServiceProvider instead of MockServiceProvider
- TEST_MODE=real environment variable triggers real mode
- Requires resource management and cost protection
- Provides higher confidence in production behavior

## Safety Considerations
- Automatic cleanup after test runs
- Test isolation with unique collection names
- Resource limits for expensive operations
- Call count limits for cost protection

## Related
- [[Mock-Mode Testing]] — opposite mode
- [[Dual-Mode Testing]] — framework supporting both
