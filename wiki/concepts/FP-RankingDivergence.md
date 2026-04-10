---
title: "FP/Ranking Divergence"
type: concept
tags: [faction-combat, ranking, data-consistency, bug-fix]
sources: [faction-ranking-recompute-tests]
last_updated: 2026-04-08
---

Bug where faction power (FP) and faction ranking become inconsistent due to LLM tool execution order issues. When the LLM emits a ranking tool call without first calculating power, or provides stale FP values, the ranking reflects incorrect data.


## Root Causes
- LLM forgets to emit faction_calculate_power before faction_calculate_ranking
- LLM provides outdated FP values in ranking request
- Timing issues between Phase 1 and Phase 2 tool execution

## Resolution
HIGH priority fix implements auto-detection and recomputation to ensure ranking always reflects accurate FP.
