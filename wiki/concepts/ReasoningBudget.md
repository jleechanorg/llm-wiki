---
title: "Reasoning Budget"
type: concept
tags: [reasoning-budget, test-time-compute, adaptive-compute]
sources: [extended-reasoning-frontier]
last_updated: 2026-04-14
---

## Summary

Reasoning Budget is the practice of allocating a variable number of thinking tokens to an AI model's inference based on task difficulty, priority, or expected complexity. Rather than a fixed per-task compute allocation, adaptive reasoning budgets allow the system to spend more compute on harder problems and less on trivially solvable ones. This creates a natural extension: assigning larger budgets to higher-priority tasks in a harness or orchestration pipeline.

## Key Claims

- Adaptive reasoning budgets are the computational equivalent of "think before you act" — harder problems receive proportionally more deliberation
- Models with reasoning budget APIs (o3, o4) expose a `max_tokens` or budget parameter that controls how much thinking can occur before output is committed
- Per-task priority routing in a harness can map task priority levels to reasoning budget tiers (e.g., P0 tasks get maximum budget, P3 tasks get minimal budget)
- Budget allocation can be optimized by collecting performance metrics per task type and tuning budget-size vs. quality tradeoffs
- Natural extension of test-time compute research: the insight that inference-time compute is a viable alternative to pre-training compute for certain problem types

## Connections

- [[ExtendedThinking]] — the underlying capability that reasoning budgets allocate
- [[TestTimeCompute]] — the research field studying how inference-time compute improves outputs
- [[AdaptiveContextTruncation]] — similar adaptive spirit applied to context window management rather than token budgets
- [[AgentPriorityOrdering]] — harness priority ordering can drive reasoning budget tier selection
- [[HarnessEngineering]] — a harness can implement reasoning budget routing as part of its worker dispatch logic

## Relationships to Other Concepts

A well-engineered harness should route tasks not only to the right agent model but also assign an appropriate reasoning budget. Low-stakes linting tasks get minimal budgets; complex multi-file refactors get high budgets with extended thinking enabled.

## See Also
- [[AdaptiveComputation]]
- [[TestTimeCompute]]
- [[ScalingLaws]]
