---
title: "Timeout Management"
type: concept
tags: [timeout, deployment, reliability]
sources: []
last_updated: 2026-04-08
---

## Description
Centralized timeout configuration synchronized across all layers: Gunicorn worker timeout, Cloud Run request timeout, load balancer timeout, and client timeout. All set to 10 minutes (600s) to prevent premature termination of long-running AI operations.

## Layer Synchronization
- Gunicorn: worker timeout from WORLDARCH_TIMEOUT_SECONDS env var
- Cloud Run: container timeout configuration
- Load balancer: backend service timeout
- Client: request timeout

## Fail-Fast Behavior
Invalid timeout values cause immediate failure at startup rather than subtle runtime issues.

## Connections
- [[GunicornConfigurationWorldarchitectAiProduction]] — Gunicorn-level timeout
- [[GeminiProviderImplementationIsolated]] — Gemini API calls require long timeout
- [[TimeoutConfigurationScript]] — scripts/timeout_config.sh for deployment management
