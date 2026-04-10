---
title: "7-Green Queue"
type: concept
tags: [ci, quality-gate, automation, verification]
sources: []
last_updated: 2026-04-07
---

## Definition
The 7-green queue is a quality gate standard requiring all seven automated checks to pass before a PR is eligible for merge. This ensures comprehensive verification before any code lands.

## The Seven Checks
1. **CI** — Continuous Integration tests pass
2. **CR** — Code Review approved
3. **Bugbot** — Bug detection passes
4. **Threads** — All discussion threads resolved
5. **Evidence** — Evidence/tests verified
6. **Skeptic** — Skeptic posts VERDICT: PASS
7. **Final Review** — Human final review (optional)

## Usage in AO Workflow
[[AgentOrchestrator]] runs workers until all 7-green conditions are met, then [[Skeptic]] posts the verdict on the current head SHA.
