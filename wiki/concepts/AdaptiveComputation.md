---
title: "AdaptiveComputation"
type: concept
tags: ["adaptive-compute", "dynamic-compute", "reasoning-budget"]
sources: []
last_updated: 2026-04-14
---

Adaptive Computation is the principle of dynamically allocating compute (tokens, time, model size) based on the complexity of the input. [[ReasoningBudget]] is the primary implementation of adaptive computation in frontier AI systems.

## Key Properties
- **Input-dependent**: More complex inputs receive more compute
- **Efficiency gains**: Avoids over-spending compute on trivial inputs
- **Multiple axes**: Can adapt model size, token budget, or number of reasoning steps
- ** [[ReasoningBudget]] implementation**: Reasoning budget is the token-based mechanism for adaptive computation

## Connections
- [[ReasoningBudget]] — the primary implementation
- [[ExtendedThinking]] — extended thinking modes implement adaptive computation
- [[AdaptiveContextTruncation]] — similar adaptive principle applied to context management

## See Also
- [[ReasoningBudget]]
- [[ExtendedThinking]]
