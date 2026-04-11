---
title: "PR #102: fix: correct Explorer/Quester XP accumulation (WC-4j2)"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-102.md
sources: []
last_updated: 2026-03-26
---

## Summary
Explorer and Quester companions could not effectively level up because the XP-to-level math contained division thresholds that produced 0 and double failure penalties. The `discoveryBoost / 2` and `cueBonus / 2` formulas always evaluated to 0 since the `'discovery'` cue tag was never present in any act phase. Additionally, failure XP was double-penalized: `rollCompanionXp` already uses a reduced failure base, but Explorer/Quester applied an additional 0.35x/0.45x multiplier on top.

## Metadata
- **PR**: #102
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +340/-7 in 2 files
- **Labels**: none

## Connections
