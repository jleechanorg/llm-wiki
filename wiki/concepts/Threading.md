---
title: "Threading"
type: concept
tags: [threading, concurrency, gthread, python]
sources: ["gunicorn-configuration-tdd-tests"]
last_updated: 2026-04-08
---

## Overview
Threading in Gunicorn allows handling multiple concurrent requests within a single worker process using Python threads.

## In This Wiki
- [[GunicornConfigurationTddTests]] — tests thread configuration
- [[WorkerConfiguration]] — broader configuration context

## Key Properties

### gthread Worker Class
Gunicorn's gthread worker class uses Python's threading module to handle concurrent requests:
- Each thread handles one request at a time
- Shared memory space within the worker process
- Lower memory overhead than multiprocessing

### Thread Pool
Default 4 threads per worker provides balance between concurrency and resource usage:
- 4 concurrent requests per worker
- Shared GIL considerations for CPU-bound work
- Suitable for I/O-bound operations (API calls, database queries)

### Configuration
```python
worker_class = "gthread"
threads = 4  # threads per worker
```
