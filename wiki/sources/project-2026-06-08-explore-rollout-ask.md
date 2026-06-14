---
title: "dark-factory explore phase rollout to all pipelines (user directive)"
type: source
tags: [dark-factory, explore-phase, rollout, model-routing, user-directive]
date: 2026-06-08
source_file: raw/project_2026-06-08_explore_rollout_ask.md
---

## Summary
User explicitly asked to extend the explore→plan gate (commit 6c6a2a3, slim-only) to all non-gate, non-review pipelines. Verbatim: 'also i want explore for all the pipelines not just one'. 5 of 7 .dot files still lack explore; primary rollout = pipelines/factory/hello.dot (jleechan-2wx, P1). Role-routing stylesheet pattern: explore/implement/fix use coder tier (--backend), plan pinned to claude-opus-4-6 (should become DARK_FACTORY_PLAN_MODEL env var per jleechan-x57), review routed to agy.

## Key Claims
- Pipeline inventory: 7 .dot files; only slim/minimal_feature.dot and slim/minimal_pr.dot have explore (canonical unchanged); factory/hello.dot is the primary target (P1)
- Role-routing stylesheet shape: explore/implement/fix honor run-level --backend (coder tier); plan pinned to claude-opus-4-6 (env var follow-up); review to agy (independent reviewer)
- Beads filed: jleechan-2wx (P1 propagate to factory/hello.dot), jleechan-80r (P3 explore early-exit on infeasible), jleechan-x57 (P3 DARK_FACTORY_PLAN_MODEL env var), jleechan-4gx (P3 cleanup untracked leftovers)

## Connections
- [[DarkFactoryExplorePhase]]
- [[ModelStylesheet]]
- [[DarkFactory]]
