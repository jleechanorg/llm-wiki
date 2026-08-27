---
title: "Gunicorn Cloud Run Concurrency Architecture"
type: concept
tags: [cloud-run, gunicorn, concurrency, architecture]
last_updated: 2026-08-25
---

# Gunicorn Cloud Run Concurrency Architecture

## Core Principle
On Google Cloud Run (Container-as-a-Service), web services should use **1 worker process with high thread count (`gthread`)** rather than multiple worker processes.

## Why 1 Worker is Optimal on Cloud Run
1. **Cold-Start Latency**: Module imports run once (~3s) instead of N times in parallel (which caused 240s boot hangs under 17 workers).
2. **Shared Memory**: ONNX embedding models (FastEmbed) and LRU prompt caches exist once in memory rather than being duplicated across N heaps.
3. **CPython GIL Release**: Python drops the GIL during all blocking network socket I/O (`recv`, `send`, `ssl.read/write`), allowing threads to stream tokens concurrently with zero GIL contention.
4. **Horizontal Scaling**: Cloud Run manages autoscaling across container instances (`max_instances=40`), not by packing processes into one instance.

## Official Reference
- Google Cloud Documentation: [Optimize Python applications for Cloud Run](https://cloud.google.com/run/docs/tips/python#optimize_gunicorn)
- Command: `CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app`
