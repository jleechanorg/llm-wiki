---
name: pr7372-bq-nonstreaming-call-sites-open
description: PR #7372 BQ logging non-streaming call sites — MERGED 2026-06-13; 5 remaining gaps documented
metadata: 
  node_type: memory
  type: project
  bead: none
  originSessionId: 7fb93c82-6491-4f2c-9a75-6a996471316c
---

## PR #7372 BQ Logging — Non-Streaming Call Sites

PR [#7372](https://github.com/jleechanorg/worldarchitect.ai/pull/7372) `fix/bq-logging-wire-call-sites` — **MERGED 2026-06-13T00:25:31Z** by `jleechan2015`.

### What It Added (vs #7439)

8 new `log_llm_payload()` call sites in `_call_llm_api` (`llm_service.py`):
- Normal Gemini success, OpenRouter/Cerebras/OpenClaw success
- Timeout, error, and retry paths
- JSON mode generation calls

Also:
- `bq_logging.py`: RFC-1918 172.16–31 subnet detection fix
- `llm_parser.py`: BQ log moved before Firestore persist (prevents skip on persist error); `_bq_turn_index_from_state` returns `int | None`, handles string coercion
- `world_logic.py`: spell repair log moved after `json.loads` (prevents duplicate success+error rows); `_bq_turn_index_from_final_state` added
- Stream narrative telemetry: `done_event_ready` flag + `GeneratorExit` handling; `_bq_streaming_cache` / `_bq_cache_replay` fields

### Merge path (final HEAD `5c4fd58e60ca`)

Hermes pushed 4 commits on top of `6161204dda` addressing CR issues:
- Moved inline test imports to module level
- Replaced source-text assertions with behavioral tests
- Fixed `test_main_boot_registers_bq_sink` to use `importlib.reload`
- Added `test_llm_parser_turn_index_skips_malformed_fallbacks`
- Added stream telemetry fields

Green Gate PASS at `2026-06-13T00:23:17Z` (run `27450068825`).
Skeptic VERDICT PASS at `2026-06-13T00:17:46Z` (run `27450558149`).

### Still Missing After Both PRs (#7439 + #7372)
1. **OpenAI provider** (`openai_provider.py`) — Gap 1, never instrumented
2. **OpenAI streaming proxy** (`main.py` ~line 2116) — always writes `response_text=""`
3. **Spell repair token counts** for OpenRouter/Cerebras — `_bq_log_spell_repair_interaction` reads Gemini-style `usage_metadata` only
4. **Duplicate rows** — structural double-logging (provider + parser) — only TODO comments
5. **Cache hit false-positive** — `_log_raw_llm_data` fires on `ServerCacheManager` replay with `final_api_response=None`

### References
- [PR #7372](https://github.com/jleechanorg/worldarchitect.ai/pull/7372)
- [PR #7439](https://github.com/jleechanorg/worldarchitect.ai/pull/7439) — MERGED 2026-06-12
