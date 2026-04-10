---
title: "Static Analysis"
type: concept
tags: [static-analysis, code-analysis, testing]
sources: [lightweight-architecture-analysis-helpers]
last_updated: 2026-04-08
---

## Definition
Code analysis performed without executing the program. Analyzes source code structure, patterns, dependencies, and metrics. Ranges from simple (line counting, regex matching) to complex (abstract syntax tree parsing, data flow analysis).

## Contrast with Lightweight Approach
The architecture helpers explicitly avoid heavyweight static analysis, using simple string counts as "proxies for patterns" rather than proper AST-based detection. This keeps the implementation lightweight and deterministic.

## Related Concepts
- [[Architecture Analysis]] — the broader process this supports
- [[Metadata Extraction]] — what the lightweight approach actually performs
