---
title: "disk_magician"
type: entity
tags: [tool, skill, disk-diagnosis]
sources: [full-disk-diagnosis-topdown-bottomup]
last_updated: 2026-07-15
---

`disk_magician` is a Claude Code skill that runs disk usage diagnostics, growth-history logs, and automated cache/temp cleanup on development machines (companion skill: `disk-audit` for the analysis-only variant).

## Default behavior (as of 2026-07-15)

Per [[DiskDiagnosisReconciliation]] (bead jleechan-rvqz), `disk_magician`'s default first-use behavior for "why is my disk growing" questions is no longer cache-first. It must launch concurrent top-down, delta-validation, and bottom-up lanes and produce a full physical-vs-readable reconciliation before treating cleanup candidates or snapshot deltas as the diagnosis.

## Connections

- [[DiskDiagnosisReconciliation]] — the methodology now wired into this skill's default flow
