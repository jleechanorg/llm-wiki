---
title: "Constitutional AI"
type: concept
tags: [alignment, safety, constitutional-classifiers, rlaif, training]
date: 2026-04-15
---

## Overview

Constitutional AI is a training methodology (Anthropic) for building safe AI systems through self-improvement guided by a "constitution" of principles. It reduces the need for human labelers by using AI feedback.

## Two-Phase Training

### Phase 1: Supervised Learning (SL)
1. Sample AI response
2. AI self-critiques against constitutional principle
3. AI revises response
4. Finetune on revised responses

### Phase 2: Reinforcement Learning (RL/RLAIF)
1. AI preference model scores responses
2. RL optimizes against preference model (RLAIF)
3. Constitutional Classifiers filter outputs

## Key Innovations

- **Chain-of-thought reasoning**: Transparency in harmlessness judgments
- **Non-evasive harmlessness**: Explains objections rather than refusing
- **Reduced labeling burden**: AI feedback replaces most human labels
- **Constitutional Classifiers**: Production deployment — "filtered overwhelming majority of jailbreaks"

## Connection to Governance

Constitutional AI's principle-based constraint model is relevant to governance layer design:
- Hard constraints (IMPLICIT_DENY_LIST) similar to constitutional principles
- Self-critique pattern relevant to evidence verification
- Constitutional Classifiers demonstrate principle-based filtering at scale

## See Also
- [[RLAIF]]
- [[ConstitutionalClassifiers]]
- [[AnthropicAlignment]]
- [[GovernanceLayer]]
