---
title: "Self-Improving"
type: concept
tags: [self-improving, AI, iteration, autonomous-improvement]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

Self-improving systems are AI systems that autonomously improve their performance over time through feedback, reflection, and iterative refinement. Meta-Harness is a self-improving system at the harness level — it iteratively refines harness code based on execution feedback, improving the information presented to the LLM.

## Key Claims

- Self-improving systems learn from feedback to improve performance
- Meta-Harness self-improves by searching over harness configurations
- Key enabler: filesystem-based history with full code + traces + scores
- 20+ prior candidates referenced per iteration — deep self-improvement
- Prior text optimizers fail at self-improvement because they are memoryless

## Self-Improvement Mechanisms

| System | How It Improves | Limitation |
|--------|-----------------|------------|
| Basic iteration | Try different prompts | No memory |
| ACE | Compressed feedback | Loses information |
| AlphaEvolv | Scalar scores | Limited signal |
| Meta-Harness | Full code + traces | Rich signal for improvement |

## The Meta-Harness Self-Improvement Loop

1. Agentic proposer reads source code + execution traces + scores
2. References 20+ prior candidates to avoid repeating failures
3. Proposes harness modifications
4. New candidate evaluated with 10M tokens
5. Results stored in filesystem history
6. Repeat with richer self-knowledge

## Connections

- [[MetaHarness]] — the self-improving system for harness engineering
- [[AgenticProposer]] — the agent that drives self-improvement
- [[ExperienceReplay]] — enables self-improvement through past experience
- [[FeedbackLoop]] — self-improvement requires effective feedback
- [[AgenticCoding]] — the broader practice of self-improving coding agents
