---
title: "Drift Detection"
type: concept
tags: [ml-observability, monitoring, policy, psi]
sources: [https://arize.com/blog/deploying-ai-spring-best-practices/]
last_updated: 2026-04-19
---

## Overview
Drift detection identifies when the distribution of model inputs, outputs, or underlying data changes over time in ways that may degrade performance. PSI (Population Stability Index) is the canonical metric: PSI < 0.1 = stable, 0.1–0.2 = warning, > 0.2 = significant drift requiring retraining or policy review.

## Key Properties
- **Feature drift**: Distribution of input features changes (P(x) shifts)
- **Prediction drift**: Distribution of model outputs changes over time
- **Concept drift**: Relationship P(y|x) between inputs and outputs shifts
- **PSI formula**: sum((Actual% - Expected%) * ln(Actual%/Expected%))
- **Kolmogorov-Smirnov test**: Non-parametric distribution equality test

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| Arize AI | ML observability | PSI monitoring platform |
| Phoenix | OSS observability | Feature drift tracking |
| OPA Bundle Revisions | Policy versioning | Git commit hash in manifest detects policy drift |

## Connection to ZFC Level-Up Architecture
The ZFC design doc's Stage 5 "Enforcement" step mentions adding grep gates to detect when new code re-interprets `level_up_signal` outside `rewards_engine.py`. This is a form of structural drift detection: monitoring whether the implementation diverges from the design contract over time.

## See Also
- [[PSI]]
- [[OPA-Bundle-Signing]]
- [[ZFC-Level-Up-Architecture]]