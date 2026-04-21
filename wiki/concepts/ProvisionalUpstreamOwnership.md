---
title: "Provisional Upstream Ownership"
type: concept
tags: [harness, blockers, ci, level-up, agent-orchestrator]
last_updated: 2026-04-21
sources: [2026-04-21-level-up-zfc-loop-postmortem]
---

An `upstream-owned` blocker label is provisional only. It is not a valid long-lived wait state on a production merge lane unless a fresh repro on current `origin/main` still fails the same exact blocker.

## Rule

Within 1-2 loop cycles, an upstream-owned claim must collapse into one of two outcomes:

1. Fresh `origin/main` repro is still red:
   - open or assign an upstream fix lane
   - keep explicit ownership on the blocker

2. Fresh `origin/main` repro is green:
   - immediately reclassify the blocker as branch-owned divergence
   - push the active PR worker back into execute mode

## Why It Matters

Without this rule, agents can substitute diagnosis for delivery. A production PR stays red while the loop keeps replaying a stale proof note instead of closing the gate.

## Failure Pattern

- worker sees a red shard and posts an upstream-style proof note
- loop accepts that note as sufficient
- no worker owns the blocker to closure
- active production lane sits in fake justified wait

## Prevention

- require fresh-main repro within 1-2 cycles
- require an explicit owner for every blocking red test
- do not let production workers stop at diagnosis when the PR is still red

## Connections

- [[Harness5LayerModel]]
- [[AutonomousAgentLoop]]
- [[AgentDrift]]
