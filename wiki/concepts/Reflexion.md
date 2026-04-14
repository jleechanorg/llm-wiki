---
title: "Reflexion"
type: concept
tags: ["self-correction", "reflection", "verbal-reinforcement", "shinn-2023"]
sources: []
last_updated: 2026-04-14
---

Reflexion (Shinn et al., 2023) is a framework that formalizes self-critique with verbal reinforcement learning. It extends basic [[SelfCritique]] by maintaining a memory of past critique experiences, allowing the model to learn from its mistakes over multiple iterations.

## Key Properties
- **Memory of failures**: Stores verbal reflections on past errors in a memory store
- **Learning from mistakes**: Uses the reflection history to avoid repeating errors
- **Language-based feedback**: Uses linguistic descriptions of errors rather than gradients
- **State-of-the-art on code generation**: Achieves state-of-the-art results on HumanEval and MBPP when combined with code agents

## Connections
- [[SelfCritique]] — the foundational capability Reflexion builds upon
- [[SelfReflection]] — the meta-cognitive process of reflecting on one's own reasoning
- [[SelfDebugging]] — Reflexion is particularly effective for self-debugging agents
- [[ExtendedThinking]] — Reflexion can be applied within extended thinking traces

## See Also
- [[SelfCritique]]
- [[SelfDebugging]]
