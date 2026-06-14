---
title: "2026-06-13 Dark Factory Ao Spawn Lock Serializes"
type: source
tags: ["feedback", "worldarchitect", "dark-factory", "agent-orchestrator"]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_dark_factory_ao_spawn_lock_serializes.md
---

## Summary
dark-factory --backend ao serializes per AO project; 5 parallel pipelines targeting

## Key Claims
- When spawning multiple dark-factory pipelines in parallel targeting the SAME AO project, **only the first one succeeds** — every subsequent pipeline's `ao spawn` call returns `ao spawn failed (rc=1): ✗ Another ao spawn is in progress for project "worldarchitect" (PID N, started ...). Wait for it to finish.`
- - Only 1 of N parallel pipelines completes a full 36-step run.
- - Others get stuck at `explore_in` / `plan` / `implement` with `ao spawn failed (rc=1)` after 1-2 successful nodes.
- - `~/.dark-factory/merge_train/*.lock` files get orphaned for each lane.
- - Evidence bundles exist but are tiny (21-48 events, not the full 154+ of a completed run).
- 1. **Switch to `--backend claude`** (or `agy` / `codex`). These backends shell out to `claude --print` / `agy --print` / `codex exec --yolo` directly per node — no AO spawn, no per-project lock. The pipelines run truly in parallel.

## Connections
- [[WorldarchitectAI]] — worldarchitect.ai project memory
- [[DarkFactory]] — dark-factory pipeline memory
- [[AgentOrchestrator]] — AO worker dispatch memory
- [[KarpathyWikiPattern]] — wiki-ingest protocol
- Source: `raw/feedback_2026-06-13_dark_factory_ao_spawn_lock_serializes.md`
