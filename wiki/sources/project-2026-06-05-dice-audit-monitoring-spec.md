---
title: "Dice Audit Monitoring Spec (GCP Heartbeat Alert — Design Only)"
type: source
tags: ["dice-audit", "gcp-monitoring", "worldarchitect-ai", "monitoring"]
date: 2026-06-05
source_file: project_2026-06-05_dice_audit_monitoring_spec.md
---

## Summary
Design spec for catching dice-audit regressions in prod GCP via 'Dice Telemetry Heartbeat' — the regression signature is the `DICE_AUDIT: notation=` INFO heartbeat going SILENT while request traffic continues. Design/research only, no code written.

## Key Claims
- Heartbeat: `DICE_AUDIT: notation=` log going SILENT (not warnings appearing)
- `conditionAbsent` does NOT reliably fire on log-based metrics — Cloud Monitoring injects synthetic zero
- Use `conditionThreshold` `COMPARISON_LT` (heartbeat < 2/1h) + `evaluationMissingData: EVALUATION_MISSING_DATA_ACTIVE`
- AND-gate with `run.googleapis.com/request_count > 0` to avoid scale-to-zero false alarms
- Daily job: `wa-daily-dice-audit` cron `17 9 * * *` America/New_York
- Beads: rev-1fmed, rev-b3ua9, rev-4rdlp, rev-gid6g, rev-qe641

## Key Quotes
> A warning-presence alert cannot catch telemetry that stopped emitting

> DB is source of truth locally; under no-auto-flush, beads.db and issues.jsonl can diverge without churn

## Connections
- [[DiceAudit]] — broader dice monitoring concept
- [[GCPHeartbeat]] — alerting pattern
