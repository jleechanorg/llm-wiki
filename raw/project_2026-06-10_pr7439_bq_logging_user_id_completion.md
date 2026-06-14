---
name: pr-7439-bq-logging-user-id-completion
description: PR
metadata: 
  node_type: memory
  type: project
  originSessionId: 31690841-453a-4800-af1f-49a6605cacdb
---

PR #7439 BQ-logging 4-path user_id closure shipped (2026-06-10).

## Final state
- HEAD `602c4eaa03` on `worktree_bq_loggin` branch; 4 unpushed commits since merge
- 58/58 unit tests pass (test_bq_logging, test_gemini_provider_bq_logging, test_llm_service_error_handling, test_llm_response)
- 4/4 testing_mcp scenarios defined in `test_bq_logging_real_llm_real_user_e2e.py` (Scenarios 1-4)

## Gap closure commits
- `782bb2df57` Gap B/C/D: thread user_id into llm_service._log_raw_llm_data (4 callers), llm_parser._log_stream_payload, world_logic._bq_log_spell_repair_interaction
- `0eaae84765` gemini_provider fix: restore `request_json` (full payload from model_name+contents+system_instruction) and `extra["path"]` (`gemini_provider.stream` / `gemini_provider.stream_fallback`) in inlined BQ calls + move `finish_reason` to top-level kwarg; also fix `test_log_raw_llm_data_survives_request_serialization_failures` to set `CAPTURE_RAW_LLM=true`
- `602c4eaa03` Gap A: gemini_provider streaming BQ log calls (2 inlined + `_bq_log_streaming_interaction` helper) read `user_id` from `logging_util.get_user_id()` ContextVar + derive `is_test` via `logging_util.is_test_user()` — works because main.py:3609 already pushes user_id before calling the generator

## Pattern (apply to future user_id propagation)
1. Add `user_id: str | None = None` kwarg to the function
2. Resolve with `resolved_user_id = user_id if user_id is not None else logging_util.get_user_id()` at the top
3. Pass both `user_id=resolved_user_id, is_test=logging_util.is_test_user(resolved_user_id)` to `bq_logging.log_llm_payload(...)
4. Callers that already have user_id in scope should pass explicitly; the ContextVar fallback is a safety net
5. Tests that mock `mvp_site.<module>.logging_util` need `mock.get_user_id.return_value = None; mock.is_test_user.return_value = True`

## Key decisions vs main's PR #7398
- Took main's `_bq_log_streaming_interaction` helper but inlined 2 sites use the same `event_type="gameplay_streaming"` convention
- `request_json=""` for streaming (main's design) but our 0eaae84765 commit restored full payload for inlined calls (better debugging, satisfies test_streaming_generator_emits_bq_row_post_stream)
- `finish_reason` is top-level kwarg (matches helper), not buried in `extra`

## Pre-existing failures now resolved
The 3 cache-fallback tests were failing on the merge commit 3715835844 because `mock_prep` was a MagicMock with no `.user_id` attribute. Setting `mock_prep.user_id = "test-user"` in `_make_mock_prep()` fixed all 3 (str(prepared.user_id) now returns a real string instead of MagicMock repr, no JSON serialization error).

## Gap 1 (openai_chat_completions in main.py:1853/1920) + Gap 2 (openrouter/cerebras/openclaw) NOT closed — out of 2h budget scope
