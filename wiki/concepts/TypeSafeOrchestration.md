---
title: "Type-Safe Orchestration"
type: concept
tags: [type-safety, orchestration, python, dataclasses]
sources: [orchestration-system-design-justification.md]
last_updated: 2026-04-07
---

The practice of using Python dataclasses (`PRInfo`, `MergeReadiness`, `CIStatus`) to provide compile-time-like safety when composing multi-step GitHub workflows. This gives orchestration code type safety without requiring a full type system — raw `gh` output is untyped JSON strings, while the wrapper provides structured data.

See: [[gh_integration.py]]
