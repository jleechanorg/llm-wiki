---
title: "Large Language Monkeys"
type: concept
tags: [inference-scaling, repeated-sampling, coverage, SWE-bench]
sources: [large-language-monkeys-paper]
last_updated: 2026-04-14
---

Inference compute scaling via repeated sampling. Key finding: coverage scales log-linearly with number of samples over four orders of magnitude. On SWE-bench Lite, DeepSeek-Coder-V2 rises from 15.9% (single sample) to 56% (250 samples).

## Core Insight

> "In domains with automatic verifiers, coverage directly translates to better task results"

## Scaling Law

```
Coverage ∝ log(N_samples)^k  (over 4 orders of magnitude)
```

## Key Findings

1. **Verifiable domains** (coding, formal proofs): coverage increases with samples, ceiling not reached at 250
2. **Non-verifiable domains**: majority voting and reward-model selection plateau after a few hundred samples

## Connections

- Evidence for harness design importance — verifier quality determines ceiling
- Related to [[SelfRefine]] — repeated attempt and selection
- Used by [[DeepSeek-Coder-V2]] for SWE-bench evaluation
- [[RefineRL]] extends this with RL-based selection
