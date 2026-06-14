---
name: BQ follow-up must pass tests and avoid duplicate rows
description: Local BQ follow-up changes currently fail a targeted test and may add duplicate rows.
type: feedback
bead: rev-c3v9t
---

Targeted verification of the post-merge local BQ diff failed: `./vpython -m pytest mvp_site/tests/test_bq_logging.py mvp_site/tests/test_bq_logging_integration.py -q` returned `1 failed, 16 passed` because `test_bq_logging_integration.py` expected `agent == "stream_narrative_simple"` while the captured row had `agent=None`. The local `llm_service.py` diff also adds a generic post-provider BQ row that can duplicate provider-owned OpenAI-compatible rows while omitting `user_id` and `event_type`.

**Why:** Follow-up observability work can easily look like progress while making forensic rows noisier or tests less truthful.

**How to apply:** Before opening a BQ follow-up PR, fix the failing test against the real logging contract and prove row ownership stays single-source for each interaction path.
