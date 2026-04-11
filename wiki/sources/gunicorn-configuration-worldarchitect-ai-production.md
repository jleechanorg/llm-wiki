---
title: "Gunicorn Configuration for WorldArchitect.AI Production"
type: source
tags: [gunicorn, production, deployment, cloud-run, concurrency, performance]
source_file: "raw/gunicorn-configuration-worldarchitect-ai-production.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Production Gunicorn configuration optimized for I/O-bound workloads including MCP, Firestore, and Gemini API calls. Uses gthread workers achieving 12+ concurrent requests on single CPU, with 10-minute timeout synchronized across Cloud Run, load balancer, and client layers.

## Key Claims
- **Concurrency model**: (2*CPU+1) workers × 4 threads = 12+ concurrent requests on 1 CPU
- **Memory optimization**: Preview environment uses 1 worker (512MB constraint), production scales dynamically
- **Timeout synchronization**: 10-minute timeout (600s) aligned with Cloud Run + load balancer + client timeouts
- **Automatic worker management**: worker_config library extracted to infrastructure package for testability

## Key Quotes
> "This configuration uses gthread workers for improved concurrency while maintaining compatibility with all Python libraries (Firebase, Firestore, Gemini SDK)."

## Connections
- [[WorldArchitectAIDockerProductionImage]] — same deployment stack
- [[GeminiProviderImplementationIsolated]] — Gemini API calls that require long timeout
- [[FirestoreServiceDatabaseOperations]] — I/O-bound Firestore operations
- [[ThreadSafeFileCachingWithTTLCache]] — fastembed cache for offline model serving

## Contradictions
- None identified
