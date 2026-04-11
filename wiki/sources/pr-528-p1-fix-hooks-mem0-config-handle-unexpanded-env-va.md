---
title: "PR #528: [P1] fix(hooks/mem0_config): handle unexpanded env vars as empty strings"
type: source
tags: []
date: 2026-04-06
source_file: raw/prs-worldai_claw/pr-528.md
sources: []
last_updated: 2026-04-06
---

## Summary
A recent merge of PR #520 introduced a regression (flagged by Cursor Bugbot) where unexpanded environment variables in `openclaw.json` (e.g., `"apiKey": "$OPENAI_API_KEY"`) were treated as literal strings when the variable was unset. This caused `mem0_hooks_enabled()` to return `True`, leading to failed API calls rather than failing open.

## Metadata
- **PR**: #528
- **Merged**: 2026-04-06
- **Author**: jleechan2015
- **Stats**: +23/-3 in 2 files
- **Labels**: none

## Connections
