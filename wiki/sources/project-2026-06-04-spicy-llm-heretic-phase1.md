---
title: "spicy_llm Heretic Abliteration Phase 1 (M4 Pro)"
type: source
tags: ["spicy-llm", "heretic", "abliteration", "apple-silicon", "m4-pro"]
date: 2026-06-04
source_file: project_2026-06-04_spicy_llm_heretic_phase1.md
---

## Summary
Repo state after Phase 1 (prebuilt smoke test): 1 commit unpushed, 2 new execution beads, MPS dual-load OOM still unroot-caused, kernels patches known-working but not ported to repo.

## Key Claims
- Hardware target: Apple M4 Pro, 14 cores, 51 GB unified memory, Metal 3
- Local `main` is 1 commit ahead of `origin/main` — commit `6992f02` (Phase 1: smoke-test heretic 20B vs stock)
- Phase 1 (prebuilt smoke test) done — 3 probes (drugs, erotica, Fibonacci) on heretic vs stock
- Phase 2 (DIY ablation) unproven on M4 Pro — Session 2 attempt on Qwen3-4B stalled at batch-128 for 30+ min
- Known M4 Pro footguns: `kernels` package import crash on Python 3.12, batch-128 stall, dual-model Ollama OOM

## Key Quotes
> When a future session touches `spicy_llm`, read this memory FIRST. It cuts the discovery loop from ~15 min to ~30 sec

## Connections
- [[SpicyLLM]] — repo entity
- [[HereticAbliteration]] — concept
- [[M4ProFootguns]] — concept
