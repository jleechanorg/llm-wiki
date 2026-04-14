---
title: "Mem²Evolve: Towards Self-Evolving Agents via Co-Evolutionary Capability Expansion and Experience Distillation"
type: source
tags: [agent-improvement, self-evolution, tool-creation, co-evolution, memory]
sources: []
last_updated: 2026-04-14
---

## Summary

Mem²Evolve (ACL 2026) introduces a co-evolutionary framework that unifies two previously isolated agent improvement processes: experience memory (accumulating lessons from past tasks) and asset memory (dynamically creating new tools). The key insight is that these two loops feed each other bidirectionally — experience guides tool creation, and new tools enable richer experience. This breaks the ceiling of experience-only approaches (bounded by static toolsets) and asset-creation-only approaches (ungrounded tool generation).

## Key Claims

- **18.53% improvement** over standard LLMs across 6 task categories and 8 benchmarks
- **11.80% improvement** over experience-only evolution baselines
- **6.46% improvement** over asset-creation-only evolution baselines
- Co-evolutionary loop outperforms both isolated strategies, validating the bidirectional thesis
- Accepted at **ACL 2026 Main**

## Key Quotes

> "Experience-only evolution is bounded by a static, manually predefined toolset, while asset-creation-only evolution generates tools without experiential guidance, leading to limited capability growth." — Mem²Evolve paper

## Technical Architecture

**Experience Memory**: Stores accumulated agent experience from task executions — failures, strategies, context patterns.

**Asset Memory**: Enables dynamic creation of new tools/assets that expand the agent's capability space.

**Co-Evolutionary Loop**:
1. Accumulated experience guides dynamic tool creation (capability expansion)
2. New tools expand capability space → agent acquires fresh experience (experience distillation)
3. Repeat: experience distills into better tools, tools enable better experience

## Connections

- [[AgentMentor]] — both address agent self-improvement, but Agent Mentor focuses on execution log monitoring while Mem²Evolve focuses on co-evolving experience and tools
- [[E3TIR]] — both improve agent task performance through experience exploitation, but E3TIR focuses on training-time warm-up while Mem²Evolve focuses on runtime tool creation
- [[AgentArchitecture]] — core architectural innovation for self-evolving agents

## Contradictions

- None
