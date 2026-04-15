---
title: "Drift Detection"
type: concept
tags: [drift-detection, ml-observability, concept-drift, data-drift]
date: 2026-04-15
---

## Overview

Drift Detection monitors production ML systems for performance degradation and distribution changes. Types include concept drift (changes in interpretable features) and data drift (changes in input distributions).

## Key Properties

- **Concept Drift**: Distribution changes in model interpretable features
- **Data Drift**: Input distribution changes
- **PSI (Population Stability Index)**: Metric for measuring drift magnitude
- **Arize/Phoenix**: Production ML observability platforms
- **Quote**: "An effective observability tool should not only automatically surface issues, but drill down to the root cause of your ML problems and act as a guardrail for models in production"

## Connection to Governance

Drift detection is the feedback loop mechanism that Grok's critique #3 calls for — governance rules that detect when they are too strict or too loose based on observed drift in outcomes.

## See Also
- [[ArizeAI]]
- [[FeedbackLoops]]
- [[GovernanceLayer]]