---
title: "PR #2254: Add per-campaign cost estimation to campaign_manager.py"
type: source
tags: []
date: 2025-12-02
source_file: raw/prs-worldarchitect-ai/pr-2254.md
sources: []
last_updated: 2025-12-02
---

## Summary
- Add `cost-report` command to estimate per-campaign costs sorted by most expensive
- Calculate token usage based on story entry count and context growth (43K base + 50K world + history tokens)
- Show short vs long context pricing breakdown (Gemini 3 Pro: $2/$4 per 1M input, $12/$18 per 1M output)
- Add Claude skill documentation for Firebase production queries

## Metadata
- **PR**: #2254
- **Merged**: 2025-12-02
- **Author**: jleechan2015
- **Stats**: +955/-3 in 10 files
- **Labels**: none

## Connections
