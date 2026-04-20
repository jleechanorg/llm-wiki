---
title: "Recursive Reward Modeling"
type: concept
tags: [ai-safety, scalable-oversight, reward-modeling, alignment]
sources: [Recursive Reward Modeling research]
last_updated: 2026-04-19
---

## Overview
Recursive Reward Modeling (RRM) is a scalable oversight technique where an AI system is trained to assist in evaluating other AI outputs, which in turn helps train better reward models for the original task. The supervisor AI learns to spot problems and flag them for human review — effectively building a hierarchy of oversight where each layer checks the next.

## Key Properties
- **Recursive structure**: AI helps evaluate AI outputs; evaluated outputs train better models
- **Human-in-the-loop preserved**: Human still provides the top-level signal, AI amplifies it
- **Scalable evaluation**: Reduces human workload by training AI to flag issues
- **Amplification**: Each iteration improves the reward model faster than pure human labeling

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| RLHF | Human feedback | Base technique RRM builds on |
| Scalable Oversight | Research field | RRM is one technique in this direction |
| Constitutional AI | Anthropic's approach | Similar goal but using AI self-critique instead of recursive evaluation |

## Connection to ZFC Level-Up Architecture
The ZFC model-computes pattern is a simplified one-step version of RRM: the model (LLM) makes the level-up judgment; the backend (rewards_engine) flags malformed outputs for fail-closed rejection. RRM's multi-layer evaluation is analogous to the ZFC pipeline: model output → formatter validation → persistence check → UI render.

## See Also
- [[Scalable-Oversight]]
- [[RLHF]]
- [[RLAIF]]
- [[ZFC-Level-Up-Architecture]]
