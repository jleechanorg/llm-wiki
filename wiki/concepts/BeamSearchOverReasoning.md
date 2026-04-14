---
title: "Beam Search Over Reasoning"
type: concept
tags: [beam-search, reasoning-search, step-level-search, process-reward-search, inference-search]
sources: []
last_updated: 2026-04-14
---

## Summary

Beam Search Over Reasoning is the inference-time technique of maintaining multiple reasoning paths in parallel and pruning them based on step-level quality signals (e.g., from [[ProcessRewardModel]]). Unlike greedy decoding which commits to a single reasoning path, beam search explores k candidate paths simultaneously, using PRM scores to eliminate paths that go wrong early before wasting compute on flawed reasoning.

## Key Claims

- **Early pruning**: PRM-guided beam search terminates bad reasoning paths at the first bad step, not after a full generation
- **k paths**: Typically k=4 to k=16 candidate paths kept in parallel at each reasoning step
- **PRM-dependent**: Beam search over reasoning requires process-level reward signals — outcome supervision alone cannot guide step-level pruning
- **Enables [[TestTimeCompute]] efficiency**: By pruning bad paths early, compute is concentrated on promising directions
- **Underlies o1/o3-style reasoning**: Best-effort inference indicates beam search guided by internal process signals

## Beam Search vs Greedy Reasoning

| Aspect | Greedy Decoding | Beam Search over Reasoning |
|--------|-----------------|---------------------------|
| Paths explored | 1 | k in parallel |
| Bad path handling | Full generation wasted | Pruned at first bad step |
| PRM dependency | Optional | Required |
| Token efficiency | Lower | Higher |
| Implementation complexity | Simple | Moderate |

## Connections

- [[ProcessRewardModel]] — PRM provides the step-level scores that guide beam search pruning decisions
- [[TestTimeCompute]] — beam search is the mechanism for more efficient test-time compute allocation
- [[ExtendedThinking]] — beam search provides intelligent exploration during extended thinking
- [[ReasoningBudget]] — beam search helps budget-aware systems allocate compute to the most promising paths
- [[SelfCritique]] — PRM can be viewed as automated step-level self-critique powering beam search

## See Also
- [[ProcessRewardModel]]
- [[TestTimeCompute]]
- [[ExtendedThinking]]
- [[ReasoningBudget]]
