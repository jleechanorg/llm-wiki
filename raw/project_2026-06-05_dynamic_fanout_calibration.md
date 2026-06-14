---
name: project_2026-06-05_dynamic_fanout_calibration
description: "dynamic_fanout deterministic A-vs-A+B separation benchmark — calibrates the workflow_graphgen instrument, proves n=10 null was a true negative. Pushed to PR"
metadata: 
  node_type: memory
  type: project
  originSessionId: 96237b72-565c-4c2d-b265-b151de9c2353
---

`benchmarks/dynamic_fanout/` — the "where it would matter" test recommended after [[project_2026-06-04_workflow_graphgen_spec]] found NO A-vs-A+B separation at n=10. Built 2026-06-05, committed `ca76afa` (replayed as `a5c2a3c` after rebase), pushed to `feat_workflow-graphgen-benchmark` = [PR #16](https://github.com/jleechanorg/dark-factory/pull/16), MERGEABLE, suite 208 green.

**Purpose = instrument calibration, not another measurement.** A null is only meaningful if the ruler can detect a real effect. dynamic_fanout grades 3 deterministic scenarios with the SAME `benchmarks.workflow_graphgen.scoring.aggregate` (range-non-overlap + `MIN_N_FOR_WINNER=5`) that returned the n=10 null. It now credits **4 winners** → the workflow_graphgen null was a **true negative**, not a blind ruler.

**Design (no LLM, real on-disk artifacts):** one deterministic coder fn shared by both modes (`add_validation`, `write_migration`) → any separation is attributable to *dispatch*, not coder skill. Determinism is intentional (removes model variance; n=5 conclusive) vs stochastic Sonnet n=10.

**Scenarios + results:**
- `validate_k6` (G3): K=6 endpoints, Mode A fixed F=3 nodes → coverage min(F,K)/K=0.5; A+B discovers K, fans out → 1.0. **A+B wins conformance; A wins tokens** (A+B pays K calls for coverage).
- `validate_k2` (G3): K=2 < F=3 → coverage ties 1.0; A wastes a dispatch → **A+B wins tokens**.
- `schema_migration` (G1): migration must match schema cols; Mode A reads only `${goal}` → drifts (0); A+B threads `state[schema.columns]` → matches (1). Tokens tie → win is purely the gap.

**Gap-tier labels (CORRECTED 2026-06-05, commit `b2bd7a3`):** earlier draft called G1 "engine-fixable" — WRONG. Empirically proven (`tests/test_state_threading.py`) that the runner ALREADY threads node output via `${state._last_output}` (engine writes `ctx.state["_last_output"]` after every node at `engine.py` `_run_single_node`; `_render_prompt` substitutes it) with **NO engine change**. So G1-adjacent is an **authoring choice**, not a gap. The naive `schema_migration` A+B win is an artifact of giving Mode A its worst (`${goal}`-only) prompt. New `schema_migration_threaded` feature: honest Mode A (threads `${state._last_output}`) **TIES** A+B — same aggregator crowns NO winner (`test_g1_win_evaporates_when_mode_a_is_honest`). Only **G1-non-adjacent** (named node N−5 output) needs a 1-line engine change. **G3 (runtime node count) is the ONLY genuine paradigm gap** that survives an honest Mode A.

**Sweep + decision rule (`sweep.py` → `SWEEP.md`, commit `b2bd7a3`):** value model `net = V·covered − C·calls` over K-distributions. Breakeven governed by **K-spread, not V/C**: spread-0 (constant K) → best static F=K ties A+B for ALL V/C (breakeven None); any spread>0 → trivial breakeven V/C>1. Rule: **Mode A+B iff K runtime-determined (spread≥1) AND V/C>1; else static Mode A.** Tests in `tests/test_dynamic_fanout_sweep.py` lock both theorems.

**Cross-bench synthesis:** `benchmarks/FINDINGS.md` — default to static Mode A (ties on first-pass + known-shape, less code/latency); dynamic fan-out only earns its complexity at G3 + V/C>1.

**Files:** `scenario.py` (make_api_source/count_endpoints), `coder_mock.py` (add_validation/write_schema/write_migration), `evaluator.py` (coverage/consistency, real file re-read), `modes.py` (run_mode_a/apb dispatch by scenario; FIXED_NODES=3, TOKENS_*_PER_CALL), `driver.py` (FEATURES catalog → assemble_record → aggregate), `__main__.py` (CLI rollup), `RESULTS.md`, `tests/test_dynamic_fanout.py` (14 tests incl. calibration meta-assert `credited>=3`).

**Repro:** `.venv/bin/python -m benchmarks.dynamic_fanout --trials 5 --out /tmp/dynfan/records.jsonl`

**PR #16 branch note:** diverged at `4b8b921`; remote = my work re-landed + `[copilot]` autofix split the harness zero_touch/{from,to} fix into 2 commits (`2766729`+`a6ef42b`). My local dup `b6e491d` was dropped via `reset --hard origin` + cherry-pick of only the new dynamic_fanout commit. If pushing to this branch again, expect copilot autofix commits on remote — rebase, don't force.
