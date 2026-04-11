---
title: "PR #33: Allow special characters in questions and prompts"
type: source
tags: [codex]
date: 2025-09-23
source_file: raw/prs-/pr-33.md
sources: []
last_updated: 2025-09-23
---

## Summary
- remove local character filtering from second opinion and multi-model schemas so providers can handle validation
- keep harmful content checks but drop script-style character rejection in multi-model tool
- update unit tests to confirm prompts with special characters are accepted and still compute estimates

## Metadata
- **PR**: #33
- **Merged**: 2025-09-23
- **Author**: jleechan2015
- **Stats**: +9/-39 in 3 files
- **Labels**: codex

## Connections
