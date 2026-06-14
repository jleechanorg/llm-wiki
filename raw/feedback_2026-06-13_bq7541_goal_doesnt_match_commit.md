---
name: bq7541-goal-doesnt-match-commit
description: PR
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ec54200f-da82-42c3-8104-06eeb29fb89f
---

The PR #7541 / explore-phase goal statement claims a "dual-provider" deliverable
(Gemini non-streaming envelope fix + OpenAI proxy BQ instrumentation with 9
paths instrumented, 9 tests in `test_bq_openai_proxy_logging.py`). The actual
commit `136b685905` contains **only** the Gemini non-streaming envelope fix
(2 files, 10 tests, bead `rev-7e1gu`):

- `mvp_site/llm_service.py` — `_log_raw_llm_data` wraps game-data dict in
  `{model, provider, system_instruction[:2000], contents}` envelope
- `mvp_site/tests/test_bq_nonstreaming_request_envelope.py` — 10 new tests

Verified absences in the workdir at HEAD `136b685905`:

- `mvp_site/tests/test_bq_openai_proxy_logging.py` does NOT exist (0 hits)
- `mvp_site/llm_providers/openai_proxy_provider.py` does NOT import `bq_logging`
  and has 0 BQ call sites in its 11 error/branch points
- The function `_bq_log_openai_proxy()` referenced in the goal does NOT exist
- PR body itself states "OpenAI provider: NOT instrumented (separate bead
  rev-7i7tc)" — the goal's "instrumentation" claim is the goal's own
  fabrication, contradicted by the PR's own description and by `metadata.json`

The existing OpenAI-proxy BQ coverage (2 call sites in `main.py:1981, 2098` via
`bq_log_openai_compatible_interaction`) is from PR #7439, NOT this commit.

**Why:** Goal/title text and actual commit content diverged — the operator
that wrote the required-checks list conflated the broader BQ-logging train
with this specific 1-bead fix. Verifying the test file name + count + path
claims against `git diff` and `grep` is mandatory before any "PASS" verdict.

**How to apply:** When a GATE_ER_REVIEW goal lists a test file that does not
appear in `git diff <prev-sha>..<pr-sha> --stat`, do not credit the work as
"passing". Re-run `git show <head-sha> --stat` first; cross-check claimed
test count against `unit_test_output.txt` line count; cross-check claimed
function/file existence with `grep -rn` before writing any verdict.
Especially load-bearing when the goal says "X tests PASS for file Y that
does not exist" — that combination cannot be true.
