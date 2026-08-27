---
title: "Gunicorn Worker Sizing and Cloud Run Concurrency Architecture"
type: source
tags: [cloud-run, gunicorn, concurrency, gil, devops, latency]
date: 2026-08-25
source_file: raw/reference_2026-08-25_gunicorn_cloudrun_concurrency.md
---

## Summary
Documents the architectural rationale for running 1 Gunicorn worker with 180 threads (`gthread`) on Google Cloud Run for Python I/O-bound streaming gateways. Explains how `(2*CPU)+1` caused 240s cold-start hangs and 17x heap duplication, why Python releases the GIL during socket I/O, and how to detect/prevent silent Cloud Run revision traffic pinning.

## Key Claims
- The classical formula `(2*CPU)+1` spawned 17 workers on 4-vCPU boosted Cloud Run instances, causing 4-minute boot delays and 6.6–8.2 GB RSS OOM kills due to module import CPU contention and isolated heap duplication.
- For I/O-bound web services (>95% waiting on Gemini API SSE tokens, Firestore gRPC, and MCP tool sockets), 1 worker with threaded concurrency (`GUNICORN_WORKERS=1`, `GUNICORN_THREADS=180`) minimizes baseline RAM and cold starts (~3s) while achieving full concurrency.
- In CPython, the Global Interpreter Lock (GIL) is released during all socket reads/writes and network I/O (`Py_BEGIN_ALLOW_THREADS`), allowing hundreds of threads to wait on streaming connections without lock contention.
- Google Cloud Run's official Python standard explicitly recommends `gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app`.
- If Cloud Run traffic is pinned to an explicit revision name in `spec.traffic`, newly deployed revisions receive 0% traffic; deploys must enforce `--to-latest`.

## Key Quotes
> "Setting too many workers or threads can have a negative impact, such as longer cold start latency, more consumed memory, smaller requests per second, etc." — Google Cloud Documentation (Optimize Python applications for Cloud Run)

## Connections
- [[CloudRunConcurrency]] — Serverless container scaling model vs traditional VM multi-processing
- [[PythonGILNetworkConcurrency]] — Mechanics of CPython GIL release during socket I/O
- [[CloudRunTrafficPinning]] — Silent 0% traffic routing trap on named revision pinning
- [[WorldArchitectAI]] — Production service deployment and streaming gateway architecture
- Bead `rev-zqtl7`
