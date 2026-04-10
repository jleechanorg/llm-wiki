---
title: "gthread Workers"
type: concept
tags: [concurrency, threading, gunicorn]
sources: []
last_updated: 2026-04-08
---

## Description
Gunicorn worker class using Python threads instead of processes. Each worker spawns multiple threads, enabling handling of multiple concurrent requests within a single process. Ideal for I/O-bound workloads like API calls, database queries, and external service requests.

## Advantages
- Lower memory footprint than process-based workers
- Better for I/O-bound (not CPU-bound) workloads
- Compatible with libraries that don't support forking


## WorldArchitect.AI Usage
- Default: 4 threads per worker
- Total concurrency: (2*CPU+1) workers × 4 threads = 12+ on single CPU

## Connections
- [[GunicornConfigurationWorldarchitectAiProduction]] — worker class configuration
- [[GeminiProviderImplementationIsolated]] — Gemini API calls benefit from threaded workers
- [[FirestoreServiceDatabaseOperations]] — Firestore I/O benefits from threading
