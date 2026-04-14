---
title: "Hyperparameter Optimization"
type: concept
tags: [hyperparameter-optimization, HPO, tuning, AutoML]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

Hyperparameter Optimization (HPO) is the process of automatically searching for optimal hyperparameters (such as learning rate, batch size, regularization) in machine learning models. Meta-Harness represents an analogous process applied to harness hyperparameters — the configuration settings that determine how context is managed and presented to the LLM.

## Key Claims

- HPO searches over model training configurations
- Meta-Harness searches over harness configurations (context management settings)
- Both use search over a configuration space to optimize performance
- The key insight: harness hyperparameters (what to store/retrieve/present) produce 6x performance gap
- Prior text optimizers fail because they don't search over the full harness configuration space

## HPO vs Meta-Harness

| Aspect | Hyperparameter Optimization | Meta-Harness |
|--------|---------------------------|--------------|
| What is optimized | Model training config | Harness context config |
| Fixed component | Model architecture | LLM |
| Search space | Learning rate, batch size, etc. | Context management code |
| Evaluation | Training metrics | Full execution with traces |
| Tokens per step | Varies | 10M tokens |

## Connections

- [[AutoML]] — hyperparameter optimization is a core AutoML component
- [[ArchitectureSearch]] — related AutoML component
- [[MetaHarness]] — applies optimization principles to harness code
- [[OuterLoopOptimization]] — harness hyperparameter optimization is outer loop
