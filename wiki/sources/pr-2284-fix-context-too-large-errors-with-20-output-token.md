---
title: "PR #2284: Fix context-too-large errors with 20% output token reserve"
type: source
tags: []
date: 2025-12-02
source_file: raw/prs-worldarchitect-ai/pr-2284.md
sources: []
last_updated: 2025-12-02
---

## Summary
- Add `OUTPUT_TOKEN_RESERVE_RATIO` (20%) to ensure sufficient output space for quality responses
- Fail fast when input exceeds 80% of context instead of sending doomed requests with `max_output_tokens=1`
- Cerebras provider now detects `finish_reason='length'` with no content and raises clear error
- Clear error messages showing token usage and limits

## Metadata
- **PR**: #2284
- **Merged**: 2025-12-02
- **Author**: jleechan2015
- **Stats**: +182/-34 in 6 files
- **Labels**: none

## Connections
