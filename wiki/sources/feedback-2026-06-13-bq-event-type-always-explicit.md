---
title: "BQ log_llm_payload() must always pass explicit event_type= (no default \"llm_payload\")"
type: source
tags: [bigquery, bq-logging, llm-forensics, log-llm-payload, code-review, event-type]
date: 2026-06-13
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-13_bq_event_type_always_explicit.md
---

## Summary
Every call to `bq_logging.log_llm_payload()` must pass an explicit `event_type=` argument that names the execution path (e.g., `"stream_narrative_simple"`, `"gameplay_streaming"`). The default `event_type="llm_payload"` is generic and makes forensic BQ rows unqueryable by path — `WHERE event_type = "stream_narrative_simple"` returns zero rows even when the path ran. Discovered post-merge of #7439/#7372 during `llm_forensics.llm_payloads` audit.

## Key Claims
- `log_llm_payload()` defaults to `event_type="llm_payload"`; any call site that omits the argument produces unqueryable forensic rows.
- Code review should fail any `log_llm_payload()` call without an explicit `event_type=`.
- Naming convention: underscore-separated lowercase descriptors matching the function name or execution path (e.g., `stream_narrative_simple`, `stream_story_with_game_state`, `gameplay_streaming`).

## Key Quotes
> "Always pass an explicit `event_type=` argument to every `bq_logging.log_llm_payload()` call site."

> "When event_type is omitted, all forensic BQ rows for that path become unqueryable — `WHERE event_type = 'stream_narrative_simple'` returns zero rows even though the path ran."

## Connections
- [[BQForensicLogging]] — the broader forensic logging pattern that requires explicit event types
- [[GeminiProviderStreaming]] — the gemini_provider.py streaming BQ path that motivated the audit
- [[PR7439]] and [[PR7372]] — the post-merge PRs where the issue was discovered
- [[EvidenceStandards]] — explicit event_type is a forensic-evidence prerequisite
