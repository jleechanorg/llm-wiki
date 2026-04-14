---
title: "AutoML"
type: concept
tags: [AutoML, automated-machine-learning, hyperparameter-optimization, architecture-search]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

AutoML (Automated Machine Learning) is the broader field of automating machine learning tasks including hyperparameter optimization, architecture search, and neural network design. Meta-Harness extends AutoML principles to the harness code layer — automating the optimization of what information is presented to a fixed LLM rather than the LLM itself.

## Key Claims

- AutoML automates model selection, hyperparameter tuning, and architecture search
- Meta-Harness automates harness engineering — the code surrounding the LLM
- Key insight: changing harness (outer loop) produces 6x performance gap on fixed model
- Prior AutoML focuses on model/hyperparameter space; Meta-Harness extends to harness space
- Full source code + execution traces + scores enables automated harness engineering

## AutoML vs Meta-Harness

| Aspect | AutoML | Meta-Harness |
|--------|--------|--------------|
| What is optimized | Model, hyperparameters | Harness code |
| Fixed component | Data/hardware | LLM |
| Search space | Model architectures, configs | Context management code |
| Evaluation | Training/validation metrics | Full execution with rich traces |

## Connections

- [[ArchitectureSearch]] — component of AutoML related to Meta-Harness
- [[HyperparameterOptimization]] — another AutoML component
- [[MetaHarness]] — extends AutoML principles to harness code
- [[OuterLoopOptimization]] — the paradigm both AutoML and Meta-Harness operate in
