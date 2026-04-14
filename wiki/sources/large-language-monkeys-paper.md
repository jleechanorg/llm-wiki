---
title: "Large Language Monkeys: Scaling Inference Compute with Repeated Sampling"
type: source
tags: [inference-scaling, repeated-sampling, coverage, SWE-bench, self-debugging]
sources: [deepseek-v2-paper]
date: 2024-07-31
source_file: raw/arxiv-2407.21787-large-language-monkeys.md
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

## Connections

- Directly relevant to harness design — harness selecting among multiple agent attempts
- Core insight for SWE-bench based agent evaluation
- Supports repeated-trial approach for agentic coding robustness
- Related to [[SelfRefine]] — iterative refinement through multiple attempts
