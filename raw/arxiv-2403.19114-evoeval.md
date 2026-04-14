---
title: "EvoEval: Evolving Coding Benchmarks via LLM"
type: paper
tags: [benchmark, code-generation, data-leakage, evaluation, evidence-based]
date: 2024-03-28
arxiv_url: https://arxiv.org/abs/2403.19114
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

## Results
- Significant performance degradation across nearly all models on evolved benchmarks
- Rankings are unstable — models that rank highly on standard benchmarks don't always rank highly on evolved ones
- Suggests benchmark saturation and potential data leakage are real concerns

## Limitations
- Evolved benchmarks may not perfectly capture "real" coding difficulty
- The evolution method itself may introduce systematic biases
- 39.4% drop is an average — some models are more robust than others
- Doesn't fully solve the data contamination problem, just exposes it

## Connections
- Core evidence for benchmark integrity concerns in [[PRWatchdog]]-style evaluation
- Relevant to evidence-based evaluation practices
- Supports the need for diverse, evolving test suites for agentic coding evaluation
