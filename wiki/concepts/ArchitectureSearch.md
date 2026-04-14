---
title: "Architecture Search"
type: concept
tags: [architecture-search, neural-architecture-search, NAS, AutoML, outer-loop]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

Architecture Search is the broader field of automated search over neural network architectures, which includes Neural Architecture Search (NAS). Meta-Harness can be viewed as applying architecture search principles to harness code rather than model architecture — searching over the space of harness configurations that determine what information is presented to the LLM.

## Key Claims

- Architecture search automates the discovery of neural network topologies
- Meta-Harness applies similar search principles to harness code
- The key difference: what to present to a fixed LLM (harness) vs what LLM architecture to use
- Outer loop optimization of harness produces 6x performance gap on fixed model
- Architecture search principles (search over large space, rich evaluation) transfer to harness engineering

## Relationship to Meta-Harness

| Aspect | Traditional Architecture Search | Meta-Harness |
|--------|--------------------------------|--------------|
| Search space | Network architectures | Harness code |
| What changes | Model weights/connections | Context management code |
| Evaluation | Training metrics | Full execution with traces |
| Scale | Millions of parameters | 10M tokens per evaluation |

## Connections

- [[AutoML]] — the broader field that includes architecture search
- [[HyperparameterOptimization]] — related automated optimization
- [[MetaHarness]] — applies architecture search to harness code
- [[OuterLoopOptimization]] — the paradigm Meta-Harness operates in
