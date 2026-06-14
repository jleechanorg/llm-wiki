---
title: "BQ truly raw logging still vulnerable to 1 MB streaming-insert row limit"
type: source
tags: [bq-logging, streaming-insert, pr-7549, follow-up, pr-followup, data-loss, fail-soft]
date: 2026-06-13
source_file: ../../raw/feedback_2026-06-13_bq_truly_raw_still_vulnerable_to_1mb_row.md
---

## Summary

PR #7549 (`bb4ce31d46`) replaced the old 2K/20K character caps with a "truly raw" log path that strips multimodal base64 to a size marker. The smoke test on 2026-06-13 proved the path is real (largest disk-mirror row = 465,581 bytes = 44% of 1 MB). But BQ streaming-insert has a hard 1 MB per-row limit; when exceeded, `_insert_rows` 413s and `bq_logging` fail-softs to local disk — the row never reaches BQ. This is silent data loss from forensic analysis. Realistic worst case: heavy combat state (6 chars + 50-turn history + rules + monster refs + file_data URIs) lands at 1.0–1.2 MB.

## Key Claims

- `_strip_multimodal_for_bq` only handles inline base64. Pure text payload (a 2 MB lore paste) or text + non-base64 URIs (file_data) bypasses the helper and can exceed 1 MB.
- BQ streaming-insert's 1 MB per-row hard limit is the structural ceiling. Failure mode = 413 → fail-soft → disk mirror → not in BQ.
- Fix pattern: pre-check row size in `log_llm_payload` and either drop the `request_json` column (keep response_text + token counts) OR truncate with a `[truncated: 1.2 MB → 800 KB at char 982134]` marker. Both must log the decision.
- Anti-pattern: adding a hard byte cap on `request_json` (regression against PR #7549 contract).
- Regression test pattern: mock `_insert_rows` to raise 413, assert row that reaches BQ is < 1 MB + warning was logged.

## Key Quotes

> "Realistic worst case (rough estimate): Light ~210 KB OK; Medium ~360 KB OK; Heavy combat ~620 KB OK but close; + file_data URIs 1.0–1.2 MB → DROP, fail-soft to disk."

> "The 'truly raw' PR title is honest about multimodal safety (the new helper) but **silent about the 1 MB per-row limit**."

## Connections

- [[PR-7549 Smoke Evidence Real Campaign]] — provides the 465 KB smoke row evidence that proves we're 44% of the way to the 1 MB cliff
- [[BQ-Logging-6PR-Complete-Gaps-Remain]] — the 6-PR closeout that #7549 closes the last gap for, but this 1 MB limit is a NEW gap that was structurally invisible until #7549 removed the character cap
- [[Feedback Deploy Gated Evidence Gap]] — the 1 MB gap is structural until a real call hits it; organic evidence requires prod traffic
- [[BqLoggingForensicMissing]] — related forensic BQ logging concerns
- [[PR-7549]] — the PR that creates this exposure by removing the old 20K cap

## Bead

`rev-szamx` (closed, learning record) — `BQ 1MB streaming-insert row-too-large guard (PR #7549 follow-up)`
