---
title: "TestTimeCompute"
type: concept
tags: ["scaling", "inference-time", "reasoning", "scaling-laws"]
sources: []
last_updated: 2026-04-14
---

Test-Time Compute (also called Inference-Time Compute) refers to the practice of scaling the amount of computation performed at inference time rather than at training time. It is the research field that explains why [[ExtendedThinking]] and [[ReasoningBudget]] work.

## Key Properties
- **New scaling axis**: Previously, scaling meant training bigger models on more data. Now, you can also scale by giving models more think time.
- **Emergent reasoning**: Complex multi-step reasoning emerges from more inference-time compute
- **o1/o3/o4 effect**: OpenAI's o-series models demonstrated that test-time compute scaling produces dramatic improvements on hard tasks

## Connections
- [[ExtendedThinking]] — the primary implementation of test-time compute scaling
- [[ReasoningBudget]] — the mechanism for allocating test-time compute
- [[ScalingLaws]] — test-time compute changes the classical pre-training scaling laws
- [[ChainOfThought]] — CoT is a simple form of test-time compute

## See Also
- [[ExtendedThinking]]
- [[ScalingLaws]]
