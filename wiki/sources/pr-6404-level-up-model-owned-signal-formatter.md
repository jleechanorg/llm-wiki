---
title: "PR #6404: Level-up add model-owned signal formatter"
type: source
tags: [zfc, level-up, model-computes, architecture, signal-formatter]
date: 2026-04-21
source_file: /Users/jleechan/roadmap/zfc-pr-task-specs-2026-04-22.md
---

## Summary
PR #6404 is the architecture lane for the ZFC level-up pivot. It adds `level_up_signal` as an explicit model-owned structured response field, persists non-empty `level_up_signal` through structured field extraction, and makes `rewards_engine.canonicalize_rewards()` prefer `level_up_signal` and format it into `rewards_box` without XP threshold inference.

## Key Claims
- Model computes level-up, XP totals, rewards, and choices
- Backend formats explicit model-owned signal
- UI renders server-provided payloads only
- Legacy backend inference remains temporarily for old responses without `level_up_signal`

## Key Quotes
> "The model decides XP totals, whether level-up is available, target level, and level-up choices. Backend code may validate explicit fields and create deterministic UI controls, but must not derive the level-up decision from XP thresholds on the new `level_up_signal` path"

## Connections
- [[Level-Up Bug Chain]] — model-owned signal architecture
- [[Normalization Atomicity]] — canonicalize_rewards formatting path
- [[ZFC PR Task Specs]] — item 2 (M1 evidence) depends on this architecture lane
