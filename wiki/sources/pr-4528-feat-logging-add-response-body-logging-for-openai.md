---
title: "PR #4528: feat(logging): add response body logging for OpenAI-compatible provider errors"
type: source
tags: []
date: 2026-02-02
source_file: raw/prs-worldarchitect-ai/pr-4528.md
sources: []
last_updated: 2026-02-02
---

## Summary
- Add response body logging when `choices[0]` is missing from OpenAI-compatible API responses
- Helps debug OpenRouter/Cerebras issues where API returns 200 OK with error body
- Truncates response to 500 chars to avoid log spam

## Metadata
- **PR**: #4528
- **Merged**: 2026-02-02
- **Author**: jleechan2015
- **Stats**: +157/-2 in 2 files
- **Labels**: none

## Connections
