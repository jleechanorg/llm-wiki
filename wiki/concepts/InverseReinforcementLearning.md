---
title: "Inverse Reinforcement Learning"
type: concept
tags: [irl, cirl, reward-learning, human-preferences]
date: 2026-04-15
---

## Overview

Inverse Reinforcement Learning (IRL) learns reward functions from observed human behavior. Rather than specifying goals directly, IRL infers what humans want from their actions.

## Key Properties

- **Learning from observation**: IRL infers reward function from human behavior
- **CIRL**: Cooperative Inverse Reinforcement Learning — CHAI's foundational framework
- **Human preferences**: IRL is a method for learning human preferences without explicit specification
- **Reward hacking prevention**: Learning from humans avoids reward hacking

## Connection to Governance

IRL-style learning from feedback is exactly what Grok's critique #3 calls for — governance rules that learn from human corrections rather than being statically specified. RLAIF uses a similar principle for AI feedback.

## See Also
- [[ValueAlignment]]
- [[CIRL]]
- [[RLAIF]]