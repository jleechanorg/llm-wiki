---
title: "2026-06-12 Pr7372 Bq Nonstram Open"
type: source
tags: ["project", "worldarchitect", "pr-7372"]
date: 2026-06-12
source_file: raw/project_2026-06-12_pr7372_bq_nonstram_open.md
---

## Summary
PR #7372 BQ logging non-streaming call sites — MERGED 2026-06-13; 5 remaining gaps documented

## Key Claims
- PR [#7372](https://github.com/jleechanorg/worldarchitect.ai/pull/7372) `fix/bq-logging-wire-call-sites` — **MERGED 2026-06-13T00:25:31Z** by `jleechan2015`.
- 8 new `log_llm_payload()` call sites in `_call_llm_api` (`llm_service.py`):
- - Normal Gemini success, OpenRouter/Cerebras/OpenClaw success
- - Timeout, error, and retry paths
- - `bq_logging.py`: RFC-1918 172.16–31 subnet detection fix
- - `llm_parser.py`: BQ log moved before Firestore persist (prevents skip on persist error); `_bq_turn_index_from_state` returns `int | None`, handles string coercion

## Connections
- [[WorldarchitectAI]] — worldarchitect.ai project memory
- Source: `raw/project_2026-06-12_pr7372_bq_nonstram_open.md`
