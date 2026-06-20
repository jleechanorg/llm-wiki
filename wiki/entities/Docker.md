---
title: "Docker"
type: entity
tags: [containers, runtime, deployment]
sources: [worldarchitect-ai-deployment-guide]
last_updated: 2026-04-08
---

## Summary
Container runtime used to containerize WorldArchitect.AI for deployment. Docker Compose supported for local development.

## Details
- **Dockerfile**: Containerizes Flask application
- **docker-compose.yml**: Local development and orchestration
- **Environment Variables**: Passed via environment key

## Connections
- [WorldArchitectAI](WorldArchitectAI.md) — containerized with Docker
- [GoogleCloudRun](GoogleCloudRun.md) — deploys Docker images
- [Kubernetes](Kubernetes.md) — orchestrates Docker containers
