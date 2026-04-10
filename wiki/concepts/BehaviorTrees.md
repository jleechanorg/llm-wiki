---
title: "Behavior Trees"
type: concept
tags: [AI-execution, deterministic, AgentLoop, hallucination-reduction]
sources: [openclaw-workshop-notes, agent-loop-demo]
last_updated: 2026-04-08
---

## Definition

A deterministic execution framework that forces LLMs to output structured JSON at each decision node, with programmatic validation verifying the fields. Used by [[AgentLoop]] to reduce hallucinations by 80-90%.

## The Problem with Pure LLMs

LLMs suffer from "graceful degradation" - when they run out of viable backup plans, rather than failing cleanly, they hallucinate and output plausible-sounding but broken code.

## The Behavior Tree Solution

1. LLM outputs highly structured JSON at each decision tree node
2. Traditional deterministic script verifies the JSON fields
3. If data is valid, script moves agent to next node
4. If invalid, agent must correct before proceeding

## Architecture Example

```
Planning -> Index Code Graph -> Write AST -> Execute Tests
    ^           |                  |
    |___________|__________________|
           (loop until valid)
```

## Key Benefits

- Explicit failure states instead of hallucination
- 80-90% reduction in hallucinations
- Makes "auto-YOLO" PR merging viable
- Deterministic execution across runs

## Why It Works

- Bounds context drift of the LLM
- Forces LLM through programmatic checkpoints
- Creates reliable, repeatable behavior

## Connections

- [[AgentLoop]] - Primary implementation
- [[DeterministicExecution]] - The goal of behavior trees
- [[HallucinationReduction]] - Measurable improvement
