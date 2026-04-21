---
title: "Level-Up ZFC Loop Postmortem — 2026-04-21"
type: source
tags: [level-up, zfc, postmortem, harness, agent-orchestrator, loop]
date: 2026-04-21
source_file: ~/llm_wiki/raw/2026-04-21-level-up-zfc-loop-postmortem.md
---

## Summary

Postmortem for the level-up ZFC supervision loop leaving `https://github.com/jleechanorg/worldarchitect.ai/pull/6420` red for too long. The immediate failure was treating an `upstream-owned` test blocker as a stable wait state rather than a provisional claim that required rapid revalidation. The eventual fresh-main repro showed the key failing provenance test passed on `origin/main`, so the blocker should have been reclassified as branch-owned divergence on the active PR much earlier.

## Key Claims

- The supervision loop accepted `upstream-owned` as a terminal wait state instead of a provisional label.
- Workers were allowed to stop at diagnosis and proof-note stage while the production lane remained red.
- Fresh-main repro later proved the critical provenance test was green on `origin/main`, invalidating the stale upstream classification.
- The active lane only moved again after the blocker was reclassified as branch-owned divergence and reassigned for closure.
- The harness failure was not lack of work; it was mis-sequencing and weak ownership rules.

## Key Quotes

> "The loop harness treated `upstream-owned` as a stable classification instead of a provisional claim that must quickly collapse into either an upstream fix lane or a branch-owned reclassification."

> "The harness let the agent substitute classification progress for delivery progress on a production-lane blocker."

## Connections

- [[ProvisionalUpstreamOwnership]] — the key harness pattern exposed by this incident
- [[Harness5LayerModel]] — useful framing for why this was a harness failure, not just a code failure
- [[AO-Daemon-Incident]] — adjacent AO observability fragility
- [[AO-Split-Brain]] — related multi-worker control-plane reliability problem
- [[AgentDrift]] — workers drifted into analysis/proof-note mode instead of closure mode
- [[AutonomousAgentLoop]] — the intended closure model that this loop failed to meet
- [[jleechan]] — operator context and preferences
