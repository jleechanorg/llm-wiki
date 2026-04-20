---
title: "Population Stability Index"
type: concept
tags: [ml-observability, drift-detection, statistics, monitoring]
sources: [ML monitoring literature]
last_updated: 2026-04-19
---

## Overview
PSI (Population Stability Index) is a statistical measure comparing the distribution of scores between two time periods or populations. It answers: has the model's input or output distribution shifted enough to warrant retraining or investigation? Industry-standard thresholds: PSI < 0.1 = stable, 0.1–0.2 = warning, > 0.2 = significant drift requiring action.

## Key Properties
- **PSI formula**: sum((Actual% - Expected%) * ln(Actual%/Expected%)) across bins
- **Stable**: PSI < 0.1 — distribution is stable
- **Warning**: PSI 0.1–0.2 — monitor closely, investigate cause
- **Significant drift**: PSI > 0.2 — retrain or repair policy/code
- **Binning sensitivity**: Choice of bin boundaries affects PSI value

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| Arize AI | ML observability | Uses PSI for production model monitoring |
| Phoenix | OSS observability | Open-source PSI monitoring |
| Drift-Detection | Concept | PSI is one specific drift detection method |

## Connection to ZFC Level-Up Architecture
PSI thresholds could monitor whether the model's `level_up_signal` output distribution shifts — e.g., if `level_up=true` rate suddenly drops from 15% to 5%, PSI would catch it before it becomes a production bug. Stage 5 of the ZFC implementation plan could incorporate PSI monitoring as a production drift indicator.

## See Also
- [[Drift-Detection]]
- [[OPA-Bundle-Signing]]
- [[ZFC-Level-Up-Architecture]]
