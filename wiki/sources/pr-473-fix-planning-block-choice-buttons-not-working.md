---
title: "PR #473: Fix planning block choice buttons not working"
type: source
tags: []
date: 2025-07-10
source_file: raw/prs-worldarchitect-ai/pr-473.md
sources: []
last_updated: 2025-07-10
---

## Summary
- Fixed planning block choice buttons that were no longer generating due to format mismatch
- Root cause: JavaScript regex expected `**Action:**` but AI generates `**Action** -` format  
- Replaced complex regex with maintainable line-by-line parsing
- Ensured structured `planning_block` field is properly parsed for button generation

## Metadata
- **PR**: #473
- **Merged**: 2025-07-10
- **Author**: jleechan2015
- **Stats**: +86/-61 in 2 files
- **Labels**: none

## Connections
