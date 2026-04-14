---
title: "AdverMCTS: Combating Pseudo-Correctness in Code Generation via Adversarial Monte Carlo Tree Search"
type: source
tags: [adversarial-testing, monte-carlo-tree-search, code-generation, hidden-tests]
sources: []
last_updated: 2026-04-14
---

## Summary

AdverMCTS tackles "pseudo-correctness" in LLM code generation — solutions that pass visible public tests but fail on hidden ones. The framework formulates code generation as a minimax game between a Solver agent (synthesizes code) and an Attacker agent (generates corner-case tests that expose logical flaws). The discovered tests form a dynamic, progressively hostile filter that penalizes fragile reasoning and forces models to generalize beyond initial constraints.

## Key Claims

- Pseudo-correctness is a fundamental problem: models overfit to static, sparse public test cases and fail on hidden tests
- Optimizing against a fixed, weak environment inherently limits robustness — adversarial dynamics are needed
- MCTS provides a natural framework for the minimax dynamics between code generation and test generation
- Dynamic adversarial filtering significantly reduces false positive rates compared to static test suites
- Forces models to generalize beyond the constraints of any fixed test distribution

## Methodology

1. **Minimax Game Formulation**: Code generation is framed as a two-player game:
   - **Solver Agent**: Synthesizes code candidates that maximize performance
   - **Attacker Agent**: Generates targeted corner-case tests that expose logical flaws in the code pool
2. **Monte Carlo Tree Search**: MCTS drives the adversarial dynamics, balancing exploration and exploitation in both code and test generation
3. **Dynamic Test Evolution**: Tests progressively adapt to the current code pool, creating a moving target that prevents overfitting
4. **False Positive Reduction**: Penalizes solutions that are correct on public tests but incorrect on adversarially generated hidden tests

## Results

- Significantly outperforms state-of-the-art baselines
- Effectively reduces false positive rates in code generation
- Forces models to generalize beyond initial constraints
- Demonstrated on code generation benchmarks with hidden test evaluation

## Connections

- [[SelfRefine]] — self-refinement applied to code generation with adversarial feedback
- [[MonteCarloTreeSearch]] — the core algorithmic framework
- [[AdversarialTesting]] — adversarial test generation for LLM evaluation
- [[PseudoCorrectness]] — the specific problem AdverMCTS addresses

## Authors

Qingyao Li, Weiwen Liu, Weinan Zhang, Yong Yu, Bo An
