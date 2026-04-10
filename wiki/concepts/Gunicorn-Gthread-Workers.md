---
title: "Gunicorn gthread Workers"
type: concept
tags: [gunicorn, wsgi, workers, concurrency, production]
sources: []
last_updated: 2026-04-08
---

## Summary
Gunicorn worker type that uses threads instead of processes for handling concurrent requests within a single worker process. Enables 12+ concurrent requests vs sync worker's single request.

## Configuration
- Worker count formula: (2×CPU+1)×4 for gthread
- Threads per worker: configurable
- Timeout alignment: 600s with Cloud Run limits

## Connections
- [[WorldArchitect.AI Deployment Guide]] — detailed worker configuration
- [[WorldArchitect.AI Docker Production Image]] — CMD configuration
