---
name: Gemini 3 ThinkingConfig Low Level and Code Execution Mutual Exclusion
description: ThinkingConfig(thinking_level='low') on gemini-3.6/3.7-flash must be omitted when code_execution is enabled to prevent FAILED_PRECONDITION; AGY CLI uses model aliases via AGY_LOW_THINKING_OPT_IN.
type: feedback
bead: rev-kql7h
---

## Context
During Gemini 3.6/3.7 Flash provider verification and BigQuery telemetry analysis on `worktree_thinking_low`:
1. `gemini-3.6-flash` and `gemini-3.7-flash` are configured for low thinking to optimize turn latency in interactive gameplay and test harness runs.
2. The Google GenAI API endpoint enforces a strict constraint: `ThinkingConfig` cannot be combined with built-in `code_execution` (returns `400 FAILED_PRECONDITION`).
3. Google Antigravity (AGY) CLI provider does not use SDK config objects; it manages thinking levels via model aliases.

## Technical Detail & Rules

### Direct Gemini API SDK (`mvp_site/llm_providers/gemini_provider.py`)
- `_GEMINI_THINKING_LEVEL_BY_MODEL = {"gemini-3.6-flash": "low", "gemini-3.7-flash": "low"}`
- When `allow_code_execution=False` (standard JSON mode, two-phase dice, and story continuation), the provider constructs `types.ThinkingConfig(thinking_level="low")`.
- When `allow_code_execution=True` (code execution active on compatible 3.x models), `thinking_config` is intentionally omitted to avoid `FAILED_PRECONDITION`.
- `_serialize_gemini_config_for_bq(config)` serializes `thinking_config` into `safe_bq_config` and records it in BigQuery `worldarchitecture-ai.llm_forensics.llm_payloads` within `request_json`.

### AGY CLI Provider (`mvp_site/llm_providers/agy_provider.py`)
- Model selection uses `_AGY_LOW_MODEL_ALIASES` when `AGY_LOW_THINKING_OPT_IN=1` or `AGY_MODEL` is set.
- Aliases map `gemini-3.x-flash` → `"Gemini 3.5 Flash (Low)"`, `"Gemini 3.6 Flash (Low)"`, `"Gemini 3.7 Flash (Low)"`.
- Subprocess invocation executes `agy --new-project --model "<Model Label (Low)>" ...` and writes `agy_request` / `agy_response` rows to BigQuery.

### Provider Selection Invariant (`testing_mcp/CLAUDE.md`)
- AGY CLI runtime (`AGY_RUNTIME_HOME=~/.cache/worldai/agy-clean-home-v1`) is mandatory by default for local integration tests and preview runs.
- Direct Gemini SDK requires explicit allowlisted opt-out (`AGY_OPT_OUT_FOR_GEMINI_SDK_ONLY=1`) due to API key lifecycle and quota management.

## Verification
- Unit test suite: `mvp_site/tests/test_gemini_provider_thinking_config.py` (100% green).
- Circuit breaker wiring: `mvp_site/tests/test_gemini_provider_circuit_breaker_wiring.py` (100% green).
- AGY provider suite: `mvp_site/tests/test_agy_provider.py` (100% green).
- Live BigQuery forensics telemetry queried in `worldarchitecture-ai.llm_forensics.llm_payloads`.

## References
- PR #4534 (initial thinking budget + code execution conflict resolution)
- Bead: `rev-kql7h`
- Files: `mvp_site/llm_providers/gemini_provider.py`, `mvp_site/llm_providers/agy_provider.py`, `testing_mcp/CLAUDE.md`, `.claude/skills/gemini-3-api.md`
