---
title: "PR Triage 4-Lens Verify Pipeline — 26 Misclassifications Caught"
type: source
tags: [pr-triage, adversarial-verify, codex, worldarchitect-ai, methodology]
date: 2026-07-24
source_file: feedback_2026-07-24_pr_triage_4lens_verify.md
---

## Summary

On 2026-07-24, a 4-lens adversarial verify pipeline (3 sonnet lenses + 1 codex cold review) caught 26 misclassifications across 73 non-draft open PRs at jleechanorg/worldarchitect.ai. The 4-lens verify standard is now mandatory for any merge-readiness classification in this repo. The lesson: title-prefix triage is insufficient — file paths must be verified against the `mvp_site/**` production boundary (per CLAUDE.md).

## Key Claims

- A single-model triage of 73 PRs is too prone to title-prefix shortcut; a 4-lens verify is the floor for production PRs.
- Lens 1 (Evidence) caught the highest-stakes defect: #8289 was classified as "superseded by #8178" based on title alone, but direct byte-content inspection showed #8289 contains the ONLY production fix functions for issue #8059 in mvp_site/world_logic.py. Closing #8289 would have lost the production fix.
- Lens 2 (Design) caught 5 false NON-PROD-DOCS classifications: e.g., #8428 title "docs(specs):" but diff touches mvp_site/action_resolution_utils.py (production code).
- Codex cold review caught 7 more defects including 2 PRs (#8545 MERGED, #8550 CLOSED) that the live state had changed during the triage itself.
- Cross-model review is non-optional: same-model verification shares blind spots. The 3-sonnet pass missed what codex caught.

## Key Quotes

> "Title-prefix triage is insufficient. A PR with title 'docs(specs):' can still modify mvp_site/. The verify pass MUST check `gh api repos/.../pulls/N/files` and grep for mvp_site/, mvp_site/prompts/**, or .github/workflows/ before accepting docs-only."

> "Cross-model review is non-optional. Same-model verification shares blind spots. The 3-sonnet pass caught 19 issues; codex caught 7 more that the sonnet agents either overlooked or got wrong. The 4-lens pipeline is the floor for any merge-readiness classification."

## Connections

- [[AdversarialVerifyPipeline]] — the 4-lens standard established by this learning
- [[WorldArchitectAI]] — repo where this was applied
- [[ClaudeCode]] — agent runtime (sonnet + codex)
- [[PRReview]] — concrete verification commands live here
- [[BeadRev-p8gin]] — the mission bead for this work
- [[MemoryFileFeedback2026-07-24PRTriage4LensVerify]] — the durable memory file

## Reusable pattern

For any merge-readiness classification:
1. Single-model triage (8-15 wide staggered fan-out per /swarm rule 4)
2. 3 sonnet adversarial lenses (evidence, design, severity) — refute-by-default
3. 1 codex cross-model cold review (full file inspection, not just reading JSON)
4. Aggregate corrected triage
5. Phase 7 close-recommendations with exact close commands
