---
title: "PR #3651: Fix Gemini code execution JSON parsing error"
type: source
tags: []
date: 2026-01-16
source_file: raw/prs-worldarchitect-ai/pr-3651.md
sources: []
last_updated: 2026-01-16
---

## Summary
This PR fixes critical JSON parsing failures that occur when Gemini uses code execution mode, causing "Invalid JSON response received" errors in production. The solution removes code execution artifacts before JSON parsing and includes comprehensive test coverage.

## Metadata
- **PR**: #3651
- **Merged**: 2026-01-16
- **Author**: jleechan2015
- **Stats**: +367/-44 in 3 files
- **Labels**: none

## Connections
