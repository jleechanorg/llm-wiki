---
title: "Render"
type: entity
tags: [cloud, deployment, platform]
sources: [worldarchitect-ai-deployment-guide]
last_updated: 2026-04-08
---

## Summary
Managed cloud platform alternative for deploying WorldArchitect.AI. Configures environment variables via dashboard.

## Details
- **Configuration**: Via Environment tab in service settings
- **Environment Variables**: GUNICORN_WORKERS, GUNICORN_THREADS

## Connections
- [[WorldArchitectAI]] — alternative deployment target
- [[Gunicorn]] — runs on Render service
