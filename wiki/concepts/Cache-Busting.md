---
title: "Cache-Busting"
type: concept
tags: [frontend, caching, deployment, assets]
sources: []
last_updated: 2026-04-08
---

## Summary
Technique for ensuring browsers load fresh frontend assets by embedding content hashes in filenames. WorldArchitect.AI applies cache-busting during Docker build to guarantee hashed assets are included in the image.

## Implementation
- Script: scripts/cache_busting.py
- Target: mvp_site/frontend_v1/
- Timing: Runs inside Docker build (not at runtime)

## Connections
- [[WorldArchitect.AI Docker Production Image]] — RUN command in Dockerfile
- [[Default Theme CSS Variables]] — frontend assets
