---
title: "Symphony"
type: entity
tags: [orchestration, daemon, openclaw]
sources: []
last_updated: 2026-04-07
---

## Description
Orchestration system used by OpenClaw for dispatching remediation tasks from the webhook pipeline worker. Symphony daemon receives tasks and executes them against PRs.

## Connections
- Used by [[WebhookPipelineOperatorRunbook]] for task dispatch
- [[Genesis]] — persistent orchestration layer that fills blank workspace files
- Referenced in [[SymphonyRuntimeDedupeContract]] for runtime deduplication
