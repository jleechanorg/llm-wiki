---
title: "Gunicorn Configuration"
type: source
tags: [production, deployment, wsgi, infrastructure]
sources: [mvp-site-gunicorn-conf]
last_updated: 2025-01-15
---

## Summary

Gunicorn WSGI server configuration for WorldArchitect.AI production deployment. Optimized for I/O-bound workloads (MCP, Firestore, Gemini API calls).

## Key Claims

- **gthread workers**: Threaded workers for concurrent I/O
- **Scalable concurrency**: (2*CPU+1) workers x 4 threads = 12+ concurrent requests
- **10-minute timeout**: Aligned with Cloud Run + load balancer for long AI operations
- **Fastembed cache validation**: Checks cache on startup
- **Environment-aware**: Preview (1 worker) vs production configuration

## Key Settings

| Setting | Value | Purpose |
|--------|-------|---------|
| workers | auto (2*CPU+1) | Worker count scaling |
| threads | 4 | Threads per worker |
| timeout | 600s (10 min) | Request timeout |
| max_requests | 1000 | Worker restart cycle |
| backlog | 2048 | Pending connection queue |

## Connections

- [[mvp-site-infrastructure]] - Worker configuration library
- Cloud Run deployment configuration
