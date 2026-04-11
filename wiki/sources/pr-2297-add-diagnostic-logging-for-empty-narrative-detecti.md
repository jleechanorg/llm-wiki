---
title: "PR #2297: Add diagnostic logging for empty narrative detection"
type: source
tags: []
date: 2025-12-03
source_file: raw/prs-worldarchitect-ai/pr-2297.md
sources: []
last_updated: 2025-12-03
---

## Summary
- Add INFO-level logging for parsed LLM responses (narrative_length, structured_response presence, raw_response_length)
- Add WARNING-level logging when narrative is empty, including raw response preview and structured field status  
- Upgrade final response logging from DEBUG to INFO for production visibility
- Apply same diagnostic logging to both `continue_story()` and `get_initial_story()` functions

## Metadata
- **PR**: #2297
- **Merged**: 2025-12-03
- **Author**: jleechan2015
- **Stats**: +70/-6 in 1 files
- **Labels**: none

## Connections
