---
title: "Mock LLM Testing"
type: concept
tags: [attractor-pattern, testing, deterministic, mock-server]
date: 2026-05-24
---
## Overview
Mock LLM testing uses a deterministic server that returns canned responses instead of making real API calls. This enables reproducible, cost-free evaluation of coding agents — the same agent should produce near-identical conformance scores across runs, with variance only from agent non-determinism.

## Key Properties
- **What**: Deterministic mock LLM server that returns canned responses for testing agent implementations
- **Why matters**: Enables reproducible evaluation without API costs; separates agent quality from LLM availability/cost; prevents eval contamination (conformance tests generated locally, not in repo)
- **Key property**: Two runs of the same agent should produce near-identical conformance scores
- **AttractorBench implementation**: Mock server generated locally by `attractorbench generate`, intentionally excluded from the repo

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| [[AttractorBench]] | Benchmark | Uses mock LLM server for deterministic verification |
| [[StrongDM]] | Company | Pioneered mock LLM + digital twin approach |
| [[DigitalTwinUniverse]] | Concept | StrongDM's broader mock approach: clone GSuite, Salesforce, Okta |

## Connection to Attractor Pattern
Mock LLM testing is essential to the Attractor pattern's eval contamination protection. The NLSpec specs are public (training data contamination is fine — analogous to a developer reading the design doc), but the conformance tests, mock server, and scoring harness are sealed (generated locally, excluded from the repo).

## See Also
- [[AttractorBench]]
- [[DigitalTwinUniverse]]
