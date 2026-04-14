---
title: "ACE"
type: concept
tags: [ACE, text-optimizer, feedback-compression, meta-harness]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

ACE (Agentic Context Engineering, or Adaptive Context Embedding) is a text optimizer referenced in the Meta-Harness paper as a prior art comparison. ACE represents the class of prior text optimizers that compress feedback to short templates and summaries. Meta-Harness outperforms ACE by 7.7 points on text classification with 4x fewer tokens.

## Key Claims

- ACE and similar text optimizers compress feedback to short templates or LLM summaries
- These optimizers operate on 100-30K tokens per optimization step vs 10M tokens for Meta-Harness
- ACE is memoryless — conditions only on current candidate, not full history
- ACE relies primarily on scalar scores, restricting feedback to short templates
- Meta-Harness demonstrates that richer access to prior experience (full code + traces) enables superior optimization

## Why ACE-Style Optimization Fails for Harness Engineering

| Limitation | ACE/Text Optimizers | Meta-Harness |
|------------|-------------------|--------------|
| Memory | Memoryless | Full filesystem history |
| Feedback richness | Scalar scores only | Full code + traces + scores |
| Context per step | 100-30K tokens | 10M tokens |
| Prior candidate access | Current candidate only | 20+ prior candidates |

## Connections

- [[MetaHarness]] — outperforms ACE by using richer access to prior experience
- [[OpenEvolve]] — another text optimizer compared against in the paper
- [[TextOptimizer]] — broader class of optimizers that ACE represents
