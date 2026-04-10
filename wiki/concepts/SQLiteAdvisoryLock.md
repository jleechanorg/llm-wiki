---
title: "SQLite Advisory Lock"
type: concept
tags: [database, concurrency, locking, sqlite]
sources: []
last_updated: 2026-04-07
---

## Description
Concurrency control mechanism where the webhook worker acquires per-PR SQLite advisory locks to prevent simultaneous remediation tasks on the same PR. Uses SQLITE_BUSY return codes to signal lock contention.

## Connections
- Used by [[WebhookPipelineOperatorRunbook]] for worker coordination
- Related to [[DeterministicFeedbackLoops]] for fail-closed error handling
