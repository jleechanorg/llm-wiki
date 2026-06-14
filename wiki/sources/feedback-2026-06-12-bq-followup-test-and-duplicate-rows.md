---
title: "BQ Follow-up Must Pass Tests and Avoid Duplicate Rows"
type: source
tags: [bq-logging, pr-7439, test-failure, duplicate-rows, worldarchitect-ai, rev-c3v9t]
date: 2026-06-12
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worktree_bq_loggin/memory/feedback_2026-06-12_bq_followup_test_and_duplicate_rows.md
---

## Summary
Post-merge local BQ diff failed targeted verification: `./vpython -m pytest mvp_site/tests/test_bq_logging.py mvp_site/tests/test_bq_logging_integration.py -q` returned `1 failed, 16 passed`. `test_bq_logging_integration.py` expected `agent == "stream_narrative_simple"` but captured row had `agent=None`. The local `llm_service.py` diff also adds a generic post-provider BQ row that can duplicate provider-owned OpenAI-compatible rows while omitting `user_id` and `event_type`.

## Key Claims
- Targeted pytest run: 1 failed, 16 passed.
- Local `llm_service.py` diff adds a generic post-provider BQ row that can duplicate provider-owned OpenAI-compatible rows.
- Generic row omits `user_id` and `event_type`.
- Bead: `rev-c3v9t`.
- Before opening a BQ follow-up PR, fix the failing test against the real logging contract and prove row ownership stays single-source for each interaction path.

## Key Quotes
> "Follow-up observability work can easily look like progress while making forensic rows noisier or tests less truthful."

## Connections
- [[BQForensicLogging]] — 4-path BQ logging design
- [[StreamingPassthrough]] — row ownership single-source
- [[EvidenceStandards]] — Layer 2 E2E proof requirement
- [[PRReviewDiscipline]] — pre-merge test verification
