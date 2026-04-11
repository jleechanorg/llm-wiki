---
title: "PR #843: refactor: Simplify Claude model names in startup script"
type: source
tags: []
date: 2025-07-22
source_file: raw/prs-worldarchitect-ai/pr-843.md
sources: []
last_updated: 2025-07-22
---

## Summary
- Update `claude_start.sh` to use simplified model names (`opus`/`sonnet`) instead of explicit versioned names
- Claude CLI automatically selects the latest available versions when using simplified names
- Makes the script more maintainable - no need to update version dates with new model releases

## Metadata
- **PR**: #843
- **Merged**: 2025-07-22
- **Author**: jleechan2015
- **Stats**: +5/-24 in 1 files
- **Labels**: none

## Connections
