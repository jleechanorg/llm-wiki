---
title: "Concurrency"
type: concept
tags: [performance, computing, web-servers]
sources: [worldarchitect-ai-deployment-guide]
last_updated: 2026-04-08
---

## Summary
Capacity to handle multiple simultaneous requests. In Gunicorn, calculated as workers × threads.

## Details
- **Formula**: `max_concurrent = workers × threads`
- **Example**: 3 workers × 4 threads = 12 concurrent requests
- **Scaling**: Increases linearly with CPU cores (2×CPU+1 workers)

## WorldArchitect.AI Configuration
- **Default**: 3 workers × 4 threads = 12 concurrent requests on 1 CPU
- **2 CPU**: 5 workers × 4 threads = 20 concurrent requests
- **4 CPU**: 9 workers × 4 threads = 36 concurrent requests

## Connections
- [[Gunicorn]] — implements concurrency via workers/threads
- [[WorkerProcess]] — parallel request handler
- [[Threading]] — enables concurrent I/O
