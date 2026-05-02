---
title: CAMEL
type: concept
tags: [multi-agent, role-playing, cooperative-agents, autonomous-collaboration]
date: 2026-04-23
sources: [chimera-p13-findings]
---

## Definition
CAMEL (Communicative Agents for Mind Exploration of Large Language Model Society), Li et al., NeurIPS 2023, is a multi-agent role-playing framework where agents are assigned specific roles and cooperate through structured conversation to solve tasks.

## Key Insight
Autonomous multi-agent cooperation requires inception prompting to maintain consistency. When agents are given clear role constraints and task goals without step-by-step instructions, they can autonomously cooperate toward solving complex tasks.

## Chimera Connection
Hybrid's failure mirrors a CAMEL anti-pattern: throwing modes together without a coordinating framework. Hybrid's arbiter receives conflicting signals from modes that were never trained to operate jointly. The contrast with Fixed mode — which uses a consistent single-critic workflow — shows that structured role/prompt alignment matters more than access to multiple modes.

## Key Quote
> "Hybrid's arbiter faces conflicting signals from modes that were never trained to operate jointly" — second opinion analysis

## Reference
- https://arxiv.org/abs/2303.17760