---
name: stale-bead-premises-and-layered-dispatch-undo
description: "4 of 5 queue items dissolved under premise-verification (already-fixed/superseded/duplicate); the one real fix needed 3 adversarial rounds because a lower-layer semantics fix was silently undone by a higher layer's defensive dispatch"
metadata: 
  node_type: memory
  type: feedback
  bead: wc-qfny
  originSessionId: eba5e70b-df38-408a-869e-9f37a1a2bb58
  modified: 2026-08-06T06:28:04.808Z
---

Session 2026-08-06 (worldai_claw, PR #408 → merged c838b9ab). Two reusable patterns:

**1. Verify bead premises before implementing — stale beads dissolve under archaeology.**
Of 5 "next work" items from the ready queue, 4 required zero new code once verified against current code+spec:
- `jleechan-twk` (P0!): its ask (level-up modal+lock) was investigated and REVERSED the day after filing (wc-rbbr: real website has no such modal); building it would have been a parity regression. Code comments (events.ts:224-230) even forbid it.
- `jleechan-0ob`: fix already squash-merged in PR #336, invisible because the squash message named only 3 of 5 sub-commits.
- `jleechan-243`: duplicate of wc-gddj/wc-ikt9 (RCTPackagerConnection port), fixed in #352/#353.
- `wc-mnbs`: backend contract problem (mvp_site prompt/schema), zero client work.
**Rule:** for beads older than ~2 weeks, spend one verification lane (code grep + closed-bead cross-ref + spec read) before any implementation lane. Squash merges hide sub-commits — verify content byte-wise (attempt the cherry-pick), not by commit-message search.

**2. Layered defensive dispatches silently undo lower-layer semantics fixes.**
PR #408 round 2 fixed `bail()` in mvpSiteClient.ts to NOT mark `disconnected` for in-band `stream_error` — but GameScreen's `onError` had its own "defensive" unconditional `SET_CONNECTION_STATUS('disconnected')` dispatch (added by PR #250) that undid the fix end-to-end. Tests passed because they asserted at the client layer, not the screen layer. Only a cross-model executing reviewer (cursor-agent) caught it.
**Rule:** when changing dispatch semantics at layer N, grep every higher layer for redundant/defensive dispatches of the same action and assert the end-to-end state in the behavioral test, not the layer-N unit test.

**Supporting facts:**
- Adversarial pipeline for #408: 3 rounds, 7 real findings (retry-dup player bubble, watchdog race swallowing the real provider error, in-flight retry guard, grep-only wiring test, disconnected semantics ×2 layers, dead retry control), each fixed with revert-RED/restore-GREEN proof.
- Cross-model fallback chain reality 2026-08-06: codex quota-dead until Aug 7, agy quota-dead (~3h), gemini CLI needs GEMINI_API_KEY (absent) — cursor-agent was the only working non-Claude executor. `agy` flag order matters: `--dangerously-skip-permissions -p "prompt"` (flags BEFORE prompt; reversed order feeds the flag into the prompt).
- `npx tsc` in a workspace can resolve a globally-installed newer TypeScript → phantom TS5108/TS5102 "option removed" config errors; always run `./node_modules/.bin/tsc` (pinned 5.3.3 here) before believing a typecheck failure.
- Unfixed user-config bug flagged, not fixed (bashrc model names are user-owned config): `~/.bashrc` exports `WORLDAI_DEFAULT_GEMINI_MODEL=gemini-3.6-flash-high` which 404s (found by evidence lane; not verified against live model registry).
- Backend persistence order (settles client-side delete safety): mvp_site/llm_parser.py:2049-2054 — user entry persists only AFTER the LLM stream completes; on in-band error nothing persists, so client-side removal of the failed turn's player bubble matches server state.

Related: [[isolated-worktree-beads-dont-sync-back]], [[feedback_2026-07-28_verify_catalog_shape_not_test_passing]], PR https://github.com/jleechanorg/worldai_claw/pull/408, evidence gist 3818147bb04b8540c6229ef9870b082f, beads wc-zwju (runner-fleet saturation misdiagnosed as dead — repo-scope runners API is the wrong probe for ORG-level runners; use `ezgha status` / `gh api orgs/<org>/actions/runners`), wc-mspv (20s establishment timeout vs 40s+ real LLM first-token latency), rev-wo0v8 (worldarchitect.ai: persisted:bool on done payload).
