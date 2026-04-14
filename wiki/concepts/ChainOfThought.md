---
title: "ChainOfThought"
type: concept
tags: ["reasoning", "prompting", "chain-of-thought"]
sources: []
last_updated: 2026-04-14
---

Chain-of-Thought prompting is a prompting technique where models are instructed to generate intermediate reasoning steps before producing a final answer. It is the precursor pattern to [[ExtendedThinking]] — CoT is a prompting technique while Extended Thinking is a built-in model capability.

## Key Properties
- **Prompting technique**: Enabled via instructions ("think step by step") not model architecture
- **Externalizes reasoning**: Makes the reasoning process visible in the output
- **Effective for arithmetic, commonsense reasoning, and code generation
- **Precursor to Extended Thinking**: Extended thinking internalizes and amplifies the CoT pattern

## Connections
- [[ExtendedThinking]] — the built-in model capability that extends CoT
- [[TestTimeCompute]] — both CoT and extended thinking leverage inference-time compute
- [[SelfCritique]] — CoT traces can be critiqued step by step

## See Also
- [[ExtendedThinking]]
- [[TestTimeCompute]]
