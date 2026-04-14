---
title: "Mem2Evolve"
type: concept
tags: [agent-improvement, self-evolution, tool-creation, co-evolution, memory]
sources: [mem2evolve-paper]
last_updated: 2026-04-14
---

## Definition

A co-evolutionary framework for self-evolving agents that simultaneously accumulates experience AND creates new tools, with each process feeding the other bidirectionally. Published at ACL 2026.

## Core Insight

Experience-only evolution is bounded by a static toolset. Asset-creation-only evolution generates ungrounded tools. Only co-evolution unlocks compounding improvement: experience guides tool creation, new tools enable richer experience.

## How It Works

**Two Memories**:
- **Experience Memory**: Stores accumulated agent experience from task executions
- **Asset Memory**: Enables dynamic creation of new tools/assets

**Co-Evolutionary Loop**:
1. Experience → Tool Creation: accumulated experience guides dynamic tool generation
2. Tool Creation → Experience: new tools expand capability space, enabling fresh experience acquisition
3. Repeat: compounding gains from bidirectional feedback

## Key Results

- **18.53%** improvement over standard LLMs
- **11.80%** over experience-only baselines
- **6.46%** over asset-creation-only baselines
- Across 6 task categories, 8 benchmarks

## Related Concepts

- [[AgentMentor]] — external behavioral correction vs Mem²Evolve's internal co-evolution
- [[E3TIR]] — training-time experience exploitation vs Mem²Evolve's runtime tool creation
- [[SelfEvolvingAgents]] — Mem²Evolve is a specific architecture for self-evolution
