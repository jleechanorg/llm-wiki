---
title: "Docker Containerization"
type: concept
tags: [docker, container, deployment, infrastructure]
sources: []
last_updated: 2026-04-08
---

## Summary
Process of packaging application with its dependencies into a portable container image. WorldArchitect.AI uses Docker for production deployment to Cloud Run with pre-baked model caches.

## Key Components
- **Base Image**: python:3.11-slim for minimal footprint
- **Build-time Provisioning**: Model downloads happen during build, not runtime
- **Environment Variables**: Configure runtime behavior without code changes
- **Cache-busting**: Hash-based asset filenames applied at build time

## Connections
- [[WorldArchitect.AI Deployment Guide]] — Gunicorn configuration details
- [[WorldArchitect.AI Docker Production Image]] — Dockerfile implementation
