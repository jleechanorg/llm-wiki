---
name: Scenario parity and an independent sentence oracle are mandatory for streaming-scroll claims
description: Preserve the reader's actual sentence through streaming completion, and fail closed when scenario, SHA, intent, or oracle parity is missing.
type: feedback
bead: rev-ppors
---

# Context

PR [#9425](https://github.com/jleechanorg/worldarchitect.ai/pull/9425) fixes a
completion-time viewport yank in `mvp_site/frontend_v1/app.js`. The first probe
at `96e60612d32ef391720d4c31152f3f618faf85fa` parked an older history sentence
and reported 0 px drift over 79 streaming samples. That result was true only for
that scenario. The user's real-site video showed a different path: while reading
a sentence inside the tall active entry, structured completion rendered Debug
Info/DM Notes and four choices and yanked the sentence out of view in one frame.

# Technical cause and fix

The old follower heuristic treated the active entry's top being near the
scrollport top as bottom-follow intent. Entry-root or constant-`scrollTop`
measurements could therefore pass while a sentence inside replaced markup moved.

FIX: PR #9425 separates mutually exclusive intent modes and implements bounded
semantic-anchor restoration in `mvp_site/frontend_v1/app.js`. Following is
earned from the real live-bottom band or explicit rejoin; trusted reader input
cancels it. Reading mode captures a visible narrative sentence with
`Range.getBoundingClientRect()`, re-resolves it across completion replacement,
and applies the measured delta in a bounded rAF transaction. Regression coverage
lives in `testing_ui/streaming/test_streaming_scroll_anchor_regression.py`.

# Mandatory evidence rule

A streaming-scroll PASS is valid only when one evidence ledger matches all of:

- exact target SHA and served `app.js` hash;
- active-entry versus history-entry anchor;
- trusted reader action and following/reading precondition;
- real streaming path;
- completion payload and layout transition;
- a fixture-owned unique sentence oracle, independent of production matching;
- every-rAF sentence viewport-Y samples through completion and settling.

Any mismatch is PARTIAL/UNPROVEN. Do not substitute entry-root Y, final-only
position, scroll percentage, global `scrollHeight` compensation, or a copied
production matcher for sentence-level proof.

# Harness failures that exposed the rule

1. The initial synthetic case answered the older-history question, not the tall
   active-entry/four-choice completion question.
2. A root-level oracle false-greened while the selected sentence moved about
   243 px during `innerHTML` replacement. The corrected test freezes a unique
   literal sentence and resolves its `Range` independently.
3. The first real-Gemini Python port omitted the trusted upward wheel gesture.
   The app correctly remained in following mode, producing 1395.453125 px drift;
   this was a harness error, not a product RED. Perform trusted input before
   precise positioning and assert the reading-mode precondition.
4. Polling a replaceable `.streaming-text` locator raced completion. Sample at
   page/rAF level, treat node disappearance as the expected transition, and
   atomically re-resolve the semantic sentence in the stable tagged entry.
5. A dev deployment serving `origin/main` was initially conflated with PR head.
   Hash the served asset and fail closed on SHA mismatch.

# Verification and evidence boundaries

- Deterministic Chromium regression evidence exercises shorter, taller,
  repeated-prefix, empty-completion, four-choice/debug, delayed-growth,
  interruption, rejoin, and bottom-follow variants with a <=2 px invariant.
- At exact PR head `b9994c0a4214c335a89f00d817ff0d2f87e8b806`, a real
  `/localserver` + Firebase-authenticated + direct Gemini SDK headless run used
  `gemini-3-flash-preview`, returned HTTP 200, emitted 82 server chunks, exposed
  34 distinct browser DOM growth states, and sampled the sentence for 857 rAFs
  with 0 missing samples and 0 px max/final drift. Debug Info and four choices
  rendered. Artifact: `/tmp/pr9425-headless-real-gemini-result.json`.
- That live run had `rootMotion=0`, so it proves real auth/provider/streaming and
  no yank for that turn; the deterministic geometry-changing cases remain the
  stronger causal proof. Real-provider proof and deterministic geometry proof
  are complementary, not interchangeable.
- The branch later advanced by merging `main`; historical evidence remains
  attributable to its recorded exact SHA and must not be relabeled as proof of a
  newer head without rerunning.

# Reusable pattern

For streamed UIs, preserve what the reader sees, not an edge-derived surrogate.
Freeze a semantic target owned by the fixture, sample it through the actual DOM
replacement, and keep bottom pinning as explicit user intent. Validate the real
provider/auth path separately, and state exactly what each evidence layer does
and does not prove.

# References

- `rev-ppors`, `rev-ppors.1`, `rev-c9wuq`, `rev-ppors.3`
- `/Users/jleechan/roadmap/worldarchitect.ai/ironclad/pr9425-middle-reading-anchor-2h-2026-08-27.md`
- `/Users/jleechan/roadmap/worldarchitect.ai/research/2026-08-27-middle-reading-anchor-preservation.md`
- `/Users/jleechan/roadmap/2026-08-27-middle-reading-anchor-plan-micro.md`

