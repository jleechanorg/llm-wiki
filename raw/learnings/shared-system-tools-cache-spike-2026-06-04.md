# Shared system/tools-only Gemini cache — SPIKE resolved, verdict GO (2026-06-04)

**Epic:** rev-9piwk (Gemini cost). **Parent spike:** rev-n6nbs / task #20. **New child impl bead:** rev-n6nbs.1.
**Spike PR:** https://github.com/jleechanorg/worldarchitect.ai/pull/7259 — branch `spike/shared-system-tools-cache`, HEAD `69311f04b4`, base main. **OPEN, NOT merged (human merge gate).**

## Finding (canonical from spec/feature.md; BigQuery is reconciliation-only, NOT display-name attribution)

- **D1 (real paid Gemini):** a campaign-free system+tools-only explicit cache discounts **99.8% of the static floor on read** (`cached_content_token_count=8580` of `prompt_token_count=8594`). **C3 proven:** referencing a cache while ALSO setting `system_instruction`/`tools` → **HTTP 400** (system must move fully into the cache). **C1:** `cached_content` is a single `Optional[str]` — one cache per request (the two-cache "shared system + per-campaign story-delta" design is NOT constructible).
- **A2 (synthetic safety proof, no API key):** two distinct contexts (camp-alpha/user-1/Itachi vs camp-beta/user-2/Gandalf) build a **BYTE-IDENTICAL** payload, **`sha256=bde3c4955afef0cc536dc306113d01c916b6fa21b1cde5526de92828c9c33d88`**, 1 distinct digest, 45577 bytes scanned, **zero per-context leakage**. This byte-identity is the impl regression invariant.
- **A4:** shared-cache key = **(model, system_prompt_sha256, tool_signature_sha256)**; `response_schema` NOT a key dimension this spike.
- **D2 cost model:** floor-dominated test/CI traffic (89% of spend) — **Option 2 (shared explicit system/tools cache) = −74%/call** ($5.36e-3 vs $2.05e-2 baseline); **Option 1 (implicit + contiguous-floor reorder) = −61% fallback**. Storage collapses **O(campaigns)=$1,440/day → O(~6 caches)=$8.64/day**. Long-campaign regime independently re-validates the #7215 cache-off decision (rev-vm10b, merged `a6d2e4e570`).
- **D3 verdict: GO** — to the follow-up IMPLEMENTATION bead **rev-n6nbs.1**, NOT to merge the spike. Option 2 primary, Option 1 fallback.
- **Constraint C8:** the spike did NOT make the brownfield reorder of `finalize_instructions()` / the `llm_service` request-building path.

## Deferred to impl bead rev-n6nbs.1 (both gate defaulting Option 2 ON)

- **A3a:** settled-window BigQuery spend via dev-runner SA.
- **A3c:** real-path A/B of Options 0/1/2.

## Impl scope (rev-n6nbs.1)

(a) Route system_instruction+tools through a shared explicit cache keyed by (model, system-hash, tool-sig); drop them from per-request config per C3.
(b) Cache lifecycle (create-on-miss, refresh-before-expiry) restricted to GLOBAL system+tools bytes only.
(c) Hard leakage boundary — NEVER user_id/campaign/world/character/story/memory in the cache (preserve A2 byte-identity).
(d) Run A3c + A3a before defaulting Option 2 on.
(e) Keep Option 1 (implicit + reorder) as fallback.

**Files:** `mvp_site/agent_prompts.py` (`finalize_instructions` ~2632-2679), `mvp_site/gemini_cache_manager.py` (contents :178-221, `should_rebuild` :93-141, key :196-197), `mvp_site/gemini_provider.py` (`config.cached_content` :829/:1137).

## Lineage

Downstream of the prefix-stability audit (rev-n6nbs, same 2026-06-04 block) which proved system_instruction has a large truly-static shareable prefix with zero injected IDs/timestamps. Nextsteps: `~/roadmap/nextsteps-2026-06-04-system-instruction-prefix-stability.md` (cont section). Learnings: `~/roadmap/learnings-2026-06.md` (2026-06-04 shared-cache spike entry).
