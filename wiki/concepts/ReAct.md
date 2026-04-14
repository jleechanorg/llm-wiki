---
title: "ReAct"
type: concept
tags: [reasoning, acting, chain-of-thought, tool-use, agent]
sources: [react-paper]
last_updated: 2026-04-14
---

Synergizing Reasoning and Acting in Language Models (2022). Uses interleaved reasoning traces and task-specific actions to overcome hallucination and error propagation in chain-of-thought reasoning.

## Core Pattern

```
Thought → Action → Observation → Thought → Action → ...
```

Reasoning traces help the model:
- Induce and track action plans
- Handle exceptions dynamically
- Update plans based on new information

## Key Results

- **ALFWorld**: 34% absolute improvement over imitation and RL baselines
- **WebShop**: 10% absolute improvement over imitation and RL baselines
- Only 1-2 in-context examples needed

## Connections

- Foundation for [[Chain-of-Thought]] prompting research
- Precursor to [[Tool-Use]] agent frameworks
- Extended by [[SelfRefine]] — adds critique step to the loop
- [[E3-TIR]] extends tool-integrated reasoning
