---
title: "Gunicorn Configuration"
type: concept
tags: [gunicorn, wsgi, server-configuration, concurrency, environment-variables]
sources: []
last_updated: 2026-04-08
---

## Definition
Gunicorn WSGI server configuration that controls worker processes and threading for the Flask application deployment.

## Environment Variables
- **GUNICORN_WORKERS**: Number of worker processes
- **GUNICORN_THREADS**: Threads per worker (only shown when workers present)
- **WORLDARCH_TIMEOUT_SECONDS**: Request timeout

## Concurrency Calculation
Max concurrent requests = workers × threads

For example: 5 workers × 4 threads = 20 max concurrent requests

## Related Concepts
- [[FlaskHealthEndpoint]] — exposes configuration via health endpoint
- [[TestDrivenDevelopment]] — validates configuration exposure
- [[WSGIServer]] — Gunicorn is a WSGI server implementation
