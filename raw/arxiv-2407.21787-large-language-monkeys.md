---
title: "Large Language Monkeys: Scaling Inference Compute with Repeated Sampling"
type: paper
tags: [inference-scaling, repeated-sampling, coverage, SWE-bench, self-debugging]
date: 2024-07-31
arxiv_url: https://arxiv.org/abs/2407.21787
---

## Summary
This paper explores inference compute scaling by generating many candidate solutions from a language model and selecting the best via verification. Coverage — the fraction of problems solved by at least one sample — scales log-linearly with the number of samples over four orders of magnitude. In domains with automatic verifiers (coding, formal proofs), coverage increases directly translate to better task results. Without verifiers, majority voting and reward-model selection plateau.

## Key Claims
- Coverage scales **log-linearly** with number of samples over **four orders of magnitude**
- The relationship follows an **exponentiated power law**, suggesting inference-time scaling laws exist
- On **SWE-bench Lite**: DeepSeek-Coder-V2 rises from **15.9%** (single sample) to **56%** (250 samples)
- Beats single-sample SOTA of 43% on SWE-bench Lite with 250 samples
- In non-verifiable domains: majority voting and reward-model selection **plateau after a few hundred samples**

## Technique/Method
- Repeated sampling: generate N candidate solutions, use verifier to select best
- Coverage metric: fraction of problems where at least one sample is correct
- Exponentiated power law fit to coverage vs. sample count
- Distinguishes verifiable domains (coding, formal proofs) from non-verifiable domains

## Results
- SWE-bench Lite: 15.9% → 56% with 250 samples (DeepSeek-Coder-V2-Instruct)
- Log-linear scaling observed across 4 orders of magnitude in sample count
- For verifiable tasks, more samples = better coverage; ceiling not reached at 250 samples
- Non-verifiable tasks hit ceiling around few hundred samples with selection strategies

## Limitations
- Requires access to a verifier (test suite, formal proof checker, etc.) for selection
- Compute cost grows linearly with sample count
- Non-verifiable tasks plateau; the approach doesn't help unboundedly there
- Single best model (DeepSeek-Coder-V2) used; generalization across models not fully characterized

## Connections
- Directly relevant to [[Harness5LayerModel]] L3 (Execution) — harness selecting among multiple agent attempts
- Core insight for SWE-bench based agent evaluation
- Supports repeated-trial approach for agentic coding robustness
