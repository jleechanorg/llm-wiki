---
title: "Skeptic"
type: entity
tags: [skeptic, ci, verification, automated-testing]
sources: []
last_updated: 2026-04-07
---

## Definition
Skeptic is an automated CI verification system that checks PRs for 7-green status and posts a VERDICT. When 7-green conditions are met (CI + CR + Bugbot + threads + evidence + skeptic verdict), skeptic-cron can auto-merge if not denylisted.

## Key Behavior
- Runs after all other checks pass
- Posts "VERDICT: PASS" or "VERDICT: FAIL"
- Auto-merge controlled by `SKEPTIC_CRON_AUTO_MERGE` and `SKEPTIC_MERGE_DENYLIST`
- Configured via GitHub repository variables

## Connections
- Works with [[AgentOrchestrator]] for automated PR handling
- Targets [[WorldArchitectAI]] repository
- Reads `SKEPTIC_MERGE_DENYLIST` to skip auto-merge
