---
title: "Timeout Configuration"
type: concept
tags: [configuration, http, timeout]
sources: [worldarchitect-ai-deployment-guide]
last_updated: 2026-04-08
---

## Summary
HTTP request timeout setting. Must be aligned across all layers (Gunicorn, Cloud Run, frontend) to avoid breaking long-running operations.

## Details
- **WorldArchitect.AI Setting**: 600 seconds (10 minutes)
- **Source**: WORLDARCH_TIMEOUT_SECONDS env var
- **Layers Requiring Alignment**:
  1. Gunicorn timeout
  2. Cloud Run service timeout
  3. Cloud Run load balancer timeout
  4. Frontend client timeout
- **Warning**: Lowering any layer breaks Gemini API calls

## Connections
- [[Gunicorn]] — configures timeout in gunicorn.conf.py
- [[GoogleCloudRun]] — requires matching timeout setting
