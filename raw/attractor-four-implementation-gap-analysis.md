---
name: Attractor Pattern Four-Implementation Gap Analysis
description: Feature-by-feature comparison of dark-factory vs AttractorBench, Kilroy, Smasher, Mammoth
type: reference
bead: none
---

## Context

Reviewed all four canonical Attractor implementations cloned at `~/projects/`:
- **AttractorBench** (`~/projects/attractorbench`) — StrongDM's benchmark harness (Python)
- **Kilroy** (`~/projects/kilroy`) — Dan Shapiro's Go implementation
- **Smasher** (`~/projects/smasher`) — 2389 Research Rust implementation
- **Mammoth** (`~/projects/mammoth`) — 2389 Research TypeScript implementation

## Feature Gap: dark-factory vs All Four

### FULLY IMPLEMENTED (matches or exceeds all four)

| Feature | dark-factory | Notes |
|---|---|---|
| DOT pipeline engine | `runner/parser.py` + `runner/engine.py` | Sequential walk, conditional edges, loop bounds, retries, goal gates |
| Sealed holdouts + agent isolation | `sandbox-exec` + `$DARK_FACTORY_HOLDOUTS` + env sanitization | Matches AttractorBench's spec-in/evaluator-out split |
| CXDB event recording | `runner/cxdb.py` — SQLite WAL, per-step recording | Less rich than Kilroy's typed event registry (20+ event types) but functional |
| Healer / failure clustering | `runner/healer.py` — clusters by (node, outcome, output_hash) | Unique to dark-factory; other 3 have no equivalent |
| /es /er /code_standards gates | `gate_es`, `gate_er`, `gate_code_standards` handlers with SHA binding | Unique to dark-factory; Kilroy has review_consensus but not slash-command gates |
| Evidence bundles | `runner/evidence.py` — manifest, pipeline DOT + SHA256, per-step output, holdout redaction | Matches Kilroy's stage-level artifacts |
| Spec-in / evaluator-out split | Visible specs in `benchmarks/*/spec.md`, evaluator in sealed repo | Matches AttractorBench's `specs/` vs locally-generated evaluators |
| Human-in-the-loop | `human_gate` handler, stdin-based, pre-seedable for tests | All four implement this; Kilroy has richest (5 interviewer types + web API) |

### PARTIALLY IMPLEMENTED (exists but weaker than reference)

| Feature | dark-factory | Best Reference | Gap |
|---|---|---|---|
| Adversarial cross-review | Sequential /es → /er → /cs gates | **Kilroy**: parallel 3-model fan-out with consensus node | No parallel fan-out; no cross-critique between reviewers |
| Cost-aware scoring | Token/cost in CXDB metadata, Healer aggregates | **Smasher**: per-session + per-pipeline accumulation, live OpenRouter pricing | No cost dimension in holdout evaluation; no cost budgets |
| Checkpoint recovery | JSON file checkpoint per step | **Kilroy**: 3 resume sources (filesystem, CXDB context-id, git branch), fidelity degradation on resume | No `--resume` CLI flag; no CXDB-based recovery |
| Multi-model support | Single `--backend` per run | **Kilroy**: CSS-like `model_stylesheet`, per-node provider, model escalation chains, `--force-model` | All LLM nodes use same backend; no per-node model routing |
| Conformance testing | `holdout_eval` against real server | **AttractorBench**: mock LLM server + 5-dim rubric + LLM Judge; **Smasher**: 3-tier conformance (SDK → agent → pipeline) | No mock LLM; no tiered conformance; no rubric scoring |

### NOT IMPLEMENTED

| Feature | Best Reference | Implementation Detail |
|---|---|---|
| **Parallel execution** (fan-out/fan-in) | **Kilroy**: `shape=component` parallel handler + `shape=tripleoctagon` fan-in with 4 join policies (wait_all, first_success, k_of_n, quorum); **Smasher**: `futures::stream::buffer_unordered` with bounded concurrency | dark-factory engine walks single path sequentially |
| **5-phase node lifecycle** | **Kilroy** spec Section 3.1: PARSE → VALIDATE → INITIALIZE → EXECUTE → FINALIZE | dark-factory has parse+execute, no validate/finalize phases |
| **Model stylesheet** (CSS-like) | **Kilroy**: `* { llm_provider: openai; } .code { llm_model: claude-opus-4-6; } #review { reasoning_effort: high; }` | No equivalent |
| **Failure classification + retry gating** | **Kilroy**: 6-class failure taxonomy (transient_infra, budget_exhausted, compilation_loop, deterministic, canceled, structural); only transient_infra is retryable by default | dark-factory has max_retries/max_visits but no failure taxonomy |
| **Model escalation chains** | **Kilroy**: `escalation_models="anthropic:claude-opus-4-6,openai:gpt-5.4"` on node; escalates after N retries | No equivalent |
| **Context fidelity control** | **Kilroy**: full/truncate/compact/summary:low/medium/high per edge or node | No equivalent (each codergen node gets fresh session) |
| **Sub-pipeline composition** | **Smasher**: `compose_graphs()` replaces SubPipeline nodes with referenced sub-graphs | No equivalent |
| **Streaming/SSE output** | **Smasher**: tokio broadcast + axum SSE + HTMX web dashboard | No equivalent |
| **Web dashboard** | **Kilroy** + **Smasher**: HTTP server with embedded UI, live event streams, human gate API | No equivalent |
| **DOT lint/validation** | **Kilroy**: dedicated `validate/` package with lint rules (reachability, provider-required, etc.); **Smasher**: `lint` subcommand | dark-factory parser validates start/exit + edge refs but no lint framework |
| **Ingest command** (English → DOT) | **Kilroy**: `kilroy attractor ingest` + create-dotfile skill | No equivalent |
| **Mock LLM server** | **AttractorBench**: Flask mock with canned responses per endpoint path | No equivalent |
| **LLM Judge scoring** | **AttractorBench**: 5 dimensions × 3 repetitions with stddev variance control | No equivalent |
| **Tiered conformance** | **AttractorBench** + **Smasher**: tier 1 (SDK) → tier 2 (agent) → tier 3 (pipeline) | No equivalent |
| **Airbnb-clone sealed scenarios** | TODO in `benchmarks/airbnb-clone/README.md:114` | Design-only, no sealed evaluator yet |

## What dark-factory has that the others DON'T

| Feature | Detail |
|---|---|
| Healer failure clustering | `runner/healer.py` clusters failures by (node, outcome, output_hash) and generates LLM-backed prescriptions. No other implementation has post-hoc failure clustering. |
| /es /er /code_standards slash gates | Factory-built via `_slash_gate()`. SHA binding + spoof protection. Unique to dark-factory. |
| Firebase emulator integration | `holdout_eval` handler starts Firebase emulators, polls for readiness, cleans up process groups. No other implementation has Firebase-specific support. |
| `df-slim` CLI | Dedicated slim runner with run.json manifest + summary.md. No other implementation has a dedicated "slim" mode. |
| Goal gate + retry_target | Node attribute `goal_gate=true` + `retry_target=` jumps directly to fix on failure. Kilroy has retry but not goal gates. |

## Key Architectural Insight

The four implementations **converge on three layers** (LLM client → Agent loop → Pipeline engine) but **diverge on execution model**:

| Impl | Language | Execution | Parallel | Multi-Model | Holdout |
|---|---|---|---|---|---|
| dark-factory | Python | Sequential graph walk | No | Single backend | Sealed repo + sandbox-exec |
| Kilroy | Go | Sequential + parallel fan-out | Yes (4 join policies) | Yes (CSS stylesheet + escalation) | No sealed holdouts; review_consensus |
| Smasher | Rust | Sequential + parallel (tokio) | Yes (bounded concurrency) | Yes (3 providers + catalog) | Tiered conformance (no sealed repo) |
| AttractorBench | Python | Sequential | Yes (Harbor --n-concurrent) | No (single provider) | Sealed mock LLM + LLM Judge |

dark-factory is the ONLY implementation with sealed holdouts + Healer + slash gates. It's also the ONLY one without parallel execution.

## Verification

- All repos confirmed at `~/projects/{attractorbench,kilroy,smasher,mammoth}`
- Feature inventory cross-referenced against source code in each repo
- dark-factory feature inventory from prior session's subagent analysis

## References

- `/Users/jleechan/projects/attractorbench/` — StrongDM AttractorBench
- `/Users/jleechan/projects/kilroy/` — Dan Shapiro Kilroy (Go)
- `/Users/jleechan/projects/smasher/` — 2389 Research Smasher (Rust)
- `/Users/jleechan/projects/mammoth/` — 2389 Research Mammoth (TypeScript)
- `/Users/jleechan/projects/dark-factory/` — dark-factory (Python)
- 2389.ai blog post: https://2389.ai/posts/the-dark-factory-is-a-dot-file/
- Dan Shapiro blog: https://www.danshapiro.com/blog/2026/02/you-dont-write-the-code/
- StrongDM AttractorBench: https://github.com/strongdm/attractorbench