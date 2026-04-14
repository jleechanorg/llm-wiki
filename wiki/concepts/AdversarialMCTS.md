---
title: "AdversarialMCTS"
type: concept
tags: [adversarial-testing, monte-carlo-tree-search, code-generation, hidden-tests, pseudo-correctness]
sources: [advermcts-paper]
last_updated: 2026-04-14
---

## Summary

AdverMCTS combats pseudo-correctness in LLM code generation by framing it as a minimax game between a Solver agent (generates code) and an Attacker agent (generates adversarial tests). MCTS drives the adversarial dynamics, creating a dynamic filter that progressively challenges code against increasingly sophisticated hidden tests, reducing false positives and forcing generalization beyond public test distributions.

## Key Claims

- Pseudo-correctness (passing public tests, failing hidden tests) is a fundamental evaluation gap
- Static test suites create a weak, fixed environment that limits robustness
- Minimax dynamics between code generation and test generation are essential
- MCTS naturally balances exploration and exploitation in the adversarial search

## How It Works

1. **Solver Agent**: Synthesizes code candidates optimized for the current test environment
2. **Attacker Agent**: Generates corner-case tests that expose logical flaws in the code pool
3. **MCTS**: Drives the adversarial search, balancing code improvement vs test improvement
4. **Dynamic Filter**: Tests evolve as the code pool evolves, creating a moving target
5. **False Positive Reduction**: Penalizes solutions that are correct on public but not adversarial tests

## Relationship to Self-Refinement

AdverMCTS is a form of adversarial self-refinement:
- **Traditional self-refinement**: Model critiques and improves its own output
- **AdverMCTS**: An adversarial agent critiques and challenges the model's output
- Both aim to move beyond the initial weak solution, but AdverMCTS uses external adversarial pressure

## Comparison

| Aspect | AdverMCTS | RefineRL | ThinkTwice |
|---|---|---|---|
| Domain | Code generation | Competitive programming | Math reasoning |
| Critique source | Adversarial agent | Self (skeptical) | Self (binary reward) |
| Feedback | Adversarial tests | Public tests | Binary correctness |
| Algorithm | MCTS | RLVR | GRPO |
| Goal | Reduce false positives | Scale reasoning | Improve reasoning |

## Related Concepts

- [[SelfRefine]] — general self-refinement framework
- [[MonteCarloTreeSearch]] — the core search algorithm
- [[RefineRL]] — RL-based self-refinement for programming
- [[ThinkTwice]] — joint reasoning + refinement
- [[AdversarialTesting]] — adversarial evaluation methodology
- [[PseudoCorrectness]] — the specific problem being solved
