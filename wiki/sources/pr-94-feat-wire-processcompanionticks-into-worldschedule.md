---
title: "PR #94: feat: wire processCompanionTicks into WorldScheduler tick loop"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-94.md
sources: []
last_updated: 2026-03-26
---

## Summary
`processCompanionTicks()` existed in `faction_simulator.ts` and was called during simulation, but only as an implicit side-effect buried inside `runSimulation()`. The WorldScheduler had no direct visibility into companion processing.

## Metadata
- **PR**: #94
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +322/-7 in 3 files
- **Labels**: none

## Connections
