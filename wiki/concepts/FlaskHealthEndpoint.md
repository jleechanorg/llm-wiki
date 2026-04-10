---
title: "Flask Health Endpoint"
type: concept
tags: [flask, health-check, api-endpoint, monitoring]
sources: []
last_updated: 2026-04-08
---

## Definition
A Flask route that provides health check functionality for the worldarchitect-ai service. Returns JSON response indicating service health status.

## Features
- Returns 200 OK status when service is healthy
- Returns JSON with status, service name, and timestamp
- Includes concurrency metrics when GUNICORN_WORKERS environment variable is set
- Exempt from rate limiting

## Response Format
```json
{
  "status": "healthy",
  "service": "worldarchitect-ai",
  "timestamp": "ISO-8601 timestamp",
  "concurrency": {
    "workers": 5,
    "threads": 4,
    "max_concurrent_requests": 20
  }
}
```

## Related Concepts
- [[TestDrivenDevelopment]] — tests validate endpoint behavior
- [[GunicornConfiguration]] — provides worker/thread configuration
- [[RateLimitingExemption]] — health endpoint bypasses rate limits
