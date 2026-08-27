---
title: "Google Cloud Run"
type: entity
tags: [cloud, deployment, platform, google]
sources: [worldarchitect-ai-deployment-guide]
last_updated: 2026-04-08
---

## Summary
Google Cloud managed compute service used as primary deployment platform for WorldArchitect.AI. Handles containerized Flask/Gunicorn applications.

## Details
- **Service Type**: Managed serverless containers
- **Timeout Limit**: Must be aligned with Gunicorn at 600s
- **Environment Variables**: Supports GUNICORN_WORKERS, GUNICORN_THREADS

## Connections
- [WorldArchitectAI](WorldArchitectAI.md) — deployed to Cloud Run
- [Gunicorn](Gunicorn.md) — runs within Cloud Run containers
- [[CloudRunTrafficRouting]] — a named-revision traffic pin from an autoscaling experiment blocked all newer deploys from serving traffic on `mvp-site-app-dev`; fixed via `--to-latest` in PR #9398
