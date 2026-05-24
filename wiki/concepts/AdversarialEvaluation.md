---
title: "Adversarial Evaluation"
type: concept
tags: [attractor-pattern, evaluation, red-teaming, scalable-oversight]
date: 2026-05-24
---
## Overview
Adversarial evaluation methods test AI systems using oppositional or critical approaches — red-teaming, constitutional AI, scalable oversight, debate, and cross-review. In the Attractor pattern, the sealed evaluator and agent isolation provide the adversarial structure.

## Key Properties
- **What**: Evaluation approaches that use opposition, critique, or hidden criteria to test AI system quality
- **Why matters**: Non-adversarial evaluation is vulnerable to Goodhart's law and reward hacking; adversarial methods produce more robust quality signals
- **Key methods**: Red-teaming (active attack), Constitutional AI (self-critique against principles), Scalable Oversight (weaker model supervised by stronger), Debate (competing agents argue), Cross-review (independent reviewers critique each other)

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| [[AttractorBench]] | Benchmark | Sealed evaluator is adversarial — agent doesn't know the tests |
| [[AgentIsolation]] | Concept | Prevents agent from gaming conformance tests |
| [[AttractorPattern]] | Pattern | CXDB + Healer is a form of automated adversarial monitoring |

## Connection to Attractor Pattern
The Attractor pattern embodies adversarial evaluation at multiple levels: (1) sealed conformance tests the agent can't see, (2) CXDB monitors every step for anomalies, (3) Healer clusters failures adversarially, (4) Tracker's cross-review uses three independent LLM providers critiquing each other.

## See Also
- [[AgentIsolation]]
- [[AttractorBench]]
- [[CXDB]]
