---
title: "WorldArchitect.AI + Agent Orchestrator Next Steps (2026-04-06)"
type: source
tags: [worldarchitect, agent-orchestrator, handoff, evidence, beads]
date: 2026-04-06
source_file: /Users/jleechan/Downloads/worldarchitect-ao-nextsteps-2026-04-06.md
---

## Summary

A handoff report covering evidence enforcement status, cross-repo priorities, and open beads for both WorldArchitect.AI (WA) and the Agent Orchestrator (AO). Evidence validation on WA is structurally incomplete — the "Evidence Bundle Validation" job only checks repo structure, not real `/tmp` bundles, and runs on too few PRs. The AO has a branch (`ao-beads-20260406`) ready for PR to main.

## Key Claims

- PR #6110 merged (evidence path, `evidence-gate.yml`, orchestration completion `exit_code`, beads)
- PR #6115 merged (roadmap `/nextsteps` + beads/docs)
- Evidence validation job is misleading — checks repo structure (grep/stubs/py_compile), not real evidence bundles
- Evidence gate workflow only runs on PRs touching `testing_mcp/**`, `testing_ui/**`, or the workflow file itself
- "Validate Evidence Bundles" must be added as a required check on `main` via branch protection (admin action)
- AO PR #335 installer (`install-skeptic-ci-for-repo.sh`) is a cross-repo dependency
- Multi-hyphen bead issue IDs caused `br` import failures; 13 renamed to 6-hex hash equivalents
- Bead `rev-stream-sign-env` had `updated_at < created_at` bug — fixed with proper timestamps

## Priority Beads (WorldArchitect.AI, prefix `rev-`)

| Bead | Focus | Blocked By |
|------|-------|-----------|
| rev-b8a0 | Add "Validate Evidence Bundles" as required check on main | — |
| rev-3oon | Validate real bundle artifacts (checksums under `EVIDENCE_TMP_ROOT`) | rev-b8a0 |
| rev-owc1 | Widen `evidence-gate.yml` path triggers or document exceptions | — |
| rev-g41u | Land/verify AO PR #335 installer | — |
| rev-zz65 | PR #6034 wizard — conflicts + review | — |
| rev-revgejn | Harness: `git worktree prune` after removing worktrees (pairv2) | — |

## Priority Beads (Agent Orchestrator, prefix `bd-`)

| Bead | Focus | Blocked By |
|------|-------|-----------|
| bd-f6uh | Cross-repo: align consumer evidence gates with WA rollout | bd-wx84 |
| bd-wx84 | Verify PR #335 installer on main; update consumer one-liners | — |
| bd-5g09 | Policy: workers attach real media evidence when job class requires | bd-7x6y, bd-806w |
| bd-7x6y | Skeptic: evidence defaults N/A — evaluate authenticity when required | — |

## Suggested Order of Work

1. Admin: Add required check "Validate Evidence Bundles" on WA main (rev-b8a0)
2. Engineering: Extend evidence CI to real bundle validation (rev-3oon)
3. Engineering: Widen evidence-gate triggers or document exceptions (rev-owc1)
4. AO: Open/merge PR `ao-beads-20260406`; complete bd-wx84 → bd-f6uh
5. Cross-repo: Keep rev-g41u / bd-wx84 / PR #335 in sync

## Connections

- [[AgentOrchestration]] — AO is the orchestration system coordinating workers
- [[EvidenceStandards]] — evidence enforcement is the central cross-repo concern
- [[Beads]] — beads tracking drives priorities and dependencies
- [[GitBranchTracking]] — branch protection rules for evidence validation

## Contradictions

- None identified
