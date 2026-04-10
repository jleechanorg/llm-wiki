---
title: "Evidence Enforcement"
type: concept
tags: [worldarchitect, evidence, ci, automation, gates]
sources: [worldarchitect-ao-nextsteps-2026-04-06, compaction-final-report-2026-04-06]
last_updated: 2026-04-06
---

## Summary
Evidence enforcement ensures AI coding agents attach real proof (screenshots, logs, video) to work artifacts before that work is considered complete or merged. In the WorldArchitect.AI context, evidence enforcement is a CI-gated workflow that prevents unverifiable claims from being promoted through the pipeline.

## Key Claims
- Evidence path merged via PR #6110 (evidence-gate.yml)
- Evidence Bundle Validation CI only checks **static structure** (grep, stubs, py_compile) — NOT actual `/tmp` bundle artifacts
- CI only fires on PRs touching `testing_mcp/**`, `testing_ui/**`, or the workflow file itself
- Branch protection: "Validate Evidence Bundles" must be added as a **required check** on `main` to fully close enforcement
- Priority beads: rev-b8a0 (branch protection), rev-3oon (real bundle CI validation)

## Evidence Gap
Evidence enforcement is "not fully enforced" because:
1. CI validates structure, not content (fake bundles could pass)
2. Many PRs never trigger the CI (path-based triggers are narrow)
3. No required check on main branch

## Connections
- [[WorldArchitect.AI]] — primary repo enforcing evidence
- [[AgentOrchestrator]] — cross-repo evidence alignment (bd-f6uh)
- [[FakeCodeDetection]] — complementary: enforces real implementations vs real evidence
- [[Beads]] — rev-b8a0 (branch protection), rev-3oon (bundle CI), rev-owc1 (gate triggers)
- [[CIgate]] — evidence-gate.yml as CI gate pattern
