---
title: "Test Isolation"
type: concept
tags: [testing, best-practices]
sources: [real-service-provider-implementation]
last_updated: 2026-04-08
---

Testing practice ensuring tests don't affect each other. RealServiceProvider implements this by tracking test collections and providing batch cleanup to remove test data after each run.

## Related Pages
- [[RealServiceProviderImplementation]] — Implements isolation via collection tracking and cleanup
- [[PreventiveGuards]] — Guards against LLM hallucinations breaking game state
- [[NarrativeSynchronizationValidator]] — Validates continuity with isolation checking
