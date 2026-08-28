---
title: "Scenario parity and an independent sentence oracle are mandatory for streaming-scroll claims"
type: source
tags: [streaming, scroll-anchor, evidence, ui, worldarchitect, pr-9425]
sources: []
date: 2026-08-28
last_updated: 2026-08-28
source_file: raw/feedback_2026-08-28_pr9425_semantic_anchor_evidence.md
---

## Summary
PR [#9425](https://github.com/jleechanorg/worldarchitect.ai/pull/9425) fixed a completion-time viewport yank in `mvp_site/frontend_v1/app.js`: while a reader tracked a sentence inside a tall active entry, structured completion (Debug Info/DM Notes + four choices) rendered and yanked the sentence out of view in one frame. An initial synthetic probe reported 0 px drift, but it tested the wrong scenario (an older history sentence, not the tall active-entry/four-choice case), producing a false-green result. The fix separates mutually exclusive following/reading intent modes and implements bounded semantic-anchor restoration using `Range.getBoundingClientRect()` to track the reader's actual sentence across DOM replacement.

## Key Claims
- The old follower heuristic conflated "active entry top near scrollport top" with bottom-follow intent; entry-root or constant-`scrollTop` measurements can pass while a sentence inside replaced markup actually moves.
- Following is earned only from the real live-bottom band or explicit rejoin; trusted reader input (e.g. an upward wheel gesture) cancels it. Reading mode captures a visible sentence via `Range.getBoundingClientRect()`, re-resolves it after completion replacement, and applies the measured delta in a bounded rAF transaction.
- A streaming-scroll PASS is valid only when one evidence ledger jointly proves: exact target SHA + served asset hash, active-entry vs history-entry anchor, trusted reader action and following/reading precondition, real streaming path, completion payload/layout transition, a fixture-owned unique sentence oracle independent of production matching, and every-rAF sentence viewport-Y samples through completion and settling.
- Entry-root Y, final-only position, scroll percentage, global `scrollHeight` compensation, or a copied production matcher are explicitly disqualified as substitutes for sentence-level proof.
- At exact PR head `b9994c0a4214c335a89f00d817ff0d2f87e8b806`, a real `/localserver` + Firebase-auth + direct Gemini SDK (`gemini-3-flash-preview`) headless run returned HTTP 200, 82 server chunks, 34 DOM growth states, 857 rAF samples, 0 missing samples, 0 px max/final drift — proving the real provider/auth/streaming path but not replacing the deterministic geometry-changing regression cases as causal proof.

## Key Quotes
> "For streamed UIs, preserve what the reader sees, not an edge-derived surrogate. Freeze a semantic target owned by the fixture, sample it through the actual DOM replacement, and keep bottom pinning as explicit user intent."

## Harness Failures That Exposed the Rule
1. Initial synthetic case answered the wrong scenario (older-history sentence vs tall active-entry/four-choice completion).
2. A root-level oracle false-greened while the selected sentence moved ~243 px during `innerHTML` replacement; fixed by freezing a unique literal sentence and resolving its `Range` independently.
3. First real-Gemini Python port omitted the trusted upward wheel gesture, so the app correctly stayed in following mode and produced 1395.453125 px drift — a harness error, not a product regression.
4. Polling a replaceable `.streaming-text` locator raced completion; fixed by sampling at page/rAF level and atomically re-resolving the semantic sentence in the stable tagged entry.
5. A dev deployment serving `origin/main` was initially conflated with PR head; fixed by hashing the served asset and failing closed on SHA mismatch.

## Connections
- [[SemanticAnchorScrollRestoration]] — the reusable fix pattern and evidence-ledger rule this source defines
- [[StreamingEvidenceValidation]] — related but distinct: server-side chunk-timing evidence vs this source's client-side scroll/DOM evidence
- [[IntegrateHardStopPattern]] — same evidence-discipline lineage (fail closed on ambiguity rather than assume)
