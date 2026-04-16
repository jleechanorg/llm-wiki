---
title: "Multi-Turn Alignment"
type: concept
tags: [multi-turn, alignment, instruction-following, agent-training]
date: 2026-04-15
---

## Overview

Multi-Turn Alignment refers to training data and methods for improving agent instruction-following across multiple conversation turns. It addresses the problem of long-horizon agent reasoning.

## Key Properties

- **Training data**: Multi-turn conversation data for alignment
- **Instruction following**: Improving agent ability to follow complex multi-step instructions
- **AgentBench finding**: "Poor long-term reasoning, decision-making, and instruction following abilities are the main obstacles for developing usable LLM agents"
- **Long-horizon**: Focus on maintaining coherence across many turns

## Connection to Governance

Multi-turn alignment is relevant to governance because governance constraints must be maintained across the entire evolve loop — not just in a single turn. Multi-turn capability ensures constraints persist.

## See Also
- [[AgentBench]]
- [[LLM Evaluation]]