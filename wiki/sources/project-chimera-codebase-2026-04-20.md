---
title: "Project Chimera Codebase: April 2026"
type: source
tags: [multi-agent-systems, gnns, collective-intelligence, llm-orchestration, minimax]
sources: [project-chimera-neural-network-llm-agents-2026-04-19]
last_updated: 2026-04-20
---

## Summary

Live codebase implementation of Project Chimera at `/Users/jleechan/Downloads/chimera/`. Full 11-agent swarm with GNN topology generator, MiniMax M2.7 API integration, knowledge graph, and AI judge. All 9 tests pass. Demo runs end-to-end on real Minimax API.

## Key Claims

- 11 specialized agents (Router, 2×Miner, Expert, 2×Critic, FactChecker, Synthesizer, QualityGate, Explainer, GNNCoordinator) with role-based prompts
- GNN TopologyGenerator uses a 3-layer MLP to produce task-specific communication graphs with sparsity control
- MiniMax integration uses Anthropic `/v1/messages` endpoint (not OpenAI `/v1/chat/completions`) with thinking block handling
- KnowledgeGraph persists research outputs as nodes with concept edges via NetworkX + JSON
- Quality Gate fixed to check both "Pass" and "Approved" in response

## Architecture

```
Query → Router → GNN Topology Generator
              ↓
      Dynamic Agent Graph (11 nodes)
              ↓
      Execution (sequential per GNN plan)
              ↓
      Synthesis → Quality Gate → Explainer
              ↓
      Living Knowledge Graph + AI Scoring
```

## Agent Roles (11 implemented, 22 in full design)

| Agent | Role | Latency (real API) |
|-------|------|--------------------|
| Router | Task decomposition | ~0.7s |
| LiteratureMiner×2 | Source discovery | ~0.6s |
| DomainExpert | Deep technical analysis | ~60s (slowest) |
| Critic×2 | Red team / find flaws | ~0.6s |
| FactChecker | Verification | ~15s |
| Synthesizer | Final integration | ~0.7s |
| QualityGate | Pass/fail scoring | ~0.6s |
| Explainer | Multiple audience output | ~0.6s |
| GNNCoordinator | Topology oversight | ~0.5s |

## Verified Working

- **Tests:** 9/9 pass (`pytest tests/ -q`)
- **Single mode:** Real API, ~1-2s, rich structured output
- **Fixed pipeline:** Real API, ~77s end-to-end, quality gate approves
- **GNN mode:** Real API, GNN produces topology → swarm executes
- **MiniMax M2.7 model slug:** `minimax-m2.7` (lowercase, not `MiniMax-M2.7` which returns 529)
- **API endpoint:** `https://api.minimax.io/anthropic/v1/messages` (Anthropic-compatible)

## Known Limitations

- DomainExpert agent has ~60s latency on real API (long output + low max_tokens default)
- No retry/backoff for 529 rate-limit errors
- GNN topology is simulated (random seed per task), not actually trained
- Quality scores (6.8/8.7/9.1) are hardcoded mock values, not computed from real rubric
- Only 11 of 22 planned agents implemented

## Source Files

- `chimera/orchestrator.py` — SwarmOrchestrator (main pipeline)
- `chimera/gnn.py` — GNNTopologyGenerator (MLP-based graph generation)
- `chimera/knowledge_graph.py` — KnowledgeGraph (NetworkX + JSON persistence)
- `chimera/judge.py` — AIJudge (LLM-as-Judge evaluation)
- `chimera/utils.py` — MiniMaxClient (Anthropic /v1/messages wrapper)
- `chimera/agents/base.py` — BaseAgent + AgentConfig + AgentMessage
- `chimera/agents/*.py` — 9 specialized agent implementations
- `tests/` — 9 passing tests (agents, GNN, orchestrator)
- `run_demo.py` — quick demo entry point

## Connections

- [[ProjectChimera]] — design document this implements
- [[MultiAgentOrchestration]] — general orchestration patterns
- [[GNN]] — topology learning concept
