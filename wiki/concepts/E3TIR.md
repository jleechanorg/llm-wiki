---
title: "E3TIR"
type: concept
tags: [agent-improvement, tool-integrated-reasoning, experience-exploitation, synthetic-data, training-paradigm]
sources: [e3-tir-paper]
last_updated: 2026-04-14
---

## Definition

Enhanced Experience Exploitation for Tool-Integrated Reasoning — a warm-up training paradigm that integrates three experience types (expert prefixes, expert guided, self-exploration) around expert anchors with mix policy optimization to resolve prefix conflicts and mitigate distribution shifts. Published at ACL 2026.

## Core Insight

Training-time experience integration is more data-efficient than training from scratch. Anchoring exploration to expert demonstrations while allowing branching preserves quality without sacrificing diversity. Mix policy optimization prevents any single experience source from dominating and causing distribution shift.

## Three Experience Types

1. **Expert Prefixes** — expert-generated solution starts providing high-quality initialization
2. **Expert Guided** — step-by-step expert reasoning paths for structured exploration
3. **Self-Exploration** — agent-generated explorations expanding beyond expert boundaries

## Key Results

- **6-point improvement** over traditional TIR training paradigms
- **<10% synthetic data** required (data-efficient)
- **1.46x ROI gain** (performance × data cost × training efficiency)

## Related Concepts

- [[Mem2Evolve]] — Mem²Evolve is runtime tool creation, E3TIR is training-time warm-up; both improve through experience exploitation
- [[AgentMentor]] — E3TIR trains the model, Agent Mentor corrects at runtime; complementary layers
- [[ToolIntegratedReasoning]] — E3TIR is a training paradigm specifically for TIR tasks
- [[SyntheticData]] — E3TIR achieves strong results with <10% synthetic data
