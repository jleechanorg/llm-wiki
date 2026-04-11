---
title: "PR #5969: fix(rate_limiting): elevate BYOK rate limits to 5000 daily / 1000 per 5h with refactored architecture"
type: source
tags: []
date: 2026-03-14
source_file: raw/prs-worldarchitect-ai/pr-5969.md
sources: []
last_updated: 2026-03-14
---

## Summary
- BYOK users were blocked by the 5-hour window (25 turns) despite supplying their own API key — only the daily limit was elevated
- Root cause: `check_rate_limit()` used the global `RATE_LIMIT_5HOUR_TURNS` for all users, ignoring BYOK status
- Fix: add per-user window limit resolution via `_get_user_turn_limits()` and elevate BYOK limits to 5000 daily / 1000 per 5-hour window
- Major refactor: extracted `_evaluate_rate_limit()` and `_build_allowed_response()` to eliminate 80-line duplication bet

## Metadata
- **PR**: #5969
- **Merged**: 2026-03-14
- **Author**: jleechan2015
- **Stats**: +620/-211 in 3 files
- **Labels**: none

## Connections
