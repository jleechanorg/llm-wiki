---
title: "jleechanclaw-webhook-worker"
type: source
tags: [jleechanclaw, webhook, worker]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/webhook_worker.py
---

## Summary
Webhook worker for processing queued webhook events. Takes webhook events from a queue and processes them through the event handling pipeline. Part of the asynchronous webhook processing system.

## Key Claims
- Async webhook event processing from queue
- Rate limiting and backoff
- Error handling and retry

## Connections
- [[jleechanclaw-webhook]] — processes events from webhook queue

## Contradictions
- None identified