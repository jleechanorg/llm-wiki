---
title: "2026-06-13 Levelup V2 Dark Factory Gate Pipeline"
type: source
tags: ["project", "worldarchitect", "dark-factory", "level-up"]
date: 2026-06-13
source_file: raw/project_2026-06-13_levelup_v2_dark_factory_gate_pipeline.md
---

## Summary
Level-up v2 lane gate pipeline = dark-factory pr_gates_split_cs.dot; holdout is SEALED and operator-run, not runnable by the implementing agent

## Key Claims
- Level-up v2 worktrees live under `~/.lvl-lanes/wt-lvl-*` (e.g. `wt-lvl-pra` = PR-A). The lane task prefix `# explore_in` is the implement phase of a dark-factory pipeline.
- The exit pipeline named "holdout eval, /er, /code_standards" is the graph `dark-factory/pipelines/pr_gates_split_cs.dot`, run via `dark-factory --pipeline pr_gates_split_cs.dot` (CLI at `~/.local/bin/dark-factory`). Flow: **holdout → /es → /er → CS fan-out (/zfc, /zfclevel, /thermo) → exit**, join policy wait_all.
- 1. The **holdout gate is SEALED** — scenarios live in the separate `jleechanorg/dark-factory-holdouts` repo and "must never be visible to the implementing agent" (dark-factory/README.md:60-62). Do NOT try to run it; it is operator/runner-run. As the implementing agent your job is to make the work pass it, not execute it.
- 2. `/code_standards` (ZFC + leveling + RCF) maps to the three lanes **/zfc + /zfclevel + /thermo** (thermo IS the root-cause-first lane). The graph owns the fan-out because single-subprocess reviewer backends (codex exec) can't spawn subagents and hit timeout if fed all three serially.

## Connections
- [[feedback-2026-06-10-sdk-mock-is-synthetic-llm]]
