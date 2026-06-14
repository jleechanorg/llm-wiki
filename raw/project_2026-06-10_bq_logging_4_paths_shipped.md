---
name: bq-logging-4-paths-shipped
description: BQ logging fix for 4 streaming/repair LLM code paths shipped (2026-06-10) — real-BQ Layer 2 evidence + 17/17 pytest
metadata: 
  node_type: memory
  type: project
  originSessionId: 31690841-453a-4800-af1f-49a6605cacdb
---

# BQ logging fix for 4 streaming/repair LLM code paths — SHIPPED (2026-06-10)

## What was fixed

4 production code paths now write LLM request/response payloads to
`worldarchitecture-ai.llm_forensics.llm_payloads` (BigQuery forensic sink):

1. `mvp_site/llm_providers/gemini_provider.py::generate_content_stream_sync`
   → new helper `_bq_log_streaming_interaction` sets `extra.path="gemini_provider.stream"`
2. `mvp_site/llm_parser.py::stream_narrative_simple`
   → new helper `_log_stream_payload` sets `extra.execution_path="llm_parser.stream_narrative_simple"`
3. `mvp_site/world_logic.py::generate_spells_via_llm` spell-repair
   → new helper `_bq_log_spell_repair_interaction` sets
   `extra.execution_path="world_logic.spell_repair"`, `agent="SpellRepairAgent"`
4. `mvp_site/llm_service.py::_log_raw_llm_data`
   → reads `execution_path` from `processing_metadata` (default `"unknown"`)

## Head / PR

- HEAD: `73b20e49dc` on `worktree_bq_loggin`
- PR: [jleechanorg/worldarchitect.ai#7439](https://github.com/jleechanorg/worldarchitect.ai/pull/7439)

## Evidence

- Bundle: `/tmp/worldarchitect.ai/worktree_bq_loggin/bq-logging-fix/2026-06-10/latest/`
- 17/17 checksums OK
- 4 production-driven BQ rows at 2026-06-10 09:30:14-16 with PRODUCTION-SET
  `execution_path`/`path` fields (verify script does NOT set them)
- 17/17 pytest passing
- Production LOC: ~336 (forces Layer 2 requirement)
- Re-dispatch of /er returned **PASS** (after Layer 2 upgrade + bundle
  self-reproducibility fix)

## Verify-script pattern (the key fix)

DO NOT call `bq_logging.log_llm_payload` directly from the verify script
with hand-crafted `execution_path` strings — this is Layer 1 evidence
(mocked boundary) NOT Layer 2 (real BQ callstack).

The correct pattern mocks ONLY the external SDK boundary
(`gemini_provider.get_client` or `gemini_provider.generate_content_stream_sync`)
and lets PRODUCTION streaming code call `log_llm_payload` naturally. The
BQ row then carries the production-set `execution_path`/`path` field,
proving the call-graph wiring is correct end-to-end.

For `llm_service._log_raw_llm_data`, the verify script intentionally
OMITS `execution_path` from `processing_metadata` so production's
default `"unknown"` is used — this proves production code set the field,
not the verify script.

## Auth chain for BQ (CRITICAL — see `bq_cli_runnable_403`)

- `unset GOOGLE_APPLICATION_CREDENTIALS` (firebase-admin SDK has READ but
  not INSERT)
- `export CLOUDSDK_CORE_ACCOUNT="jleechan@gmail.com"` for bq CLI
- App code uses user ADC chain (jleechan@gmail.com cached refresh token)
  with Owner/Admin

## Bead

rev-61wn2 (closed)

## Why this matters

Before this fix, only non-streaming LLM calls were logged to BQ. Streaming
and JSON-mode repair calls (the vast majority of the Gemini bill) had
zero forensic visibility — no token counts, no per-call execution_path,
no cost attribution. This PR closes the visibility gap and unlocks
per-campaign cost dashboards.
