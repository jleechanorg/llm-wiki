---
title: "PR #1304: Fix: Export Command LLM Placeholder Replacement"
type: source
tags: []
date: 2025-08-15
source_file: raw/prs-worldarchitect-ai/pr-1304.md
sources: []
last_updated: 2025-08-15
---

## Summary
Fixes the export command to properly replace LLM placeholders in README generation instead of just copying the template file.

### Problem
The export system was copying `README_EXPORT_TEMPLATE.md` directly without processing LLM placeholders, resulting in exported READMEs containing placeholder comments instead of actual version information. This is visible in [PR #58](https://github.com/jleechanorg/claude-commands/pull/58/files) where the README still shows `<!-- LLM_VERSION_START -->` comments

## Metadata
- **PR**: #1304
- **Merged**: 2025-08-15
- **Author**: jleechan2015
- **Stats**: +736/-475 in 9 files
- **Labels**: none

## Connections
