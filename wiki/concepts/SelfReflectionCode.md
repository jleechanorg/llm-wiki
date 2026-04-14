---
title: "Self-Reflection in Code Generation"
type: concept
tags: [self-reflection, code-representation, self-debugging]
sources: [self-reflection-code-paper]
last_updated: 2026-04-14
---

Self-reflection approach for generating Equivalent Representations (ERs) of code. Two LLMs collaborate iteratively to produce semantic-preserving representations (comments, pseudocode, flowcharts).

## Core Pattern

```
Dual-LLM Collaboration:
  LLM-1 generates representation
  LLM-2 evaluates and critiques
  → Iteration until semantic preservation confirmed
```

## Key Empirical Findings

1. LLMs understand syntactic structures better than expected
2. API usage comprehension is strong
3. Numerical computation understanding is limited
4. Iterative reflection outperforms single-pass

## Connections

- Precursor to [[SelfRefine]] — iterative refinement
- [[SelfDebugging]] extends self-reflection to code correctness
- [[AgentMentor]] applies reflection to execution logs
