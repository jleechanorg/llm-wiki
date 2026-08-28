---
title: "Semantic Anchor Scroll Restoration"
type: concept
tags: [streaming, scroll-anchor, ui, evidence, worldarchitect]
sources: [feedback-2026-08-28-pr9425-semantic-anchor-evidence]
last_updated: 2026-08-28
---

## Summary
Pattern for preserving a reader's actual reading position across streaming-completion DOM replacement, instead of relying on edge-derived surrogates (entry-root Y, `scrollTop`, scroll percentage). Introduced in `mvp_site/frontend_v1/app.js` by PR #9425 to fix a completion-time viewport yank: a heuristic that treated "active entry top near scrollport top" as bottom-follow intent would pass even when a sentence inside replaced markup moved hundreds of pixels.

## Key Claims

### Mutually exclusive intent modes
- Following is earned only from the real live-bottom band or an explicit rejoin action; trusted reader input (e.g. an upward wheel gesture) cancels it.
- Reading mode captures a visible narrative sentence with `Range.getBoundingClientRect()`, re-resolves that same sentence after completion replaces the DOM, and applies the measured delta in a bounded rAF transaction.

### Mandatory evidence ledger for a streaming-scroll PASS
One evidence bundle must jointly cover, or the result is PARTIAL/UNPROVEN:
- exact target SHA and served asset hash (not just branch name — dev deployments can silently serve `origin/main`)
- active-entry vs history-entry anchor identity
- trusted reader action and following/reading precondition
- real streaming path (not a mocked/synthetic completion)
- completion payload and layout transition (e.g. Debug Info/DM Notes + choices appearing)
- a fixture-owned unique sentence oracle, independent of any production text-matching code
- every-rAF sentence viewport-Y samples through completion and settling

Disqualified substitutes: entry-root Y, final-only position, scroll percentage, global `scrollHeight` compensation, a copied production matcher.

### Failure modes this rule was written to catch
- Testing the wrong scenario (older-history sentence) while shipping a fix for a different one (tall active-entry + four-choice completion).
- A root-level oracle that false-greens because the selected sentence moved ~243px during `innerHTML` replacement — fixed by freezing a unique literal sentence and resolving its `Range` independently each sample.
- Omitting a required trusted-input gesture in a harness port, producing a large drift number that is a harness bug, not a product regression.
- Polling a replaceable DOM locator that races completion — sample at page/rAF level and treat node disappearance as an expected transition.
- Conflating a dev deployment serving `origin/main` with the actual PR head — hash the served asset and fail closed on mismatch.

## Reusable Pattern
For any streamed UI, preserve what the reader sees, not an edge-derived surrogate: freeze a semantic target owned by the test fixture, sample it through the actual DOM replacement, treat bottom-pinning as explicit user intent, and validate the real provider/auth path separately from deterministic geometry-changing regression cases — each evidence layer proves something different and neither substitutes for the other.

## Connections
- [feedback-2026-08-28-pr9425-semantic-anchor-evidence](../sources/feedback-2026-08-28-pr9425-semantic-anchor-evidence.md) — originating source (PR #9425)
- [[StreamingEvidenceValidation]] — sibling evidence-discipline concept for server-side chunk timing
- [[IntegrateHardStopPattern]] — same fail-closed-on-ambiguity lineage
