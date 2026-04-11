---
title: "Webhook Pipeline Operator Runbook"
type: source
tags: [webhook, pipeline, runbook, symphony, github, sqlite, metrics, slo]
sources: []
source_file: "raw/webhook-pipeline-operator-runbook.md"
last_updated: 2026-04-07
---

## Summary
Operational runbook for the webhook pipeline that receives GitHub App webhook deliveries via HTTP (port 9100), validates HMAC-SHA256 signatures, deduplicates by delivery ID, and persists to SQLite. Includes worker architecture with per-PR locking, reconciler cron, and SLO alert procedures.

## Key Claims
- **HTTP ingress on port 9100**: Receives GitHub App webhooks with HMAC-SHA256 signature validation
- **SQLite queue at ~/.openclaw/webhook_queue.db**: Raw payload persistence with deduplication by X-GitHub-Delivery ID
- **Per-PR SQLite advisory lock**: Worker acquires locks to prevent concurrent remediation on same PR
- **Reconciler cron every 5 minutes**: Resets stuck IN_PROGRESS, recovers stale PENDING, re-enqueues exhausted FAILED
- **In-process MetricsCollector**: Lightweight metrics with SLO alert evaluation via check_slo_alerts
- **SLO target: 95% dispatch success rate**: Alert triggers when events_dispatched / events_enqueued < 0.95

## Key Quotes
> "The webhook pipeline receives GitHub App webhook deliveries via an HTTP ingress (port 9100), validates HMAC-SHA256 signatures, deduplicates by X-GitHub-Delivery ID, and persists raw payloads to a SQLite queue"

## Connections
- [[Symphony]] — dispatches remediation tasks from the webhook worker
- [[GitHub]] — source of App webhook deliveries
- [[OpenClaw]] — owns the webhook_queue.db at ~/.openclaw/

## Contradictions
- None identified
