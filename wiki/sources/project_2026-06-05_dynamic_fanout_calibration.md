---
title: "Dynamic Fanout Calibration Benchmark (2026-06-05)"
type: source
tags: [dark-factory, workflow-graphgen, benchmark, fanout, calibration, determinism]
date: 2026-06-05
source_file: raw/project_2026-06-05_dynamic_fanout_calibration.md
---

## Summary
`benchmarks/dynamic_fanout/` is a deterministic A-vs-A+B separation benchmark built to calibrate the workflow_graphgen instrument — proving the n=10 null was a true negative (the ruler can detect real effects; it just didn't see one). Three scenarios use the same `benchmarks.workflow_graphgen.scoring.aggregate` (range-non-overlap + `MIN_N_FOR_WINNER=5`) and credit 4 winners. Pushed to PR #16 on dark-factory (MERGEABLE, suite 208 green).

## Key Claims
- **Purpose = instrument calibration, not another measurement.** A null is only meaningful if the ruler can detect a real effect.
- Determinism is intentional (removes model variance; n=5 conclusive) vs stochastic Sonnet n=10.
- Gap-tier CORRECTION: G1-adjacent (threaded state) is an **authoring choice**, not a gap — engine ALREADY threads via `${state._last_output}` (engine writes `ctx.state["_last_output"]` after every node at `engine.py` `_run_single_node`; `_render_prompt` substitutes it) with NO engine change. Only G1-non-adjacent (named node N−5 output) needs a 1-line engine change.
- **G3 (runtime node count) is the ONLY genuine paradigm gap** that survives an honest Mode A.
- Sweep decision rule: **Mode A+B iff K runtime-determined (spread≥1) AND V/C>1; else static Mode A.** Locked by `test_dynamic_fanout_sweep.py`.
- Default to static Mode A (ties on first-pass + known-shape, less code/latency); dynamic fan-out earns its complexity only at G3 + V/C>1.

## Key Quotes
> "A null is only meaningful if the ruler can detect a real effect."

> "G3 (runtime node count) is the ONLY genuine paradigm gap that survives an honest Mode A."

## Connections
- [[project_2026-06-04_workflow_graphgen_spec]] — the prior n=10 null that this benchmark calibrates
- [[WorkflowGraphgen]] — instrument being calibrated
- [[DarkFactory]] — repo where this lives
- [[AgentOrchestrator]] — fanout dispatcher
- [[DeterministicBenchmark]] — design pattern (no LLM, real on-disk artifacts)
- [[RangeNonOverlapAggregator]] — shared scoring function
- [[GapTierLabels]] — G1/G3 paradigm-gap taxonomy
- [[AuthoringChoiceNotGap]] — G1-adjacent correction
