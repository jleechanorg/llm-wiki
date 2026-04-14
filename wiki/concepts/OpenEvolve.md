---
title: "OpenEvolve"
type: concept
tags: [OpenEvolve, text-optimizer, prompt-evolution, meta-harness]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

OpenEvolve is a text optimizer referenced in the Meta-Harness paper as a prior art comparison. Like ACE and AlphaEvolv, OpenEvolve represents the class of systems that attempt to optimize prompts or text through evolutionary or iterative methods, but with limitations on context access and feedback richness.

## Key Claims

- OpenEvolve is an evolutionary prompt/text optimizer
- One of several text optimizers compared against Meta-Harness
- Operates with compressed feedback and limited context (100-30K tokens)
- Like other prior text optimizers, fails on harness engineering due to memoryless operation
- Meta-Harness outperforms OpenEvolve by using full source code access and filesystem history

## Comparison Matrix

| Aspect | OpenEvolve | Meta-Harness |
|--------|------------|--------------|
| Optimization target | Prompts/text | Harness code |
| Context per step | 100-30K tokens | 10M tokens |
| Prior access | Current candidate | 20+ prior candidates |
| Feedback | Compressed templates | Full code + traces + scores |
| Results | Limited | State-of-the-art |

## Connections

- [[MetaHarness]] — outperforms OpenEvolve by optimizing harness rather than prompts
- [[ACE]] — another text optimizer compared in the paper
- [[AlphaEvolv]] — related optimizer with scalar feedback focus
- [[TextOptimizer]] — broader class OpenEvolve represents
