---
title: "Voyager"
type: concept
tags: [agentic-coding, embodied-agent, skill-library, self-verification, lifelong-learning]
sources: [voyager-paper]
last_updated: 2026-04-14
---

First LLM-powered embodied lifelong learning agent in Minecraft (2023). Three key components: automatic curriculum, ever-growing skill library of executable code, and iterative prompting with environment feedback + self-verification.

## Key Metrics
- 3.3x more unique items collected vs. prior SOTA
- 2.3x longer travel distances
- 15.3x faster at unlocking tech tree milestones
- Skills transfer to novel Minecraft worlds

## Architecture Pattern

```
Automatic Curriculum → Skill Library ←→ Iterative Prompting (GPT-4)
                         ↓
                   Self-Verification
```

## Core Innovations

1. **Automatic Curriculum**: continuously generates increasingly difficult tasks
2. **Skill Library**: stores executable code for reusable behaviors, retrieved by similarity
3. **Iterative Prompting**: incorporates environment feedback and self-verification

## Connections

- Pioneer of [[SelfRefine]] pattern — iterative prompting with self-verification
- Skill library pattern adopted by later frameworks
- [[AgentMentor]] extends self-verification as corrective instruction
- [[Mem2Evolve]] extends memory evolution from Voyager's skill library concept

## See Also
- [[SelfRefine]] — Madaan 2023 iterative refinement
- [[AgentMentor]] — execution log monitoring for corrective instructions
- [[SWE-Shepherd]] — PRM-based step-level guidance
