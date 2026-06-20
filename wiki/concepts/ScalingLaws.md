---
title: "ScalingLaws"
type: concept
tags: ["scaling", "large-language-models", "compute", "pre-training"]
sources: []
last_updated: 2026-04-14
---

Scaling Laws describe the empirical relationship between model performance and factors like model size, training data, and compute. Classical scaling laws (Chinchilla, etc.) focused on pre-training compute. [TestTimeCompute](TestTimeCompute.md) introduces a new scaling dimension.

## Key Claims
- **Classical scaling**: Performance improves predictably with log-linear relationship to model parameters, dataset size, and training compute
- **Chinchilla scaling**: For a fixed compute budget, optimal performance requires scaling model size and training tokens proportionally
- **New frontier**: Inference-time compute (Extended Thinking, [ReasoningBudget](ReasoningBudget.md)) adds a new scaling axis that operates differently from pre-training scaling
- **Diminishing returns at scale**: At frontier model scale, further pre-training scaling yields diminishing returns; inference-time scaling may be more efficient

## Connections
- [TestTimeCompute](TestTimeCompute.md) — the new scaling axis
- [ExtendedThinking](ExtendedThinking.md) — benefits from test-time compute scaling
- [ReasoningBudget](ReasoningBudget.md) — mechanism for test-time compute allocation
- [Post-Chinchilla Era](ScalingLaws.md) — the shift from pure pre-training scaling to hybrid pre-training + inference-time scaling

## See Also
- [TestTimeCompute](TestTimeCompute.md)
- [ExtendedThinking](ExtendedThinking.md)
