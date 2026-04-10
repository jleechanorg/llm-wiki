---
title: "Startup Warmup"
type: concept
tags: [optimization, latency, initialization, lazy-loading]
sources: [firebase-mock-mode-initialization-tests]
last_updated: 2026-04-08
---

Process of eagerly loading dependencies and querying data at application startup to reduce first-request latency. The warmup queries Firestore for user campaigns to pre-populate caches.

## Requirements
- Must NOT block startup — must complete within 0.25 seconds
- Should be skipped in mock mode (MOCK_SERVICES_MODE=true)
- Can be explicitly disabled via DISABLE_STARTUP_WARMUP env var
- Uses threading to avoid blocking the main thread

## Wiki Connections
- Tested by [[Firebase Mock Mode Initialization Tests]] — validates non-blocking behavior
- Related to [[Lazy Loading]] concept
