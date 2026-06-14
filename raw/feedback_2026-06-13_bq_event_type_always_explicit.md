---
name: bq-event-type-always-explicit
description: "Always pass explicit event_type= to log_llm_payload() — never rely on default \"llm_payload\""
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 7fb93c82-6491-4f2c-9a75-6a996471316c
---

Always pass an explicit `event_type=` argument to every `bq_logging.log_llm_payload()` call site.

**Why:** `log_llm_payload()` defaults to `event_type="llm_payload"` (generic). When event_type is omitted, all forensic BQ rows for that path become unqueryable — `WHERE event_type = "stream_narrative_simple"` returns zero rows even though the path ran. This was discovered post-merge of #7439/#7372 when auditing `llm_forensics.llm_payloads` for row quality.

**How to apply:** Any new call to `log_llm_payload()` must include `event_type="<path-specific-string>"`. Use underscore-separated lowercase descriptors that match the function name or execution path (e.g., `"stream_narrative_simple"`, `"stream_story_with_game_state"`, `"gameplay_streaming"`). Code review should fail any call without an explicit `event_type`.
