---
title: "AO Skeptic Gate + Killing AO Workers Breaks PR Gate Pipeline"
type: source
tags: ["ao", "skeptic", "agent-orchestrator", "worker-kill", "regression"]
date: 2026-06-04
source_file: project_ao_skeptic_gate_and_worker_kill.md
---

## Summary
Killing AO workers has TWO downstream side effects: takes down Skeptic Gate verdict pipeline (no VERDICT → gate times out failing closed) AND regresses agent-antigravity dist (lifecycle rebuilds dist from live branch). Skeptic Gate manual-verdict workflow documented.

## Key Claims
- `pkill` of AO lifecycle/agy workers does NOT stick — launchd jobs revive them within minutes
- Skeptic Gate manual-verdict: `node packages/cli/dist/index.js skeptic verify -n <PR> -m claude --trigger-sha <full-head-sha> --request-id <request-id>`
- `--dry-run` prints verdict WITHOUT posting (preview before committing)
- PR gate-chasing lessons: put evidence in gist (not docs/evidence/.md) to avoid CodeRabbit MD040

## Key Quotes
> Required checks on main: Green Gate, Test, Typecheck, Skeptic Gate. Evidence Gate and Green Gate Orchestrator are NOT required — their failures don't block merge (UNSTABLE ≠ blocked)

## Connections
- [[AgentOrchestrator]] — worker kill impacts
- [[SkepticReview]] — manual verdict workflow
