---
title: "Project Chimera: A Neural Network of LLM Agents"
type: source
tags: [multi-agent-systems, gnns, collective-intelligence, llm-orchestration]
sources: []
last_updated: 2026-04-19
---

## Summary

Project Chimera is a design for a dynamic multi-agent system where frontier LLMs (primarily MiniMax M2.7, with selective GPT-5.4 for synthesis/gate roles) act as neurons in a learned graph. A Graph Neural Network (GNN) generates task-specific communication topologies, deciding which agents participate, how they connect, and how information flows. The primary application is a Living Knowledge Wiki — a self-updating, multi-perspective encyclopedia.

## Key Claims

- Multi-agent collaboration with learned topology outperforms fixed pipelines and single-model outputs
- A GNN can learn to optimize agent communication graphs based on quality, efficiency, and sparsity
- Budget implementation ($30–80/month) is viable using M2.7 as the primary model
- 22-agent system should beat single-model baseline by ≥20% on quality metrics
- System self-improves via triadic co-evolution: agents propose new roles, patterns, and architectures

## Key Quotes

> "Instead of fixed pipelines or hand-crafted swarms, Chimera uses a learned GNN to dynamically design the optimal agent collaboration graph for every task."

> "Neurons = Individual specialized LLM agents (MiniMax M2.7 + selective GPT-5.4); Connections/Weights = Learned edges produced by the GNN; Forward Pass = Task flows through the dynamically generated graph."

## Architecture

**5-Layer System:**
1. **Input Layer** — Task Router & Decomposer
2. **Dynamic Topology Layer** — GNN generating communication graphs
3. **Execution Layer** — Specialized agent swarm
4. **Memory & Knowledge Layer** — Shared blackboard + persistent Knowledge Graph
5. **Output & Evaluation Layer** — Synthesis, Quality Gate, AI Scoring

**GNN Training Signal:** Maximize quality score + factual accuracy, minimize tokens used, maximize graph sparsity.

## 22-Agent MVP Configuration

| Count | Role | Model |
|-------|------|-------|
| 1 | Task Router | M2.7 |
| 5 | Literature Miners | M2.7 |
| 4 | Domain Experts | M2.7 |
| 4 | Critics / Red Team | M2.7 |
| 2 | Fact Checkers | M2.7 + GPT-5.4 |
| 1 | Synthesizer | GPT-5.4 |
| 1 | Quality Gate | GPT-5.4 |
| 2 | Explainers | M2.7 |
| 1 | GNN Coordinator | M2.7 |
| 1 | Meta-Evolver (future) | M2.7 |

## Evaluation

5-dimension LLM-as-Judge rubric:
- Factual Accuracy (30%)
- Comprehensiveness & Depth (25%)
- Clarity & Structure (20%)
- Usefulness (15%)
- Efficiency (10%)

Comparisons run blind: single model vs fixed 22-agent pipeline vs full Chimera with GNN.

## 6-Week Roadmap (31 commits, TDD style)

- **Phase 0 (Week 1):** Project setup, base Agent class, pytest infrastructure
- **Phase 1 (Weeks 1–2):** SwarmOrchestrator with sequential + parallel execution
- **Phase 2 (Weeks 2–3):** Full 22-agent roles, first working swarm
- **Phase 3 (Weeks 3–5):** GNN topology layer (PyTorch Geometric or MLP)
- **Phase 4 (Weeks 5–6):** Knowledge Graph (NetworkX + JSON persistence), blackboard
- **Phase 5 (Weeks 6–7):** AI Judge, quality gate, full evaluation harness

## Living Knowledge Wiki

Every entry is: continuously updated by agent swarms, backed by debate traces and confidence scores, available in multiple difficulty levels, proactively expanded when gaps detected.

## Connections

- [[MultiAgentOrchestration]] — relates to the swarm execution pattern
- [[GNN]] — the topology learning mechanism
- [[CollectiveIntelligence]] — the emergent capability concept
- [[LLM Scoring]] — the 5-dimension evaluation rubric
