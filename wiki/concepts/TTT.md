---
title: "TTT"
type: concept
tags: [TTT, test-time-training, test-time-computation, inference-time]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

TTT (Test-Time Training) is an approach mentioned in the Meta-Harness paper as part of the text optimization landscape. TTT involves training models at inference time on the specific task distribution to improve performance. It represents inference-time computation approaches that are compared against outer-loop optimization strategies.

## Key Claims

- TTT trains models at inference time on specific task distributions
- Part of the text optimization landscape compared against Meta-Harness
- TTT and similar approaches operate within the inner loop paradigm (optimizing inference)
- Meta-Harness demonstrates that outer loop optimization (optimizing harness code) can be more effective
- TTT is mentioned alongside OpenEvolve and AlphaEvolv as prior approaches

## Relationship to Meta-Harness

| Aspect | TTT (Test-Time Training) | Meta-Harness |
|--------|-------------------------|--------------|
| What is optimized | Model weights at inference | Harness code |
| Loop | Inner loop approach | Outer loop approach |
| Tokens per step | Per-inference training | 10M tokens per evaluation |
| Prior experience | Limited | Full filesystem history |

## Connections

- [[MetaHarness]] — demonstrates superior approach to TTT for harness engineering
- [[OpenEvolve]] — text optimizer also compared in the paper
- [[AlphaEvolv]] — related optimization approach
- [[InnerLoop]] — TTT is an inner loop optimization technique
