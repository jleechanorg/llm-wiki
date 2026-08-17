---
title: "Stale bead premises + layered dispatch undo — worldai_claw PR #408 session learnings"
type: source
tags: [engineering-process, code-review, beads, react-native, sse, adversarial-review]
date: 2026-08-06
source_file: raw/feedback_2026-08-06_stale_bead_premises_and_layered_dispatch_undo.md
---

## Summary
Session capture from the worldai_claw stream-error pipeline (PR #408, merged `c838b9ab`). Two durable engineering patterns: (1) verify a bead's premise against current code and spec before implementing — four of five queue items dissolved under archaeology (already-fixed in unnamed squash sub-commits, superseded the day after filing, duplicate, or backend-scope); (2) a semantics fix at a lower layer can be silently undone by a higher layer's "defensive" duplicate dispatch of the same action, and only end-to-end assertions or an executing cross-model reviewer will catch it.

## Key Claims
- 4 of 5 "ready" work items required zero new code once verified: a P0 whose ask had been source-refuted the day after filing (building it would have been a parity regression), a bug already merged inside a squash commit that named only 3 of its 5 sub-commits, a duplicate of an already-fixed packager-port bug, and a client-blamed defect that was actually a backend prompt-contract gap.
- Squash merges hide content: verify by attempting the cherry-pick (byte-wise), never by commit-message search.
- GameScreen's unconditional defensive `SET_CONNECTION_STATUS('disconnected')` dispatch undid mvpSiteClient `bail()`'s `stream_error` semantics fix end-to-end while all layer-level unit tests stayed green.
- Adversarial multi-round review (Opus + cursor-agent executing code + prior-art research) surfaced 7 real defects a same-model pass had certified; each was fixed with revert-RED/restore-GREEN proof.
- `npx tsc` inside a workspace can resolve a globally-installed newer TypeScript and emit phantom "option removed" config errors — trust only the package-pinned `./node_modules/.bin/tsc`.
- mvp_site persists the user's story entry only after the LLM stream completes (llm_parser.py:2049-2054), so client-side removal of a failed turn's player bubble matches server state.

## Key Quotes
> "for beads older than ~2 weeks, spend one verification lane (code grep + closed-bead cross-ref + spec read) before any implementation lane" — the archaeology rule

> "when changing dispatch semantics at layer N, grep every higher layer for redundant/defensive dispatches of the same action and assert the end-to-end state" — the layered-dispatch rule

## Connections
- [[worldai-claw]] — the RNW/Expo thin client where the pipeline ran
- [[BeadsIssueTracking]] — the stale-premise verification rule extends bead lifecycle discipline
- [[AdversarialReview]] — 3-round cross-model refutation loop as the mechanism that caught the layered-dispatch undo
- [[EvidenceStandards]] — real-backend RED/GREEN capture (gist 3818147bb04b8540c6229ef9870b082f) as the merge basis when CI runners are starved
