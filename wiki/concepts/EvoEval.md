---
title: "EvoEval"
type: concept
tags: [benchmark, data-leakage, evaluation, evidence-based]
sources: [evoeval-paper]
last_updated: 2026-04-14
---

Evolving coding benchmarks via LLM to test robustness. Key finding: 39.4% average performance drop when benchmarks are evolved, with drastic ranking changes among top models.

## Core Problem

> Existing benchmarks show "potential overfitting" from data leakage and age

## Key Numbers

- **39.4%** average drop on evolved vs. original benchmarks
- **19.6% to 47.7%** range across models
- **51 LLMs** tested
- **Drastic ranking changes** among models

## Implication

Benchmark saturation and potential data contamination are real concerns. Instruction-following models are brittle when encountering rewording or subtle changes.

## Connections

- Evidence for benchmark integrity concerns
- Related to [[AgentBench]] evaluation methodology
- Supports need for diverse, evolving test suites
