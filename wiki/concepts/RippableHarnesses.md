---
title: "Rippable Harnesses"
type: concept
tags: ["architecture", "replaceability", "future-proofing", "model-updates"]
sources: ["harness-engineering-philosophy"]
last_updated: 2026-04-07
---

The principle that the orchestration layer should be thin and replaceable so that harness survives model updates. If AO adds native judgment support, or if Claude Agent Teams subsumes the reaction engine, the Python layer can be removed.

## Key Quote
> "If you over-engineer the control flow, the next model update will break your system."

## Implementation
- Keep orchestration layer thin (~3k lines of Python)
- Don't touch agent configs or project structure when replacing
- Design for replacement, not permanence

## Related Concepts
- [[Harness Engineering]] — overall discipline
- [[Agent Orchestrator]] — the orchestration layer
- [[OpenClaw]] — could subsume some AO functionality
