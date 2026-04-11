---
title: "PR #230: Fix some tests and extract shared json parser code + tweaks"
type: source
tags: []
date: 2025-07-03
source_file: raw/prs-worldarchitect-ai/pr-230.md
sources: []
last_updated: 2025-07-03
---

## Summary
Extracts common JSON parsing routines into a new `json_utils.py` module and refactors existing parsers to use these utilities; it also updates the test runner to skip manual tests. Additionally addresses all GitHub Copilot review comments.

### Changes Made
- Refactored `robust_json_parser.py` and `debug_json_response.py` to call shared functions from `json_utils.py`
- Added `json_utils.py` with utilities for counting unmatched tokens, extracting boundaries, completing truncated JSON, and extrac

## Metadata
- **PR**: #230
- **Merged**: 2025-07-03
- **Author**: jleechan2015
- **Stats**: +598/-515 in 15 files
- **Labels**: none

## Connections
