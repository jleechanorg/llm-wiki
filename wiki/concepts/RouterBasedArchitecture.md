---
title: "Router-Based Architecture"
type: concept
tags: [routing, agent-skill, decision-making, orchestration]
date: 2026-04-15
---

## Overview

Router-based architectures use a central decision component to select which agent skill or tool to invoke for a given task. The router evaluates the input and decides the execution path.

## Key Properties

- **Central router**: Decision-making component for task routing
- **Skill selection**: Routes to appropriate agent skill based on input
- **AgentBench**: Uses router-based evaluation across 8 environments
- **Decision criteria**: Router evaluates task type, complexity, domain

## Connection to Governance

Router-based architectures are relevant to governance gate enforcement — a router could evaluate whether a PR meets governance criteria and route accordingly (to merge gate, to escalation, etc.).

## See Also
- [[AgentBench]]
- [[GovernanceLayer]]