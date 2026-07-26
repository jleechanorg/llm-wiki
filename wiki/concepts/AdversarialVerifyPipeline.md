---
title: "Adversarial Verify Pipeline"
type: concept
tags: [methodology, verification, code-review, pr-triage]
last_updated: 2026-07-24
sources: [sources/feedback-2026-07-24-pr-triage-4lens-verify.md]
---

## Definition

A multi-lens verification protocol where 2+ independent LLM agents with different prompts / model tiers are dispatched in parallel to refute-by-default a candidate finding. Survive only on majority non-refutation. Originated in the 2026-06 design-retro swarm (3-lens: evidence, design, severity) and extended in 2026-07-24 with a 4th codex cold-review lens for merge-readiness classification.

## Standard

For any merge-readiness classification on a real codebase:
1. **Lens 1 (Evidence)** — check actual file diffs, branch state, bead evidence, and recent commits
2. **Lens 2 (Design)** — check file paths against the production boundary (mvp_site/** etc.); verify scope creep
3. **Lens 3 (Severity)** — check staleness, supersession, WIP markers, blocking conditions
4. **Lens 4 (Codex cold review)** — full file inspection by a different model family (gpt-5.3-codex-spark), not just reading JSON

## Cost

- 3 sonnet lenses: ~$0.20-0.50 per finding class
- 1 codex cold review: ~$1-3 per mission (15-20 min wall time)
- Time: 5-15 min per lens, parallelizable

## When to use

- ANY merge-readiness classification on 10+ PRs
- ANY claim that a code change is "verified" or "tested"
- ANY recommendation to close, merge, or supersede a PR

## When NOT to use

- 1-3 PR triages (overhead exceeds value)
- Doc-only changes with no production code (Lens 1 and Lens 3 are overkill)
- Trivial dep bumps (1-line review sufficient)

## Origin

- 2026-06-25: First used in 42-agent design-retro swarm, 7/10 findings confirmed after 3-lens verify
- 2026-07-06: 180-agent design-retro docset published, codex cold review found 6 real defect classes that the same-model pass missed entirely
- 2026-07-24: 4-lens pipeline applied to 73-PR triage at jleechanorg/worldarchitect.ai; 26 misclassifications caught (1 false CLOSE, 5 false NON-PROD-DOCS, 13 false KEEP, 7 more by codex including 2 PRs already MERGED/CLOSED)

## Related

- [[PRReview]] — concrete commands
- [[SwarmStaggerFanout]] — staggering rule to avoid 429s
- [[CrossModelReview]] — the codex cold review lens
