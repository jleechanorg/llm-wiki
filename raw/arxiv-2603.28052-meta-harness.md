---
title: "Meta-Harness: End-to-End Optimization of Model Harnesses"
type: paper
tags: [meta-harness, harness-optimization, context-management, outer-loop]
date: 2026-03-30
arxiv_url: https://arxiv.org/abs/2603.28052
---

## Summary
Meta-Harness is an outer-loop system that searches over harness code (context management, prompting strategies, tool use patterns) for LLM applications. It uses an agentic proposer that accesses source code, scores, and execution traces of prior candidates through a filesystem interface. Discovered harnesses outperform hand-engineered baselines by significant margins.

## Key Claims
- Improves over state-of-the-art context management by **7.7 accuracy points** while using **4x fewer context tokens**
- Improves accuracy on 200 IMO-level problems by **4.7 points** across five held-out models
- Discovered harnesses surpass hand-engineered baselines on TerminalBench-2
- Outer-loop optimization over harness code is tractable via agentic search

## Technique/Method
- **Agentic proposer**: reads prior harness candidates, execution traces, and scores to propose improvements
- **File-system interface**: proposer accesses structured information about past experiments
- **Search over harness space**: optimizes context management strategies, prompting approaches, tool selection
- **Model-agnostic**: validated across five held-out models

## Results
- 7.7 point improvement over best prior context management on held-out tasks
- 4x reduction in context tokens while improving accuracy
- TerminalBench-2: discovered harnesses beat human-engineered baselines
- 4.7 point gain on IMO-level problems (across 5 models)

## Limitations
- Computational cost of outer-loop search may be high for resource-constrained teams
- Search space definition requires upfront engineering to specify valid harness mutations
- Generalization to entirely new task domains not fully characterized

## Connections
- Related to [[Harness5LayerModel]] — Meta-Harness is an L2 (Context) and L3 (Execution) optimization technique
- Connects to prompt chaining and context management research
- Relevant to [[ZeroFrameworkCognition]] — harness as orchestrator, model as executor
