---
title: "WorldArchitect.AI Docker Production Image"
type: source
tags: [docker, production, deployment, gunicorn, fastembed, cloud-run]
source_file: "raw/worldarchitect-ai-dockerfile-production.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Production Dockerfile for WorldArchitect.AI Python application. Uses Python 3.11-slim base, installs dependencies from requirements.txt, provisions fastembed model cache during build, configures Gunicorn with gthread workers for concurrent request handling, and applies cache-busting to frontend assets.

## Key Claims
- **Base Image**: python:3.11-slim for minimal production footprint
- **Fastembed Cache**: Pre-provisioned at build time via FASTEMBED_CACHE_PATH=/opt/fastembed_cache to survive Cloud Run cold starts
- **Gunicorn gthread Workers**: Configurable worker count for 12+ concurrent requests vs sync default
- **Build-time Cache-busting**: Applies hash-based filenames to frontend assets during Docker build
- **Offline Mode**: HF_HUB_OFFLINE=1 prevents runtime network calls, model must be pre-baked
- **PYTHONPATH**: Set to /app for package resolution of mvp_site and infrastructure

## Key Technical Details
| Component | Configuration |
|-----------|---------------|
| Base | python:3.11-slim |
| Cache Location | /opt/fastembed_cache |
| Worker Type | gthread (concurrent) |
| PYTHONPATH | /app |
| HuggingFace | offline mode enabled |

## Connections
- [[WorldArchitect.AI Deployment Guide]] — production deployment methodology
- [[Gunicorn gthread Worker Configuration]] — concurrent request handling
- [[Fastembed Model Cache]] — embedding model provisioning

## Contradictions
- None identified
