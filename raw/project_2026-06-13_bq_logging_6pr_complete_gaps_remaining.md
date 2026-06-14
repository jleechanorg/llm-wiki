---
name: bq-logging-6pr-complete-gaps-remaining
description: "All 6 BQ forensic logging PRs merged as of 2026-06-13; 5 known gaps remain (OpenAI, streaming proxy, spell repair tokens, duplicates, cache false-positive)"
metadata: 
  node_type: memory
  type: project
  originSessionId: f31deb23-62a1-4ab2-8fbe-46806e1539fb
---

## BQ Forensic Logging — All 6 PRs Merged; 5 Gaps Remain

**Status as of 2026-06-13:** All BQ logging PRs merged. No open BQ logging PRs.

### Merged PRs (in order)
1. [#7372](https://github.com/jleechanorg/worldarchitect.ai/pull/7372) — 8 `log_llm_payload()` call sites in `_call_llm_api` (llm_service.py non-streaming paths)
2. [#7439](https://github.com/jleechanorg/worldarchitect.ai/pull/7439) — 4 streaming paths (`_bq_log_streaming_interaction`, `_log_stream_payload`, `_bq_log_spell_repair_interaction`, extended `_log_raw_llm_data`)
3. [#7488](https://github.com/jleechanorg/worldarchitect.ai/pull/7488) — `agent` field to `stream_narrative_simple`, RFC-1918 endpoint detection
4. [#7504](https://github.com/jleechanorg/worldarchitect.ai/pull/7504) — `_log_stream_payload` event_type fixed to `stream_narrative_simple`
5. [#7506](https://github.com/jleechanorg/worldarchitect.ai/pull/7506) — `stream_story_with_game_state` 3 call sites explicit event_type
6. [#7509](https://github.com/jleechanorg/worldarchitect.ai/pull/7509) — gemini_provider.py `agent`/`finish_reason` fields in streaming BQ rows

### 5 Known Remaining Gaps
1. **OpenAI provider** (`openai_provider.py`) — never instrumented at all
2. **OpenAI streaming proxy** (`main.py` ~line 2116) — always writes `response_text=""`  
3. **Spell repair token counts** for OpenRouter/Cerebras — `_bq_log_spell_repair_interaction` reads Gemini-style `usage_metadata` only
4. **Duplicate rows** — structural double-logging in both provider layer AND parser layer (only TODO comments left)
5. **Cache hit false-positive** — `_log_raw_llm_data` fires on `ServerCacheManager` replay with `final_api_response=None`

### Open BQ-adjacent Beads
- `rev-8py6d` [IN_PROGRESS P1] — Fix daily Gemini cost report BigQuery TIMESTAMP parse crash (epoch-seconds vs ISO)
- `rev-wj9mo` [OPEN P1] — Enable BigQuery billing export (data stops at 2026-05-13; actual query permissions work now)
- `rev-pr6tv` [OPEN P2] — Reduce raw LLM logging overhead (old, Feb 2026 — lower priority)

**Why:** The forensic audit trail for per-user LLM cost and behavior is now comprehensive for Gemini streaming/non-streaming paths. OpenAI path is the largest remaining gap.

**How to apply:** When picking the next BQ task, target gap #1 (OpenAI) or bead `rev-8py6d` (TIMESTAMP crash in cost report).
