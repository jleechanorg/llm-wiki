---
title: "WorldArchitect.AI Deployment Guide"
type: source
tags: [deployment, gunicorn, performance, concurrency, worldarchitect]
source_file: "raw/worldarchitect-ai-deployment-guide.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Production deployment configuration guide for WorldArchitect.AI covering Gunicorn worker configuration, environment variables, and performance tuning. Uses gthread workers optimized for I/O-bound workloads with a formula of (2×CPU+1) workers × 4 threads providing 12+ concurrent requests on a single CPU.


## Key Claims
- **Gthread Workers**: WorldArchitect.AI uses Gunicorn with gthread workers for production, optimized for I/O-bound workloads (MCP server, Firestore, Gemini API calls)
- **Worker Formula**: `workers = (2 × CPU_cores) + 1` ensures continuous request handling during worker restarts
- **Concurrency Calculation**: 3 workers × 4 threads = 12 concurrent requests on 1 CPU, scaling linearly with cores
- **Timeout Alignment**: Gunicorn, Cloud Run, and frontend clients must all use 600s timeout to avoid breaking long-running Gemini calls

## Key Quotes
> "Keep Gunicorn, Cloud Run (service + load balancer), and frontend clients aligned at 600s." — Configuration warning

## Connections
- [[Gunicorn]] — web server providing HTTP handling
- [[GoogleCloudRun]] — primary deployment platform
- [[Kubernetes]] — container orchestration
- [[Docker]] — container runtime
- [[Render]] — deployment platform alternative
- [[Concurrency]] — simultaneous request handling capacity
- [[TimeoutConfiguration]] — request timeout management

## Contradictions
- None identified
