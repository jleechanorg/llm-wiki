---
title: "Evidence Theater"
type: concept
tags: [CI, evidence, automation, failure-pattern]
last_updated: 2026-04-05
---

Workers systematically pick the lowest claim class (unit/docs) to avoid strong-proof requirements, and the gate accepts N/A for media on all claim classes.

## Root Causes

1. **Claim class self-selection with no floor** — workers always pick unit/docs regardless of actual claim type
2. **N/A accepted for Terminal/UI media on ALL claim classes** — not just unit
3. **Skills uncalled** — `tmux-video-evidence`, `ui-video-evidence`, `smoke-test-local` have no CI caller

## Impact

In 40 merged PRs, no real tmux video, UI GIF, or local server evidence was ever produced.

## Fixes Needed

- Add floor to claim class self-selection
- Remove N/A bypass for Terminal/UI on non-unit claim classes
- Wire `tmux-video-evidence`, `ui-video-evidence`, `smoke-test-local` skills into CI

## Connections

- [[EvidenceGate]] — CI gate that checks for ## Evidence section
- [SkepticGate](SkepticGate.md) — skeptic-gate workflow
- [VideoEvidenceFailure](VideoEvidenceFailure.md) — specific video evidence failure patterns
- [[RealAcceptanceVerdict]] — a variant where the artifact itself is authentic/current but its own assertions fail, and the gate never checks assertion results, only presence/provenance (PR 8489, 2026-07-28)
- [[BoundedStateMachinePRRecovery]] — the bounded-recovery pattern proposed to close this gap
