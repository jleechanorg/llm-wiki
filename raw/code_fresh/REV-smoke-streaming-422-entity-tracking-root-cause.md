# REV: Streaming smoke failures traced to entity-tracking shape regression in `llm_service.py`

**Status:** OPEN
**Priority:** CRITICAL
**Component:** LLM service / MCP smoke
**Created:** 2026-02-21
**Owner:** Codex / User-requested root-cause

## Goal

Capture and verify the actual root cause of `test_smoke.py` 422 failures before changing PR scope, and preserve the evidence so the follow-up fix can be executed deterministically.

## Modification

Added a focused investigation bead:
- Root-cause signal: `AttributeError: 'list' object has no attribute 'get'` in `mvp_site/llm_service.py`.
- Error path: `_tier_entities` assumes each entity record is a mapping and calls `.get(...)`; in failing campaigns at least one record is a list.
- Symptom in smoke output: repeated LLM failures (`An unexpected error occurred while streaming the response`) and `client_error` SSE path for character / think / god streaming scenarios.

## Necessity

The smoke suite currently fails before streaming chunk contracts can be validated:
- `test_smoke.py` scenario 7 all three streaming mode checks fail due to malformed/failed done payloads.
- Character action paths also fail, making it impossible to validate any schema/timing changes until request preparation is stabilized.
- Multiple other tests were cleanly patched to hard-ban mock mode in MCP scripts; current failures are now clearly production/runtime, not mock-mode configuration.

## Integration Proof

Captured evidence (this run):
- Evidence bundle: `/tmp/worldarchitectai/fix_narrative-mode-contrast-instruction-remake-full/smoke/iteration_014`
- Failure logs: `/var/folders/j0/byd1z6px50v88lf679bgt0h00000gn/T/worldarchitect.ai/fix_narrative-mode-contrast-instruction-remake-full/app.log`
- Traceback signature:
  - `Entity manifest creation failed (validation error), continuing without entity tracking: 'list' object has no attribute 'get'`
  - `File ".../mvp_site/llm_service.py", line 476, in _tier_entities, npc_location = data.get(...)`
  - `AttributeError: 'list' object has no attribute 'get'`
  - `Error in continue_story_streaming` (streaming path)

## Next Actions (Root-Cause Work Plan)

1. Inspect entity-tracking payload shape in campaign state before `_build_trimmed_entity_tracking` and `entity_tracking` ingestion.
2. Normalize/defensive-guard malformed entity records (or skip invalid types) in `_tier_entities` before `.get` access.
3. Re-run `testing_mcp/test_smoke.py` (real local server + real LLM) and confirm:
   - character/think/god streaming scenarios return valid `done_payload`.
   - chunk contracts validate with timed chunking.
4. Only then proceed with narrative schema streaming hardening work.

## Evidence Snapshot

- Failed streaming scenarios:
  - `character_streaming_contract`
  - `think_streaming_contract`
  - `god_streaming_contract`
- Common error mode:
  - `done payload missing/malformed`
  - `client_error` SSE event in event stream
