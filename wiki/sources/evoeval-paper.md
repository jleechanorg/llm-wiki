---
title: "EvoEval: Evolving Coding Benchmarks via LLM"
type: source
tags: [benchmark, code-generation, data-leakage, evaluation, evidence-based]
sources: []
date: 2024-03-28
source_file: raw/arxiv-2403.19114-evoeval.md
---

## Summary

EvoEval examines whether leaderboard rankings on existing coding benchmarks reliably measure LLM program synthesis abilities. The paper introduces a benchmark suite that evolves existing benchmarks into different targeted domains to test robustness. Across 51 LLMs tested, there was an average 39.4% performance drop compared to standard benchmarks, with ranking changes among top models.

## Key Claims

- **39.4% average drop** in LLM performance when using evolved benchmarks vs. standard benchmarks
- Performance drops range from **19.6% to 47.7%** across models
- Causes "**drastic ranking changes**" among LLMs — leaderboard positions shift significantly
- Existing benchmarks (e.g., HumanEval) show "**potential overfitting**" from data leakage and age
- Instruction-following models are brittle when encountering rewording or subtle changes
- Highlights importance of learning **problem composition and decomposition**

## Technique/Method

- Uses LLMs to evolve existing benchmark problems into variants
- Targets different domains and problem compositions
- Tests 51 different LLMs on evolved benchmarks
- Compares performance and ranking stability between original and evolved benchmarks

## Connections

- Core evidence for benchmark integrity concerns in agent evaluation
- Relevant to evidence-based evaluation practices
- Supports the need for diverse, evolving test suites for agentic coding evaluation
