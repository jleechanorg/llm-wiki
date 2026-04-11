---
title: "PR #98: fix: incorporate world day/hour into companion RNG seed (WC-a55)"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-98.md
sources: []
last_updated: 2026-03-26
---

## Summary
Companion RNG seeds were constructed as `companion.id:tickSeed` where `tickSeed` came from `state.simulationTickCount`. When `runCompanionTicks` ran as a standalone WorldScheduler phase without `runSimulation` having advanced the tick counter, companions produced identical action outcomes across ticks. The faction simulator already addressed this by seeding its RNG with `campaignId::tick::day::hour`.

## Metadata
- **PR**: #98
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +133/-5 in 3 files
- **Labels**: none

## Connections
