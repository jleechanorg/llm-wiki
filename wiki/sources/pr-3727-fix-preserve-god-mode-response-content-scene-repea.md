---
title: "PR #3727: fix: Preserve god_mode_response content (scene repeat bug)"
type: source
tags: []
date: 2026-01-17
source_file: raw/prs-worldarchitect-ai/pr-3727.md
sources: []
last_updated: 2026-01-17
---

## Summary
- Fixed critical bug where god_mode_response content was being replaced by "You pause to consider your options..." placeholder
- Root cause: `create_from_structured_response` was not receiving the combined narrative text from `parse_structured_response`

## Metadata
- **PR**: #3727
- **Merged**: 2026-01-17
- **Author**: jleechan2015
- **Stats**: +661/-0 in 4 files
- **Labels**: none

## Connections
