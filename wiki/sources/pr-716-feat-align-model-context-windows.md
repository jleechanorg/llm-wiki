---
title: "PR #716: feat: align model context windows"
type: source
tags: []
date: 2025-11-13
source_file: raw/prs-/pr-716.md
sources: []
last_updated: 2025-11-13
---

## Summary
- add provider-specific context token limits for every configured model so we no longer cap requests at 50k tokens
- plumb the new limits through the ConfigManager output (including OpenAI) so backend tools inherit the larger contexts automatically
- update the ConfigManager test suite to lock in the new limits

## Metadata
- **PR**: #716
- **Merged**: 2025-11-13
- **Author**: jleechan2015
- **Stats**: +26/-11 in 2 files
- **Labels**: none

## Connections
