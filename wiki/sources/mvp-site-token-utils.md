---
title: "mvp_site token_utils"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/token_utils.py
---

## Summary
Token counting utilities for consistent logging across the application. Uses CHARS_PER_TOKEN = 4 for Gemini token estimation. Provides estimate_tokens(), log_with_tokens(), and format_token_count().

## Key Claims
- CHARS_PER_TOKEN = 4 for Gemini token estimation
- estimate_tokens() counts tokens as chars // 4
- log_with_tokens() logs message with character and token counts
- format_token_count() formats as "1000 characters (~250 tokens)"

## Connections
- [[ContextCompaction]] — token estimation for budget management
