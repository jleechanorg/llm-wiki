---
title: "AI Debate"
type: concept
tags: [ai-safety, alignment, scalable-oversight, truth-seeking]
sources: [AI alignment debate research]
last_updated: 2026-04-19
---

## Overview
AI Debate is an alignment technique where two competing AI systems argue for different answers to a question; a human judge evaluates which argument is more truthful. The premise is that false statements are easier to attack than true ones — a truthful argument survives scrutiny that would defeat a false one. Introduced as a scalable oversight technique by the AI safety community.

## Key Properties
- **Truth-seeking**: False claims are easier to attack; good arguments survive adversarial debate
- **Human judge**: Human evaluates argument quality and correctness
- **Scalable**: Shifts evaluation burden from output quality to argument quality
- **Alignment technique**: Part of the scalable oversight research direction

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| Scalable Oversight | Research direction | Debate is one technique in this field |
| Constitutional AI | Anthropic implementation | Self-critique as a simpler version of debate |
| RLAIF | Feedback mechanism | AI preference model replaces human judge |

## Connection to ZFC Level-Up Architecture
Debate's principle — an honest agent can defend its choices under adversarial scrutiny — maps to why model-computed `level_up_signal` is more trustworthy than backend inference: the model's explicit structured output survives the formatter's fail-closed validation because it was explicitly computed and can be traced back to the model's reasoning.

## See Also
- [[Scalable-Oversight]]
- [[RLAIF]]
- [[Constitutional-AI]]
- [[ZFC-Level-Up-Architecture]]