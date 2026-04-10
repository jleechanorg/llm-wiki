---
title: "Ranking Recompute"
type: concept
tags: [faction-combat, ranking, fp-consistency, bug-fix]
sources: [faction-ranking-recompute-tests]
last_updated: 2026-04-08
---

Pattern for ensuring faction ranking always uses accurate faction power values. When the LLM emits a ranking tool call without first emitting a power calculation, or with stale FP values, the system detects this and recomputes.

## Mechanism
1. **Detection**: When ranking tool is called with FP=0 or mismatched FP values
2. **Dropping**: Original ranking tool request with bad FP is dropped (not executed)
3. **Auto-Invocation**: Power tool is auto-invoked using state_updates data
4. **Reattachment**: Ranking is recalculated using the correct FP from auto-invoked power

## Why This Matters
FP/ranking divergence causes incorrect game state — players could receive artificially high or low rankings based on stale data.
