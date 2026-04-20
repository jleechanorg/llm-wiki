---
title: "Scalable Oversight"
type: concept
tags: [ai-safety, alignment, reinforcement-learning, human-feedback]
sources: [DeepMind scalable oversight research]
last_updated: 2026-04-19
---

## Overview
Scalable oversight is the research direction focused on enabling humans to supervise AI systems performing tasks too complex for direct human evaluation. The core problem: for tasks where humans cannot directly evaluate every decision (e.g., long-horizon code generation, multi-step reasoning), how do we train AI to behave correctly without constant human oversight?

## Key Properties
- **RLHF**: Learns reward model from human preference comparisons between trajectory pairs
- **RLAIF**: Uses AI feedback as reward signal when human labels are too expensive
- **Debate**: Competing AI systems argue; human judges evaluate which argument is more truthful
- **Recursive Reward Modeling (RRM)**: AI assists in evaluating other AI outputs to scale oversight
- **Paul Christiano et al.**: Canonical RLHF paper (NeurIPS 2017)

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| Constitutional AI | Anthropic's method | RLAIF variant using constitutional principles |
| RLHF | OpenAI's method | Human feedback for reward modeling |
| Debate | Alignment technique | AI competes to be more truthful |

## Connection to ZFC Level-Up Architecture
ZFC Level-Up's core question — should backend code or the model decide level-up facts — is a practical scalable oversight problem. The model is the "AI assistant" that can evaluate the game state; the backend is the "overseer" that receives the model's judgment and enforces it fail-closed. The model-as-judge pattern (RLAIF/CAI) is the pattern ZFC formalizes.

## See Also
- [[RLAIF]]
- [[Constitutional-AI]]
- [[Debate]]
- [[Recursive-Reward-Modeling]]
- [[ZFC-Level-Up-Architecture]]