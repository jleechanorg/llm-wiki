---
name: levelup-v2-dark-factory-gate-pipeline
description: "Level-up v2 lane gate pipeline = dark-factory pr_gates_split_cs.dot; holdout is SEALED and operator-run, not runnable by the implementing agent"
metadata: 
  node_type: memory
  type: project
  originSessionId: f6102da4-134b-4287-8e22-b7ce4f5222e8
---

Level-up v2 worktrees live under `~/.lvl-lanes/wt-lvl-*` (e.g. `wt-lvl-pra` = PR-A). The lane task prefix `# explore_in` is the implement phase of a dark-factory pipeline.

The exit pipeline named "holdout eval, /er, /code_standards" is the graph `dark-factory/pipelines/pr_gates_split_cs.dot`, run via `dark-factory --pipeline pr_gates_split_cs.dot` (CLI at `~/.local/bin/dark-factory`). Flow: **holdout → /es → /er → CS fan-out (/zfc, /zfclevel, /thermo) → exit**, join policy wait_all.

**Why:** Two things are non-obvious and waste time if unknown:
1. The **holdout gate is SEALED** — scenarios live in the separate `jleechanorg/dark-factory-holdouts` repo and "must never be visible to the implementing agent" (dark-factory/README.md:60-62). Do NOT try to run it; it is operator/runner-run. As the implementing agent your job is to make the work pass it, not execute it.
2. `/code_standards` (ZFC + leveling + RCF) maps to the three lanes **/zfc + /zfclevel + /thermo** (thermo IS the root-cause-first lane). The graph owns the fan-out because single-subprocess reviewer backends (codex exec) can't spawn subagents and hit timeout if fed all three serially.

**How to apply:** For a level-up lane, self-run /er + the three CS lenses (or one adversarial reviewer subagent across all four) to gain confidence; report holdout as operator-run. /er hard-rule exception: unit-only proof is OK for production changes under 100 delta lines of non-test code — most prompt-only lanes qualify, but still prefer Layer-2 real-LLM evidence. See [[feedback-2026-06-10-sdk-mock-is-synthetic-llm]] for what counts as the real network boundary.
