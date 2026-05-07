---
title: "TokenUtils"
type: entity
tags: [module, token-utilities, python]
sources: ["token-utils-tests", "gemini-token-ratio-real-calibration-2026-05-05"]
last_updated: 2026-05-05
---

Python module providing token counting and logging utilities.

## Functions
- `estimate_tokens(text)` — Estimates token count by dividing character length by 4
- `format_token_count(count)` — Returns formatted string like "N characters (~M tokens)"
- `log_with_tokens(message, text, logger)` — Logs message with token count using specified logger

## Calibration Notes
- `GEMINI_LARGE_STRUCTURED_CHARS_PER_TOKEN` was adjusted to `3.455` in PR #6812 after real calibration showed `3.45` failed a Firestore compacted case at `5.003%`.
- For calibrated estimator constants, validate the full real-service calibration suite before accepting point fixes.

## Source
Tested by [[Token Utils Tests]]
