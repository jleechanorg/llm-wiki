---
title: "PR #6048: fix(llm_service): eliminate cache double-billing for story entries (REV-8mgs)"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldarchitect-ai/pr-6048.md
sources: []
last_updated: 2026-04-04
---

## Summary
The explicit caching implementation in `_call_llm_api_with_explicit_cache` sends old story entries TWICE per request:
1. In the cache prefix (at \$0.05/M cached rate)
2. In the live `story_history` JSON (at \$0.50/M full rate)

This doubles the cost of old entries — ~\$0.069/req wasted for a campaign like Visenya v5 (529 entries, 138K double-billed tokens).

## Metadata
- **PR**: #6048
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +1776/-108 in 18 files
- **Labels**: none

## Connections
