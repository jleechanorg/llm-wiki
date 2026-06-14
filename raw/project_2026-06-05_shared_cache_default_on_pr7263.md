---
name: shared-system-tools-gemini-cache-shipped-default-on-test-traffic-exclusion-pr
description: Option-2 shared cache default-ON gated to real play; proof split (gate-independent A/B engagement + testing_mcp correct-skip); pushed baeedefb68
metadata: 
  node_type: memory
  type: project
  originSessionId: 855fb6ab-0543-406d-b8ac-2520432d826a
---

PR [#7263](https://github.com/jleechanorg/worldarchitect.ai/pull/7263) (branch
`feat/shared-system-tools-cache-impl`) ships the **Option-2 shared system/tools Gemini cache
default-ON** (`SHARED_SYSTEM_TOOLS_CACHE_ENABLED = True` at `mvp_site/gemini_shared_cache.py:60`,
module constant, NO env var). Directive: "no make it default on and test it"; chosen scope
"On + skip test traffic — cache engages only for real multi-turn play."

**Routing helper** `llm_service._should_use_shared_cache(user_id)` (llm_service.py:599) =
`SHARED_SYSTEM_TOOLS_CACHE_ENABLED and not _is_test_cache_disabled_context() and not
_is_test_user(user_id)` — mirrors `_should_use_explicit_cache` and the merged cache-off-on-
test-traffic precedent `eb1970962e`. Wraps all THREE engagement points (non-streaming
`_call_llm_api` ~3031, deferral driver `_prepare_story_continuation` ~6157, streaming gate
~8042). **Import-by-value gotcha:** llm_service does `from gemini_shared_cache import
SHARED_SYSTEM_TOOLS_CACHE_ENABLED` (separate binding) — patch `llm_service.SHARED_...`, never
the source module.

**Why default-ON needs the skip:** shared-cache prefix fragments per campaign (character
identity rides the cached prefix) so one-shot test/CI fixtures (~89% of historical Gemini
volume) get ~0 cross-turn reuse → caching them only accrues storage cost. Excluding test
traffic keeps default-ON net-positive; the win is cross-TURN reuse within real multi-turn play.

**Proof split (forced by skip policy):** testing_mcp runs `MCP_TEST_MODE=real` → the gate
SKIPS by design, and the real-server subprocess can't be patched in-process. So:
- ENGAGEMENT money-proof = `scripts/shared_cache_ab.py` (direct real Gemini SDK, gate-
  independent): 74.6% input-token reduction, single `cachedContents/...` reused both calls,
  cached_tokens 30829 (99.5%/99.4%), git_head stamped 508760da.
- CORRECT-SKIP proofs = testing_mcp real-mode: streaming (campaign hn2u8EPsh387r9EB6fwX,
  used=0/hit=0/2 turns) + cross-campaign (3 campaigns/users, total_create=0/total_hit=0).
- Deterministic gating = `TestShouldUseSharedCacheMatrix` (5 tests) + e2e wiring (registry HIT
  turn 2). Evidence bundle: `scripts/evidence_shared_cache_impl/EVIDENCE_default_on.md`.

**Gotcha:** `vpython` is a shell function — fails under `nohup`/background as "No such file or
directory". Use the venv python directly: `/Users/jleechan/projects/worldarchitect.ai/venv/bin/python`.

State at handoff: pushed `1eb8220eba`→`baeedefb68` (evidence commit on top of code commit
508760da); PR MERGEABLE, headRefOid baeedefb68, reviewDecision EMPTY (fresh CodeRabbit pending),
0 CI failures. Merge human-gated. Beads rev-n6nbs (spike) / rev-biu3j / rev-95rja. Epic
[[project_2026-05-31_gemini_cost_phase_roadmap]] rev-9piwk.
