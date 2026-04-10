---
title: "TokenUtils"
type: entity
tags: [module, token-utilities, python]
sources: ["token-utils-tests"]
last_updated: 2026-04-08
---

Python module providing token counting and logging utilities.

## Functions
- `estimate_tokens(text)` — Estimates token count by dividing character length by 4
- `format_token_count(count)` — Returns formatted string like "N characters (~M tokens)"
- `log_with_tokens(message, text, logger)` — Logs message with token count using specified logger

## Source
Tested by [[Token Utils Tests]]
