---
name: feedback-2026-06-13-bq-truly-raw-still-vulnerable-to-1mb-row
description: PR
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 33b6218a-1fc0-42b9-b4f8-1814474904eb
---

## Context

PR #7549 (`bb4ce31d46`) replaced the old 2K/20K character caps with a "truly raw" log path. The smoke test on 2026-06-13 proved the path is real: largest row in the disk mirror was **465,581 bytes (44% of 1 MB)**. Real campaign `69ihH873nJjbiq5Akj4U` produced rows of 332,962 / 430,617 / 465,581 bytes of `request_json`.

But BQ streaming-insert has a hard **1 MB per-row limit**. When a row exceeds that, `_insert_rows()` returns 413 and `bq_logging` fail-softs the row to the local disk mirror. **The row is not in BQ** — it's silently lost from forensic analysis. This is exactly the failure mode the 6-PR closeout + PR #7549 were supposed to prevent.

## Realistic worst case (rough estimate)

| Game state shape | `request_json` size | Risk |
|---|---|---|
| Light (1 char, short history) | ~210 KB | OK |
| Medium (6 chars, 50 turns) | ~360 KB | OK |
| Heavy combat (6 chars, 50 turns, full rules) | ~620 KB | OK but close |
| + file_data URIs (not stripped by helper) | 1.0–1.2 MB | **DROP, fail-soft to disk** |
| A user pastes a 2 MB lore text | > 1 MB | **DROP** |

## The fix pattern (NOT yet in code)

Two acceptable patterns, both unblocks the row but preserve forensic intent:

1. **Pre-check in `log_llm_payload()`**: `if len(row_json_bytes) > 1 MB: warn + skip request_json, keep response_text + token counts`. Row still goes to BQ. Forensic column is `null` for that call.
2. **`_truncate_text_with_marker`**: replace tail with `[truncated: 1.2 MB → 800 KB at char 982134]`. Row stays in BQ, but the column is no longer "truly raw" — this is a contract change so needs a bead + body update.

`#1` is the safer fix: it keeps the existing "truly raw" contract for the 99% case, and the 1% case gets a `null` request_json with a logged reason. The regression test in `test_bq_truly_raw_gemini.py::test_streaming_row_under_one_megabyte_with_image` already documents the failure mode.

## Why this matters

- The "truly raw" PR title is honest about multimodal safety (the new helper) but **silent about the 1 MB per-row limit**.
- A future contributor could fix the silent drop with a `try/except` swallow that masks the issue, OR could re-introduce a 1 MB cap on `request_json` (which is a regression against the PR #7549 contract).
- The right architectural answer is: detect the size, decide at the call site whether to drop the column or skip the row entirely, and LOG the decision so forensic analysis can tell the difference.

## How to apply

When touching `mvp_site/bq_logging.py` for row-size reasons:
- Do NOT add a hard cap on `request_json` bytes — that's the regression that #7549 fought to prevent.
- DO add a pre-check at the row build site that logs `warning("BQ row too large: {bytes}B; dropping request_json for {event_type}")` and either (a) drops the column, (b) writes a truncated marker.
- Add a regression test like `test_one_megabyte_row_skips_request_json_with_warning` that mocks `_insert_rows` to raise 413, then asserts the row that reaches BQ is `< 1 MB` and the warning was logged.

## Related memories

- [[project-2026-06-13-pr7549-smoke-evidence-real-campaign]] — the 465 KB smoke row evidence
- [[project-2026-06-13-bq-logging-6pr-complete-gaps-remain]] — the 6-PR closeout that #7549 closes
- [[feedback-2026-06-11-deploy-gated-evidence-gap]] — structural vs organic; the 1 MB gap is structural until a real call hits it
