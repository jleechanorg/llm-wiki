---
title: "Celery Patterns"
type: concept
tags: [canonical, python, celery, async, task-queue]
sources: [canonical-code-repos/celery]
last_updated: 2026-04-14
---

## Summary

Celery is the canonical reference for distributed task queues in Python. Its core insight: tasks are functions with guarantees — at-least-once delivery, configurable retry policies, and result tracking — achieved through a broker (Redis/RabbitMQ) separating the caller from execution. The `canvas` system (chain, group, chord, chunk) composes tasks into workflows. Error handling is built-in via retry decorators with exponential backoff. Celery's task registry and naming conventions are the template for any async job system.

## Key Patterns

### Task Definition
```python
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

@celery_app.task(
    bind=True,              # pass self (task request) to the function
    name="tasks.process_file",
    max_retries=3,
    default_retry_delay=60,
)
def process_file(self, file_id: int, path: str) -> dict:
    try:
        result = do_work(file_id, path)
        return {"status": "success", "result": result}
    except TransientError as e:
        raise self.retry(exc=e)  # re-queue with backoff
```

`bind=True` gives access to `self.request` for retry control. Explicit `name=` prevents auto-naming collisions across modules. `max_retries` + `retry()` raises `Retry` exception internally — never `raise RetryError` directly.

### Automatic Retry with Exponential Backoff
```python
@celery_app.task(
    bind=True,
    autoretry_for=(TransientError, ConnectionError),
    retry_backoff=True,         # exponential: 2^attempt seconds
    retry_backoff_max=600,      # cap at 10 minutes
    retry_jitter=True,          # randomize to prevent thundering herd
)
def fetch_url(self, url: str) -> str:
    return requests.get(url, timeout=10).text
```

`autoretry_for` specifies which exceptions trigger automatic retry. `retry_backoff=True` doubles delay each attempt (2s, 4s, 8s...). `retry_jitter=True` adds randomness to prevent synchronized retries from multiple workers hitting the broker simultaneously.

### Canvas: Composing Task Workflows

**Chain** — sequential execution, output of one feeds into the next:
```python
from celery import chain

chain(
    tasks.fetch_data.s(url),
    tasks.parse_data.s(),
    tasks.store_results.s(db_id)
)()
```

**Group** — parallel execution, wait for all results:
```python
from celery import group

group(
    tasks.process_item.s(item_id) for item_id in item_ids
)()
```

**Chord** — group with a callback once all complete:
```python
from celery import chord

chord(
    tasks.process_batch.s(batch_id) for batch_id in batch_ids
)(tasks.notify_complete.s())
```

**Chunk** — split large iterables into parallel batches:
```python
from celery import chunk

tasks.process_item.chunks(list(item_ids), 10)()
# 10 items per worker task, parallel workers
```

### Task Time Limits
```python
@celery_app.task(
    time_limit=300,       # hard kill after 5 minutes
    soft_time_limit=240,  # raise SoftTimeLimitExceeded after 4 min
)
def long_running_task(self):
    try:
        do_work()
    except SoftTimeLimitExceeded:
        cleanup_gracefully()
```

`time_limit` is a hard kill (SIGKILL). `soft_time_limit` raises a catchable exception, allowing cleanup. Essential for preventing runaway tasks from exhausting worker resources.

### Result Handling
```python
result = tasks.process_file.apply_async(
    args=[file_id],
    kwargs={"path": "/data/file.csv"},
    countdown=30,         # delay execution by 30 seconds
    expires=300,          # discard if not started within 5 minutes
)

# Async: don't block
result.id        # UUID of the task
result.ready()   # is it done?
result.get()     # blocking — wait for result
result.get(timeout=10)  # with timeout

# Result backend patterns
celery_app.conf.result_expires = 3600  # auto-delete results after 1 hour
```

`apply_async()` for async dispatch with full control. `delay()` for fire-and-forget shorthand. Results stored in backend (Redis, DB) — not in memory. Always set `expires` and configure `result_expires` to prevent backend bloat.

### Broker Patterns
```python
# Redis — fast, in-memory, good for single-node
celery_app = Celery("tasks", broker="redis://localhost:6379/0")

# RabbitMQ — durable, ACID, good for multi-node
celery_app = Celery("tasks", broker="pyamqp://user:pass@rabbitmq//")

# Task routing
celery_app.conf.task_routes = {
    "tasks.high_priority.*": {"queue": "high"},
    "tasks.low_priority.*": {"queue": "low"},
}
```

Redis is the default for development; RabbitMQ for production durability. Task routing separates workloads onto dedicated queues. Workers consume from specific queues: `celery -A tasks worker -Q high,default`.

### Task Signature (s())
```python
from celery import signature as sig

# Partial with arguments
task_sig = tasks.process_file.s(file_id, path="/data/")
task_sig.apply_async(countdown=10)

# Cloning with new args
task_sig.clone(args=[42])  # override args
```

`s()` creates a task signature — a frozen reference to a task + args. Can be passed around, cloned with `clone()`, composed into canvas primitives.

### Error Callbacks and On Failure
```python
@celery_app.task(
    bind=True,
    throws=(ExpectedError,),  # don't retry on expected errors
    on_failure=notify_admins.s(),   # always called on failure
    on_retry=notify_retry.s(),      # called on each retry
    on_success=record_success.s(),  # called on success
)
def sensitive_task(self, data: dict):
    pass
```

`throws` lists exceptions that should not be retried (treated as success). `on_failure`/`on_retry`/`on_success` hooks are themselves tasks. Use for alerting, cleanup, and audit logging.

## Connections

- [[FastAPIErrorHandling]] — Celery's task error handling pairs well with FastAPI. FastAPI endpoints dispatch Celery tasks and return a `task_id`; clients poll or use WebSocket for result updates.
- [[AsyncioOrchestrationMigration]] — Celery predates async/await in Python. Modern code may replace Celery's blocking `.get()` with async wrappers (`celery.asyncio`).
- [[AutoRetryMechanism]] — Celery's retry decorator is the canonical implementation of exponential backoff with jitter — the same pattern referenced for API client retry logic.

## What This Means for Code Generation

Generated async job code should:
1. Follow Celery's task decorator pattern: `bind=True`, explicit naming, typed args
2. Use `autoretry_for` + `retry_backoff` instead of manual try/except/retry blocks
3. Compose complex workflows with canvas primitives rather than ad-hoc orchestration
4. Always set `time_limit` and `expires` to prevent resource exhaustion and result bloat
5. Use `SoftTimeLimitExceeded` for graceful cleanup rather than hard crashes
6. Never block on `.get()` in async contexts — use polling or WebSocket result streaming
7. Route tasks by priority/urgency to separate queues
