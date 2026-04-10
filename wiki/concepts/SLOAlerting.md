---
title: "SLO Alerting"
type: concept
tags: [metrics, alerting, reliability, slo]
sources: []
last_updated: 2026-04-07
---

## Description
Service Level Objective alerting in the webhook pipeline. Alerts trigger when dispatch success rate drops below 95% (events_dispatched / events_enqueued < 0.95). Includes alert response procedures for common failure modes.

## Connections
- Implemented by [[WebhookPipelineOperatorRunbook]] via check_slo_alerts
- Related to [[E2ETesting]] for verifying pipeline health
