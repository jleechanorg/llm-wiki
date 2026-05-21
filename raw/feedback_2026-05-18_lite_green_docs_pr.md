---
name: Lite-green PR workflow for docs-only changes
description: Docs-only PRs use lite-green (3 gates: CI, mergeable, CR) not full 7-green
type: feedback
bead: none
---

## Context
PR #6945 (docs: trim mvp_site/CLAUDE.md) is docs-only — no production code under mvp_site/**.
The Green Gate workflow ran full 7-green and failed at Gate 6 (evidence), but for docs-only
PRs, evidence is not required.

## Technical detail
- Lite-green gates: (1) CI green for core checks, (2) mergeable=true, (3) CR APPROVED
- Skip: evidence (Gate 6), skeptic (Gate 7), Bugbot (Gate 4), comment resolution (Gate 5)
- Green Gate workflow does NOT distinguish lite-green from full 7-green
- Non-required CI failures (deploy-preview, test-deployment-build, generate-design-doc) are
  infra issues, not content-related — don't block lite-green
- Self-hosted runners offline (0 registered) cause permanent queued state for those jobs
- Branch protection with 0 required checks means infra failures are technically non-blocking

## Solution / Rule
For docs-only PRs (no production code under mvp_site/**):
1. Classify as lite-green, not 7-green
2. Only verify: CI core checks pass, mergeable=true, CR APPROVED exists
3. Ignore non-required workflow failures (deploy-preview, design-doc-gen, self-hosted runner jobs)
4. Report lite-green verdict explicitly in the status table

## Verification
PR #6945: Green Gate gates 1-5 all pass, Gate 6 fails (expected for docs-only).
CodeRabbit APPROVED, mergeable=MERGEABLE, core CI passes. Lite-green confirmed.

## References
- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/6945
- HEAD: 530d99d9d21f2a5b29e68bbdb799c3f0075572db
