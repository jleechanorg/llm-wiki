---
title: "Faction 25-Turn E2E Campaign"
type: entity
tags: [testing, campaign, e2e, faction]
sources: []
last_updated: 2026-04-07
---

## Description
End-to-end test campaign used for validating timestamp progression, level progression, and gold tracking fixes across 20-25 turn sequences.

## Test Iterations
- **Iteration 004**: Before prompt clarifications, showed timestamp reversals and level jumps
- **Iteration 005**: After 5 prompt clarifications, resolved most issues

## Connections
- [[TimestampProgression]] — tested for forward progression
- [[LevelProgression]] — tested for incremental advancement
- [[GoldTracking]] — tested for dual pool tracking
