---
title: "Scheduled Automation Runner"
type: concept
tags: [agent-orchestrator, automation, scheduled, cron, AO]
last_updated: 2026-04-07
---

Automation runner design only implementable after switching to a two-config contract: `agent-orchestrator.yaml` stays authoritative for projects/plugins/notifiers, while `scheduled-workers.yaml` only defines recurring jobs.

## Two-Config Contract

1. **agent-orchestrator.yaml** — authoritative for projects, plugins, notifiers
2. **scheduled-workers.yaml** — only defines recurring jobs

Reusing bare `--config` for the automation file was ambiguous and wrong for AO's actual boot path.

## Completion Needs

`ao automation run` can synchronously record dispatch, but durable final result recording needs:
1. `automationJobId` and `automationRunId` persisted on sessions
2. Narrow lifecycle terminal-state hook to update the ledger
3. Completion notifications emitted

## Pattern

Automation completion needs explicit job/session correlation plus lifecycle callback. Cannot rely on implicit side effects.

## Connections

- [[CronJobAutomation]] — cron job automation patterns
- [[AO-Claim-Fail-Closed]] — AO claim verification
- [[AO-Blocker-Matrix]] — PR blocker triage
- [[DaemonBootstrap]] — daemon bootstrap patterns
