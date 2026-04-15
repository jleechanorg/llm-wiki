---
title: "RLAIF"
type: concept
tags: [reinforcement-learning, ai-feedback, alignment, constitutional-ai]
date: 2026-04-15
---

## Overview

RLAIF (Reinforcement Learning from AI Feedback) is a training paradigm where an AI model provides feedback signals to train another AI model, replacing or augmenting human feedback.

## Key Properties

- **Feedback source**: AI preference model (not human labelers)
- **Used in**: Constitutional AI (RL phase)
- **Advantage**: Scales beyond human labeling capacity
- **Risk**: Cascading errors if feedback model is flawed

## Relevance to Governance

RLAIF-like feedback loops could inform governance rule improvement:
- If a governance rule causes 80% of PRs to fail, the system needs a feedback mechanism to detect and correct this
- Current PR #452/#453 design lacks this feedback loop (per Grok's critique)
- A RLAIF-inspired system could learn which constraints are too strict or too loose

## See Also
- [[ConstitutionalAI]]
- [[GovernanceLayer]]
- [[AnthropicAlignment]]
