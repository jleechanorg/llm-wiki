---
title: "Worker Process"
type: concept
tags: [computing, process, gunicorn]
sources: [worldarchitect-ai-deployment-guide]
last_updated: 2026-04-08
---

## Summary
Independent Unix process that handles HTTP requests in Gunicorn. Each worker runs the WSGI application independently.

## Details
- **Formula**: `(2 × CPU_cores) + 1`
- **Purpose**: Ensures continuous handling during worker restarts
- **I/O Handling**: One worker handles I/O while others process
- **Restart Overhead**: +1 provides buffer during restarts

## Connections
- [[Gunicorn]] — spawns worker processes
- [[Concurrency]] — determinined by worker count
