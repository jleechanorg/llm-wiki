---
title: "LLM-as-Judge Pattern"
type: concept
tags: ["llm", "judge", "evaluation", "review"]
sources: ["orchestration-architecture-research"]
last_updated: 2026-04-07
---

Pattern where a secondary LLM evaluates agent outputs (diffs, code changes) before merge. Used by Spotify's Honk System. Vetoes approximately 25% of sessions. Agents successfully course-correct in about 50% of veto cases.

## Failure Modes (in order of severity)
1. Failed PR generation (minor — manual fallback acceptable)
2. CI failures (frustrating — forces engineer remediation)
3. Functionally incorrect but CI-passing code (critical — erodes trust)

## See Also
- [[Spotify]] — implementation reference
- [[Deterministic Orchestration]] — inner loop verifiers run before PR creation
- [[Orchestration Architecture Research]]
