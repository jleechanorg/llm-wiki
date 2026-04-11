---
title: "PR #2502: Fix Gemini code_execution dice fabrication"
type: source
tags: []
date: 2025-12-19
source_file: raw/prs-worldarchitect-ai/pr-2502.md
sources: []
last_updated: 2025-12-19
---

## Summary
- Fixed Gemini fabricating dice rolls despite claiming code_execution_used=True
- Updated prompt to include explicit Python code that must be executed
- Added detection/logging for fabricated dice rolls
- Added smoke test script for validation

## Metadata
- **PR**: #2502
- **Merged**: 2025-12-19
- **Author**: jleechan2015
- **Stats**: +351/-2 in 3 files
- **Labels**: none

## Connections
