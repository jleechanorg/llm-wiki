---
title: "MOCK_SERVICES_MODE"
type: concept
tags: [environment-variable, testing, mocking, configuration]
sources: [firebase-mock-mode-initialization-tests]
last_updated: 2026-04-08
---

Environment variable that when set to "true" causes the application to use fake/mock services instead of real backend services (Firebase Auth, Firestore, etc.).

## Behavior
When MOCK_SERVICES_MODE=true:
- create_app() skips _warm_startup_lazy_dependencies()
- Firebase initialization is bypassed
- Fake services are used for all backend operations

## Related Configuration
- [[DISABLE_STARTUP_WARMUP]] — explicit flag to disable warmup independently of mock mode
- [[ENABLE_SEMANTIC_ROUTING]] — controls semantic routing feature

## Wiki Connections
- Tested by [[Firebase Mock Mode Initialization Tests]]
