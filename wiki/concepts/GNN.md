---
title: "GNN (Graph Neural Network)"
type: concept
tags: [graph-neural-networks, machine-learning, topology, agent-communication]
sources: [project-chimera-neural-network-llm-agents-2026-04-19]
last_updated: 2026-04-19
---

## Definition

A Graph Neural Network that operates on graph-structured data. In Project Chimera, the GNN learns to generate optimal communication topologies between LLM agents, outputting which agents should participate, how they connect, and how information flows.

## How It Works (Chimera Context)

**Inputs to GNN:**
- Task embedding
- Current agent pool state
- Historical performance data

**Outputs from GNN:**
- Selected agents (nodes)
- Communication edges with weights
- Recommended interaction style (debate, handoff, blackboard, etc.)

**Training Signal:**
- Maximize quality score (factual accuracy + usefulness)
- Minimize total tokens used
- Maximize graph sparsity

## Connections

- [[ProjectChimera]] uses GNN as its "neural" core for dynamic topology generation
- Related to [[CollectiveIntelligence]] — the learned topology enables emergent group reasoning
