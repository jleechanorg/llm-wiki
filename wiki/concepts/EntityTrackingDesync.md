---
title: "Entity Tracking Desync"
type: concept
tags: [testing, metrics, entity-tracking]
sources: [sariel-campaign-replay-desync-measurement]
last_updated: 2026-04-08
---

## Summary
Measurement of entity tracking accuracy drift across campaign interactions. Desync rate calculated as: `1 - (found / expected)` for each entity per interaction. Used to validate architecture decisions for game state management.

## Key Metrics
- **Tracking Rate** — `found / appearances` per entity
- **Success Rate** — `successful / total` per interaction
- **Cassian Problem Rate** — Edge case handling success

## Connections
- [[StatisticalValidation]] — Requires 10+ replays for significance
- [[IntegrationTesting]] — Test methodology used
