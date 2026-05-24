---
title: "NLSpec"
type: concept
tags: [attractor-pattern, specification, natural-language]
date: 2026-05-24
---
## Overview
NLSpec (Natural Language Specification) is a detailed prose specification that describes a software system with enough precision for a coding agent to implement it from scratch. The Attractor project provides ~5,700 lines of NLSpec across three tiers.

## Key Properties
- **What**: Prose specifications (not code) that describe a system's behavior, contracts, and Definition of Done
- **Why matters**: NLSpecs are the primary artifact in the Attractor pattern; code is disposable dorodango
- **Structure**: Tier 1 (~2,150 lines, unified LLM SDK), Tier 2 (~1,450 lines, coding agent loop), Tier 3 (~2,080 lines, DOT pipeline engine)
- **Key property**: Intentionally public — training data contamination is analogous to a developer reading the design doc before starting

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| [[AttractorBench]] | Benchmark | Tests NLSpec-following ability |
| [[AttractorPattern]] | Pattern | NLSpecs are the core artifact |
| [[Attractor]] | Repo | strongdm/attractor hosts the upstream NLSpecs |

## Connection to Attractor Pattern
NLSpecs ARE the Attractor pattern's primary deliverable. The bet is that well-written NLSpecs act as attractors in design space, pulling implementations toward a common architecture.

## See Also
- [[AttractorPattern]]
- [[DOTAsArtifact]]
- [[Dorodango]]
