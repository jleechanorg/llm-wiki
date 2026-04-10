---
title: "Cold Start Optimization"
type: concept
tags: [performance, deployment, serverless, latency]
sources: [startup-import-lazy-loading-tests]
last_updated: 2026-04-08
---

## Definition
Techniques to reduce the time between process start and readiness to handle requests. For Python web services, this means keeping heavy dependencies (cloud SDKs, ML libraries) out of the startup import path.

## Key Strategies
- **Lazy loading**: Defer module imports until first use
- **Module splitting**: Separate heavy optional deps into submodules
- **Import ordering**: Import cheap modules first, defer expensive ones

## Verification
Tests like [[StartupImportLazyLoadingTests]] verify that `google.genai` and `google.cloud.firestore` never load at import time, proving cold start optimization is working.

## Metrics
- Target: Import path should complete in <100ms
- Heavy SDKs add seconds to startup time if loaded eagerly

## Wiki Connections
- Enabled by [[LazyLoading]]
- Measured by [[ImportPerformance]] tests
