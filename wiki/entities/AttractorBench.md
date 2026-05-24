---
title: "AttractorBench"
type: entity
tags: [attractor-pattern, benchmark, coding-agents, nlspec]
date: 2026-05-24
---
## Overview
AttractorBench is StrongDM's benchmark for measuring how well coding agents implement systems from natural language specifications. It tests spec-following ability with deterministic verification against a mock LLM server.

## Key Properties
- **Type**: Benchmark harness
- **Key features**: Language-agnostic, deterministic mock LLM server, weighted composite scoring, cost-aware metrics
- **Source**: https://github.com/strongdm/attractorbench
- **Tiers**: 0 (smoke test), 1 (unified LLM SDK, 2150 spec lines, 35 tests), 2 (coding agent loop, 1450 lines, 20 tests), 3 (attractor pipeline, 2080 lines, 28 tests)
- **Scoring**: 5% build + 5% self-test + 30% each for T1/T2/T3 conformance (main task)
- **Contamination protection**: Conformance tests generated locally, excluded from repo; specs are intentionally public

## Connections
- [[StrongDM]] — StrongDM created AttractorBench
- [[Harbor]] — AttractorBench runs through Harbor's concurrent benchmark runner
- [[NLSpec]] — AttractorBench tests NLSpec-following ability
- [[MockLLMTesting]] — AttractorBench uses a mock LLM server for deterministic verification
- [[AttractorPattern]] — AttractorBench is the benchmark arm of the Attractor pattern

## See Also
- [[StrongDM]]
- [[NLSpec]]
- [[MockLLMTesting]]
