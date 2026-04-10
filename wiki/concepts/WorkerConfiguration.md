---
title: "Worker Configuration"
type: concept
tags: [infrastructure, scaling, deployment]
sources: []
last_updated: 2026-04-08
---

## Description
Infrastructure library for determining optimal Gunicorn worker and thread counts based on environment. Extracted to infrastructure package for testability and reusability.

## Environment-Aware Defaults
- **Preview**: 1 worker (512MB memory constraint)
- **Production**: (2*CPU+1) workers
- **Override**: GUNICORN_WORKERS and GUNICORN_THREADS environment variables

## Connections
- [[GunicornConfigurationWorldarchitectAiProduction]] — uses worker_config library
- [[WorldArchitectAIDockerProductionImage]] — same deployment stack
