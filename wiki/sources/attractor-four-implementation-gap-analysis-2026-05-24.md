---
title: "Attractor Pattern Four-Implementation Gap Analysis"
type: source
tags: [attractor, dark-factory, benchmark]
date: 2026-05-24
source_file: raw/attractor-four-implementation-gap-analysis.md
---

## Summary

Feature-by-feature comparison of dark-factory (Python) against the four canonical Attractor pattern implementations: AttractorBench (StrongDM, Python), Kilroy (Dan Shapiro, Go), Smasher (2389 Research, Rust), and Mammoth (2389 Research, TypeScript). All four converge on a three-layer architecture (LLM client → Agent loop → Pipeline engine) but diverge significantly on execution model, parallelism, and quality assurance features.

## Key Claims

1. **Three-layer convergence** — All four implementations independently arrived at the same architecture: LLM client layer, agent loop layer, pipeline engine layer. This is strong evidence the pattern is structurally correct.
2. **dark-factory is unique** — It is the ONLY implementation with sealed holdouts + Healer failure clustering + slash-command gates. It is also the ONLY one without parallel execution.
3. **Kilroy is the most feature-rich** — CSS-like model stylesheets, parallel fan-out/fan-in with 4 join policies, 6-class failure taxonomy, model escalation chains, context fidelity control, 5-phase node lifecycle, and a dedicated lint/validate package.
4. **Smasher is the most performant** — Rust + tokio gives bounded parallel concurrency; SSE streaming + HTMX dashboard; 3-tier conformance testing; live OpenRouter pricing integration.
5. **AttractorBench is the benchmark reference** — Mock LLM server with deterministic canned responses, 5-dimension LLM Judge with stddev variance control, Harbor concurrent runner.

## Key Quotes

- "dark-factory is the ONLY implementation with sealed holdouts + Healer + slash gates. It's also the ONLY one without parallel execution."
- "The four implementations **converge on three layers** (LLM client → Agent loop → Pipeline engine) but **diverge on execution model**"
- "Healer failure clustering — `runner/healer.py` clusters failures by (node, outcome, output_hash) and generates LLM-backed prescriptions. No other implementation has post-hoc failure clustering."

## Connections

- [[AttractorPattern]] — The three-layer convergence pattern shared by all four implementations
- [[AttractorBench]] — StrongDM's benchmark harness
- [[Kilroy]] — Dan Shapiro's Go implementation
- [[Smasher]] — 2389 Research Rust implementation
- [[Mammoth]] — 2389 Research TypeScript implementation
- [[ModelStylesheet]] — CSS-like model routing in DOT files (Kilroy)
- [[AttractorParallelExecution]] — Fan-out/fan-in parallel execution (Kilroy + Smasher)
- [[FailureDossier]] — Per-stage structured failure analysis (Kilroy)