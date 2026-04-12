---
title: "24h PR Bug Sweep"
type: concept
tags: [worldarchitect, CI, bug, PR, production]
last_updated: 2026-04-10
---

High merge velocity (17 PRs/day) in worldarchitect.ai introduced 6 bugs across production, deploy, and CI layers in a single 24h sweep.

## 6 Bugs Found

| Bug | Component | File |
|-----|-----------|------|
| rev-xcak | campaign-wizard.js | — |
| rev-w1dt | deploy.sh | — |
| rev-p3wg | world_logic.py | rewards_box |
| rev-xxsx | constants.py | — |
| rev-hj4n | temporal correction | — |
| rev-qk2h | pr-cleanup.yml | CI |

## Root Cause

High merge velocity without corresponding test/coverage increase.

## Connections

- [[RewardsBoxAtomicity]] — rewards_box atomicity bugs in world_logic.py
- [[StructureDriftPattern]] — structural drift in world_logic.py response assembly
- [[LevelUpBug]] — level-up bug chain
- [[MergeReadiness]] — merge readiness criteria
